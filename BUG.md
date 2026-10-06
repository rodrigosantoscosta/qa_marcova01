# Bugs encontrados no código original — `calcular_desconto`

Código analisado: lógica do Dev Jr. (versão executável em
[`src/codigo_original.py`](src/codigo_original.py); evidência literal em
[`src/codigo.py`](src/codigo.py)).
Respostas à missão 3 do [`desafio.txt`](desafio.txt).

---

## Pergunta: Quais foram os bugs (erros de lógica)?

### Bug 1 — Fronteira de R$ 100,00 excluída dos 10%

**Regra (Critérios de Aceite):** "Compras com valor **igual ou maior** que
R$ 100,00 e menor que R$ 500,00 recebem 10% de desconto base."

**Código original:**

```python
if valor_compra > 100 and valor_compra < 500:
    desconto = 0.10
```

**Erro:** `> 100` (estritamente maior) deixa de fora a compra de exatamente
R$ 100,00, que cai na faixa sem desconto → **0% em vez de 10%**.
A regra pedia `>= 100`.

**Correção aplicada:** cadeia progressiva `if < 100 / elif < 500 / else`,
em que `>= 100` passa a ser implícito — não há mais "buraco" na fronteira.

---

### Bug 2 — Bônus VIP reconhecido apenas em caixa alta

**Regra:** "Se o tipo_cliente for "VIP" (**independente de estar escrito em
maiúsculo ou minúsculo**), deve-se adicionar 5% extras sobre a porcentagem
base."

**Código original:**

```python
if tipo_cliente == "VIP":
    desconto += 0.05
```

**Erro:** `== "VIP"` é case-sensitive (e sensível a espaços). Entradas como
`"vip"`, `"Vip"`, `"vIp"` ou `" vip "` **não recebiam o +5%**, violando a
regra do PO. A diferença é silenciosa: nenhuma exceção é lançada — o desconto
apenas sai menor.

**Correção aplicada:** normalização da entrada antes da comparação:

```python
if str(tipo_cliente).strip().upper() == "VIP":
```

---

### Bugs que o código **não** tinha (confirmados pela suite)

Para não "achar bug onde não há", a suite também comprovou o que estava
correto — se algum teste falhasse aí, seria problema do teste/correção:

- **Teto de R$ 200,00** — `valor_desconto > 200` → corta em 200; todos os
  CT-TETO já passavam no original.
- **Faixa ≥ R$ 500 → 20%** — `elif valor_compra >= 500` correto.
- **VIP em caixa alta** (`CT-VIP-01/05`) — bônus calculado certo quando a
  string batia exatamente.
- **Cliente não-VIP** (`COMUM`, `OURO`, `""`, `None`) — nenhum acréscimo
  indevido; `None` não quebrava a comparação.

---

### Achados de robustez (fora da regra — documentados como `xfail`)

Não são violações dos Critérios de Aceite (a regra não define o comportamento),
mas limitações que a suite registrou para melhoria futura (CT-INV-02/03/04):

| Entrada | Comportamento atual | Risco |
|---|---|---|
| `(-100, "VIP")` | retorna `-5.0` | desconto negativo = cobrança a mais, sem erro |
| `("300", "COMUM")` / `(None, "COMUM")` | `TypeError` cru, sem mensagem clara | erro difícil de rastrear em produção |

---

## Pergunta: Como a escolha dos valores dos testes revelou esses erros?

A premissa foi a frase do Jr.: *"testei de cabeça com uma compra de
R$ 300 e funcionou"*. **R$ 300 é o pior valor para encontrar o Bug 1** —
está no meio da faixa de 10%, onde as duas implementações coincidem. A suite
foi desenhada justamente onde código e regra podem divergir:

### 1. Análise de valor limite (boundary value analysis)

Os bugs 1 e 2 moram **nas fronteiras**, não no centro das faixas. Por isso os
testes atacam os limites ± 1 centavo:

| Teste | Entrada | Original | Esperado | O que revela |
|---|---|---|---|---|
| CT-BASE-02 | `(99.99, "COMUM")` | 0.0 ✅ | 0.0 | confirma que a isenção começa antes do limite |
| **CT-BASE-03** | **`(100, "COMUM")`** | **0 (❌)** | **10.0** | **Bug 1**: o R$ 100 exato perde o desconto |
| CT-INV-06a/06b | `(100, …)` e `(100.0, …)` | ambos 0 (❌) | 10.0 | o bug é na **comparação**, não no tipo numérico (`int` vs `float` falham igual) |
| CT-BASE-06 | `(500, "COMUM")` | 100.0 ✅ | 100.0 | fronteira das faixas 10%/20% funcionando (não era bug) |
| CT-TETO-01/02 | `1000` vs `1000.01` | 200.0 vs 200 ✅ | idem | valida o **corte exato** no teto (200.002 → 200) |

Um teste "óbvio" com R$ 300 teria deixado o Bug 1 passar em branco — só a
fronteira de R$ 100 expôs.

### 2. Particionamento por variação de escrita (VIP)

O Bug 2 é invisível para `"VIP"` (a única forma que o Jr. testou de cabeça).
A matriz de entradas cobriu as variações que a regra menciona explicitamente:

| Teste | Entrada | Original | Esperado |
|---|---|---|---|
| CT-VIP-04 | `(300, "vip")` | 30.0 (❌) | 45.0 |
| CT-VIP-06 | `(300, "vIp")` | 30.0 (❌) | 45.0 |
| CT-VIP-07 | `(300, " vip ")` | 30.0 (❌) | 45.0 |
| CT-VIP-02/03 | `(99.99, "vip")`, `(100, "Vip")` | 0 / 0 (❌) | 5.0 / 15.0 |
| CT-VIP-05 | `(500, "VIP")` | 125.0 ✅ | 125.0 |

O contraste entre CT-VIP-04 (falha) e CT-VIP-05 (passa) **isola a causa na
comparação de strings** — o cálculo do bônus em si estava certo. Sem esse
par, seria fácil culpar a matemática do percentual.

### 3. Valores que isolam cada regra

- **Meio de faixa** (`300`, `800`): garantem que a correção não quebrou o
  comportamento que já funcionava (regressão do "teste de cabeça" do Jr.).
- **Par `int`/`float` na fronteira** (`100` e `100.0`): separa bug de lógica
  de bug de tipo — os dois falham igual, logo é lógica.
- **Cliente "lixo"** (`""`, `OURO`, `None`, `123`): garante que o bônus VIP
  só dispara para VIP de verdade (falso positivo de VIP).
- **Um centavo além do teto** (`1000.01`, `800.01`): valida `>` vs `>=` no
  corte de R$ 200 — mesma classe de bug do R$ 100, aplicada ao teto.

### Resultado

- **PRINT1 (código original): 8 falhas** — CT-BASE-03, CT-VIP-02, CT-VIP-03,
  CT-VIP-04, CT-VIP-06, CT-VIP-07, CT-INV-06a, CT-INV-06b: todas apontando
  para os **2 bugs de lógica** acima.
- **PRINT2 (código corrigido): 32 passaram, 3 xfail, 0 falhas.**

> Lição de QA: testar o caso "famoso" do R$ 300 é necessário, mas
> **insuficiente** — bugs de lógica em regras de faixa se escondem nas
> fronteiras e nas variações de formato da entrada.

---

Ver também: [`cenarios.md`](cenarios.md) · [`README.md`](README.md) ·
`prints/print_01.png` · `prints/print_02.png`
