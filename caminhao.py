"""Caminhão do Drive Race em pixel art 8 bits, visto de cima.

Mantém as funções e a movimentação do módulo original.
O retângulo recebido continua com 60 x 120 pixels e define a colisão.
"""

import pygame


# ==========================================================
# 1 - CONFIGURAÇÕES DO CAMINHÃO
# ==========================================================

LARGURA_RODAS = 8
ALTURA_RODAS = 25
MARGEM_PISTA = 8

# Sprite desenhado em resolução reduzida e ampliado sem filtro.
ESCALA_PIXEL = 2
LARGURA_SPRITE = 38  # 30 pixels de carroceria + 4 de roda em cada lado
ALTURA_SPRITE = 60

# Paleta retrô
CONTORNO = (19, 24, 44)
AZUL_ESCURO = (26, 65, 139)
AZUL = (42, 103, 198)
AZUL_CLARO = (79, 157, 232)
VERMELHO_ESCURO = (139, 37, 54)
VERMELHO = (217, 58, 67)
VERMELHO_CLARO = (246, 109, 92)
VIDRO = (132, 215, 236)
VIDRO_ESCURO = (51, 123, 169)
CINZA = (116, 135, 157)
PRATA = (190, 206, 217)
AMARELO = (255, 218, 100)
PRETO_PNEU = (17, 20, 29)


# ==========================================================
# 2 - CONSTRUÇÃO DO SPRITE EM PIXEL ART
# ==========================================================

def _criar_sprite():
    """Desenha uma vez o caminhão pequeno, com pixels bem definidos."""
    sprite = pygame.Surface(
        (LARGURA_SPRITE, ALTURA_SPRITE),
        pygame.SRCALPHA
    )

    def bloco(cor, x, y, largura, altura):
        pygame.draw.rect(sprite, cor, (x, y, largura, altura))

    # ------------------------------------------------------
    # RODAS: ficam ligeiramente para fora da carroceria.
    # ------------------------------------------------------
    for y in (10, 42):
        bloco(PRETO_PNEU, 0, y, 5, 13)
        bloco(PRETO_PNEU, 33, y, 5, 13)
        bloco(CINZA, 0, y + 3, 2, 6)
        bloco(CINZA, 36, y + 3, 2, 6)
        bloco((45, 51, 64), 2, y + 2, 2, 9)
        bloco((45, 51, 64), 34, y + 2, 2, 9)

    # ------------------------------------------------------
    # SILHUETA E CARROCERIA AZUL.
    # ------------------------------------------------------
    bloco(CONTORNO, 3, 0, 32, 60)
    bloco(AZUL_ESCURO, 5, 2, 28, 56)
    bloco(AZUL, 6, 19, 26, 37)
    bloco(AZUL_CLARO, 7, 20, 24, 3)
    bloco((34, 83, 171), 8, 26, 22, 26)
    bloco(AZUL_ESCURO, 8, 54, 22, 3)

    # Laterais, painéis e frisos da carroceria.
    bloco(AZUL_CLARO, 6, 25, 2, 28)
    bloco(AZUL_ESCURO, 30, 25, 2, 28)
    bloco((23, 62, 139), 12, 27, 2, 23)
    bloco((23, 62, 139), 24, 27, 2, 23)
    bloco(AZUL_CLARO, 9, 49, 20, 2)
    bloco(CINZA, 9, 57, 20, 2)

    # ------------------------------------------------------
    # CABINE VERMELHA (parte da frente do caminhão).
    # ------------------------------------------------------
    bloco(VERMELHO_ESCURO, 4, 1, 30, 22)
    bloco(VERMELHO, 5, 2, 28, 19)
    bloco(VERMELHO_CLARO, 7, 3, 24, 3)

    # Para-brisa pixelado.
    bloco(CONTORNO, 8, 7, 22, 9)
    bloco(VIDRO_ESCURO, 9, 8, 20, 7)
    bloco(VIDRO, 10, 8, 17, 5)
    bloco((207, 244, 247), 11, 9, 6, 2)
    bloco(VIDRO_ESCURO, 18, 8, 2, 7)

    # Capô e grade frontal.
    bloco(VERMELHO_ESCURO, 8, 17, 22, 3)
    bloco(CINZA, 13, 18, 12, 2)
    bloco(CONTORNO, 6, 0, 26, 2)
    bloco(PRATA, 8, 0, 22, 1)

    # Faróis na frente, vistos de cima.
    bloco(AMARELO, 5, 2, 4, 3)
    bloco(AMARELO, 29, 2, 4, 3)

    # Retrovisores.
    bloco(CONTORNO, 2, 9, 3, 6)
    bloco(CONTORNO, 33, 9, 3, 6)
    bloco(PRATA, 2, 10, 2, 3)
    bloco(PRATA, 34, 10, 2, 3)

    # Separação entre cabine e carroceria.
    bloco(CONTORNO, 5, 21, 28, 2)
    bloco(CINZA, 9, 22, 20, 1)

    # Lanternas traseiras e para-choque.
    bloco(VERMELHO_CLARO, 5, 56, 4, 3)
    bloco(VERMELHO_CLARO, 29, 56, 4, 3)
    bloco(PRATA, 8, 59, 22, 1)

    return sprite


_SPRITE = None


# ==========================================================
# 3 - DESENHA O CAMINHÃO
# ==========================================================

def desenhar_caminhao(tela, caminhao):
    """Desenha o sprite sem alterar o retângulo de colisão."""
    global _SPRITE

    if _SPRITE is None:
        _SPRITE = pygame.transform.scale(
            _criar_sprite(),
            (
                LARGURA_SPRITE * ESCALA_PIXEL,
                ALTURA_SPRITE * ESCALA_PIXEL
            )
        )

    # O sprite tem 8 pixels extras de rodas em cada lado.
    # A carroceria coincide com o pygame.Rect do caminhão.
    tela.blit(_SPRITE, (caminhao.x - LARGURA_RODAS, caminhao.y))


# ==========================================================
# 4 - MOVIMENTAÇÃO DO CAMINHÃO (LÓGICA ORIGINAL)
# ==========================================================

def movimentar_caminhao(caminhao, velocidade, pista_x, pista_largura):
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        caminhao.x -= velocidade

    if teclas[pygame.K_RIGHT]:
        caminhao.x += velocidade

    # Mantém as rodas inteiramente dentro da pista.
    limite_esquerdo = pista_x + MARGEM_PISTA + LARGURA_RODAS
    limite_direito = (
        pista_x + pista_largura - MARGEM_PISTA - LARGURA_RODAS
    )

    if caminhao.left < limite_esquerdo:
        caminhao.left = limite_esquerdo

    if caminhao.right > limite_direito:
        caminhao.right = limite_direito
