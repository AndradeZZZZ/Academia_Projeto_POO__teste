"""Hierarquia de pessoas: Pessoa (abstrata), Aluno e Instrutor."""
import re
from abc import ABC, abstractmethod

from excecoes import (AlunoSemPlanoError, DadoInvalidoError, LimiteAlunosError,
                      LimiteTreinosError)
from modelos.plano import Plano
from modelos.treino import Treino


class Pessoa(ABC):
    """Classe base abstrata de quem frequenta ou trabalha na academia."""

    total_criados: int = 0   # R6

    def __init__(self, nome: str, cpf: str) -> None:
        """Cria a pessoa. Nome e CPF passam pelos setters."""
        self.nome = nome
        self.cpf = cpf
        Pessoa.total_criados += 1

    @property
    def nome(self) -> str:
        """Nome da pessoa."""
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = valor.strip()
        if len(valor) < 2:
            raise DadoInvalidoError('O nome deve ter ao menos 2 caracteres.')
        self._nome = valor

    @property
    def cpf(self) -> str:
        """CPF somente com números."""
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str) -> None:
        limpo = Pessoa.limpar_cpf(valor)
        if not Pessoa.validar_cpf(limpo):
            raise DadoInvalidoError(f'CPF {valor!r} inválido. Informe 11 números.')
        self._cpf = limpo

    @property
    def papel(self) -> str:
        """Property calculada: nome da classe concreta (Aluno, Instrutor)."""
        return type(self).__name__

    @classmethod
    def from_string(cls, texto: str) -> 'Pessoa':
        """Construtor alternativo: 'nome;cpf' (Aluno) ou 'nome;cpf;registro;especialidade' (Instrutor)."""
        partes = [p.strip() for p in texto.split(';')]
        try:
            return cls(*partes)
        except TypeError:
            raise DadoInvalidoError(f'Quantidade ou tipo de campos inválido para {cls.__name__}.')

    @classmethod
    def total_cadastradas(cls) -> int:
        """Quantidade de pessoas já criadas."""
        return cls.total_criados

    @staticmethod
    def limpar_cpf(cpf: str) -> str:
        """Remove pontos, traços e espaços do CPF."""
        return cpf.replace('.', '').replace('-', '').replace(' ', '')

    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """Confere se o CPF tem 11 dígitos numéricos."""
        return cpf.isdigit() and len(cpf) == 11

    @abstractmethod
    def apresentar(self) -> str:
        """Texto de apresentação (cada tipo de pessoa mostra o seu)."""

    def para_csv(self) -> str:
        """Cumpre o Protocol Exportavel."""
        return f'{self.papel.lower()};{self.nome};{self.cpf}'

    def __str__(self) -> str:
        return self.apresentar()


class Aluno(Pessoa):
    """Aluno da academia: tem plano, treinos e presenças."""

    LIMITE_TREINOS: int = 3   # R6
    _proximo_numero: int = 1  # R6: gerador de matrículas

    def __init__(self, nome: str, cpf: str, peso: float = 70.0, altura: float = 1.70) -> None:
        super().__init__(nome, cpf)   # R7
        self.matricula: str = f'ALU-{Aluno._proximo_numero:03d}'
        Aluno._proximo_numero += 1
        self.peso = peso
        self.altura = altura
        self._plano: Plano | None = None       # R2: composição
        self._treinos: list[Treino] = []       # R2: composição
        self.__presencas: int = 0              # R3: atributo privado

    @property
    def peso(self) -> float:
        """Peso em kg."""
        return self._peso

    @peso.setter
    def peso(self, valor: float) -> None:
        if not 20 <= valor <= 300:
            raise DadoInvalidoError(f'Peso {valor} inválido. Use de 20 a 300 kg.')
        self._peso = valor

    @property
    def altura(self) -> float:
        """Altura em metros."""
        return self._altura

    @altura.setter
    def altura(self, valor: float) -> None:
        if not 1.0 <= valor <= 2.5:
            raise DadoInvalidoError(f'Altura {valor} inválida. Use de 1,00 a 2,50 m.')
        self._altura = valor

    @property
    def imc(self) -> float:
        """Property calculada: índice de massa corporal."""
        return self.peso / self.altura ** 2

    @property
    def plano(self) -> Plano | None:
        """Plano atual (somente leitura; muda por `assinar_plano`)."""
        return self._plano

    @property
    def treinos(self) -> list[Treino]:
        """Cópia da lista de treinos."""
        return list(self._treinos)

    @property
    def presencas(self) -> int:
        """Quantidade de presenças (somente leitura)."""
        return self.__presencas

    @property
    def mensalidade(self) -> float:
        """Property calculada: mensalidade do plano atual (0 se não tem plano)."""
        return self._plano.calcular_mensalidade() if self._plano else 0.0

    def classificacao_imc(self) -> str:
        """Faixa do IMC em texto."""
        if self.imc < 18.5:
            return 'abaixo do peso'
        if self.imc < 25:
            return 'peso normal'
        if self.imc < 30:
            return 'sobrepeso'
        return 'obesidade'

    def assinar_plano(self, plano: Plano) -> None:
        """Contrata (ou troca) o plano do aluno."""
        if not isinstance(plano, Plano):
            raise DadoInvalidoError('Plano inválido.')
        self._plano = plano

    def adicionar_treino(self, treino: Treino) -> None:
        """Recebe um treino; exige plano ativo e respeita o limite."""
        if self._plano is None:
            raise AlunoSemPlanoError(f'{self.nome} não tem plano ativo.')
        if treino in self._treinos:
            raise DadoInvalidoError(f'{self.nome} já tem o treino {treino.codigo}.')
        if len(self._treinos) >= Aluno.LIMITE_TREINOS:
            raise LimiteTreinosError(
                f'{self.nome} já tem {Aluno.LIMITE_TREINOS} treinos (limite máximo).')
        self._treinos.append(treino)

    def registrar_presenca(self) -> int:
        """Check-in na academia; exige plano ativo. Retorna o total de presenças."""
        if self._plano is None:
            raise AlunoSemPlanoError(f'{self.nome} não tem plano ativo.')
        self.__presencas += 1
        return self.__presencas

    def apresentar(self) -> str:
        plano = self._plano.tipo if self._plano else 'sem plano'
        return (f'🎓 Aluno {self.nome} (Mat: {self.matricula}) - Plano: {plano} - '
                f'Mensalidade: R$ {self.mensalidade:.2f} - Presenças: {self.presencas} - '
                f'IMC {self.imc:.1f} ({self.classificacao_imc()})')

    def para_csv(self) -> str:
        plano = self._plano.tipo if self._plano else '-'
        return f'{super().para_csv()};{self.matricula};{plano}'


class Instrutor(Pessoa):
    """Instrutor: acompanha alunos e prescreve treinos."""

    LIMITE_ALUNOS: int = 5   # R6

    def __init__(self, nome: str, cpf: str, registro: str, especialidade: str = 'Musculação') -> None:
        super().__init__(nome, cpf)
        self.registro = registro
        self.especialidade = especialidade
        self._alunos: list[Aluno] = []   # R2: composição

    @property
    def registro(self) -> str:
        """Registro profissional (formato CREF-123456)."""
        return self._registro

    @registro.setter
    def registro(self, valor: str) -> None:
        valor = valor.strip().upper()
        if not Instrutor.validar_registro(valor):
            raise DadoInvalidoError(f'Registro {valor!r} inválido. Use o formato CREF-123456.')
        self._registro = valor

    @property
    def alunos(self) -> list[Aluno]:
        """Cópia da lista de alunos atendidos."""
        return list(self._alunos)

    @staticmethod
    def validar_registro(registro: str) -> bool:
        """Confere o formato CREF- seguido de 4 a 6 números."""
        return re.fullmatch(r'CREF-\d{4,6}', registro) is not None

    def prescrever(self, aluno: Aluno, treino: Treino) -> None:
        """Passa um treino a um aluno, respeitando o limite de alunos do instrutor."""
        novo_vinculo = aluno not in self._alunos
        if novo_vinculo and len(self._alunos) >= Instrutor.LIMITE_ALUNOS:
            raise LimiteAlunosError(
                f'{self.nome} já atende {Instrutor.LIMITE_ALUNOS} alunos (limite máximo).')
        aluno.adicionar_treino(treino)   # valida plano e limite do aluno
        if novo_vinculo:
            self._alunos.append(aluno)

    def apresentar(self) -> str:
        return (f'🏋️ Instrutor {self.nome} (Reg: {self.registro}) - {self.especialidade} - '
                f'{len(self._alunos)} aluno(s)')
