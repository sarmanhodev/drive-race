"""Pista Drive Race: cenários rural e urbano em pixel art 8 bits.

Mantém constantes e assinaturas usadas pelos demais módulos.
Chame definir_cenario(pontos) a cada quadro para selecionar o ambiente.
"""
import pygame

PISTA_X = 50
PISTA_LARGURA = 400
QUANTIDADE_FAIXAS = 3
LARGURA_FAIXA = PISTA_LARGURA / QUANTIDADE_FAIXAS
LARGURA_AREA_JOGO = 500
COR_PAINEL = (22, 27, 36)
COR_DIVISORIA = (75, 90, 110)
COR_GRAMA = (48, 139, 65)
COR_GRAMA_CLARA = (65, 157, 70)
COR_GRAMA_ESCURA = (29, 104, 53)
COR_ASFALTO = (55, 59, 68)
COR_ASFALTO_CLARO = (65, 69, 76)
COR_ASFALTO_ESCURO = (47, 51, 60)
COR_AMARELO = (250, 206, 67)
COR_AMARELO_SOMBRA = (172, 120, 45)
COR_BRANCO = (242, 239, 217)
COR_BRANCO_SOMBRA = (159, 164, 166)
TAMANHO_TRACO = 50
ESPACO_TRACO = 40
VELOCIDADE_PISTA = 5
deslocamento = 0.0
_deslocamento_cenario = 0.0
_distancia_cenario = 0.0
_cenario_atual = 'rural'
_pontos_cenario = 0
_inicio_transicao = None
_transicao_concluida = False


def definir_cenario(pontos):
    """Inicia a entrada na cidade aos 700 pontos; mantém a API original."""
    global _cenario_atual, _pontos_cenario, _inicio_transicao, _transicao_concluida
    _pontos_cenario = pontos
    if pontos < 700:
        # Reinício da partida: o ambiente volta à estrada rural.
        _cenario_atual = 'rural'
        _inicio_transicao = None
        _transicao_concluida = False
    elif not _transicao_concluida:
        if _inicio_transicao is None:
            _inicio_transicao = _distancia_cenario
        _cenario_atual = 'transicao'
    else:
        _cenario_atual = 'urbano'
    return _cenario_atual


def atualizar_pista(velocidade=VELOCIDADE_PISTA):
    """Rola faixas e cenário acompanhando a velocidade do jogo."""
    global deslocamento, _deslocamento_cenario, _distancia_cenario
    deslocamento = (deslocamento + velocidade) % (TAMANHO_TRACO + ESPACO_TRACO)
    _deslocamento_cenario = (_deslocamento_cenario + velocidade) % 240
    _distancia_cenario += velocidade


def _bloco(tela, cor, x, y, largura, altura):
    pygame.draw.rect(tela, cor, (int(x), int(y), int(largura), int(altura)))


def _desenhar_grama(tela, altura):
    """Margens verdes com textura e vegetação rolando verticalmente."""
    _bloco(tela, COR_GRAMA, 0, 0, LARGURA_AREA_JOGO, altura)
    passo = 24
    desloc = int(_distancia_cenario) % passo
    for linha, y in enumerate(range(-passo, altura + passo, passo)):
        yy = y + desloc
        for coluna, x in enumerate(range(0, LARGURA_AREA_JOGO, 12)):
            if PISTA_X <= x < PISTA_X + PISTA_LARGURA:
                continue
            codigo = (linha * 13 + coluna * 7) % 9
            if codigo in (0, 3):
                _bloco(tela, COR_GRAMA_CLARA, x + 2, yy + 5, 5, 4)
            elif codigo == 5:
                _bloco(tela, COR_GRAMA_ESCURA, x + 3, yy + 8, 6, 5)
    # Árvores e flores com posição estável no mundo (sem saltos a cada ciclo).
    espacamento = 155
    primeiro = int(_distancia_cenario // espacamento)
    for n in range(primeiro - 1, primeiro + altura // espacamento + 3):
        yy = int(n * espacamento + _distancia_cenario) % (altura + espacamento * 2) - espacamento
        # O desenho acompanha o deslocamento e usa lados alternados.
        for xx in (10, 465):
            _bloco(tela, (99, 72, 43), xx + 12, yy + 21, 6, 19)
            _bloco(tela, COR_GRAMA_ESCURA, xx + 3, yy + 9, 25, 20)
            _bloco(tela, COR_GRAMA_CLARA, xx + 7, yy + 3, 18, 20)
            _bloco(tela, (106, 184, 80), xx + 11, yy + 5, 7, 7)
        _bloco(tela, (255, 215, 95), 8, yy + 92, 4, 4)
        _bloco(tela, (255, 192, 214), 484, yy + 105, 4, 4)


def _desenhar_cidade(tela, altura):
    """Calçadas, edifícios, postes e árvores pixeladas nas margens."""
    _bloco(tela, (104, 106, 109), 0, 0, LARGURA_AREA_JOGO, altura)
    _bloco(tela, (147, 147, 143), 0, 0, PISTA_X, altura)
    _bloco(tela, (147, 147, 143), PISTA_X + PISTA_LARGURA, 0,
           LARGURA_AREA_JOGO - PISTA_X - PISTA_LARGURA, altura)
    # Juntas do pavimento acompanham a velocidade do cenário.
    espacamento = 70
    fase = int(_distancia_cenario) % espacamento
    for y in range(-espacamento, altura + espacamento, espacamento):
        yy = y + fase
        _bloco(tela, (115, 116, 114), 0, yy, 50, 3)
        _bloco(tela, (115, 116, 114), 450, yy, 50, 3)
    # Construções e postes: posições vinculadas ao deslocamento acumulado.
    bloco = 175
    fase = int(_distancia_cenario) % bloco
    for i, y in enumerate(range(-bloco, altura + bloco, bloco)):
        yy = y + fase
        # Prédios estreitos vistos de cima nas duas laterais.
        _bloco(tela, (53, 66, 88), 0, yy + 14, 29, 98)
        _bloco(tela, (84, 99, 120), 3, yy + 18, 22, 88)
        _bloco(tela, (37, 48, 66), 471, yy + 30, 29, 94)
        _bloco(tela, (77, 92, 115), 475, yy + 34, 25, 86)
        for j in range(3):
            _bloco(tela, (238, 199, 97), 7, yy + 28 + j * 22, 7, 10)
            _bloco(tela, (164, 210, 225), 18, yy + 28 + j * 22, 5, 10)
            _bloco(tela, (238, 199, 97), 481, yy + 44 + j * 22, 9, 10)
        # Postes junto ao meio-fio (não invadem a área dos veículos).
        _bloco(tela, (58, 60, 65), 39, yy + 128, 4, 22)
        _bloco(tela, (252, 220, 112), 35, yy + 124, 12, 7)
        _bloco(tela, (58, 60, 65), 457, yy + 128, 4, 22)
        _bloco(tela, (252, 220, 112), 453, yy + 124, 12, 7)
        # Pequena árvore urbana em alguns trechos.
        if i % 2 == 0:
            _bloco(tela, (99, 72, 43), 32, yy + 56, 5, 14)
            _bloco(tela, (39, 115, 66), 28, yy + 47, 14, 15)
            _bloco(tela, (83, 167, 87), 31, yy + 45, 8, 9)


def _desenhar_asfalto(tela, altura):
    _bloco(tela, COR_ASFALTO, PISTA_X, 0, PISTA_LARGURA, altura)
    passo_y = 28
    desloc = int(_distancia_cenario) % passo_y
    for linha, y in enumerate(range(-passo_y, altura + passo_y, passo_y)):
        yy = y + desloc
        for coluna in range(20):
            xx = PISTA_X + 12 + coluna * 19 + ((linha * 7) % 8)
            if xx >= PISTA_X + PISTA_LARGURA - 10:
                continue
            if (linha * 11 + coluna * 5) % 7 == 0:
                _bloco(tela, COR_ASFALTO_CLARO, xx, yy + 5, 5, 3)
            elif (linha * 3 + coluna * 13) % 11 == 0:
                _bloco(tela, COR_ASFALTO_ESCURO, xx, yy + 16, 7, 3)


def _desenhar_bordas(tela, altura):
    for x in (PISTA_X, PISTA_X + PISTA_LARGURA):
        _bloco(tela, COR_AMARELO_SOMBRA, x - 4, 0, 8, altura)
        _bloco(tela, COR_AMARELO, x - 2, 0, 4, altura)


def _desenhar_divisoes(tela, altura):
    ciclo = TAMANHO_TRACO + ESPACO_TRACO
    for i in range(1, QUANTIDADE_FAIXAS):
        x = round(PISTA_X + i * LARGURA_FAIXA)
        for y in range(-ciclo, altura + ciclo, ciclo):
            inicio = round(y + deslocamento)
            topo = max(0, inicio)
            fim = min(altura, inicio + TAMANHO_TRACO)
            if topo < fim:
                _bloco(tela, COR_BRANCO_SOMBRA, x - 3, topo, 7, fim - topo)
                _bloco(tela, COR_BRANCO, x - 2, topo, 4, fim - topo)


def _desenhar_painel(tela, largura, altura):
    if largura > LARGURA_AREA_JOGO:
        _bloco(tela, COR_PAINEL, LARGURA_AREA_JOGO, 0,
               largura - LARGURA_AREA_JOGO, altura)
        _bloco(tela, COR_DIVISORIA, LARGURA_AREA_JOGO, 0, 2, altura)


def _desenhar_placa_cidade(tela, altura):
    """Placa pequena de acostamento, antes da entrada na cidade."""
    # Mantém a placa no acostamento, sem ocupar a pista de veículos.
    y = int(altura * .35 + (_distancia_cenario % 160) - 80)
    _bloco(tela, (65, 67, 72), 23, y + 23, 4, 25)
    _bloco(tela, (20, 45, 33), 2, y, 46, 27)
    _bloco(tela, (240, 236, 204), 4, y + 2, 42, 23)
    _bloco(tela, (29, 92, 65), 6, y + 4, 38, 19)
    fonte = pygame.font.Font(None, 13)
    titulo = fonte.render('CIDADE', False, (250, 250, 220))
    distancia = fonte.render('500 M', False, (250, 250, 220))
    tela.blit(titulo, (25 - titulo.get_width() // 2, y + 4))
    tela.blit(distancia, (25 - distancia.get_width() // 2, y + 13))


def desenhar_pista(tela, largura, altura):
    """Desenha a pista e faz a cidade entrar pelo horizonte, sem corte seco."""
    global _cenario_atual, _transicao_concluida
    if _cenario_atual == 'urbano':
        _desenhar_cidade(tela, altura)
    elif _cenario_atual == 'transicao' and _inicio_transicao is not None:
        # Uma fronteira visual desce a tela conforme a estrada avança.
        # Não depende de FPS: usa a distância já percorrida pela pista.
        avancado = max(0.0, _distancia_cenario - _inicio_transicao)
        fronteira = min(altura, int(avancado))
        if fronteira >= altura:
            _transicao_concluida = True
            _cenario_atual = 'urbano'
            _desenhar_cidade(tela, altura)
        else:
            _desenhar_grama(tela, altura)
            recorte_anterior = tela.get_clip()
            try:
                tela.set_clip(pygame.Rect(0, 0, LARGURA_AREA_JOGO, fronteira))
                _desenhar_cidade(tela, altura)
            finally:
                tela.set_clip(recorte_anterior)
    else:
        _desenhar_grama(tela, altura)

    _desenhar_asfalto(tela, altura)
    _desenhar_bordas(tela, altura)
    _desenhar_divisoes(tela, altura)
    if 650 <= _pontos_cenario < 700:
        _desenhar_placa_cidade(tela, altura)
    _desenhar_painel(tela, largura, altura)
