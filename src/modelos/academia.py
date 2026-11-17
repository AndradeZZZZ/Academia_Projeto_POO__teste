"""Classe Academia: guarda tudo e concentra as operações de negócio."""
from excecoes import DadoInvalidoError, NaoEncontradoError
from interfaces import Exportavel
from modelos.pessoa import Aluno, Instrutor, Pessoa
from modelos.plano import Plano
from modelos.treino import Treino


class Academia:
    """A academia (composição: possui pessoas, planos e treinos)."""

    def __init__(self, nome: str) -> None:
        self.nome = nome
        self._pessoas: dict[str, Pessoa] = {}
        self._planos: dict[str, Plano] = {}
        self._treinos: dict[str, Treino] = {}

    # ---------- cadastros ----------
    def cadastrar_pessoa(self, pessoa: Pessoa) -> None:
        """Adiciona aluno ou instrutor; o CPF não pode se repetir."""
        if pessoa.cpf in self._pessoas:
            raise DadoInvalidoError(f'Já existe pessoa com o CPF {pessoa.cpf}.')
        self._pessoas[pessoa.cpf] = pessoa

    def cadastrar_plano(self, plano: Plano) -> None:
        """Adiciona um plano ao catálogo; cada tipo só pode existir uma vez."""
        if plano.tipo in self._planos:
            raise DadoInvalidoError(f'O plano {plano.tipo} já está cadastrado.')
        self._planos[plano.tipo] = plano

    def cadastrar_treino(self, treino: Treino) -> None:
        """Adiciona um treino ao catálogo."""
        self._treinos[treino.codigo] = treino

    # ---------- consultas ----------
    @property
    def pessoas(self) -> list[Pessoa]:
        """Cópia da lista de pessoas."""
        return list(self._pessoas.values())

    @property
    def planos(self) -> list[Plano]:
        """Cópia da lista de planos."""
        return list(self._planos.values())

    @property
    def treinos(self) -> list[Treino]:
        """Cópia da lista de treinos."""
        return list(self._treinos.values())

    @property
    def alunos(self) -> list[Aluno]:
        """Somente os alunos."""
        return [p for p in self._pessoas.values() if isinstance(p, Aluno)]

    def buscar_pessoa(self, cpf: str) -> Pessoa:
        """Busca aluno ou instrutor pelo CPF."""
        chave = Pessoa.limpar_cpf(cpf)
        if chave not in self._pessoas:
            raise NaoEncontradoError(f'Pessoa com CPF {chave} não encontrada.')
        return self._pessoas[chave]

    def buscar_aluno(self, cpf: str) -> Aluno:
        """Busca um aluno pelo CPF."""
        pessoa = self.buscar_pessoa(cpf)
        if not isinstance(pessoa, Aluno):
            raise NaoEncontradoError(f'{pessoa.nome} não é aluno.')
        return pessoa

    def buscar_instrutor(self, cpf: str) -> Instrutor:
        """Busca um instrutor pelo CPF."""
        pessoa = self.buscar_pessoa(cpf)
        if not isinstance(pessoa, Instrutor):
            raise NaoEncontradoError(f'{pessoa.nome} não é instrutor.')
        return pessoa

    def buscar_plano(self, tipo: str) -> Plano:
        """Busca plano pelo tipo (Mensal, Trimestral, Anual)."""
        chave = tipo.strip().capitalize()
        if chave not in self._planos:
            raise NaoEncontradoError(f'Plano {chave} não encontrado.')
        return self._planos[chave]

    def buscar_treino(self, codigo: str) -> Treino:
        """Busca treino pelo código (ex.: TRE-001)."""
        chave = codigo.strip().upper()
        if chave not in self._treinos:
            raise NaoEncontradoError(f'Treino {chave} não encontrado.')
        return self._treinos[chave]

    # ---------- operações de negócio ----------
    def matricular(self, cpf: str, tipo_plano: str) -> Aluno:
        """Matricula (ou troca o plano de) um aluno."""
        aluno = self.buscar_aluno(cpf)
        aluno.assinar_plano(self.buscar_plano(tipo_plano))
        return aluno

    def prescrever_treino(self, cpf_instrutor: str, cpf_aluno: str, codigo_treino: str) -> Treino:
        """Instrutor passa um treino a um aluno."""
        instrutor = self.buscar_instrutor(cpf_instrutor)
        aluno = self.buscar_aluno(cpf_aluno)
        treino = self.buscar_treino(codigo_treino)
        instrutor.prescrever(aluno, treino)
        return treino

    def registrar_presenca(self, cpf: str) -> int:
        """Check-in do aluno; retorna o total de presenças dele."""
        return self.buscar_aluno(cpf).registrar_presenca()

    def simular_planos(self) -> list[Plano]:
        """Planos para comparação (polimorfismo: cada um calcula o seu valor)."""
        return self.planos

    # ---------- relatórios ----------
    def faturamento_mensal(self) -> float:
        """Soma das mensalidades de todos os alunos com plano."""
        return sum(a.mensalidade for a in self.alunos)

    def faturamento_por_plano(self) -> dict[str, float]:
        """Faturamento mensal separado por tipo de plano."""
        resultado: dict[str, float] = {}
        for aluno in self.alunos:
            if aluno.plano is not None:
                tipo = aluno.plano.tipo
                resultado[tipo] = resultado.get(tipo, 0.0) + aluno.mensalidade
        return resultado

    def ranking_presencas(self, quantidade: int = 3) -> list[Aluno]:
        """Alunos com mais presenças, do maior para o menor."""
        ordenados = sorted(self.alunos, key=lambda a: a.presencas, reverse=True)
        return ordenados[:quantidade]

    def exportar_dados(self) -> list[str]:
        """Exporta tudo em linhas CSV usando o Protocol Exportavel."""
        itens: list[Exportavel] = [*self._pessoas.values(), *self._planos.values(),
                                   *self._treinos.values()]
        return [item.para_csv() for item in itens]
