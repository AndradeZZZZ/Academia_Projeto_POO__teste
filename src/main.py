"""Ponto de entrada. Execute com: python src/main.py"""
from dados_exemplo import criar_academia_exemplo
from menu import executar

if __name__ == '__main__':
    executar(criar_academia_exemplo())
