"""Interface arcade 8 bits do Drive Race.

Compatível com as chamadas atuais do main.py.
Não utiliza imagens ou fontes externas.
"""

import pygame

# Cores no estilo de jogos de 8 bits.
FUNDO = (19, 32, 65)
SOMBRA = (8, 13, 28)
BORDA = (255, 209, 68)
BRANCO = (248, 242, 211)
AMARELO = (255, 209, 68)
VERMELHO = (235, 75, 70)
CINZA = (161, 186, 210)

CORES_FASES = {
    "NORMAL": (80, 220, 120),
    "ALTA VELOCIDADE": (255, 100, 80),
    "TRÂNSITO INTENSO": (255, 190, 60),
    "TRÂNSITO MISTO": (180, 130, 255),
}

# Fonte renderizada em tamanho menor e ampliada sem interpolação.
_FONTES = {}


def _fonte(tamanho):
    if tamanho not in _FONTES:
        _FONTES[tamanho] = pygame.font.Font(None, tamanho)
    return _FONTES[tamanho]


def _texto_pixelado(texto, tamanho, cor):
    """Renderiza letras com pixels visíveis e sem antialiasing."""
    original = _fonte(tamanho).render(str(texto), False, cor)
    return pygame.transform.scale(
        original, (original.get_width() * 2, original.get_height() * 2)
    )


def _caixa_pixelada(tela, rect, cor_borda=BORDA, cor_fundo=FUNDO):
    """Caixa com contorno quadrado e sombra deslocada, estilo NES."""
    pygame.draw.rect(tela, SOMBRA, rect.move(5, 5))
    pygame.draw.rect(tela, cor_borda, rect)
    pygame.draw.rect(tela, cor_fundo, rect.inflate(-8, -8))
    # Detalhes quadrados nos cantos.
    for x in (rect.left + 8, rect.right - 12):
        for y in (rect.top + 8, rect.bottom - 12):
            pygame.draw.rect(tela, cor_borda, (x, y, 4, 4))


def _texto_card(texto, tamanho, cor, largura_maxima):
    """Cria texto pixelado, reduzindo-o quando necessário para caber no card."""
    imagem = _texto_pixelado(texto, tamanho, cor)
    if imagem.get_width() > largura_maxima:
        proporcao = largura_maxima / imagem.get_width()
        imagem = pygame.transform.scale(
            imagem,
            (int(largura_maxima), max(1, round(imagem.get_height() * proporcao))),
        )
    return imagem


def desenhar_pontuacao(tela, pontuacao):
    """Desenha a pontuação no card superior da barra lateral (x >= 500)."""
    largura_lateral = tela.get_width() - 500
    if largura_lateral < 55:
        return

    margem = 7
    x = 500 + margem
    y = 12
    largura = largura_lateral - margem * 2
    altura = 112

    fundo = (15, 22, 38)
    borda = (49, 129, 203)
    borda_interna = (30, 70, 117)
    amarelo = (255, 209, 68)

    # Sombra, contorno e fundo: geometria simples, sem imagens externas.
    pygame.draw.rect(tela, (7, 12, 23), (x + 3, y + 3, largura, altura))
    pygame.draw.rect(tela, borda, (x, y, largura, altura), 3)
    pygame.draw.rect(tela, fundo, (x + 3, y + 3, largura - 6, altura - 6))
    pygame.draw.rect(tela, borda_interna, (x + 6, y + 6, largura - 12, altura - 12), 1)

    centro_x = x + largura // 2
    titulo = _texto_card("PONTOS", 15, BRANCO, largura - 18)
    tela.blit(titulo, titulo.get_rect(center=(centro_x, y + 25)))

    pygame.draw.rect(tela, borda_interna, (x + 12, y + 43, largura - 24, 2))

    # Exibe os pontos reais, sem limitar a quantidade de dígitos.
    numero = _texto_card(str(pontuacao.pontos), 29, amarelo, largura - 18)
    tela.blit(numero, numero.get_rect(center=(centro_x, y + 76)))

    # Pequenos detalhes luminosos reforçam a estética arcade.
    pygame.draw.rect(tela, amarelo, (x + 12, y + altura - 12, 5, 3))
    pygame.draw.rect(tela, amarelo, (x + largura - 17, y + altura - 12, 5, 3))


def desenhar_aviso_fase(tela, largura, nome_fase):
    """Aviso temporário de fase, centralizado somente na área do jogo."""
    cor = CORES_FASES.get(nome_fase, AMARELO)
    titulo = _texto_pixelado("NEW STAGE!", 20, AMARELO)
    fase = _texto_pixelado(nome_fase, 17, cor)
    largura_caixa = min(
        largura - 24, max(265, titulo.get_width() + 32, fase.get_width() + 32)
    )
    caixa = pygame.Rect((largura - largura_caixa) // 2, 148, largura_caixa, 103)
    _caixa_pixelada(tela, caixa, cor_borda=cor)
    tela.blit(titulo, titulo.get_rect(center=(largura // 2, caixa.top + 31)))
    tela.blit(fase, fase.get_rect(center=(largura // 2, caixa.top + 72)))


def desenhar_game_over(tela, largura, altura, pontuacao):
    """Tela de fim de jogo em pixel art, com opções R e ESC."""
    # A largura recebida é 500: escurece somente a área jogável.
    camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
    camada.fill((7, 11, 24, 205))
    tela.blit(camada, (0, 0))

    largura_caixa = min(largura - 32, 428)
    caixa = pygame.Rect(
        (largura - largura_caixa) // 2, altura // 2 - 157, largura_caixa, 315
    )
    _caixa_pixelada(tela, caixa, cor_borda=VERMELHO)

    titulo = _texto_pixelado("GAME OVER", 36, VERMELHO)
    pontos = _texto_pixelado(f"SCORE  {pontuacao.pontos:06d}", 20, BRANCO)
    recorde = _texto_pixelado(f"HI-SCORE  {pontuacao.recorde:06d}", 19, AMARELO)
    reiniciar = _texto_pixelado("R  - RESTART", 18, BRANCO)
    menu = _texto_pixelado("ESC - MENU", 18, CINZA)

    centro_x = largura // 2
    for imagem, y in (
        (titulo, caixa.top + 50),
        (pontos, caixa.top + 127),
        (recorde, caixa.top + 174),
        (reiniciar, caixa.top + 236),
        (menu, caixa.top + 274),
    ):
        tela.blit(imagem, imagem.get_rect(center=(centro_x, y)))

    pygame.draw.rect(
        tela, BORDA, (caixa.left + 28, caixa.top + 88, caixa.width - 56, 4)
    )
