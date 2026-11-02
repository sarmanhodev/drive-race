# ==========================================================
# 1 - CONFIGURAÇÕES DE ACELERAÇÃO
# ==========================================================

# Quantidade de velocidade alterada por segundo
TAXA_ACELERACAO = 2.0

# Quantidade de velocidade reduzida por segundo
TAXA_DESACELERACAO = 3.0


# ==========================================================
# 2 - ATUALIZAÇÃO PROGRESSIVA DA VELOCIDADE
# ==========================================================

def atualizar_velocidade(
    velocidade_atual,
    velocidade_alvo,
    delta_time
):

    # ------------------------------------------------------
    # ACELERAÇÃO
    # ------------------------------------------------------

    if velocidade_atual < velocidade_alvo:

        velocidade_atual += (
            TAXA_ACELERACAO * delta_time
        )

        # Impede ultrapassar a velocidade desejada
        velocidade_atual = min(
            velocidade_atual,
            velocidade_alvo
        )

    # ------------------------------------------------------
    # DESACELERAÇÃO
    # ------------------------------------------------------

    elif velocidade_atual > velocidade_alvo:

        velocidade_atual -= (
            TAXA_DESACELERACAO * delta_time
        )

        # Impede reduzir além da velocidade desejada
        velocidade_atual = max(
            velocidade_atual,
            velocidade_alvo
        )

    return velocidade_atual