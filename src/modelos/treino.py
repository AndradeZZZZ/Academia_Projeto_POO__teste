"""Classe Treino."""
from excecoes import DadoInvalidoError


class Treino:
    """Ficha de treino (ex.: Treino A - Peito e Tríceps)."""

    DURACAO_MINIMA: int = 10               # R6
    DURACAO_MAXIMA: int = 180              # R6
    GASTO_CALORICO_POR_MINUTO: float = 7.0  # R6
    total_criados: int = 0                 # R6
    _proximo_codigo: int = 1               # R6: gerador de códigos

    def __init__(self, nome: str, grupo_muscular: str, duracao_min: int,
                 exercicios: list[str] | None = None) -> None:
        """Cria o treino. Nome e duração passam pelos setters."""
        self.codigo: str = f'TRE-{Treino._proximo_codigo:03d}'
        Treino._proximo_codigo += 1
        self.nome = nome
        self.grupo_muscular = grupo_muscular
        self.duracao_min = duracao_min
        # None evita a armadilha da lista mutável como valor padrão
        self._exercicios: list[str] = exercicios if exercicios is not None else []
        Treino.total_criados += 1

    @property
    def nome(self) -> str:
        """Nome do treino."""
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = valor.strip()
        if len(valor) < 2:
            raise DadoInvalidoError('O nome do treino deve ter ao menos 2 caracteres.')
        self._nome = valor

    @property
    def duracao_min(self) -> int:
        """Duração em minutos."""
        return self._duracao_min

    @duracao_min.setter
    def duracao_min(self, valor: int) -> None:
        if not Treino.validar_duracao(valor):
            raise DadoInvalidoError(
                f'Duração {valor} inválida. Use de {Treino.DURACAO_MINIMA} '
                f'a {Treino.DURACAO_MAXIMA} minutos.')
        self._duracao_min = valor

    @property
    def exercicios(self) -> list[str]:
        """Cópia da lista de exercícios (a original fica protegida)."""
        return list(self._exercicios)

    @property
    def calorias_estimadas(self) -> float:
        """Property calculada: gasto estimado do treino."""
        return self.duracao_min * Treino.GASTO_CALORICO_POR_MINUTO

    @classmethod
    def from_string(cls, texto: str) -> 'Treino':
        """Construtor alternativo: 'nome;grupo;duracao;ex1,ex2,ex3'."""
        partes = [p.strip() for p in texto.split(';')]
        if len(partes) != 4:
            raise DadoInvalidoError("Formato esperado: 'nome;grupo;duracao;ex1,ex2'.")
        nome, grupo, duracao, lista = partes
        try:
            minutos = int(duracao)
        except ValueError:
            raise DadoInvalidoError(f'Duração {duracao!r} não é um número inteiro.')
        exercicios = [e.strip() for e in lista.split(',') if e.strip()]
        return cls(nome, grupo, minutos, exercicios)

    @staticmethod
    def validar_duracao(minutos: int) -> bool:
        """Confere se a duração está entre o mínimo e o máximo."""
        return Treino.DURACAO_MINIMA <= minutos <= Treino.DURACAO_MAXIMA

    def para_csv(self) -> str:
        """Cumpre o Protocol Exportavel."""
        return f'treino;{self.codigo};{self.nome};{self.grupo_muscular};{self.duracao_min}'

    def __str__(self) -> str:
        return (f'{self.codigo} - {self.nome} ({self.grupo_muscular}) - '
                f'{self.duracao_min} min - ~{self.calorias_estimadas:.0f} kcal - '
                f'{len(self._exercicios)} exercício(s)')
