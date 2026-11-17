"""Interfaces (Protocols) do sistema."""
from typing import Protocol


class Exportavel(Protocol):
    """Contrato de quem sabe se converter em uma linha de texto (CSV).

    Qualquer classe que tenha o método `para_csv` cumpre este contrato,
    mesmo sem herdar de nada (Pessoa, Plano e Treino não têm parentesco).
    """

    def para_csv(self) -> str:
        """Retorna os dados do objeto em uma linha separada por ';'."""
        ...
