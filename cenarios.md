# Cenários de Teste — `calcular_desconto(valor_compra, tipo_cliente)`

Regra resumida (de `desafio.txt`): desconto base progressivo por faixa
(< R$ 100 → 0%; 100–499,99 → 10%; ≥ R$ 500 → 20%),
+5% se cliente VIP (qualquer caixa alta/baixa), teto de R$ 200,00.
Técnica: análise de valor limite nas fronteiras 100 / 500 e no teto.

---

## 1. Desconto base — fronteiras de faixa (cliente COMUM)

| ID | Descrição | Entrada (valor, tipo) | Esperado |
|---|---|---|---|
| CT-BASE-01 | Abaixo da faixa (sem desconto) | (50, "COMUM") | 0 |
| CT-BASE-02 | Limite inferior da isenção | (99.99, "COMUM") | 0.0 |
| CT-BASE-03 | Início da faixa 10% (inclui o 100) | (100, "COMUM") | 10.0 |
| CT-BASE-04 | Meio da faixa 10% (caso do "teste de cabeça" do Jr.) | (300, "COMUM") | 30.0 |
| CT-BASE-05 | Fim da faixa 10% (+ arredondamento 49.999 → 50.0) | (499.99, "COMUM") | 50.0 |
| CT-BASE-06 | Início da faixa 20% (inclui o 500) | (500, "COMUM") | 100.0 |
| CT-BASE-07 | Faixa 20% sem teto | (800, "COMUM") | 160.0 |

## 2. Bônus VIP — acréscimo de 5% e variações de escrita

| ID | Descrição | Entrada (valor, tipo) | Esperado |
|---|---|---|---|
| CT-VIP-01 | VIP sobre faixa isenta (0% vira 5%) | (50, "VIP") | 2.5 |
| CT-VIP-02 | VIP minúsculo no limite da isenção | (99.99, "vip") | 5.0 |
| CT-VIP-03 | VIP capitalizado no limite R$ 100 (15%) | (100, "Vip") | 15.0 |
| CT-VIP-04 | VIP minúsculo na faixa 10% (10% vira 15%) | (300, "vip") | 45.0 |
| CT-VIP-05 | VIP na faixa 20% (20% vira 25%) | (500, "VIP") | 125.0 |
| CT-VIP-06 | VIP com caixa alternada | (300, "vIp") | 45.0 |
| CT-VIP-07 | VIP com espaços em branco | (300, " vip ") | 45.0 |
| CT-VIP-08 | "comum" minúsculo não recebe acréscimo | (300, "comum") | 30.0 |
| CT-VIP-09 | Categoria desconhecida tratada sem acréscimo | (300, "OURO") | 30.0 |
| CT-VIP-10 | Tipo vazio tratado sem acréscimo | (300, "") | 30.0 |
| CT-VIP-11 | Tipo `None` tratado sem acréscimo | (300, None) | 30.0 |

## 3. Teto de R$ 200,00 — valor exato vs. corte

| ID | Descrição | Entrada (valor, tipo) | Esperado |
|---|---|---|---|
| CT-TETO-01 | COMUM atinge exatos R$ 200 (1000 × 20%, sem corte) | (1000, "COMUM") | 200.0 |
| CT-TETO-02 | COMUM um centavo acima (200.002 → corta) | (1000.01, "COMUM") | 200 |
| CT-TETO-03 | VIP atinge exatos R$ 200 (800 × 25%, sem corte) | (800, "VIP") | 200.0 |
| CT-TETO-04 | VIP um centavo acima (200.0025 → corta) | (800.01, "VIP") | 200 |
| CT-TETO-05 | COMUM bem acima do teto | (2000, "COMUM") | 200 |
| CT-TETO-06 | VIP bem acima do teto | (2000, "VIP") | 200 |
| CT-TETO-07 | Valor muito alto (ordem de grandeza) | (1000000, "VIP") | 200 |

## 4. Arredondamento (2 casas)

| ID | Descrição | Entrada (valor, tipo) | Esperado |
|---|---|---|---|
| CT-ROUND-01 | 199.99 × 10% = 19.999 → 20.0 | (199.99, "COMUM") | 20.0 |
| CT-ROUND-02 | 499.99 × 10% = 49.999 → 50.0 | (499.99, "COMUM") | 50.0 |

## 5. Dados inesperados — fora do que a regra descreve (robustez)

| ID | Descrição | Entrada (valor, tipo) | Esperado (proposto) |
|---|---|---|---|
| CT-INV-01 | Valor zerado COMUM / VIP | (0, "COMUM") / (0, "VIP") | 0 / 0.0 |
| CT-INV-02 | Valor negativo COMUM / VIP | (-100, "COMUM") / (-100, "VIP") | **Proposta:** rejeitar (`ValueError`). Comportamento atual: retorna `0` (mascara a entrada inválida) e `-5.0` (desconto "negativo", sem sentido no negócio) |
| CT-INV-03 | Valor como texto numérico | ("300", "COMUM") | **Proposta:** validar tipo (hoje lança `TypeError` sem mensagem clara) |
| CT-INV-04 | Valor `None` | (None, "COMUM") | **Proposta:** validar tipo (hoje lança `TypeError` sem mensagem clara) |
| CT-INV-05 | Tipo de cliente numérico | (300, 123) | 30.0 (sem acréscimo — documentar o comportamento) |
| CT-INV-06 | Inteiro vs. float no limite | (100, "COMUM") / (100.0, "COMUM") | 10.0 em ambos |

---

## Observações para a automação (Pytest)

- Grupos 1–4: testes de conformidade com a regra (devem passar no código corrigido e **falhar** no código original nos casos CT-BASE-03, CT-VIP-02/03/04/06/07 e CT-INV-06a/06b — os dois últimos cobrem a mesma fronteira de R$ 100 com `int`/`float`). CT-VIP-11 passa em ambos (o `== "VIP"` original já ignora `None` sem quebrar).
- Grupo 5: testes exploratórios de robustez — CT-INV-01 e CT-INV-05 documentam o comportamento; CT-INV-02/03/04 propõem validação de entrada como melhoria futura (fora do escopo da regra atual).
