"""Exceções customizadas do sistema da academia."""


class ErroAcademia(Exception):
    """Base de todos os erros de regra de negócio da academia."""


class DadoInvalidoError(ErroAcademia):
    """Lançada quando um dado informado não respeita a validação."""


class NaoEncontradoError(ErroAcademia):
    """Lançada quando uma pessoa, plano ou treino não existe."""


class AlunoSemPlanoError(ErroAcademia):
    """Lançada quando o aluno precisa de um plano ativo e não tem."""


class LimiteTreinosError(ErroAcademia):
    """Lançada quando o aluno já tem o máximo de treinos."""


class LimiteAlunosError(ErroAcademia):
    """Lançada quando o instrutor já atende o máximo de alunos."""

