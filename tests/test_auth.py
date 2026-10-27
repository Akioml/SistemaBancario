from unittest.mock import patch

# Testes de criação de contas e controle de acesso.
# Verifica se um cliente autenticado consegue criar uma conta 
# e se os dados retornados correpondem à conta criada.
def test_criacao_de_conta_(cliente):
    cliente.post(
        "/clientes/",
        json = {
            "cpf": "12345678901",
            "senha_app": "12345",
            "nome_completo": "Cliente Teste",
            "idade": 25,
            "endereco": "Rua de Teste"
        }
    )

    login_resp = cliente.post(
        "/login",
        json={"cpf": "12345678901", "senha_app": "12345"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resposta = cliente.post(
        "/contas/",
        headers = headers,
        json = {
            "tipo": "corrente",
            "senha_cartao": "123455"  
        }
    )

    assert resposta.status_code in (200, 201), resposta.text
    dados = resposta.json()
    assert "numero" in dados
    assert dados["tipo"] == "corrente"

# Verifica se um cliente consegue acessar à propria conta, 
# mas não consegue consultar a conta de outro titular.
def test_acesso_indevido(cliente):
    dados_a = {
        "cpf": "12345678901",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste",
        "idade": 25,
        "endereco": "Rua de Teste",
    }
    dados_b = {
        "cpf": "12345678976",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste 2",
        "idade": 25,
        "endereco": "Rua de Teste",
    }

    resposta = cliente.post("/clientes/", json = dados_a)
    assert resposta .status_code in (200, 201), resposta.json()

    resposta = cliente.post("/clientes/", json = dados_b)
    assert resposta.status_code in (200, 201), resposta.json()

    login_a = cliente.post("/login", json={"cpf": dados_a["cpf"], "senha_app": "12345"})
    assert login_a.status_code == 200, login_a.json()

    token_a = login_a.json()["access_token"]

    login_b = cliente.post("/login", json={"cpf": dados_b["cpf"], "senha_app": "12345"})
    assert login_b.status_code == 200, login_b.json()

    token_b = login_b.json()["access_token"]

    resp_conta_a = cliente.post(
        "/contas/",
        json={"tipo": "corrente", "senha_cartao": "1234"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert resp_conta_a.status_code in (200, 201), resp_conta_a.json()

    conta_a = resp_conta_a.json()

    # sanidade: A consegue acessar a própria conta
    acessoContaA = cliente.get(
        f"/contas/{conta_a['id']}",
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert acessoContaA.status_code == 200, acessoContaA.json()

    # B tenta acessar a conta de A
    acessoContaB = cliente.get(
        f"/contas/{conta_a['id']}",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert acessoContaB.status_code in (403, 404), acessoContaB.json()

# Verifica com a API responde quando recebe uma requisição 
# Inválida para consultar um cliente
def test_conta_inexistente(cliente):
    conta = cliente.get("/todosClientes/{id_cliente : 3}",)
    assert conta.status_code == 422
    
# Verifica se um cliente cadastrado consegue autenticar-se com suas credencias
# Corretas e recebe um token de acesso.
def test_login_com_senha_correta(cliente):
    cadastro = cliente.post(
        "/clientes/",
        json = {"cpf": "12345678901", "senha_app": "12345", "nome_completo": "Teste", "idade": 25, "endereco": "Rua de Teste"}
    )
    assert cadastro.status_code in (200, 201), cadastro.text

    resposta = cliente.post(
        "/login",
        json = {
            "cpf": "12345678901",
            "nome_completo": "Cliente Teste",
            "senha_app": "12345",
            "idade": 25,
            "endereco": "Rua de Teste",
        }
    )
    
    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["token_type"] == "bearer"

# Verifica se a API rejeita a autenticação quando a senha informada não corresponder 
# à senha cadastrada.
def test_login_com_senha_incorreta(cliente):
    resposta = cliente.post(
        "/login",
        json = {
            "cpf": "12345678901",
            "senha_app": "senha_incorreta"
        }
    )

    assert resposta.status_code == 401

# Verifia se uma rota protegida impede o acesso quando a requisição não apresentar
# um token de autenticação.
def test_consulta_saldo_sem_token(cliente):
    resposta = cliente.get("/contas/1")

    assert resposta.status_code == 401

# Verifica se a API rejeita depósitos com valores negativos
# e impede que uma operação inválida seja processada.
def test_deposito_numero_negativo(cliente):
    dados_teste = {
        "cpf": "12345678901",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste",
        "idade": 25,
        "endereco": "Rua de Teste",
    }

    resposta = cliente.post("/clientes/", json = dados_teste)
    assert resposta.status_code in (200, 201), resposta.json()

    login_resp = cliente.post("/login", json={"cpf": dados_teste["cpf"], "senha_app": "12345"})
    assert login_resp.status_code == 200, login_resp.json()

    token = login_resp.json()["access_token"]

    resp_conta_a = cliente.post(
        "/contas/",
        json={"tipo": "corrente", "senha_cartao": "1234"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_conta_a.status_code in (200, 201), resp_conta_a.json()

    conta_a = resp_conta_a.json()

    deposito = cliente.post(
        "/depositos/",
        json={
            "conta_id": conta_a["id"],
            "valor": -100
    },
)

    assert deposito.status_code in (400, 422), deposito.text

# Verifica se a API rejeita transferências com valores negativos
# e garante que os saldos das contas permaneçam inalterados.
def test_transaferencias_valor_negativo(cliente):
    dados_a = {
        "cpf": "12345678901",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste",
        "idade": 25,
        "endereco": "Rua de Teste",
    }
    dados_b = {
        "cpf": "12345678976",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste 2",
        "idade": 25,
        "endereco": "Rua de Teste",
    }

    resposta = cliente.post("/clientes/", json = dados_a)
    assert resposta.status_code in (200, 201), resposta.json()

    resposta = cliente.post("/clientes/", json = dados_b)
    assert resposta.status_code in (200, 201), resposta.json()

    login_a = cliente.post("/login", json={"cpf": dados_a["cpf"], "senha_app": "12345"})
    assert login_a.status_code == 200, login_a.json()

    token_a = login_a.json()["access_token"]

    login_b = cliente.post("/login", json={"cpf": dados_b["cpf"], "senha_app": "12345"})
    assert login_b.status_code == 200, login_b.json()

    token_b = login_b.json()["access_token"]

    resp_conta_a = cliente.post(
        "/contas/",
        json={"tipo": "corrente", "senha_cartao": "1234"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert resp_conta_a.status_code in (200, 201), resp_conta_a.json()

    resp_conta_b = cliente.post(
        "/contas/",
        json={"tipo": "corrente", "senha_cartao": "1234"},
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert resp_conta_b.status_code in (200, 201), resp_conta_b.text

    conta_a = resp_conta_a.json()
    conta_b = resp_conta_b.json()

    saldo_a_antes = cliente.get(
        f"/contas/{conta_a['id']}",
        headers={"Authorization": f"Bearer {token_a}"}
    )

    saldo_b_antes = cliente.get(
    f"/contas/{conta_b['id']}",
    headers={"Authorization": f"Bearer {token_b}"}
    )

    assert saldo_a_antes.status_code == 200, saldo_a_antes.text
    assert saldo_b_antes.status_code == 200, saldo_b_antes.text

    valor_a_antes = saldo_a_antes.json()["saldo"]
    valor_b_antes = saldo_b_antes.json()["saldo"]

    transferencia = cliente.post(
        "/transacao",
        json = {
            "conta_origem_id": conta_a['id'],
            "conta_destino_id": conta_b['id'],
            "valor": -50
        },
        headers={"Authorization": f"Bearer {token_a}"}
    )

    saldo_a_depois = cliente.get(
        f"/contas/{conta_a['id']}",
        headers={"Authorization": f"Bearer {token_a}"}
    )

    saldo_b_depois = cliente.get(
        f"/contas/{conta_b['id']}",
        headers={"Authorization": f"Bearer {token_b}"}
    )

    assert saldo_a_depois.status_code == 200, saldo_a_depois.text
    assert saldo_b_depois.status_code == 200, saldo_b_depois.text

    assert saldo_a_depois.json()["saldo"] == valor_a_antes 
    assert saldo_b_depois.json()["saldo"] == valor_b_antes

    assert transferencia.status_code in (400, 422), transferencia.text

def test_transferencia_saldo_positivo(cliente):
    dados_a = {
        "cpf": "12345678901",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste",
        "idade": 25,
        "endereco": "Rua de Teste"
    }

    dados_b = {
        "cpf": "12345678976",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste 2",
        "idade": 25,
        "endereco": "Rua de Teste"
    }

    # 1. Cadastrar os clientes envolvidos na tranfereencias
    resposta_a = cliente.post("/clientes/", json=dados_a)
    assert resposta_a.status_code in (200, 201), resposta_a.text

    resposta_b = cliente.post("/clientes/", json=dados_b)
    assert resposta_b.status_code in (200, 201), resposta_b.text

    # 2. Autententica os clientes e obtem sesus token de acesso
    login_a = cliente.post(
        "/login",
        json={"cpf": dados_a["cpf"], "senha_app": dados_a["senha_app"]}
    )
    assert login_a.status_code == 200, login_a.text
    token_a = login_a.json()["access_token"]

    login_b = cliente.post(
        "/login",
        json={"cpf": dados_b["cpf"], "senha_app": dados_b["senha_app"]}
    )
    assert login_b.status_code == 200, login_b.text
    token_b = login_b.json()["access_token"]

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 3. Cria uma conta para cada cliente.
    resposta_conta_a = cliente.post(
        "/contas/",
        json={"tipo": "corrente", "senha_cartao": "1234"},
        headers=headers_a
    )
    assert resposta_conta_a.status_code in (200, 201), resposta_conta_a.text
    conta_a = resposta_conta_a.json()

    resposta_conta_b = cliente.post(
        "/contas/",
        json={"tipo": "corrente", "senha_cartao": "1234"},
        headers=headers_b
    )
    assert resposta_conta_b.status_code in (200, 201), resposta_conta_b.text
    conta_b = resposta_conta_b.json()

    # 4. Depositar os valores iniciais nas contas.
    deposito_a = cliente.post(
        "/depositos/",
        json={"conta_id": conta_a["id"], "valor": 500},
        headers=headers_a
    )
    assert deposito_a.status_code == 200, deposito_a.text

    deposito_b = cliente.post(
        "/depositos/",
        json={"conta_id": conta_b["id"], "valor": 300},
        headers=headers_b
    )
    assert deposito_b.status_code == 200, deposito_b.text

    # 5. Registrar os saldos iniciais para comparação.
    saldo_inicial_a = float(deposito_a.json()["saldo"])
    saldo_inicial_b = float(deposito_b.json()["saldo"])

    valor_transferencia = 100

    # 6. Realizar a transferência entre as contas.
    transferencia = cliente.post(
        "/transacao/",
        json={
            "conta_origem_id": conta_a["id"],
            "conta_destino_id": conta_b["id"],
            "valor": valor_transferencia,
            "tipo": "transferencia"
        },
        headers=headers_a
    )

    assert transferencia.status_code == 200, transferencia.text

    # 7. Consultar os saldos após a tranferencias.
    saldo_a_depois = cliente.get(
        f"/contas/{conta_a['id']}",
        headers=headers_a
    )
    saldo_b_depois = cliente.get(
        f"/contas/{conta_b['id']}",
        headers=headers_b
    )

    assert saldo_a_depois.status_code == 200, saldo_a_depois.text
    assert saldo_b_depois.status_code == 200, saldo_b_depois.text

    saldo_final_a = float(saldo_a_depois.json()["saldo"])
    saldo_final_b = float(saldo_b_depois.json()["saldo"])

    # 8. Verificia se o valor debitado da conta de origem e creditado na conta destino.
    assert saldo_final_a == saldo_inicial_a - valor_transferencia
    assert saldo_final_b == saldo_inicial_b + valor_transferencia

    # 9. Verifica se a soma dos saldos permaneceu constante.
    assert saldo_final_a + saldo_final_b == saldo_inicial_a + saldo_inicial_b

# Verifica se uma transferência atualiza corretamente
# os saldos das contas de origem e destino.
def test_atualizacao_correta_saldos(cliente):
    dados_a = {
        "cpf": "12345678901",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste",
        "idade": 25,
        "endereco": "Rua de Teste",
    }
    dados_b = {
        "cpf": "12345678976",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste 2",
        "idade": 25,
        "endereco": "Rua de Teste",
    }

    resposta = cliente.post("/clientes/", json = dados_a)
    assert resposta.status_code in (200, 201), resposta.json()

    resposta = cliente.post("/clientes/", json = dados_b)
    assert resposta.status_code in (200, 201), resposta.json()

    login_a = cliente.post("/login", json={"cpf": dados_a["cpf"], "senha_app": "12345"})
    assert login_a.status_code == 200, login_a.json()

    token_a = login_a.json()["access_token"]

    login_b = cliente.post("/login", json={"cpf": dados_b["cpf"], "senha_app": "12345"})
    assert login_b.status_code == 200, login_b.json()

    token_b = login_b.json()["access_token"]
    
    # Guarde os IDs das contas e os tokens.
    resp_conta_a = cliente.post(
        "/contas/",
        json={"tipo": "corrente", "senha_cartao": "1234"},
        headers={"Authorization": f"Bearer {token_a}"},
    )

    resp_conta_b = cliente.post(
        "/contas/",
        json={"tipo": "corrente", "senha_cartao": "1234"},
        headers={"Authorization": f"Bearer {token_b}"},
    )

    # Consulte os saldos iniciais das contas.
    saldo_inicial_a = 500.00
    saldo_inicial_b = 300.00


    valor_transferencia = 100.00

    conta_a = resp_conta_a.json()
    conta_b = resp_conta_b.json()

    depositoa = cliente.post(
        "/depositos/",
        json={
            "conta_id": conta_a["id"],
            "valor": 500
    })
    assert depositoa.status_code == 200, depositoa.text

    depositob = cliente.post(
        "/depositos/",
        json={
            "conta_id": conta_b['id'],
            "valor": 300
    })
    assert depositob.status_code == 200, depositob.text

    # Faça a transferência usando o token do titular da conta A.
    resposta = cliente.post(
        "/transacao/",
        json={
            "conta_origem_id": conta_a['id'],
            "conta_destino_id": conta_b['id'],
            "valor": valor_transferencia,
            "tipo" : 'transferencia'
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    assert resposta.status_code == 200, resposta.text

     # Consulta novamente o saldo da conta A (com token da conta A)
    resp_saldo_a = cliente.get(
        f"/contas/{conta_a['id']}",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert resp_saldo_a.status_code == 200, resp_saldo_a.text
    saldo_final_a = resp_saldo_a.json()["saldo"]
    
    # Consulta novamente o saldo da conta B (com token da conta B)
    resp_saldo_b = cliente.get(
        f"/contas/{conta_b['id']}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert resp_saldo_b.status_code == 200, resp_saldo_b.text
    saldo_final_b = resp_saldo_b.json()["saldo"]
    # Valida se os saldos no banco foram atualizados corretamente
    assert saldo_final_a == saldo_inicial_a - valor_transferencia  # 500 - 100 = 400.0
    assert saldo_final_b == saldo_inicial_b + valor_transferencia  # 300 + 100 = 400.0

# Verifica se um cliente autenticado não consegue realizar
# uma transferência utilizando uma conta de origem
# pertencente a outro cliente.
def test_titualiridade(cliente):
    cliente_a = {
        "cpf": "12345678901",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste",
        "idade": 25,
        "endereco": "Rua de Teste",
    }
    cliente_b = {
        "cpf": "12345678976",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste 2",
        "idade": 25,
        "endereco": "Rua de Teste",
    }
    
    cliente.post("/clientes/", json=cliente_a)
    cliente.post("/clientes/", json=cliente_b)

    # 2. Fazer login como Cliente A
    login_a = cliente.post(
        "/login", 
        json= {"cpf": cliente_a["cpf"],
               "senha_app": "12345"}
        )

    token_a = login_a.json()["access_token"]

    # 3. Criar uma conta para cada cliente
    resposta_conta_a = cliente.post(
        "/contas/",
        json={"tipo": "corrente", "senha_cartao": "1234"},
        headers={"Authorization": f"Bearer {token_a}"}
    )

    conta_a = resposta_conta_a.json()

    # Para criar a conta B, faça login como Cliente B
    login_b = cliente.post(
        "/login", 
        json= {"cpf": cliente_b["cpf"],
               "senha_app": "12345"}
        )

    token_b = login_b.json()["access_token"]

    resposta_conta_b = cliente.post(
        "/contas/",
        json={"tipo": "corrente", "senha_cartao": "5678"},
        headers={"Authorization": f"Bearer {token_b}"}
    )

    conta_b = resposta_conta_b.json()

    # 4. Cliente A tenta usar a conta de origem de B
    resposta = cliente.post(
        "/transacao/",
        json={
            "conta_origem_id": conta_b["id"],
            "conta_destino_id": conta_a["id"],
            "valor": 50,
            "tipo": "transferencia"
        },
        headers={"Authorization": f"Bearer {token_a}"}
    )

    assert resposta.status_code == 404

# Verifica se a consulta de uma conta sem movimentações
# retorna uma resposta bem-sucedida com uma lista vazia.
def test_consultar_extrato_sem_movimentacao(cliente):
    cliente_a = {
        "cpf": "12345678901",
        "senha_app": "12345",
        "nome_completo": "Cliente Teste",
        "idade": 25,
        "endereco": "Rua de Teste",
    }

    # Cadastrar cliente
    resposta_cadastro = cliente.post(
        "/clientes/",
        json=cliente_a
    )

    assert resposta_cadastro.status_code in (200, 201), resposta_cadastro.json()

    # Fazer login
    login_a = cliente.post(
        "/login", 
        json= {"cpf": cliente_a["cpf"],
               "senha_app": "12345"}
        )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token_a}"
    }

    # Criar conta para o cliente autenticado
    resposta_conta = cliente.post(
        "/contas/",
        json={
            "tipo": "corrente",
            "senha_cartao": "1234"
        },
        headers=headers
    )

    assert resposta_conta.status_code == 200

    id_conta = resposta_conta.json()["id"]

    # Consultar extrato sem movimentações
    extrato = cliente.get(
        f"/consultaExtrato/{id_conta}/extrato",
        headers=headers
    )

    assert extrato.status_code == 200
    assert extrato.json() == []

def test_falha_na_transferencia_impede_atualizacao_de_apenas_uma_conta(cliente):
    # 1. PREPARANDO O CENÁRIO: Cadastrando Clientes A e B e abrindo suas contas

    cliente.post(
        "/clientes/",
        json={"cpf": "11111111111", "senha_app": "12345", "nome_completo": "Cliente A", "idade": 30, "endereco": "Rua A"}
    )
    token_a = cliente.post("/login", json={"cpf": "11111111111", "senha_app": "12345"}).json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}
    resp_conta_a = cliente.post("/contas/", headers=headers_a, json={"tipo": "corrente", "senha_cartao": "1234"})
    conta_a_id = resp_conta_a.json()["id"]
    # --- Cadastra e faz login do Cliente B ---
    cliente.post(
        "/clientes/",
        json={"cpf": "22222222222", "senha_app": "12345", "nome_completo": "Cliente B", "idade": 28, "endereco": "Rua B"}
    )
    token_b = cliente.post("/login", json={"cpf": "22222222222", "senha_app": "12345"}).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    resp_conta_b = cliente.post("/contas/", headers=headers_b, json={"tipo": "corrente", "senha_cartao": "1234"})
    conta_b_id = resp_conta_b.json()["id"]
    # --- Depósito inicial de R$ 500,00 na Conta A ---
    cliente.post(
        "/depositos/",
        json={"conta_id": conta_a_id, "valor": 500.0, "descricao": "Saldo inicial"}
    )
    # =========================================================================
    # 2. A EXECUÇÃO COM FALHA SIMULADA
    # =========================================================================
    # Simulamos que no exato momento do commit no banco, ocorre um erro inesperado
    # (queda de rede, timeout, erro de integridade, etc.)
    with patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Erro simulado no banco")):
        # Como a exceção não é capturada pelo router, a chamada vai estourar ou retornar erro 500
        try:
            cliente.post(
                "/transacao/",
                headers=headers_a,
                json={
                    "conta_origem_id": conta_a_id,
                    "conta_destino_id": conta_b_id,
                    "tipo": "TRANSFERENCIA",
                    "valor": 200.0
                }
            )
        except Exception:
            pass  # Esperamos que ocorra uma falha proposital aqui
    # =========================================================================
    # 3. VERIFICAÇÃO (ASSERT): Garantir que NENHUMA das contas mudou o saldo
    # =========================================================================
    # Consulta o saldo da Conta A
    saldo_a_resp = cliente.get(f"/contas/{conta_a_id}", headers=headers_a)
    saldo_a = saldo_a_resp.json()["saldo"]
    # Consulta o saldo da Conta B
    saldo_b_resp = cliente.get(f"/contas/{conta_b_id}", headers=headers_b)
    saldo_b = saldo_b_resp.json()["saldo"]
    # Ambas as contas devem permanecer com seus saldos intactos!
    assert saldo_a == 500.0, f"O saldo de A deveria continuar 500.0, mas está {saldo_a}"
    assert saldo_b == 0.0, f"O saldo de B deveria continuar 0.0, mas está {saldo_b}"