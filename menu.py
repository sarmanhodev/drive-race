"""Menu animado em pixel art (8 bits) do Drive Race.

Compatível com main.py: desenhar_menu(tela, largura, altura, recorde=0)
e processar_evento_menu(evento). Nenhuma imagem externa necessária.
"""
import math
import pygame

BASE_LARGURA = 310
BASE_ALTURA = 350

CEU = (39, 77, 135)
CEU_CLARO = (78, 137, 186)
AZUL_ESCURO = (19, 32, 65)
BRANCO = (248, 242, 211)
AMARELO = (255, 209, 68)
LARANJA = (235, 111, 49)
VERMELHO = (199, 54, 61)
AZUL = (40, 106, 201)
AZUL_LUZ = (77, 161, 231)
CINZA = (90, 103, 124)
ASFALTO = (53, 58, 79)
VERDE = (48, 126, 83)
PRETO = (21, 25, 38)


def _ret(surface, cor, x, y, w, h):
    pygame.draw.rect(surface, cor, (int(x), int(y), int(w), int(h)))


def _texto(surface, texto, tamanho, cor, x, y, *, centro=True, sombra=False):
    fonte = pygame.font.Font(None, tamanho)
    imagem = fonte.render(texto, False, cor)
    rect = imagem.get_rect(midtop=(x, y)) if centro else imagem.get_rect(topleft=(x, y))
    if sombra:
        sombra_img = fonte.render(texto, False, PRETO)
        surface.blit(sombra_img, rect.move(2, 2))
    surface.blit(imagem, rect)


def _nuvem(surface, x, y):
    _ret(surface, BRANCO, x + 5, y, 19, 5)
    _ret(surface, BRANCO, x, y + 5, 34, 8)
    _ret(surface, BRANCO, x + 10, y - 4, 12, 5)


def _caminhao(surface, x, y, tempo):
    """Caminhão fictício, sem marca, desenhado de lado em pixels."""
    y += int(math.sin(tempo * 0.008) > 0.7)
    _ret(surface, (35, 40, 55), x + 9, y + 48, 143, 4)
    _ret(surface, PRETO, x + 3, y + 5, 108, 39)
    _ret(surface, AZUL, x + 5, y + 7, 104, 34)
    _ret(surface, AZUL_LUZ, x + 8, y + 9, 97, 5)
    _ret(surface, (29, 72, 148), x + 8, y + 32, 98, 7)
    for dx in (23, 53, 83):
        _ret(surface, (27, 83, 169), x + dx, y + 15, 3, 17)
    _ret(surface, PRETO, x + 111, y + 17, 42, 27)
    _ret(surface, VERMELHO, x + 113, y + 18, 36, 24)
    _ret(surface, LARANJA, x + 116, y + 20, 5, 18)
    _ret(surface, (158, 216, 235), x + 126, y + 21, 18, 12)
    _ret(surface, AZUL_ESCURO, x + 125, y + 21, 2, 13)
    _ret(surface, AMARELO, x + 148, y + 34, 5, 5)
    _ret(surface, PRETO, x + 4, y + 42, 152, 5)
    _ret(surface, CINZA, x + 8, y + 44, 143, 3)
    for dx in (26, 79, 130):
        _ret(surface, PRETO, x + dx - 9, y + 38, 20, 16)
        _ret(surface, (35, 39, 50), x + dx - 7, y + 40, 16, 12)
        _ret(surface, (170, 183, 194), x + dx - 4, y + 43, 10, 6)
        _ret(surface, BRANCO, x + dx, y + 45, 2, 2)


def desenhar_menu(tela, largura=None, altura=None, recorde=0):
    """Desenha o menu retrô e mostra o maior recorde informado."""
    largura = largura or tela.get_width()
    altura = altura or tela.get_height()
    t = pygame.time.get_ticks()
    s = pygame.Surface((BASE_LARGURA, BASE_ALTURA))
    s.fill(CEU)

    # Céu e paisagem pixelados.
    _ret(s, CEU_CLARO, 0, 93, 310, 90)
    _ret(s, (114, 164, 185), 0, 168, 310, 23)
    _ret(s, (239, 172, 106), 0, 191, 310, 13)
    _ret(s, AMARELO, 239, 143, 24, 24)
    _ret(s, (246, 183, 89), 235, 147, 32, 16)
    _nuvem(s, int(45 - t * 0.009) % 365 - 35, 109)
    _nuvem(s, int(245 - t * 0.006) % 365 - 35, 137)
    pygame.draw.polygon(s, (49, 87, 117), [(0, 203), (43, 166), (76, 196), (126, 159), (175, 203)])
    pygame.draw.polygon(s, (35, 69, 99), [(122, 204), (188, 164), (225, 189), (262, 158), (310, 199), (310, 212)])
    _ret(s, (38, 107, 68), 0, 204, 310, 20)
    for x in range(0, 310, 21):
        _ret(s, (27, 81, 60), x, 198 + (x % 3) * 3, 11, 20)

    # Estrada animada.
    _ret(s, (119, 126, 129), 0, 221, 310, 5)
    _ret(s, ASFALTO, 0, 226, 310, 62)
    _ret(s, AMARELO, 0, 232, 310, 3)
    _ret(s, BRANCO, 0, 281, 310, 3)
    desloc = int(t * 0.09) % 52
    for x in range(-52, 362, 52):
        _ret(s, BRANCO, x - desloc, 260, 25, 3)
    _caminhao(s, 77, 207, t)

    # Título e recorde. O recorde ocupa uma faixa própria sem cobrir o cenário.
    _ret(s, AZUL_ESCURO, 0, 0, 310, 100)
    _ret(s, AMARELO, 0, 0, 310, 4)
    _texto(s, 'DRIVE RACE', 56, AMARELO, 155, 10, sombra=True)
    _texto(s, '8-BIT ROAD CHALLENGE', 19, BRANCO, 155, 61)
    _ret(s, (33, 49, 83), 65, 79, 180, 17)
    _ret(s, LARANJA, 65, 79, 180, 2)
    _texto(s, f'HI-SCORE  {max(0, int(recorde)):06d}', 17, AMARELO, 155, 81)
    _ret(s, LARANJA, 20, 98, 270, 2)

    # Rodapé com controles e mensagem piscante.
    _ret(s, AZUL_ESCURO, 0, 288, 310, 62)
    _ret(s, LARANJA, 0, 288, 310, 3)
    _texto(s, '<  >  MOVER   |   DESVIE DOS OBSTACULOS', 17, BRANCO, 155, 295)
    if (t // 450) % 2 == 0:
        _texto(s, 'PRESS ENTER TO START', 26, AMARELO, 155, 313, sombra=True)
    _texto(s, 'ESC: SAIR', 15, (165, 190, 218), 155, 338)

    imagem = pygame.transform.scale(s, (largura, altura))
    tela.blit(imagem, (0, 0))


def processar_evento_menu(evento):
    """Retorna 'jogar', 'sair' ou None; compatível com main.py."""
    if evento.type == pygame.KEYDOWN:
        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return 'jogar'
        if evento.key == pygame.K_ESCAPE:
            return 'sair'
    return None
