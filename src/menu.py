"""Terminal interativo. Aqui só há leitura de dados, chamadas e exibição.

As regras de negócio ficam nas classes de modelos/.
"""
from excecoes import ErroAcademia
from modelos.academia import Academia
from modelos.pessoa import Aluno, Instrutor
from modelos.plano import Anual, Mensal, Trimestral
from modelos.treino import Treino

# Para criar um novo tipo de plano no menu, basta acrescentar uma linha aqui.
TIPOS_PLANO = {
    '1': Mensal,
    '2': Trimestral,
    '3': Anual,
}


def ler_numero(mensagem: str, conversor=int):
    """Lê um número aceitando vírgula decimal. Lança ValueError se inválido."""
    return conversor(input(mensagem).strip().replace(',', '.'))


def cadastrar_aluno(academia: Academia) -> None:
    nome = input('Nome: ')
    cpf = input('CPF (11 números): ')
    peso = ler_numero('Peso (kg): ', float)
    altura = ler_numero('Altura (m): ', float)
    academia.cadastrar_pessoa(Aluno(nome, cpf, peso, altura))
    print('✅ Aluno cadastrado.')


def cadastrar_instrutor(academia: Academia) -> None:
    nome = input('Nome: ')
    cpf = input('CPF (11 números): ')
    registro = input('Registro (ex.: CREF-123456): ')
    especialidade = input('Especialidade: ')
    academia.cadastrar_pessoa(Instrutor(nome, cpf, registro, especialidade))
    print('✅ Instrutor cadastrado.')


def cadastrar_plano(academia: Academia) -> None:
    print('Tipo: 1 - Mensal | 2 - Trimestral | 3 - Anual')
    escolha = input('Tipo: ').strip()
    if escolha not in TIPOS_PLANO:
        print('❌ Tipo inválido.')
        return
    valor = ler_numero('Valor base da mensalidade (R$): ', float)
    academia.cadastrar_plano(TIPOS_PLANO[escolha](valor))
    print('✅ Plano cadastrado.')


def criar_treino(academia: Academia) -> None:
    nome = input('Nome do treino: ')
    grupo = input('Grupo muscular: ')
    duracao = ler_numero('Duração (minutos): ')
    lista = input('Exercícios (separados por vírgula): ')
    exercicios = [e.strip() for e in lista.split(',') if e.strip()]
    treino = Treino(nome, grupo, duracao, exercicios)
    academia.cadastrar_treino(treino)
    print(f'✅ Treino criado com o código {treino.codigo}.')


def listar_pessoas(academia: Academia) -> None:
    print('--- Pessoas ---')
    for pessoa in academia.pessoas:      # lista mista: polimorfismo
        print(pessoa)


def listar_planos(academia: Academia) -> None:
    print('--- Planos ---')
    for plano in academia.planos:        # lista mista: polimorfismo
        print(plano)


def listar_treinos(academia: Academia) -> None:
    print('--- Treinos ---')
    for treino in academia.treinos:
        print(treino)


def buscar_pessoa(academia: Academia) -> None:
    pessoa = academia.buscar_pessoa(input('CPF: '))
    print(pessoa)
    if isinstance(pessoa, Aluno):
        for treino in pessoa.treinos:
            print(f'   • {treino}')


def matricular(academia: Academia) -> None:
    cpf = input('CPF do aluno: ')
    tipo = input('Plano (Mensal, Trimestral ou Anual): ')
    aluno = academia.matricular(cpf, tipo)
    print(f'✅ Matrícula realizada: {aluno}')


def prescrever(academia: Academia) -> None:
    cpf_instrutor = input('CPF do instrutor: ')
    cpf_aluno = input('CPF do aluno: ')
    codigo = input('Código do treino (ex.: TRE-001): ')
    treino = academia.prescrever_treino(cpf_instrutor, cpf_aluno, codigo)
    print(f'✅ Treino {treino.codigo} prescrito.')


def registrar_presenca(academia: Academia) -> None:
    total = academia.registrar_presenca(input('CPF do aluno: '))
    print(f'✅ Presença registrada. Total do aluno: {total}')


def simular_planos(academia: Academia) -> None:
    print('--- Comparação de planos ---')
    for plano in academia.simular_planos():
        print(f'{plano.tipo:11} mensalidade R$ {plano.calcular_mensalidade():7.2f} | '
              f'desconto {plano.desconto_percentual:4.1f}% | '
              f'contrato ({plano.duracao_meses()} m) R$ {plano.valor_contrato:8.2f}')


def relatorio(academia: Academia) -> None:
    print('--- Relatório ---')
    print(f'Faturamento mensal: R$ {academia.faturamento_mensal():.2f}')
    for tipo, valor in academia.faturamento_por_plano().items():
        print(f'  {tipo}: R$ {valor:.2f}')
    print('Ranking de presenças:')
    for posicao, aluno in enumerate(academia.ranking_presencas(), start=1):
        print(f'  {posicao}º {aluno.nome} - {aluno.presencas} presença(s)')


def exportar(academia: Academia) -> None:
    print('--- Exportação (CSV) ---')
    for linha in academia.exportar_dados():
        print(linha)


ACOES = {
    '1': ('Cadastrar aluno', cadastrar_aluno),
    '2': ('Cadastrar instrutor', cadastrar_instrutor),
    '3': ('Cadastrar plano', cadastrar_plano),
    '4': ('Criar treino', criar_treino),
    '5': ('Listar pessoas', listar_pessoas),
    '6': ('Listar planos', listar_planos),
    '7': ('Listar treinos', listar_treinos),
    '8': ('Buscar pessoa por CPF', buscar_pessoa),
    '9': ('Matricular aluno em plano', matricular),
    '10': ('Prescrever treino', prescrever),
    '11': ('Registrar presença', registrar_presenca),
    '12': ('Comparar planos', simular_planos),
    '13': ('Relatório de faturamento e presenças', relatorio),
    '14': ('Exportar dados (CSV)', exportar),
}


def mostrar_menu(nome: str) -> None:
    print(f'\n========== {nome.upper()} ==========')
    for numero, (titulo, _) in ACOES.items():
        print(f'{numero} - {titulo}')
    print('0 - Sair')


def executar(academia: Academia) -> None:
    """Loop principal do menu."""
    while True:
        mostrar_menu(academia.nome)
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '0':
            print('Até logo!')
            break
        if opcao not in ACOES:
            print('❌ Opção inválida.')
            continue
        try:
            ACOES[opcao][1](academia)
        except ErroAcademia as erro:      # erros de regra de negócio
            print(f'❌ {erro}')
        except ValueError:                # texto digitado onde era esperado número
            print('❌ Valor numérico inválido.')
