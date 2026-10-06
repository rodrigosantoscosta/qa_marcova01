"""Testes de conformidade — `calcular_desconto` x Critérios de Aceite.

Cenários: cenarios.md (grupos 1–4). IDs parametrizados como test IDs.

Alvo via variável de ambiente ALVO:
  ALVO=codigo_original   -> lógica do Jr. (PRINT1, esperado: 6 falhas)
  ALVO=codigo_corrigido  -> lógica corrigida (PRINT2, esperado: verde)
Padrão: codigo_corrigido.
"""
import importlib
import os

import pytest

ALVO = os.getenv("ALVO", "codigo_corrigido")
_mod = importlib.import_module(f"src.{ALVO}")
calcular_desconto = _mod.calcular_desconto


def caso(valor, tipo, esperado, id):
    return pytest.param(valor, tipo, esperado, id=id)


class TestDescontoBase:
    @pytest.mark.parametrize(
        "valor,tipo,esperado",
        [
            caso(50, "COMUM", 0, "CT-BASE-01"),
            caso(99.99, "COMUM", 0.0, "CT-BASE-02"),
            caso(100, "COMUM", 10.0, "CT-BASE-03"),
            caso(300, "COMUM", 30.0, "CT-BASE-04"),
            caso(499.99, "COMUM", 50.0, "CT-BASE-05"),
            caso(500, "COMUM", 100.0, "CT-BASE-06"),
            caso(800, "COMUM", 160.0, "CT-BASE-07"),
        ],
    )
    def test_faixa_base(self, valor, tipo, esperado):
        assert calcular_desconto(valor, tipo) == esperado


class TestBonusVip:
    @pytest.mark.parametrize(
        "valor,tipo,esperado",
        [
            caso(50, "VIP", 2.5, "CT-VIP-01"),
            caso(99.99, "vip", 5.0, "CT-VIP-02"),
            caso(100, "Vip", 15.0, "CT-VIP-03"),
            caso(300, "vip", 45.0, "CT-VIP-04"),
            caso(500, "VIP", 125.0, "CT-VIP-05"),
            caso(300, "vIp", 45.0, "CT-VIP-06"),
            caso(300, " vip ", 45.0, "CT-VIP-07"),
            caso(300, "comum", 30.0, "CT-VIP-08"),
            caso(300, "OURO", 30.0, "CT-VIP-09"),
            caso(300, "", 30.0, "CT-VIP-10"),
            caso(300, None, 30.0, "CT-VIP-11"),
        ],
    )
    def test_bonus_vip(self, valor, tipo, esperado):
        assert calcular_desconto(valor, tipo) == esperado


class TestTeto:
    @pytest.mark.parametrize(
        "valor,tipo,esperado",
        [
            caso(1000, "COMUM", 200.0, "CT-TETO-01"),
            caso(1000.01, "COMUM", 200, "CT-TETO-02"),
            caso(800, "VIP", 200.0, "CT-TETO-03"),
            caso(800.01, "VIP", 200, "CT-TETO-04"),
            caso(2000, "COMUM", 200, "CT-TETO-05"),
            caso(2000, "VIP", 200, "CT-TETO-06"),
            caso(1000000, "VIP", 200, "CT-TETO-07"),
        ],
    )
    def test_teto_200(self, valor, tipo, esperado):
        assert calcular_desconto(valor, tipo) == esperado


class TestArredondamento:
    @pytest.mark.parametrize(
        "valor,tipo,esperado",
        [
            caso(199.99, "COMUM", 20.0, "CT-ROUND-01"),
            caso(499.99, "COMUM", 50.0, "CT-ROUND-02"),
        ],
    )
    def test_duas_casas(self, valor, tipo, esperado):
        assert calcular_desconto(valor, tipo) == esperado
