# Diagrama de classes – Academia

```mermaid
classDiagram
    class Exportavel {
        <<interface>>
        +para_csv() str
    }

    class Pessoa {
        <<abstract>>
        +total_criados int
        +nome str
        +cpf str
        +papel str
        +from_string(texto)$ Pessoa
        +total_cadastradas()$ int
        +validar_cpf(cpf)$ bool
        +limpar_cpf(cpf)$ str
        +apresentar()* str
        +para_csv() str
    }

    class Aluno {
        +LIMITE_TREINOS int
        +matricula str
        +peso float
        +altura float
        -presencas int
        +imc float
        +mensalidade float
        +assinar_plano(plano)
        +adicionar_treino(treino)
        +registrar_presenca() int
        +apresentar() str
    }

    class Instrutor {
        +LIMITE_ALUNOS int
        +registro str
        +especialidade str
        +validar_registro(registro)$ bool
        +prescrever(aluno, treino)
        +apresentar() str
    }

    class Plano {
        <<abstract>>
        +VALOR_MINIMO float
        +total_criados int
        +valor_base float
        +tipo str
        +desconto_percentual float
        +valor_contrato float
        +from_string(texto)$ Plano
        +validar_valor(valor)$ bool
        +calcular_mensalidade()* float
        +duracao_meses()* int
        +beneficios()* str
        +descricao() str
        +para_csv() str
    }

    class Mensal {
        +calcular_mensalidade() float
        +duracao_meses() int
        +beneficios() str
    }

    class Trimestral {
        +DESCONTO float
        +calcular_mensalidade() float
        +duracao_meses() int
        +beneficios() str
    }

    class Anual {
        +DESCONTO float
        +AVALIACOES_GRATIS int
        +calcular_mensalidade() float
        +duracao_meses() int
        +beneficios() str
    }

    class Treino {
        +DURACAO_MINIMA int
        +DURACAO_MAXIMA int
        +codigo str
        +nome str
        +grupo_muscular str
        +duracao_min int
        +exercicios list
        +calorias_estimadas float
        +from_string(texto)$ Treino
        +validar_duracao(minutos)$ bool
        +para_csv() str
    }

    class Academia {
        +nome str
        +cadastrar_pessoa(pessoa)
        +cadastrar_plano(plano)
        +cadastrar_treino(treino)
        +buscar_pessoa(cpf) Pessoa
        +matricular(cpf, tipo_plano) Aluno
        +prescrever_treino(cpf_instrutor, cpf_aluno, codigo) Treino
        +registrar_presenca(cpf) int
        +faturamento_mensal() float
        +faturamento_por_plano() dict
        +ranking_presencas(quantidade) list
        +exportar_dados() list
    }

    Pessoa <|-- Aluno
    Pessoa <|-- Instrutor
    Plano <|-- Mensal
    Plano <|-- Trimestral
    Plano <|-- Anual

    Academia "1" *-- "0..*" Pessoa : possui
    Academia "1" *-- "0..*" Plano : oferece
    Academia "1" *-- "0..*" Treino : cataloga
    Aluno "0..*" --> "0..1" Plano : plano atual
    Aluno "1" *-- "0..3" Treino : treinos
    Instrutor "1" o-- "0..5" Aluno : atende

    Exportavel <|.. Pessoa
    Exportavel <|.. Plano
    Exportavel <|.. Treino
```

Legenda: `<|--` herança · `*--` composição · `o--` agregação · `-->` associação · `<|..` implementa o Protocol · `$` método estático/de classe · `*` método abstrato · `-` privado.
