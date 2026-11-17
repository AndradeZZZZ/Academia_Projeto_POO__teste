# Roteiro de apresentação (até 10 minutos)

## Divisão sugerida (5 integrantes)

Todos devem saber explicar qualquer parte, mas cada um conduz um bloco.

| Integrante | Conduz | Requisitos |
|---|---|---|
| 1 | Cenário, regras de negócio e diagrama de classes (1 min) | visão geral |
| 2 | Classes, composição, encapsulamento e properties | R1, R2, R3, R5 |
| 3 | Atributos de classe, classmethod, staticmethod | R4, R6 |
| 4 | Herança, `super()`, sobrescrita, polimorfismo | R7, R8 |
| 5 | Classes abstratas, Protocol, exceções | R9, R10 |

## Demonstração no terminal (sequência pronta)

1. Opção **5**: lista as pessoas (polimórfica: aluno mostra plano e IMC, instrutor mostra registro e alunos).
2. Opção **12**: compara planos (cada subclasse calcula mensalidade, desconto e contrato do seu jeito).
3. Opção **10**: instrutor `55566677788` prescreve `TRE-002` para a Carla `11122233344` → erro, ela está sem plano.
4. Opção **9**: matricula a Carla no plano `Trimestral` → sucesso. Repete a opção **10** → sucesso.
5. Opção **10** de novo com um treino que a Ana (`12345678901`) já tem → erro de treino repetido.
6. Opção **11**: registra presença da Ana e mostra o contador subindo.
7. Opção **13**: faturamento mensal por plano e ranking de presenças. Opção **14**: exportação via Protocol.
8. Entradas inválidas: opção **1** com CPF `123`; opção **3** com valor `20`; opção **4** com duração `5` e depois `abc`.

## Alterações ao vivo (já testadas neste código)

### A) Nova subclasse sem mexer no que já usa a base

Acrescentar no fim de `src/modelos/plano.py`:

```python
class Semestral(Plano):
    """Plano de 6 meses com 15% de desconto."""

    DESCONTO: float = 0.15

    def calcular_mensalidade(self) -> float:
        return self.valor_base * (1 - Semestral.DESCONTO)

    def duracao_meses(self) -> int:
        return 6

    def beneficios(self) -> str:
        return 'Musculação, aulas coletivas e 1 avaliação física'
```

- `listar_planos`, `simular_planos`, `Plano.descricao`, `faturamento_mensal` e `matricular` **não mudam**: já funcionam com o novo plano (é o polimorfismo).
- Para cadastrar pelo menu: importar `Semestral` em `menu.py` e acrescentar `'4': Semestral` em `TIPOS_PLANO`. Para só mostrar funcionando, basta `academia.cadastrar_plano(Semestral(120.0))` em `dados_exemplo.py`.

### B) Nova regra com nova exceção (aluno não pode contratar o plano que já tem)

1. Em `excecoes.py`:

```python
class PlanoJaContratadoError(ErroAcademia):
    """Lançada quando o aluno tenta contratar o plano que já possui."""
```

2. Em `modelos/pessoa.py`, importar a exceção e, em `Aluno.assinar_plano`, antes de `self._plano = plano`:

```python
if self._plano is not None and self._plano.tipo == plano.tipo:
    raise PlanoJaContratadoError(f'{self.nome} já está no plano {plano.tipo}.')
```

O menu **não muda**: ele já captura `ErroAcademia`.

### C) Mudar uma validação de property

- Valor mínimo do plano: trocar `VALOR_MINIMO = 50.0` em `Plano`.
- Duração máxima do treino: trocar `DURACAO_MAXIMA = 180` em `Treino`.
- Peso mínimo: alterar `20 <= valor <= 300` no setter de `Aluno.peso`.
- Limite de treinos ou de alunos: `Aluno.LIMITE_TREINOS` e `Instrutor.LIMITE_ALUNOS`.

Como os `__init__` usam `self.x = x`, a nova regra vale já na criação do objeto.

## Perguntas que o professor pode fazer neste código

- **Onde está o polimorfismo?** `menu.listar_pessoas` e `menu.listar_planos`: mesmo `for`, cada objeto responde do seu jeito.
- **Por que `Plano` e `Pessoa` são abstratas?** Não existe um plano nem uma pessoa genéricos na academia; elas definem o contrato que as subclasses cumprem.
- **Por que `desconto_percentual` é property e não atributo?** Ele é calculado a partir de `calcular_mensalidade()`; assim nunca fica desatualizado.
- **Por que `__presencas` é privado?** Para só subir por `registrar_presenca()`, que exige plano. Fora da classe o nome vira `_Aluno__presencas`.
- **Por que `Treino` recebe `exercicios=None` e não `[]`?** Lista como valor padrão seria compartilhada entre todos os treinos.
- **Por que `Pessoa.from_string` usa `cls(*partes)`?** Para funcionar em `Aluno.from_string` e `Instrutor.from_string`, cada um com seus campos. Chamar em `Pessoa` dá erro porque ela é abstrata.
- **Quais classes usam o Protocol e por que não herdam?** `Pessoa`, `Plano` e `Treino`: não têm parentesco, só o mesmo método `para_csv`.
- **Por que `Aluno.para_csv` chama `super().para_csv()`?** Para reaproveitar a linha base de `Pessoa` e só acrescentar matrícula e plano.
- **A regra de plano ativo está no menu?** Não: `Aluno.adicionar_treino` e `Aluno.registrar_presenca` lançam `AlunoSemPlanoError`.
- **Por que `Pessoa.total_criados += 1` e não `self.total_criados`?** `self.` criaria um atributo de instância e não alteraria o contador da classe.
