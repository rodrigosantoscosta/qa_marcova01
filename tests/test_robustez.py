"""Testes de robustez — dados inesperados (cenarios.md, grupo 5).

CT-INV-02/03/04 propõem validação de entrada que nenhuma versão implementa:
marcados como xfail NÃO estrito (documentam a limitação sem quebrar o
resultado verde). Se a validação for implementada no futuro, eles passam
a valer como testes reais — basta remover a marca.
"""
import importlib
import os

import pytest

ALVO = os.getenv("ALVO", "codigo_corrigido")
_mod = importlib.import_module(f"src.{ALVO}")
calcular_desconto = _mod.calcular_desconto


@pytest.mark.parametrize(
    "valor,tipo,esperado",
    [
        pytest.param(0, "COMUM", 0, id="CT-INV-01a"),
        pytest.param(0, "VIP", 0.0, id="CT-INV-01b"),
        pytest.param(300, 123, 30.0, id="CT-INV-05"),
        pytest.param(100, "COMUM", 10.0, id="CT-INV-06a"),
        pytest.param(100.0, "COMUM", 10.0, id="CT-INV-06b"),
    ],
)
def test_comportamento_documentado(valor, tipo, esperado):
    assert calcular_desconto(valor, tipo) == esperado


@pytest.mark.xfail(
    strict=False, reason="Sem validação de entrada — melhoria futura (CT-INV-02)"
)
def test_negativo_rejeitado():
    with pytest.raises(ValueError):
        calcular_desconto(-100, "COMUM")


@pytest.mark.xfail(
    strict=False, reason="Sem validação de entrada — melhoria futura (CT-INV-03)"
)
def test_valor_texto_rejeitado():
    with pytest.raises(ValueError):
        calcular_desconto("300", "COMUM")


@pytest.mark.xfail(
    strict=False, reason="Sem validação de entrada — melhoria futura (CT-INV-04)"
)
def test_valor_none_rejeitado():
    with pytest.raises(ValueError):
        calcular_desconto(None, "COMUM")
