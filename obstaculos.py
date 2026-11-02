"""Obstáculos Drive Race: carros vermelhos, azuis, motos e buracos (8 bits).

API compatível com main.py. Pontuação exclusivamente por moedas.
"""
import random
import pygame
from pista import PISTA_X, LARGURA_FAIXA, QUANTIDADE_FAIXAS

CARRO_LARGURA, CARRO_ALTURA = 50, 90
MOTO_LARGURA, MOTO_ALTURA = 26, 62
BURACO_LARGURA, BURACO_ALTURA = 62, 39
VELOCIDADE_CARROS = 5
obstaculos = []
PRETO = (21, 24, 34)
VERMELHO = (214, 48, 57)
VERMELHO_CLARO = (248, 91, 75)
VERMELHO_ESCURO = (136, 31, 45)
AZUL = (38, 115, 207)
AZUL_CLARO = (111, 198, 239)
AZUL_ESCURO = (25, 62, 124)
BRANCO = (235, 237, 221)
AMARELO = (255, 216, 85)
CINZA = (112, 119, 132)
CINZA_CLARO = (175, 184, 191)
ASFALTO_QUEBRADO = (121, 111, 95)
ASFALTO_SOMBRA = (78, 73, 69)
BURACO_ESCURO = (19, 19, 24)


def _centro_faixa(faixa):
    return round(PISTA_X + (faixa + .5) * LARGURA_FAIXA)


def escolher_tipo_obstaculo(pontos):
    """Carros desde o início, motos aos 500 e buracos aos 750 pontos."""
    if pontos < 500:
        return 'carro'
    if pontos < 750:
        return random.choices(['carro', 'moto'], weights=[70, 30])[0]
    if pontos < 1250:
        pesos = [60, 30, 10]
    elif pontos < 2000:
        pesos = [50, 30, 20]
    else:
        pesos = [40, 35, 25]
    return random.choices(['carro', 'moto', 'buraco'], weights=pesos)[0]


def _chance_azul(pontos):
    if pontos < 250: return 0
    if pontos < 500: return .25
    if pontos < 1000: return .35
    if pontos < 1500: return .45
    if pontos < 2500: return .55
    return .60


def criar_obstaculo(pontos=0):
    tipo = escolher_tipo_obstaculo(pontos)
    dimensoes = {'carro': (50, 90), 'moto': (26, 62), 'buraco': (62, 39)}
    largura, altura = dimensoes[tipo]
    faixa = random.randrange(QUANTIDADE_FAIXAS)
    retangulo = pygame.Rect(0, -altura, largura, altura)
    retangulo.centerx = _centro_faixa(faixa)
    # Impede nascimento sobre outro obstáculo na mesma faixa.
    for existente in obstaculos:
        outro = existente['rect']
        if abs(outro.centerx - retangulo.centerx) < LARGURA_FAIXA / 2 and outro.top < altura + 30:
            return
    cor = 'azul' if tipo == 'carro' and random.random() < _chance_azul(pontos) else 'vermelho'
    obstaculos.append({
        'rect': retangulo, 'tipo': tipo, 'cor': cor, 'faixa': faixa,
        'pontuado': False, 'posicao_y': float(retangulo.y),
        'posicao_x': float(retangulo.centerx), 'pontos_criacao': pontos,
        'estado': 'reto', 'destino': faixa, 'inicio_seta': 0,
        'inicio_manobra': 0, 'x_origem': float(retangulo.centerx),
        'proxima_tentativa': pygame.time.get_ticks() + random.randint(550, 1500),
    })


def _intervalo_manobra(obj):
    pontos = obj['pontos_criacao']
    if obj['tipo'] == 'moto':
        if pontos < 1250: return (950, 1750)
        if pontos < 2500: return (650, 1250)
        return (400, 900)
    if pontos < 1000: return (1300, 2300)
    if pontos < 2000: return (900, 1700)
    return (650, 1300)


def _faixa_livre(obj, destino):
    """Evita cruzar/aterrar sobre obstáculos próximos na faixa de destino."""
    rect = obj['rect']
    centro = _centro_faixa(destino)
    margem_y = 85 if obj['tipo'] == 'moto' else 110
    for outro_obj in obstaculos:
        if outro_obj is obj:
            continue
        outro = outro_obj['rect']
        # Inclui o destino de outro veículo que já esteja mudando de faixa.
        centros = [outro.centerx]
        if outro_obj.get('estado') == 'mudando':
            centros.append(_centro_faixa(outro_obj['destino']))
        if any(abs(c - centro) < LARGURA_FAIXA * .65 for c in centros):
            if rect.top < outro.bottom + margem_y and rect.bottom + margem_y > outro.top:
                return False
    return True


def _iniciar_manobra(obj, destino, agora):
    obj['destino'] = destino
    obj['x_origem'] = obj['posicao_x']
    obj['inicio_manobra'] = agora
    obj['estado'] = 'mudando'


def movimentar_obstaculos(altura, caminhao, pontuacao, velocidade=VELOCIDADE_CARROS):
    """Movimenta obstáculos, sem adicionar pontos por ultrapassagem."""
    agora = pygame.time.get_ticks()
    for obj in obstaculos[:]:
        rect = obj['rect']
        obj['posicao_y'] += velocidade
        rect.y = round(obj['posicao_y'])
        tipo = obj['tipo']
        # Motos aparecem aos 500 pontos, mas seguem reto até 1.250.
        pontos_atuais = getattr(pontuacao, 'pontos', obj['pontos_criacao'])
        manobravel = (tipo == 'moto' and pontos_atuais >= 1250) or (
            tipo == 'carro' and obj['cor'] == 'azul')
        if manobravel:
            estado = obj['estado']
            if estado == 'reto' and agora >= obj['proxima_tentativa']:
                opcoes = [f for f in (obj['faixa'] - 1, obj['faixa'] + 1)
                          if 0 <= f < QUANTIDADE_FAIXAS and _faixa_livre(obj, f)]
                # Não inicia manobra muito perto do caminhão.
                distancia = caminhao.top - rect.bottom
                if opcoes and 95 < distancia < 480:
                    destino = random.choice(opcoes)
                    # Carros azuis e motos anunciam a manobra brevemente.
                    obj['destino'] = destino
                    obj['estado'] = 'seta'
                    obj['inicio_seta'] = agora
                else:
                    obj['proxima_tentativa'] = agora + random.randint(220, 450)
            elif estado == 'seta' and agora - obj['inicio_seta'] >= (250 if tipo == 'moto' else 350):
                # Revalida a faixa antes de iniciar a troca.
                if _faixa_livre(obj, obj['destino']):
                    _iniciar_manobra(obj, obj['destino'], agora)
                else:
                    obj['estado'] = 'reto'
                    obj['proxima_tentativa'] = agora + 500
            elif estado == 'mudando':
                duracao = 300 if tipo == 'moto' else 450
                t = min(1.0, (agora - obj['inicio_manobra']) / duracao)
                # Interpolação suave, sem teletransporte.
                suavizado = t * t * (3 - 2 * t)
                obj['posicao_x'] = obj['x_origem'] + (
                    _centro_faixa(obj['destino']) - obj['x_origem']) * suavizado
                rect.centerx = round(obj['posicao_x'])
                if t >= 1:
                    obj['faixa'] = obj['destino']
                    obj['estado'] = 'reto'
                    a, b = _intervalo_manobra(obj)
                    obj['proxima_tentativa'] = agora + random.randint(a, b)
        if rect.top > altura:
            obstaculos.remove(obj)


def _bloco(tela, cor, x, y, largura, altura):
    pygame.draw.rect(tela, cor, (x, y, largura, altura))


def _sprite(tela, retangulo, largura_base, altura_base, desenhar):
    superficie = pygame.Surface((largura_base, altura_base), pygame.SRCALPHA)
    desenhar(superficie)
    ampliada = pygame.transform.scale(superficie, retangulo.size)
    tela.blit(ampliada, retangulo.topleft)


def _desenhar_indicador_mudanca(tela, rect, direcao, moto=False):
    """Seta amarela 8 bits acima do veículo, apontando para a nova faixa."""
    # Seta maior que a seta da carroceria para ser percebida em movimento.
    escala = 3 if moto else 3
    largura = 9 * escala
    altura = 5 * escala
    centro_x = rect.centerx
    topo = rect.top - altura - (7 if moto else 8)
    if topo < 2:
        return

    # Sombra pixelada para destacar a seta sobre qualquer cor da pista.
    x = centro_x - largura // 2
    y = topo
    pygame.draw.rect(tela, PRETO, (x - 2, y - 2, largura + 4, altura + 4))
    pygame.draw.rect(tela, (45, 45, 55), (x, y, largura, altura))

    # Desenha uma flecha feita somente de blocos (sem antialiasing).
    def bloco(px, py, w, h, cor=AMARELO):
        pygame.draw.rect(tela, cor, (x + px * escala, y + py * escala,
                                     w * escala, h * escala))

    if direcao > 0:
        bloco(1, 2, 5, 1)
        bloco(5, 1, 2, 3)
        bloco(7, 2, 2, 1)
        bloco(6, 0, 1, 5)
    else:
        bloco(3, 2, 5, 1)
        bloco(2, 1, 2, 3)
        bloco(0, 2, 2, 1)
        bloco(2, 0, 1, 5)


def desenhar_obstaculos(tela):
    agora = pygame.time.get_ticks()
    for obj in obstaculos:
        rect, tipo = obj['rect'], obj.get('tipo', 'carro')
        azul = tipo == 'carro' and obj.get('cor') == 'azul'
        avisando = obj.get('estado') == 'seta'
        direcao = (1 if obj['destino'] > obj['faixa'] else -1) if avisando else 0

        # O indicador externo pisca rapidamente enquanto a seta está ativa.
        indicador_visivel = avisando and ((agora - obj['inicio_seta']) // 85) % 2 == 0

        if tipo == 'moto':
            desenhar_moto(tela, rect)
        elif tipo == 'buraco':
            desenhar_buraco(tela, rect)
        else:
            # Preserva a seta já existente na carroceria do carro azul.
            desenhar_carro(tela, rect, azul=azul,
                          seta=direcao if indicador_visivel and azul else 0)

        if indicador_visivel and (azul or tipo == 'moto'):
            _desenhar_indicador_mudanca(tela, rect, direcao, moto=(tipo == 'moto'))


def desenhar_carro(tela, carro, azul=False, seta=0):
    """Carro vermelho ou azul, visto de cima, em pixels 25 x 45."""
    cor = AZUL if azul else VERMELHO
    claro = AZUL_CLARO if azul else VERMELHO_CLARO
    escuro = AZUL_ESCURO if azul else VERMELHO_ESCURO
    def pintar(s):
        for y in (8, 30):
            _bloco(s, PRETO, 0, y, 4, 9)
            _bloco(s, PRETO, 21, y, 4, 9)
            _bloco(s, CINZA, 1, y + 2, 2, 4)
            _bloco(s, CINZA, 22, y + 2, 2, 4)
        _bloco(s, PRETO, 5, 0, 15, 45)
        _bloco(s, PRETO, 3, 3, 19, 39)
        _bloco(s, escuro, 5, 2, 15, 41)
        _bloco(s, cor, 4, 5, 17, 35)
        _bloco(s, claro, 6, 5, 3, 34)
        _bloco(s, escuro, 18, 6, 2, 32)
        _bloco(s, PRETO, 6, 8, 13, 9)
        _bloco(s, AZUL_CLARO, 7, 9, 11, 6)
        _bloco(s, BRANCO, 8, 10, 3, 2)
        _bloco(s, AZUL_ESCURO, 7, 15, 11, 1)
        _bloco(s, PRETO, 6, 29, 13, 8)
        _bloco(s, AZUL_CLARO, 7, 30, 11, 5)
        _bloco(s, AZUL_ESCURO, 7, 35, 11, 1)
        _bloco(s, escuro, 7, 18, 11, 10)
        _bloco(s, cor, 8, 19, 9, 8)
        _bloco(s, claro, 9, 20, 2, 6)
        _bloco(s, AMARELO, 5, 2, 4, 2)
        _bloco(s, AMARELO, 16, 2, 4, 2)
        _bloco(s, PRETO, 5, 41, 15, 2)
        _bloco(s, claro, 5, 41, 4, 2)
        _bloco(s, claro, 16, 41, 4, 2)
        if seta < 0:
            _bloco(s, AMARELO, 3, 3, 5, 3)
        elif seta > 0:
            _bloco(s, AMARELO, 17, 3, 5, 3)
    _sprite(tela, carro, 25, 45, pintar)


def desenhar_moto(tela, moto):
    """Moto azul vista de cima, com piloto, em pixels 13 x 31."""
    def pintar(s):
        _bloco(s, PRETO, 5, 0, 3, 8)
        _bloco(s, CINZA, 6, 1, 1, 5)
        _bloco(s, PRETO, 5, 23, 3, 8)
        _bloco(s, CINZA, 6, 25, 1, 4)
        _bloco(s, PRETO, 1, 7, 11, 2)
        _bloco(s, CINZA_CLARO, 0, 6, 2, 3)
        _bloco(s, CINZA_CLARO, 11, 6, 2, 3)
        _bloco(s, PRETO, 3, 8, 7, 17)
        _bloco(s, AZUL_ESCURO, 4, 9, 5, 15)
        _bloco(s, AZUL, 3, 11, 7, 10)
        _bloco(s, AZUL_CLARO, 4, 11, 2, 7)
        _bloco(s, BRANCO, 5, 3, 3, 2)
        _bloco(s, PRETO, 3, 12, 7, 8)
        _bloco(s, (235, 195, 75), 4, 12, 5, 5)
        _bloco(s, AZUL_ESCURO, 4, 15, 5, 2)
        _bloco(s, PRETO, 4, 20, 5, 5)
        _bloco(s, CINZA, 5, 21, 3, 2)
    _sprite(tela, moto, 13, 31, pintar)


def desenhar_buraco(tela, buraco):
    """Buraco irregular em degraus, sem elipses ou arcos suavizados."""
    def pintar(s):
        _bloco(s, ASFALTO_QUEBRADO, 5, 2, 21, 16)
        _bloco(s, ASFALTO_QUEBRADO, 2, 5, 27, 11)
        _bloco(s, ASFALTO_QUEBRADO, 0, 8, 31, 5)
        _bloco(s, ASFALTO_SOMBRA, 4, 5, 23, 11)
        _bloco(s, ASFALTO_SOMBRA, 2, 8, 27, 5)
        _bloco(s, BURACO_ESCURO, 7, 5, 17, 11)
        _bloco(s, BURACO_ESCURO, 4, 8, 23, 5)
        _bloco(s, PRETO, 9, 7, 14, 7)
        _bloco(s, PRETO, 7, 9, 18, 3)
        _bloco(s, CINZA, 4, 5, 5, 2)
        _bloco(s, CINZA, 22, 14, 5, 2)
        _bloco(s, (164, 147, 120), 11, 3, 7, 2)
        _bloco(s, (55, 52, 51), 1, 3, 4, 1)
        _bloco(s, (55, 52, 51), 26, 16, 4, 1)
        _bloco(s, (55, 52, 51), 27, 4, 2, 3)
    _sprite(tela, buraco, 31, 20, pintar)

