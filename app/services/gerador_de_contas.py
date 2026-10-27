import random

def calcular_digito_verificador(numero_base: str) -> str:
    soma = 0 
    peso = 2

    for digito in reversed(numero_base):
        soma += int(digito) * peso

        peso += 1  

        if peso > 9:
            peso = 2 

    resto = soma % 11

    if resto in (0,1):
        digito = 0 
    else:
        digito = 11 - resto

    return str(digito)

def gerar_numero_conta(db):
    from app.models.conta_models import Conta

    while True:
        numero_base = str(random.randint(100000, 999999))

        digito = calcular_digito_verificador(numero_base)

        numero_conta = f"{numero_base}--{digito}"

        conta_existente = db.query(Conta).filter(
            Conta.numero == numero_conta
        ).first()

        if conta_existente is None:
            return numero_conta