"""Painel arcade Drive Race: cards FASE e VELOCIDADE.

Compatível com main.py: desenhar_velocimetro(tela, largura, velocidade, nome_fase).
Combina com os cards PONTOS e RECORDE do interface.py.
"""
import pygame
from dificuldade import FASES

LARGURA_AREA_JOGO = 500
VELOCIDADE_MAXIMA_JOGO = 10
VELOCIDADE_MAXIMA_KMH = 200

COR_FUNDO = (9, 20, 41)
COR_BORDA = (23, 154, 242)
COR_BRILHO = (66, 212, 255)
COR_INTERNA = (26, 77, 137)
COR_TEXTO = (246, 248, 252)
COR_OURO = (255, 209, 40)
COR_APAGADO = (49, 61, 76)
COR_VERDE = (65, 220, 95)
COR_AMARELO = (245, 205, 45)
COR_VERMELHO = (235, 65, 55)
COR_ROXO = (185, 139, 244)

DIGITOS = {
    "0": ("111", "101", "101", "101", "111"),
    "1": ("010", "110", "010", "010", "111"),
    "2": ("111", "001", "111", "100", "111"),
    "3": ("111", "001", "111", "001", "111"),
    "4": ("101", "101", "111", "001", "001"),
    "5": ("111", "100", "111", "001", "111"),
    "6": ("111", "100", "111", "101", "111"),
    "7": ("111", "001", "010", "010", "010"),
    "8": ("111", "101", "111", "101", "111"),
    "9": ("111", "101", "111", "001", "111"),
}
_FONTES = {}


def _fonte(tamanho):
    if tamanho not in _FONTES:
        _FONTES[tamanho] = pygame.font.Font(None, tamanho)
    return _FONTES[tamanho]


def _texto(tela, texto, cx, cy, tamanho, cor, largura_maxima):
    """Reduz o tamanho da fonte antes de renderizar: não distorce pixels."""
    texto = str(texto)
    tamanho = int(tamanho)
    while tamanho > 11 and _fonte(tamanho).size(texto)[0] > largura_maxima:
        tamanho -= 1
    imagem = _fonte(tamanho).render(texto, False, cor)
    tela.blit(imagem, imagem.get_rect(center=(int(cx), int(cy))))


def _card(tela, x, y, largura, altura, titulo, largo):
    r = pygame.Rect(int(x), int(y), int(largura), int(altura))
    pygame.draw.rect(tela, (3, 9, 19), r.move(4, 4))
    pygame.draw.rect(tela, COR_BORDA, r, 4)
    pygame.draw.rect(tela, COR_FUNDO, r.inflate(-8, -8))
    pygame.draw.rect(tela, COR_INTERNA, r.inflate(-14, -14), 2)
    for px in (r.left + 9, r.right - 13):
        pygame.draw.rect(tela, COR_BRILHO, (px, r.top + 6, 5, 3))
        pygame.draw.rect(tela, COR_OURO, (px, r.bottom - 12, 4, 4))
    _texto(tela, titulo, r.centerx, r.top + (26 if largo else 24),
           29 if largo else 23, COR_TEXTO, r.width - 18)
    linha_y = r.top + (48 if largo else 43)
    pygame.draw.rect(tela, COR_INTERNA, (r.left + 13, linha_y, r.width - 26, 3))
    pygame.draw.rect(tela, COR_BRILHO, (r.left + 21, linha_y, max(0, r.width - 42), 1))
    return r, linha_y


def _numero_pixelado(tela, numero, cx, y, cor, escala):
    texto = str(numero)
    largura_total = len(texto) * (4 * escala) - escala
    x0 = int(cx - largura_total / 2)
    for i, digito in enumerate(texto):
        for linha, bits in enumerate(DIGITOS.get(digito, ())):
            for coluna, bit in enumerate(bits):
                if bit == '1':
                    pygame.draw.rect(tela, cor,
                                     (x0 + i * 4 * escala + coluna * escala,
                                      y + linha * escala, escala, escala))


def converter_velocidade(velocidade):
    return max(0.0, min(1.0, velocidade / VELOCIDADE_MAXIMA_JOGO)) * VELOCIDADE_MAXIMA_KMH


def obter_cor_velocidade(velocidade_kmh):
    if velocidade_kmh < 120:
        return COR_VERDE
    if velocidade_kmh < 160:
        return COR_AMARELO
    return COR_VERMELHO


def _cor_fase(nome):
    nome = str(nome).upper()
    if any(p in nome for p in ('ALTA', 'EXTREMA', 'VERMELHA')):
        return COR_VERMELHO
    if any(p in nome for p in ('INTENSO', 'RUSH', 'PESADO')):
        return COR_AMARELO
    if any(p in nome for p in ('CAOS', 'IMPOSSIVEL')):
        return COR_ROXO
    return COR_VERDE


def _linhas_fase(nome, largura, tamanho):
    """Divide nomes longos sem deixar as palavras ilegíveis."""
    palavras = str(nome).upper().split()
    if not palavras:
        return ['NORMAL']
    linha = ' '.join(palavras)
    if _fonte(tamanho).size(linha)[0] <= largura:
        return [linha]
    if len(palavras) == 1:
        return [linha]
    cortes = [(' '.join(palavras[:i]), ' '.join(palavras[i:]))
              for i in range(1, len(palavras))]
    return list(min(cortes, key=lambda par: max(_fonte(tamanho).size(par[0])[0],
                                               _fonte(tamanho).size(par[1])[0])))


def desenhar_velocimetro(tela, largura, velocidade, nome_fase):
    """Desenha FASE e VELOCIDADE entre PONTOS e RECORDE."""
    largura_painel = min(largura, tela.get_width()) - LARGURA_AREA_JOGO
    if largura_painel < 55:
        return
    x = LARGURA_AREA_JOGO + 8
    card_largura = largura_painel - 16
    largo = card_largura >= 155
    altura_tela = tela.get_height()

    # Mesmas posições usadas em interface.py para evitar sobreposições.
    pontos_fim = 12 + (136 if largo else 112)
    recorde_inicio = altura_tela - (166 if largo else 128) - 16
    fase_y = pontos_fim + 14
    fase_h = 148 if largo else 151
    velocidade_y = fase_y + fase_h + 14
    velocidade_h = min(188 if largo else 184, recorde_inicio - velocidade_y - 14)
    if velocidade_h < 145:
        return

    fase, linha_fase = _card(tela, x, fase_y, card_largura, fase_h, 'FASE', largo)
    numero_fase = next((i for i, f in enumerate(FASES, 1) if f['nome'] == nome_fase), 1)
    _texto(tela, f'{numero_fase:02d} / {len(FASES):02d}', fase.centerx,
           linha_fase + (33 if largo else 32), 44 if largo else 30,
           COR_OURO, fase.width - 18)

    cor_fase = _cor_fase(nome_fase)
    faixa = pygame.Rect(fase.left + 10, fase.bottom - 47, fase.width - 20, 32)
    pygame.draw.rect(tela, cor_fase, faixa, 2)
    linhas = _linhas_fase(nome_fase, faixa.width - 10, 21 if largo else 16)
    tamanho = 21 if largo else 16
    espacamento = 15 if len(linhas) > 1 else 0
    inicio = faixa.centery - (len(linhas) - 1) * espacamento / 2
    for i, linha in enumerate(linhas):
        _texto(tela, linha, faixa.centerx, inicio + i * espacamento,
               tamanho, COR_TEXTO, faixa.width - 10)

    vel, linha_vel = _card(tela, x, velocidade_y, card_largura,
                           velocidade_h, 'VELOCIDADE', largo)
    kmh = converter_velocidade(velocidade)
    escala = 7 if largo else 5
    _numero_pixelado(tela, f'{round(kmh):03d}', vel.centerx,
                     linha_vel + 15, obter_cor_velocidade(kmh), escala)
    _texto(tela, 'KM/H', vel.centerx, linha_vel + (61 if largo else 52),
           26 if largo else 20, COR_TEXTO, vel.width - 20)

    blocos = 10
    ativos = round(kmh / VELOCIDADE_MAXIMA_KMH * blocos)
    espaco = 3 if largo else 2
    bloco_largura = max(5, (vel.width - 28 - (blocos - 1) * espaco) // blocos)
    barra_largura = blocos * bloco_largura + (blocos - 1) * espaco
    barra_x = vel.centerx - barra_largura // 2
    barra_y = vel.bottom - 52
    for i in range(blocos):
        cor = (COR_APAGADO if i >= ativos else
               COR_VERDE if i < 6 else COR_AMARELO if i < 8 else COR_VERMELHO)
        pygame.draw.rect(tela, cor,
                         (barra_x + i * (bloco_largura + espaco), barra_y,
                          bloco_largura, 16))
    _texto(tela, 'MAX: 200', vel.centerx, vel.bottom - 20,
           24 if largo else 19, COR_TEXTO, vel.width - 18)
