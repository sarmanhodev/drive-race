"""Cards de fase e velocidade do Drive Race, em pixel art 8 bits.

Compatível com a chamada original do main.py:
    desenhar_velocimetro(tela, largura, velocidade, nome_fase)
O card de pontos continua sendo desenhado pelo interface.py.
"""

import pygame
from dificuldade import FASES

LARGURA_AREA_JOGO = 500
VELOCIDADE_MAXIMA_JOGO = 10
VELOCIDADE_MAXIMA_KMH = 200

COR_FUNDO = (15, 22, 38)
COR_BORDA = (49, 129, 203)
COR_BORDA_INTERNA = (30, 70, 117)
COR_SOMBRA = (7, 12, 23)
COR_TEXTO = (248, 242, 211)
COR_APAGADO = (49, 61, 76)
COR_VERDE = (65, 190, 85)
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


def converter_velocidade(velocidade):
    percentual = max(0.0, min(1.0, velocidade / VELOCIDADE_MAXIMA_JOGO))
    return percentual * VELOCIDADE_MAXIMA_KMH


def obter_cor_velocidade(velocidade_kmh):
    if velocidade_kmh < 120:
        return COR_VERDE
    if velocidade_kmh < 160:
        return COR_AMARELO
    return COR_VERMELHO


def _texto_pixelado(tela, texto, tamanho, cor, centro_x, y, largura_maxima=None):
    fonte = pygame.font.Font(None, tamanho)
    base = fonte.render(str(texto), False, cor)
    largura, altura = base.get_width() * 2, base.get_height() * 2
    if largura_maxima is not None and largura > largura_maxima:
        fator = largura_maxima / largura
        largura = max(1, int(largura * fator))
        altura = max(1, int(altura * fator))
    imagem = pygame.transform.scale(base, (largura, altura))
    tela.blit(imagem, imagem.get_rect(midtop=(centro_x, y)))


def _numero_pixelado(tela, numero, centro_x, y, cor, escala=5):
    caracteres = str(numero)
    largura_digito = 3 * escala
    espaco = escala
    largura_total = len(caracteres) * largura_digito + (len(caracteres) - 1) * espaco
    x_inicial = centro_x - largura_total // 2
    for indice, caractere in enumerate(caracteres):
        matriz = DIGITOS.get(caractere)
        if matriz is None:
            continue
        x = x_inicial + indice * (largura_digito + espaco)
        for linha, bits in enumerate(matriz):
            for coluna, bit in enumerate(bits):
                if bit == "1":
                    pygame.draw.rect(tela, cor, (x + coluna * escala, y + linha * escala, escala, escala))


def _cor_fase(nome_fase):
    nome = str(nome_fase).upper()
    if "ALTA" in nome or "EXTREMA" in nome or "VERMELHA" in nome:
        return COR_VERMELHO
    if "INTENSO" in nome or "RUSH" in nome or "PESADO" in nome:
        return COR_AMARELO
    if "CAOS" in nome or "IMPOSSIVEL" in nome:
        return COR_ROXO
    return COR_VERDE


def _linhas_fase(nome_fase):
    nome = " ".join(str(nome_fase).upper().strip().split()) or "NORMAL"
    palavras = nome.split()
    if len(palavras) <= 1:
        return (nome,)
    cortes = [(" ".join(palavras[:i]), " ".join(palavras[i:])) for i in range(1, len(palavras))]
    return min(cortes, key=lambda par: max(len(par[0]), len(par[1])))


def _desenhar_card(tela, x, y, largura, altura, titulo):
    pygame.draw.rect(tela, COR_SOMBRA, (x + 3, y + 3, largura, altura))
    pygame.draw.rect(tela, COR_BORDA, (x, y, largura, altura), 3)
    pygame.draw.rect(tela, COR_FUNDO, (x + 3, y + 3, largura - 6, altura - 6))
    pygame.draw.rect(tela, COR_BORDA_INTERNA, (x + 6, y + 6, largura - 12, altura - 12), 1)
    centro_x = x + largura // 2
    _texto_pixelado(tela, titulo, 15, COR_TEXTO, centro_x, y + 14, largura - 16)
    pygame.draw.rect(tela, COR_BORDA_INTERNA, (x + 12, y + 43, largura - 24, 2))
    return centro_x


def desenhar_velocimetro(tela, largura, velocidade, nome_fase):
    """Desenha os cards FASE e VELOCIDADE abaixo do card PONTOS.

    O número da fase vem da lista oficial FASES, sem mudar o main.py.
    """
    largura_painel = min(largura, tela.get_width()) - LARGURA_AREA_JOGO
    if largura_painel < 55:
        return

    margem = 7
    x = LARGURA_AREA_JOGO + margem
    card_largura = largura_painel - 2 * margem
    altura_tela = tela.get_height()

    # O card PONTOS do interface.py termina em y=124.
    fase_y = 138
    fase_altura = 151
    velocidade_y = 303
    velocidade_altura = 184
    if altura_tela < velocidade_y + velocidade_altura + 5:
        return

    centro_x = _desenhar_card(tela, x, fase_y, card_largura, fase_altura, "FASE")
    numero_fase = next(
        (indice for indice, fase in enumerate(FASES, start=1) if fase["nome"] == nome_fase),
        1,
    )
    _texto_pixelado(
        tela, f"{numero_fase:02d} / {len(FASES):02d}", 25,
        COR_AMARELO, centro_x, fase_y + 57, card_largura - 14,
    )
    cor_fase = _cor_fase(nome_fase)
    for indice, linha in enumerate(_linhas_fase(nome_fase)):
        _texto_pixelado(
            tela, linha, 13, cor_fase, centro_x,
            fase_y + 100 + indice * 17, card_largura - 14,
        )
    pygame.draw.rect(tela, cor_fase, (centro_x - 4, fase_y + fase_altura - 12, 8, 4))

    centro_x = _desenhar_card(
        tela, x, velocidade_y, card_largura, velocidade_altura, "VELOCIDADE"
    )
    velocidade_kmh = converter_velocidade(velocidade)
    cor_velocidade = obter_cor_velocidade(velocidade_kmh)
    _numero_pixelado(
        tela, f"{round(velocidade_kmh):03d}",
        centro_x, velocidade_y + 59, cor_velocidade, escala=5,
    )
    _texto_pixelado(
        tela, "KM/H", 13, COR_TEXTO, centro_x, velocidade_y + 92,
        card_largura - 18,
    )

    total_blocos = 10
    percentual = max(0.0, min(1.0, velocidade_kmh / VELOCIDADE_MAXIMA_KMH))
    blocos_acesos = round(percentual * total_blocos)
    bloco_largura, espaco = 7, 2
    barra_largura = total_blocos * bloco_largura + (total_blocos - 1) * espaco
    barra_x = centro_x - barra_largura // 2
    barra_y = velocidade_y + 128
    for i in range(total_blocos):
        if i >= blocos_acesos:
            cor_bloco = COR_APAGADO
        elif i < 6:
            cor_bloco = COR_VERDE
        elif i < 8:
            cor_bloco = COR_AMARELO
        else:
            cor_bloco = COR_VERMELHO
        pygame.draw.rect(
            tela, cor_bloco,
            (barra_x + i * (bloco_largura + espaco), barra_y, bloco_largura, 15),
        )
    _texto_pixelado(
        tela, "MAX 200", 11, COR_TEXTO, centro_x, velocidade_y + 153,
        card_largura - 18,
    )
