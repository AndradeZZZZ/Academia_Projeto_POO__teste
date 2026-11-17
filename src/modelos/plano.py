"""Hierarquia de planos: Plano (abstrata), Mensal, Trimestral e Anual."""
from abc import ABC, abstractmethod

from excecoes import DadoInvalidoError


class Plano(ABC):
    """Classe base abstrata dos planos da academia."""

    VALOR_MINIMO: float = 50.0   # R6: constante compartilhada
    total_criados: int = 0       # R6: contador compartilhado

    def __init__(self, valor_base: float) -> None:
        """Cria o plano. O valor base passa pelo setter (validação)."""
        self.valor_base = valor_base
        Plano.total_criados += 1

    # ---------- R5: properties ----------
    @property
    def valor_base(self) -> float:
        """Valor cheio de uma mensalidade, antes de descontos."""
        return self._valor_base

    @valor_base.setter
    def valor_base(self, valor: float) -> None:
        if not Plano.validar_valor(valor):
            raise DadoInvalidoError(
                f'Valor R$ {valor:.2f} inválido. Mínimo: R$ {Plano.VALOR_MINIMO:.2f}.')
        self._valor_base = valor

    @property
    def tipo(self) -> str:
        """Property calculada: nome da classe concreta (Mensal, Anual...)."""
        return type(self).__name__

    @property
    def desconto_percentual(self) -> float:
        """Property calculada: quanto a mensalidade é menor que o valor base."""
        return (1 - self.calcular_mensalidade() / self.valor_base) * 100

    @property
    def valor_contrato(self) -> float:
        """Property calculada: mensalidade vezes a duração do plano."""
        return self.calcular_mensalidade() * self.duracao_meses()

    # ---------- R4: classmethod e staticmethod ----------
    @classmethod
    def from_string(cls, texto: str) -> 'Plano':
        """Construtor alternativo a partir do valor em texto (ex.: '120,00')."""
        try:
            return cls(float(texto.strip().replace(',', '.')))
        except ValueError:
            raise DadoInvalidoError(f'Valor {texto!r} não é um número.')

    @classmethod
    def total_cadastrados(cls) -> int:
        """Quantidade de planos já criados."""
        return cls.total_criados

    @staticmethod
    def validar_valor(valor: float) -> bool:
        """Confere se o valor atinge o mínimo (não depende de nenhum objeto)."""
        return valor >= Plano.VALOR_MINIMO

    # ---------- R9: contrato abstrato ----------
    @abstractmethod
    def calcular_mensalidade(self) -> float:
        """Valor cobrado por mês (cada plano calcula o seu)."""

    @abstractmethod
    def duracao_meses(self) -> int:
        """Duração do contrato em meses."""

    @abstractmethod
    def beneficios(self) -> str:
        """Texto com o que o plano oferece."""

    # ---------- métodos concretos herdados por todos ----------
    def descricao(self) -> str:
        """Linha de descrição usada nas listagens."""
        return (f'Plano {self.tipo} - R$ {self.calcular_mensalidade():.2f}/mês '
                f'({self.desconto_percentual:.0f}% de desconto) - '
                f'{self.duracao_meses()} mês(es) - {self.beneficios()}')

    def para_csv(self) -> str:
        """Cumpre o Protocol Exportavel."""
        return f'plano;{self.tipo};{self.valor_base:.2f};{self.calcular_mensalidade():.2f}'

    def __str__(self) -> str:
        return self.descricao()


class Mensal(Plano):
    """Plano de 1 mês, sem desconto."""

    def calcular_mensalidade(self) -> float:
        """Paga o valor cheio."""
        return self.valor_base

    def duracao_meses(self) -> int:
        return 1

    def beneficios(self) -> str:
        return 'Musculação'


class Trimestral(Plano):
    """Plano de 3 meses com 10% de desconto."""

    DESCONTO: float = 0.10

    def calcular_mensalidade(self) -> float:
        """Valor base com 10% de desconto."""
        return self.valor_base * (1 - Trimestral.DESCONTO)

    def duracao_meses(self) -> int:
        return 3

    def beneficios(self) -> str:
        return 'Musculação e aulas coletivas'


class Anual(Plano):
    """Plano de 12 meses com 20% de desconto e avaliações físicas."""

    DESCONTO: float = 0.20
    AVALIACOES_GRATIS: int = 2

    def calcular_mensalidade(self) -> float:
        """Valor base com 20% de desconto."""
        return self.valor_base * (1 - Anual.DESCONTO)

    def duracao_meses(self) -> int:
        return 12

    def beneficios(self) -> str:
        return f'Musculação, aulas coletivas e {Anual.AVALIACOES_GRATIS} avaliações físicas'
