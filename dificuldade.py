# ==========================================================
# 1 - CONFIGURAÇÕES DA DIFICULDADE
# ==========================================================

# Quantidade de pontos necessária para mudar de fase
PONTOS_POR_FASE = 250


# ==========================================================
# 2 - CONFIGURAÇÕES DAS FASES
# ==========================================================

FASES = [

    # FASE 1 - 0 A 249 PONTOS
    {
        "nome": "AQUECIMENTO",
        "velocidade": 5.0,
        "intervalo": 1400
    },

    # FASE 2 - 250 A 499 PONTOS
    {
        "nome": "TRANSITO MODERADO",
        "velocidade": 6.0,
        "intervalo": 1100
    },

    # FASE 3 - 500 A 999 PONTOS
    {
        "nome": "ALTA VELOCIDADE",
        "velocidade": 8.0,
        "intervalo": 1200
    },

    # FASE 4 - 1500 A 1999 PONTOS
    {
        "nome": "TRANSITO INTENSO",
        "velocidade": 6.5,
        "intervalo": 700
    },

    # FASE 5 - 2000 A 2499 PONTOS
    {
        "nome": "RECUPERACAO",
        "velocidade": 5.5,
        "intervalo": 1250
    },

    # FASE 6 - 2500 A 2999 PONTOS
    {
        "nome": "HORA DO RUSH",
        "velocidade": 8.0,
        "intervalo": 650
    },

    # FASE 7 - 3000 A 3499 PONTOS
    {
        "nome": "VELOCIDADE EXTREMA",
        "velocidade": 10.0,
        "intervalo": 950
    },

    # FASE 8 - 3500 A 3999 PONTOS
    {
        "nome": "CAOS URBANO",
        "velocidade": 8.5,
        "intervalo": 550
    },

    # FASE 9 - 4000 A 4499 PONTOS
    {
        "nome": "FOLEGO EXTRA",
        "velocidade": 6.0,
        "intervalo": 1100
    },

    # FASE 10 - 4500 A 4999 PONTOS
    {
        "nome": "TRANSITO PESADO",
        "velocidade": 8.0,
        "intervalo": 550
    },

    # FASE 11 - 5000 A 5499 PONTOS
    {
        "nome": "RODOVIA INSANA",
        "velocidade": 10.0,
        "intervalo": 650
    },

    # FASE 12 - 5500 A 5999 PONTOS
    {
        "nome": "SOBREVIVENCIA",
        "velocidade": 9.0,
        "intervalo": 500
    },

    # FASE 13 - 6000 A 6499 PONTOS
    {
        "nome": "ALIVIO TEMPORARIO",
        "velocidade": 7.0,
        "intervalo": 950
    },

    # FASE 14 - 6500 A 6999 PONTOS
    {
        "nome": "CAOS TOTAL",
        "velocidade": 10.0,
        "intervalo": 550
    },

    # FASE 15 - 7000 A 7499 PONTOS
    {
        "nome": "ZONA VERMELHA",
        "velocidade": 9.5,
        "intervalo": 480
    },

    # FASE 16 - 7500 PONTOS OU MAIS
    {
        "nome": "MODO IMPOSSIVEL",
        "velocidade": 10.0,
        "intervalo": 450
    }

]


# ==========================================================
# 3 - OBTÉM A DIFICULDADE ATUAL
# ==========================================================

def obter_dificuldade(pontos):

    # Calcula a fase conforme a pontuação
    indice = pontos // PONTOS_POR_FASE

    # Impede que o jogo volte para a primeira fase
    # depois de ultrapassar a última.
    indice = min(indice, len(FASES) - 1)

    # Retorna as configurações da fase
    return FASES[indice]