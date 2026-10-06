def calcular_desconto(valor_compra, tipo_cliente):
    desconto = 0

    # Desconto base progressivo
    if valor_compra < 100:
        desconto = 0
    elif valor_compra < 500:
        desconto = 0.10
    else:
        desconto = 0.20

    # Bônus VIP (case-insensitive)
    if str(tipo_cliente).strip().upper() == "VIP":
        desconto += 0.05

    valor_desconto = valor_compra * desconto

    # Regra do Teto de R$ 200,00
    if valor_desconto > 200:
        valor_desconto = 200

    return round(valor_desconto, 2)
