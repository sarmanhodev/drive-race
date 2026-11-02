import pygame


# ==========================================================
# 1 - CONFIGURAÇÕES DO PAINEL
# ==========================================================

LARGURA_AREA_JOGO = 500

VELOCIDADE_MAXIMA_JOGO = 10
VELOCIDADE_MAXIMA_KMH = 200

COR_FUNDO = (15, 22, 38)
COR_MOLDURA = (247, 196, 63)
COR_SOMBRA = (8, 12, 22)
COR_TEXTO = (237, 238, 218)
COR_APAGADO = (49, 61, 76)

COR_VERDE = (65, 190, 85)
COR_AMARELO = (245, 205, 45)
COR_VERMELHO = (235, 65, 55)
COR_ROXO = (185, 139, 244)


# ==========================================================
# 2 - FONTE NUMÉRICA PIXELADA
# ==========================================================

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


# ==========================================================
# 3 - CONVERSÃO DA VELOCIDADE
# ==========================================================

def converter_velocidade(velocidade):

    percentual = velocidade / VELOCIDADE_MAXIMA_JOGO

    percentual = max(
        0.0,
        min(1.0, percentual)
    )

    return percentual * VELOCIDADE_MAXIMA_KMH


# ==========================================================
# 4 - CORES DA VELOCIDADE
# ==========================================================

def obter_cor_velocidade(velocidade_kmh):

    if velocidade_kmh < 120:
        return COR_VERDE

    if velocidade_kmh < 160:
        return COR_AMARELO

    return COR_VERMELHO


# ==========================================================
# 5 - TEXTO PIXELADO
# ==========================================================

def _texto_pixelado(
    tela,
    texto,
    tamanho,
    cor,
    centro_x,
    y,
    largura_maxima=None
):

    fonte = pygame.font.Font(None, tamanho)

    base = fonte.render(
        texto,
        False,
        cor
    )

    largura = base.get_width() * 2
    altura = base.get_height() * 2

    # Impede que o texto ultrapasse o painel.
    if largura_maxima is not None and largura > largura_maxima:

        fator = largura_maxima / largura

        largura = max(
            1,
            int(largura * fator)
        )

        altura = max(
            1,
            int(altura * fator)
        )

    imagem = pygame.transform.scale(
        base,
        (largura, altura)
    )

    tela.blit(
        imagem,
        imagem.get_rect(
            midtop=(centro_x, y)
        )
    )


# ==========================================================
# 6 - NÚMEROS PIXELADOS
# ==========================================================

def _numero_pixelado(
    tela,
    numero,
    centro_x,
    y,
    cor,
    escala=5
):

    caracteres = str(numero)

    largura_digito = 3 * escala
    espaco = escala

    largura_total = (
        len(caracteres) * largura_digito
        + (len(caracteres) - 1) * espaco
    )

    x_inicial = centro_x - largura_total // 2

    for indice, caractere in enumerate(caracteres):

        matriz = DIGITOS.get(caractere)

        if matriz is None:
            continue

        x = x_inicial + indice * (
            largura_digito + espaco
        )

        for linha, bits in enumerate(matriz):

            for coluna, bit in enumerate(bits):

                if bit == "1":

                    pygame.draw.rect(
                        tela,
                        cor,
                        (
                            x + coluna * escala,
                            y + linha * escala,
                            escala,
                            escala
                        )
                    )


# ==========================================================
# 7 - COR DA FASE
# ==========================================================

def _cor_fase(nome_fase):

    nome = str(nome_fase).upper()

    if "ALTA" in nome:
        return COR_VERMELHO

    if "INTENSO" in nome:
        return COR_AMARELO

    if "MISTO" in nome:
        return COR_ROXO

    return COR_VERDE


# ==========================================================
# 8 - DIVISÃO DO NOME DA FASE
# ==========================================================

def _linhas_fase(nome_fase):

    nome = " ".join(
        str(nome_fase).upper().strip().split()
    ) or "NORMAL"

    nome = nome.replace(
        "TRÂNSITO",
        "TRANSITO"
    )

    palavras = nome.split()

    if len(palavras) <= 1:
        return (nome,)

    if len(palavras) == 2:
        return tuple(palavras)

    # Para nomes maiores, divide em duas linhas.
    cortes = [
        (
            " ".join(palavras[:i]),
            " ".join(palavras[i:])
        )
        for i in range(1, len(palavras))
    ]

    return min(
        cortes,
        key=lambda par: max(
            len(par[0]),
            len(par[1])
        )
    )


# ==========================================================
# 9 - DESENHA O VELOCÍMETRO DIGITAL ARCADE
# ==========================================================

def desenhar_velocimetro(
    tela,
    largura,
    velocidade,
    nome_fase
):

    largura_painel = (
        largura - LARGURA_AREA_JOGO
    )

    if largura_painel <= 0:
        return

    altura = tela.get_height()

    centro_x = (
        LARGURA_AREA_JOGO
        + largura_painel // 2
    )

    # ------------------------------------------------------
    # CONFIGURAÇÕES DA MOLDURA
    # ------------------------------------------------------

    margem = 7

    painel_x = (
        LARGURA_AREA_JOGO + margem
    )

    painel_largura = (
        largura_painel - margem * 2
    )

    if painel_largura < 45:
        return

    painel_altura = 218

    painel_y = max(
        8,
        altura - painel_altura - 16
    )

    # ------------------------------------------------------
    # SOMBRA
    # ------------------------------------------------------

    pygame.draw.rect(
        tela,
        COR_SOMBRA,
        (
            painel_x + 3,
            painel_y + 3,
            painel_largura,
            painel_altura
        )
    )

    # ------------------------------------------------------
    # MOLDURA AMARELA
    # ------------------------------------------------------

    pygame.draw.rect(
        tela,
        COR_MOLDURA,
        (
            painel_x,
            painel_y,
            painel_largura,
            painel_altura
        )
    )

    # ------------------------------------------------------
    # FUNDO ESCURO
    # ------------------------------------------------------

    pygame.draw.rect(
        tela,
        COR_FUNDO,
        (
            painel_x + 3,
            painel_y + 3,
            painel_largura - 6,
            painel_altura - 6
        )
    )

    # ------------------------------------------------------
    # TÍTULO SPEED
    # ------------------------------------------------------

    _texto_pixelado(
        tela,
        "SPEED",
        13,
        COR_TEXTO,
        centro_x,
        painel_y + 10
    )

    pygame.draw.rect(
        tela,
        COR_MOLDURA,
        (
            painel_x + 10,
            painel_y + 32,
            painel_largura - 20,
            2
        )
    )

    # ------------------------------------------------------
    # VELOCIDADE ATUAL
    # ------------------------------------------------------

    velocidade_kmh = converter_velocidade(
        velocidade
    )

    cor_velocidade = obter_cor_velocidade(
        velocidade_kmh
    )

    _numero_pixelado(
        tela,
        f"{round(velocidade_kmh):03d}",
        centro_x,
        painel_y + 46,
        cor_velocidade,
        escala=5
    )

    _texto_pixelado(
        tela,
        "KM/H",
        12,
        COR_TEXTO,
        centro_x,
        painel_y + 77
    )

    # ------------------------------------------------------
    # BARRA DIGITAL DE VELOCIDADE
    # ------------------------------------------------------

    total_blocos = 10

    percentual = max(
        0.0,
        min(
            1.0,
            velocidade_kmh / VELOCIDADE_MAXIMA_KMH
        )
    )

    blocos_acesos = round(
        percentual * total_blocos
    )

    bloco_largura = 7
    espaco = 2

    barra_largura = (
        total_blocos * bloco_largura
        + (total_blocos - 1) * espaco
    )

    barra_x = (
        centro_x - barra_largura // 2
    )

    barra_y = painel_y + 103

    for i in range(total_blocos):

        if i < blocos_acesos:

            if i < 6:
                cor_bloco = COR_VERDE

            elif i < 8:
                cor_bloco = COR_AMARELO

            else:
                cor_bloco = COR_VERMELHO

        else:
            cor_bloco = COR_APAGADO

        pygame.draw.rect(
            tela,
            cor_bloco,
            (
                barra_x + i * (
                    bloco_largura + espaco
                ),
                barra_y,
                bloco_largura,
                13
            )
        )

    # ------------------------------------------------------
    # DIVISÓRIA DA FASE
    # ------------------------------------------------------

    pygame.draw.rect(
        tela,
        COR_MOLDURA,
        (
            painel_x + 10,
            painel_y + 130,
            painel_largura - 20,
            2
        )
    )

    # ------------------------------------------------------
    # TÍTULO FASE ATUAL
    # ------------------------------------------------------

    _texto_pixelado(
        tela,
        "FASE ATUAL",
        12,
        COR_TEXTO,
        centro_x,
        painel_y + 138,
        painel_largura - 20
    )

    # ------------------------------------------------------
    # NOME DA FASE CORRIGIDO
    # ------------------------------------------------------

    linhas = _linhas_fase(
        nome_fase
    )

    cor_fase = _cor_fase(
        nome_fase
    )

    for indice, linha in enumerate(linhas):

        _texto_pixelado(
            tela,
            linha,
            13,
            cor_fase,
            centro_x,
            painel_y + 160 + indice * 19,
            painel_largura - 22
        )

    # ------------------------------------------------------
    # INDICADOR LUMINOSO
    # ------------------------------------------------------

    pygame.draw.rect(
        tela,
        cor_fase,
        (
            centro_x - 4,
            painel_y + 199,
            8,
            6
        )
    )