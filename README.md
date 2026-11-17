# Sistema de Academia

Trabalho de **Programação Orientada a Objetos** (Python), UniAnchieta.

**Integrantes:**

- Guilherme Luna de Andrade (RA: 2610936)
- Rodrigo Callegari Prebianchi (RA: 2602287)
- Pedro Henrique Roberto da Silva (RA: 2612743)
- Fabrício Biagi (RA: 2528778)

## Descrição do cenário

Uma academia tem **alunos** e **instrutores**, oferece **planos** (Mensal, Trimestral e Anual) e monta **treinos**. O aluno contrata um plano, recebe treinos prescritos por um instrutor e registra presença a cada ida à academia. Cada plano calcula a mensalidade de um jeito (com mais desconto nos contratos longos). O sistema funciona por um menu no terminal.

### Regras de negócio

| # | Regra | Onde está |
|---|---|---|
| 1 | CPF com 11 números (aceita pontos e traço); não pode repetir | `Pessoa.cpf` (setter) / `Academia.cadastrar_pessoa` |
| 2 | Nome com ao menos 2 caracteres | `Pessoa.nome` (setter) |
| 3 | Peso de 20 a 300 kg e altura de 1,00 a 2,50 m; o IMC é calculado | `Aluno.peso`, `Aluno.altura`, `Aluno.imc` |
| 4 | Registro do instrutor no formato `CREF-` + 4 a 6 números | `Instrutor.registro` / `Instrutor.validar_registro` |
| 5 | Valor base do plano de no mínimo R$ 50,00; cada tipo de plano só é cadastrado uma vez | `Plano.valor_base` / `Academia.cadastrar_plano` |
| 6 | **Mensal:** valor cheio, 1 mês. **Trimestral:** 10% de desconto, 3 meses. **Anual:** 20% de desconto, 12 meses e 2 avaliações físicas | `calcular_mensalidade()`, `duracao_meses()`, `beneficios()` em cada subclasse de `Plano` |
| 7 | Treino de 10 a 180 minutos; gasto estimado de 7 kcal por minuto | `Treino.duracao_min` / `Treino.calorias_estimadas` |
| 8 | Aluno **sem plano** não recebe treino nem registra presença | `Aluno.adicionar_treino`, `Aluno.registrar_presenca` |
| 9 | Aluno pode ter no máximo 3 treinos, sem repetir | `Aluno.adicionar_treino` |
| 10 | Instrutor atende no máximo 5 alunos | `Instrutor.prescrever` |

## Mapeamento das entidades

| Entidade | Atributos | Comportamentos (métodos) |
|---|---|---|
| `Pessoa` *(abstrata)* | nome, cpf | `apresentar()` *(abstrato)*, `para_csv()`, `from_string()`, `validar_cpf()`, `limpar_cpf()` |
| `Aluno` *(herda de Pessoa)* | matricula, peso, altura, plano, treinos, presencas (privado) | `imc` *(property calculada)*, `mensalidade` *(property calculada)*, `assinar_plano()`, `adicionar_treino()`, `registrar_presenca()`, `apresentar()` |
| `Instrutor` *(herda de Pessoa)* | registro, especialidade, alunos | `prescrever()`, `validar_registro()`, `apresentar()` |
| `Plano` *(abstrata)* | valor_base | `calcular_mensalidade()` *(abstrato)*, `duracao_meses()` *(abstrato)*, `beneficios()` *(abstrato)*, `desconto_percentual` *(property calculada)*, `valor_contrato` *(property calculada)*, `descricao()` |
| `Mensal`, `Trimestral`, `Anual` *(herdam de Plano)* | — | `calcular_mensalidade()`, `duracao_meses()`, `beneficios()` |
| `Treino` | codigo, nome, grupo_muscular, duracao_min, exercicios | `calorias_estimadas` *(property calculada)*, `from_string()`, `validar_duracao()` |
| `Academia` | nome, pessoas, planos, treinos | `cadastrar_pessoa()`, `cadastrar_plano()`, `cadastrar_treino()`, `buscar_pessoa()`, `matricular()`, `prescrever_treino()`, `registrar_presenca()`, `faturamento_mensal()`, `faturamento_por_plano()`, `ranking_presencas()`, `exportar_dados()` |
| `Exportavel` *(Protocol)* | — | `para_csv()` |

Relacionamentos:

```
        Pessoa (ABC)                      Plano (ABC)
        /         \                      /     |      \
    Aluno      Instrutor            Mensal Trimestral Anual     → Herança ("é um")

Academia ◆── Pessoa / Plano / Treino                            → Composição ("possui")
Aluno    ◆── Plano, Treino (lista)                              → Composição ("tem um")
Instrutor ◆── Aluno (lista)                                     → Composição ("tem um")

Pessoa, Plano, Treino  ··▷ Exportavel                           → Protocol (sem herança)
```

O diagrama completo (Mermaid) está em [`docs/diagrama-classes.md`](docs/diagrama-classes.md).

## Onde cada requisito foi aplicado

| # | Requisito | Arquivo | Classe / método |
|---|---|---|---|
| R1 | Classes e objetos (9 classes de domínio) | `src/modelos/` | `Pessoa`, `Aluno`, `Instrutor`, `Plano`, `Mensal`, `Trimestral`, `Anual`, `Treino`, `Academia`, todas com `__init__` e `self` |
| R2 | Composição | `pessoa.py`, `academia.py` | `Aluno.__init__` (`_plano`, `_treinos`); `Instrutor.__init__` (`_alunos`); `Academia.__init__` (`_pessoas`, `_planos`, `_treinos`) |
| R3 | Encapsulamento | `pessoa.py`, `plano.py`, `treino.py` | `Aluno.__presencas` (privado, acessado por `presencas` e `registrar_presenca`); `Aluno._plano` (muda só por `assinar_plano`); `_nome`, `_cpf`, `_peso`, `_altura`, `_registro`, `Plano._valor_base`, `Treino._duracao_min`, `Treino._exercicios` |
| R4 | `@classmethod` e `@staticmethod` | `pessoa.py`, `plano.py`, `treino.py` | classmethod: `Pessoa.from_string`, `Pessoa.total_cadastradas`, `Plano.from_string`, `Plano.total_cadastrados`, `Treino.from_string`; staticmethod: `Pessoa.validar_cpf`, `Pessoa.limpar_cpf`, `Instrutor.validar_registro`, `Plano.validar_valor`, `Treino.validar_duracao` |
| R5 | Properties | `pessoa.py`, `plano.py`, `treino.py` | setters com validação: `Pessoa.nome/cpf`, `Aluno.peso/altura`, `Instrutor.registro`, `Plano.valor_base`, `Treino.nome/duracao_min`; calculadas: `Aluno.imc`, `Aluno.mensalidade`, `Plano.desconto_percentual`, `Plano.valor_contrato`, `Plano.tipo`, `Pessoa.papel`, `Treino.calorias_estimadas` |
| R6 | Atributos de classe | todos em `src/modelos/` | `Pessoa.total_criados`, `Aluno.LIMITE_TREINOS`, `Aluno._proximo_numero`, `Instrutor.LIMITE_ALUNOS`, `Plano.VALOR_MINIMO`, `Plano.total_criados`, `Trimestral.DESCONTO`, `Anual.DESCONTO`, `Anual.AVALIACOES_GRATIS`, `Treino.DURACAO_MINIMA/MAXIMA`, `Treino.GASTO_CALORICO_POR_MINUTO` |
| R7 | Herança e `super()` | `pessoa.py`, `plano.py` | `Aluno` e `Instrutor` herdam de `Pessoa` (`super().__init__()`; `Aluno.para_csv` usa `super().para_csv()`); `Mensal`, `Trimestral` e `Anual` herdam de `Plano` |
| R8 | Sobrescrita e polimorfismo | `pessoa.py`, `plano.py`, `menu.py`, `academia.py` | `apresentar` sobrescrito em `Aluno` e `Instrutor`; `calcular_mensalidade`, `duracao_meses`, `beneficios` sobrescritos nos 3 planos; chamados de forma uniforme em `menu.listar_pessoas`, `menu.listar_planos`, `menu.simular_planos` e `Plano.descricao` |
| R9 | Classe abstrata | `pessoa.py`, `plano.py` | `Pessoa(ABC)` com `@abstractmethod apresentar`; `Plano(ABC)` com `@abstractmethod` em `calcular_mensalidade`, `duracao_meses` e `beneficios` |
| R10 | Protocol | `src/interfaces.py`, `src/modelos/academia.py` | `Exportavel` implementado por `Pessoa`, `Plano` e `Treino` (sem herança em comum) e usado em `Academia.exportar_dados` |

Outros itens do enunciado:

- **Exceções customizadas:** `src/excecoes.py` (`ErroAcademia` e filhas).
- **Type hints e docstrings:** em todas as classes e métodos públicos.
- **Somente biblioteca padrão:** usa `abc`, `re` e `typing`.
- **Regras nas classes, não no menu:** o `menu.py` só lê dados, chama métodos e imprime resultados e erros.
- **Dados de exemplo:** `src/dados_exemplo.py` (3 planos, 3 alunos, 2 instrutores, 3 treinos, matrículas, presenças e 1 treino já prescrito).

## Menu do terminal

| Opção | Função |
|---|---|
| 1 | Cadastrar aluno |
| 2 | Cadastrar instrutor |
| 3 | Cadastrar plano |
| 4 | Criar treino |
| 5 | Listar pessoas *(listagem polimórfica)* |
| 6 | Listar planos *(listagem polimórfica)* |
| 7 | Listar treinos |
| 8 | Buscar pessoa por CPF |
| 9 | Matricular aluno em plano *(operação de negócio)* |
| 10 | Prescrever treino *(operação de negócio: instrutor, aluno e treino)* |
| 11 | Registrar presença *(operação de negócio)* |
| 12 | Comparar planos *(cálculo polimórfico)* |
| 13 | Relatório de faturamento e presenças |
| 14 | Exportar dados (CSV) |
| 0 | Sair |

## Como executar

Requer **Python 3.10 ou superior** (nenhuma instalação extra).

```bash
python src/main.py
```

Entradas para testar os erros: prescrever treino para a Carla (CPF `11122233344`, sem plano), CPF `123`, valor de plano `20`, duração de treino `5`, treino repetido para a Ana (CPF `12345678901`).

## Estrutura

```
trabalho-poo/
├── README.md
├── docs/
│   ├── diagrama-classes.md
│   └── roteiro-apresentacao.md
└── src/
    ├── main.py
    ├── menu.py
    ├── dados_exemplo.py
    ├── excecoes.py
    ├── interfaces.py
    └── modelos/
        ├── __init__.py
        ├── pessoa.py
        ├── plano.py
        ├── treino.py
        └── academia.py
```
