"""Dados de exemplo carregados ao iniciar o sistema."""
from modelos.academia import Academia
from modelos.pessoa import Aluno, Instrutor
from modelos.plano import Anual, Mensal, Trimestral
from modelos.treino import Treino


def criar_academia_exemplo() -> Academia:
    """Monta uma academia já com planos, pessoas, treinos e presenças."""
    academia = Academia('Academia Força Total')

    academia.cadastrar_plano(Mensal.from_string('120'))
    academia.cadastrar_plano(Trimestral(120.0))
    academia.cadastrar_plano(Anual(120.0))

    academia.cadastrar_pessoa(Aluno.from_string('Ana Souza;12345678901'))
    academia.cadastrar_pessoa(Aluno('Bruno Lima', '98765432100', 82.5, 1.78))
    academia.cadastrar_pessoa(Aluno('Carla Dias', '11122233344', 60.0, 1.65))
    academia.cadastrar_pessoa(Instrutor.from_string('Marcos Rocha;55566677788;CREF-123456;Musculação'))
    academia.cadastrar_pessoa(Instrutor('Juliana Reis', '99988877766', 'CREF-654321', 'Funcional'))

    academia.cadastrar_treino(Treino.from_string('Treino A;Peito e Tríceps;60;Supino,Crucifixo,Tríceps pulley'))
    academia.cadastrar_treino(Treino('Treino B', 'Costas e Bíceps', 50, ['Remada', 'Puxada', 'Rosca direta']))
    academia.cadastrar_treino(Treino('Treino C', 'Pernas', 55, ['Agachamento', 'Leg press', 'Cadeira extensora']))

    # Ana: plano anual com 3 presenças e um treino. Bruno: plano mensal. Carla fica sem plano.
    academia.matricular('12345678901', 'Anual')
    academia.matricular('98765432100', 'Mensal')
    for _ in range(3):
        academia.registrar_presenca('12345678901')
    academia.registrar_presenca('98765432100')
    academia.prescrever_treino('55566677788', '12345678901', 'TRE-001')
    return academia
