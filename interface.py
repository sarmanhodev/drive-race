"""Interface arcade 8 bits do Drive Race.

Cards PONTOS e RECORDE na lateral direita; avisos e game over preservados.
Compatível com desenhar_pontuacao(tela, pontuacao) do main.py.
Não utiliza imagens nem fontes externas.
"""
import pygame

FUNDO = (19, 32, 65)
SOMBRA = (8, 13, 28)
BORDA = (255, 209, 68)
BRANCO = (248, 242, 211)
AMARELO = (255, 209, 68)
VERMELHO = (235, 75, 70)
CINZA = (161, 186, 210)

# Paleta dos novos cards.
CARD_FUNDO = (9, 20, 41)
CARD_BORDA = (23, 154, 242)
CARD_BRILHO = (66, 212, 255)
CARD_INTERNA = (26, 77, 137)
CARD_TEXTO = (246, 248, 252)
CARD_OURO = (255, 209, 40)

CORES_FASES = {
    "NORMAL": (80, 220, 120),
    "ALTA VELOCIDADE": (255, 100, 80),
    "TRÂNSITO INTENSO": (255, 190, 60),
    "TRÂNSITO MISTO": (180, 130, 255),
}

_FONTES = {}


def _fonte(tamanho):
    if tamanho not in _FONTES:
        _FONTES[tamanho] = pygame.font.Font(None, tamanho)
    return _FONTES[tamanho]


def _texto_pixelado(texto, tamanho, cor):
    """Fonte pixelada para telas de aviso e game over originais."""
    original = _fonte(tamanho).render(str(texto), False, cor)
    return pygame.transform.scale(
        original, (original.get_width() * 2, original.get_height() * 2)
    )


def _caixa_pixelada(tela, rect, cor_borda=BORDA, cor_fundo=FUNDO):
    """Caixa original de avisos, sem alterações na identidade NES."""
    pygame.draw.rect(tela, SOMBRA, rect.move(5, 5))
    pygame.draw.rect(tela, cor_borda, rect)
    pygame.draw.rect(tela, cor_fundo, rect.inflate(-8, -8))
    for x in (rect.left + 8, rect.right - 12):
        for y in (rect.top + 8, rect.bottom - 12):
            pygame.draw.rect(tela, cor_borda, (x, y, 4, 4))


def _texto_legivel(tela, texto, centro_x, centro_y, tamanho, cor, largura_maxima):
    """Escolhe um tamanho de fonte que caiba sem deformar as letras."""
    texto = str(texto)
    tamanho = int(tamanho)
    while tamanho > 11 and _fonte(tamanho).size(texto)[0] > largura_maxima:
        tamanho -= 1
    imagem = _fonte(tamanho).render(texto, False, cor)
    tela.blit(imagem, imagem.get_rect(center=(int(centro_x), int(centro_y))))


def _card(tela, x, y, largura, altura, titulo):
    """Moldura neon com detalhes pixelados e título legível."""
    r = pygame.Rect(int(x), int(y), int(largura), int(altura))
    pygame.draw.rect(tela, (3, 9, 19), r.move(4, 4))
    pygame.draw.rect(tela, CARD_BORDA, r, 4)
    pygame.draw.rect(tela, CARD_FUNDO, r.inflate(-8, -8))
    pygame.draw.rect(tela, CARD_INTERNA, r.inflate(-14, -14), 2)

    # Cantos e pequenos rebites dourados.
    for px in (r.left + 9, r.right - 13):
        pygame.draw.rect(tela, CARD_BRILHO, (px, r.top + 6, 5, 3))
        pygame.draw.rect(tela, CARD_OURO, (px, r.bottom - 12, 4, 4))

    titulo_y = r.top + (26 if r.width >= 155 else 24)
    _texto_legivel(
        tela, titulo, r.centerx, titulo_y,
        29 if r.width >= 155 else 23, CARD_TEXTO, r.width - 18,
    )
    linha_y = r.top + (48 if r.width >= 155 else 43)
    pygame.draw.rect(tela, CARD_INTERNA, (r.left + 13, linha_y, r.width - 26, 3))
    pygame.draw.rect(tela, CARD_BRILHO, (r.left + 21, linha_y, max(0, r.width - 42), 1))
    return r, linha_y


def _trofeu(tela, cx, cy, escala=3):
    """Troféu 8 bits feito com retângulos, sem arquivos externos."""
    s = max(1, int(escala))
    ouro = (255, 210, 45)
    brilho = (255, 241, 126)
    sombra = (186, 114, 18)

    def bloco(dx, dy, w, h, cor):
        pygame.draw.rect(tela, cor, (int(cx + dx*s), int(cy + dy*s), w*s, h*s))

    # Taça, alças e base.
    bloco(-7, -8, 14, 2, brilho)
    bloco(-7, -6, 14, 8, ouro)
    bloco(-5, 2, 10, 2, sombra)
    bloco(-3, 4, 6, 3, ouro)
    bloco(-1, 7, 2, 4, ouro)
    bloco(-6, 11, 12, 2, ouro)
    bloco(-8, 13, 16, 2, sombra)
    bloco(-10, -6, 3, 6, ouro)
    bloco(-12, -5, 2, 3, ouro)
    bloco(-10, 0, 4, 2, ouro)
    bloco(7, -6, 3, 6, ouro)
    bloco(10, -5, 2, 3, ouro)
    bloco(6, 0, 4, 2, ouro)
    bloco(-4, -5, 2, 5, brilho)


def desenhar_pontuacao(tela, pontuacao):
    """Desenha PONTOS no topo e RECORDE embaixo da lateral (x >= 500)."""
    largura_lateral = tela.get_width() - 500
    if largura_lateral < 55:
        return

    margem = 8
    x = 500 + margem
    largura = largura_lateral - margem * 2
    altura_tela = tela.get_height()
    largo = largura >= 155

    # Pontos: espaço superior reservado para a fase e o velocímetro.
    pontos_altura = 136 if largo else 112
    r, linha = _card(tela, x, 12, largura, pontos_altura, "PONTOS")
    valor_y = (linha + r.bottom) // 2 + 5
    _texto_legivel(
        tela, str(pontuacao.pontos), r.centerx, valor_y,
        62 if largo else 40, CARD_OURO, r.width - 20,
    )

    # Recorde: quarto card no rodapé; a altura se adapta à janela.
    recorde_altura = 166 if largo else 128
    recorde_y = altura_tela - recorde_altura - 16
    if recorde_y <= r.bottom + 12:
        return

    rr, linha_recorde = _card(
        tela, x, recorde_y, largura, recorde_altura, "RECORDE"
    )
    if largo:
        _trofeu(tela, rr.centerx, linha_recorde + 28, escala=2)
        numero_y = rr.bottom - 31
        tamanho = 46
    else:
        # Com 120 px de lateral, prioriza legibilidade do recorde.
        numero_y = (linha_recorde + rr.bottom) // 2 + 4
        tamanho = 32

    _texto_legivel(
        tela, f"{pontuacao.recorde:,}".replace(",", "."),
        rr.centerx, numero_y, tamanho, CARD_OURO, rr.width - 18,
    )


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
