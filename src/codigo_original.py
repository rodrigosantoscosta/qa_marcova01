"""Código ORIGINAL do Dev Jr. — apenas com a indentação normalizada.

Lógica 100% preservada (incluindo os bugs). Evidência literal em `src/codigo.py`.
Existe só para permitir a execução da suite de testes no PRINT1.

Bugs conhecidos (vs. desafio.txt):
  1. `valor_compra > 100` exclui compras de exatamente R$ 100,00 dos 10%.
  2. `tipo_cliente == "VIP"` é case-sensitive (regra exige qualquer caixa).
"""


def calcular_desconto(valor_compra, tipo_cliente):
    desconto = 0

    # Validação do desconto base
    if valor_compra > 100 and valor_compra < 500:
        desconto = 0.10
    elif valor_compra >= 500:
        desconto = 0.20

    # Validação do cliente VIP
    if tipo_cliente == "VIP":
        desconto += 0.05

    valor_desconto = valor_compra * desconto

    # Regra do Teto de R$ 200,00
    if valor_desconto > 200:
        valor_desconto = 200

    return round(valor_desconto, 2)
