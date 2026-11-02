import json
from pathlib import Path


# ==========================================================
# 1 - CONFIGURAÇÕES DO SISTEMA DE PONTUAÇÃO
# ==========================================================

# Salva o recorde na mesma pasta deste arquivo, mesmo quando
# o jogo é executado a partir de outro diretório.
ARQUIVO_RECORDE = Path(__file__).resolve().parent / "recorde.json"


# ==========================================================
# 2 - SISTEMA DE PONTUAÇÃO
# ==========================================================

class Pontuacao:

    # ------------------------------------------------------
    # INICIALIZAÇÃO
    # ------------------------------------------------------

    def __init__(self):
        # Pontuação da partida atual
        self.pontos = 0

        # Maior pontuação salva entre as partidas
        self.recorde = self.carregar_recorde()

    # ------------------------------------------------------
    # CARREGAR RECORDE
    # ------------------------------------------------------

    def carregar_recorde(self):
        try:
            with ARQUIVO_RECORDE.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            valor = dados.get("recorde", 0)

            # Evita carregar valores inválidos ou negativos.
            if type(valor) is int and valor >= 0:
                return valor

        except (FileNotFoundError, OSError, json.JSONDecodeError, AttributeError):
            pass

        return 0

    # ------------------------------------------------------
    # SALVAR RECORDE
    # ------------------------------------------------------

    def salvar_recorde(self):
        try:
            with ARQUIVO_RECORDE.open("w", encoding="utf-8") as arquivo:
                json.dump({"recorde": self.recorde}, arquivo, indent=4)
        except OSError as erro:
            # O jogo continua funcionando mesmo se a gravação falhar.
            print(f"Não foi possível salvar o recorde: {erro}")

    # ------------------------------------------------------
    # ADICIONAR PONTOS
    # ------------------------------------------------------

    def adicionar_pontos(self, quantidade=100):
        self.pontos += quantidade

        if self.pontos > self.recorde:
            self.recorde = self.pontos
            self.salvar_recorde()

    # ------------------------------------------------------
    # REINICIAR PONTUAÇÃO
    # ------------------------------------------------------

    def reiniciar(self):
        # Reinicia apenas a partida; preserva o recorde.
        self.pontos = 0
