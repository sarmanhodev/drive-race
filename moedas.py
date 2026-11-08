"""Moedas 8 bits com movimento horizontal aleatório para Drive Race.

Mantém as assinaturas usadas pelo main.py existente.
"""

import random
import pygame
from sons import tocar_moeda
from pista import PISTA_X, PISTA_LARGURA, LARGURA_FAIXA, QUANTIDADE_FAIXAS

TAMANHO = 28
PONTOS_COMUM = 50
PONTOS_RAPIDA = 100
PONTOS_ESPECIAL = 200
DISTANCIA_SEGURANCA = 85
MARGEM_PISTA = 13

moedas = []
efeitos = []

DESENHO = (
    "....OOOOOO....",
    "..OOYYYYYYOO..",
    ".OYYLLLLLLYYO.",
    ".OYLWWLLLLLYO.",
    "OYYLWWLLLLLYYO",
    "OYLWWLLLLLLLYO",
    "OYLWLLWWLLLYYO",
    "OYLWLLWWLLLYYO",
    "OYLWLLLLLLLYYO",
    "OYYLLLLLLLLYYO",
    ".OYYLLLLLLYYO.",
    ".OYYYYYYYYYYO.",
    "..OOYYYYYYOO..",
    "....OOOOOO....",
)


def _sprite(tipo, quadro):
    if tipo == "especial":
        paleta = {
            "O": (67, 30, 95),
            "Y": (218, 112, 255),
            "L": (249, 191, 255),
            "W": (255, 247, 255),
        }
    elif tipo == "rapida":
        paleta = {
            "O": (16, 49, 95),
            "Y": (46, 158, 250),
            "L": (118, 217, 255),
            "W": (236, 253, 255),
        }
    else:
        paleta = {
            "O": (91, 55, 16),
            "Y": (250, 183, 39),
            "L": (255, 220, 78),
            "W": (255, 247, 184),
        }

    superficie = pygame.Surface((14, 14), pygame.SRCALPHA)
    for y, linha in enumerate(DESENHO):
        for x, pixel in enumerate(linha):
            if pixel != ".":
                superficie.set_at((x, y), paleta[pixel])
    if quadro % 2:
        pygame.draw.rect(superficie, (255, 255, 255), (10, 3, 2, 2))
    return pygame.transform.scale(superficie, (TAMANHO, TAMANHO))


def reiniciar_moedas():
    moedas.clear()
    efeitos.clear()


def _chance_movimento(pontos):
    if pontos < 250:
        return 0.20
    if pontos < 500:
        return 0.40
    if pontos < 750:
        return 0.50
    if pontos < 1000:
        return 0.65
    if pontos < 1500:
        return 0.75
    return 0.85


def escolher_tipo_moeda(pontos):
    """Retorna o tipo de moeda; as raras só surgem a partir de 500 pontos."""
    if pontos < 500:
        return "comum"
    if pontos < 1000:
        chance_especial, chance_rapida = 0.05, 0.12
    elif pontos < 1500:
        chance_especial, chance_rapida = 0.08, 0.16
    else:
        chance_especial, chance_rapida = 0.12, 0.20
    sorteio = random.random()
    if sorteio < chance_especial:
        return "especial"
    if sorteio < chance_especial + chance_rapida:
        return "rapida"
    return "comum"


def _perto_de_obstaculo(retangulo, obstaculos_atuais):
    if not obstaculos_atuais:
        return False
    for obstaculo in obstaculos_atuais:
        outro = obstaculo["rect"]
        if retangulo.right + 8 <= outro.left or retangulo.left - 8 >= outro.right:
            continue
        if (
            retangulo.top < outro.bottom + DISTANCIA_SEGURANCA
            and retangulo.bottom > outro.top - DISTANCIA_SEGURANCA
        ):
            return True
    return False


def _perto_de_outra_moeda(retangulo, ignorar=None):
    for moeda in moedas:
        if moeda is ignorar:
            continue
        if retangulo.colliderect(moeda["rect"].inflate(16, 65)):
            return True
    return False


def criar_moeda(obstaculos_atuais=None, pontos=0):
    """Cria uma moeda em faixa segura, já com comportamento sorteado."""
    faixas = list(range(QUANTIDADE_FAIXAS))
    random.shuffle(faixas)
    for faixa in faixas:
        centro = round(PISTA_X + (faixa + 0.5) * LARGURA_FAIXA)
        retangulo = pygame.Rect(0, -TAMANHO, TAMANHO, TAMANHO)
        retangulo.centerx = centro
        if _perto_de_outra_moeda(retangulo):
            continue
        if _perto_de_obstaculo(retangulo, obstaculos_atuais):
            continue

        tipo = escolher_tipo_moeda(pontos)
        movel = tipo == "rapida" or random.random() < _chance_movimento(pontos)
        imprevisivel = movel and random.random() < 0.40
        velocidade_x = random.uniform(48, 82)
        if pontos >= 1000:
            velocidade_x *= 1.25
        if pontos >= 1500:
            velocidade_x *= 1.20
        if tipo == "rapida":
            velocidade_x *= 1.35
        velocidade_x *= random.choice((-1, 1))

        moedas.append(
            {
                "rect": retangulo,
                "posicao_x": float(retangulo.x),
                "posicao_y": float(retangulo.y),
                "tipo": tipo,
                "especial": tipo == "especial",
                "movel": movel,
                "imprevisivel": imprevisivel,
                "velocidade_x": velocidade_x if movel else 0.0,
                "tempo_mudanca": random.uniform(0.35, 0.95),
                "fase_animacao": random.randrange(100),
            }
        )
        return True
    return False


def _mover_horizontal(moeda, delta_time, obstaculos_atuais):
    if not moeda["movel"] or delta_time <= 0:
        return True

    retangulo = moeda["rect"]
    x_anterior = moeda["posicao_x"]
    limite_esquerdo = PISTA_X + MARGEM_PISTA
    limite_direito = PISTA_X + PISTA_LARGURA - MARGEM_PISTA - TAMANHO

    moeda["tempo_mudanca"] -= delta_time
    if moeda["imprevisivel"] and moeda["tempo_mudanca"] <= 0:
        moeda["tempo_mudanca"] = random.uniform(0.35, 1.0)
        if random.random() < 0.65:
            moeda["velocidade_x"] *= -1

    novo_x = x_anterior + moeda["velocidade_x"] * delta_time
    if novo_x < limite_esquerdo or novo_x > limite_direito:
        moeda["velocidade_x"] *= -1
        novo_x = max(limite_esquerdo, min(limite_direito, novo_x))

    candidato = retangulo.copy()
    candidato.x = round(novo_x)
    if _perto_de_obstaculo(candidato, obstaculos_atuais) or _perto_de_outra_moeda(
        candidato, moeda
    ):
        # Tenta inverter o movimento; se a posição atual deixou de ser segura,
        # a moeda será descartada pelo verificador do loop principal.
        moeda["velocidade_x"] *= -1
        novo_x = x_anterior

    moeda["posicao_x"] = novo_x
    retangulo.x = round(novo_x)
    return True


def movimentar_moedas(
    altura, caminhao, pontuacao, velocidade, delta_time, obstaculos_atuais=None
):
    # Limita saltos horizontais após pausas/engasgos do computador.
    dt = max(0.0, min(float(delta_time), 0.05))
    for moeda in moedas[:]:
        moeda["posicao_y"] += velocidade
        moeda["rect"].y = round(moeda["posicao_y"])
        _mover_horizontal(moeda, dt, obstaculos_atuais)

        # Evita moedas escondidas em veículos ou perigosamente próximas.
        if _perto_de_obstaculo(
            moeda["rect"], obstaculos_atuais
        ) or _perto_de_outra_moeda(moeda["rect"], moeda):
            moedas.remove(moeda)
            continue

        if caminhao.colliderect(moeda["rect"].inflate(-6, -6)):
            tipo = moeda["tipo"]
            pontos = {
                "comum": PONTOS_COMUM,
                "rapida": PONTOS_RAPIDA,
                "especial": PONTOS_ESPECIAL,
            }[tipo]
            pontuacao.adicionar_pontos(pontos)
            # Reproduz o efeito sonoro ao coletar a moeda
            tocar_moeda()
            efeitos.append(
                {
                    "x": moeda["rect"].centerx,
                    "y": float(moeda["rect"].y),
                    "pontos": pontos,
                    "tipo": tipo,
                    "tempo": 0.7,
                }
            )
            moedas.remove(moeda)
        elif moeda["rect"].top > altura:
            moedas.remove(moeda)

    for efeito in efeitos[:]:
        efeito["tempo"] -= delta_time
        efeito["y"] -= 42 * delta_time
        if efeito["tempo"] <= 0:
            efeitos.remove(efeito)


def desenhar_moedas(tela):
    quadro = pygame.time.get_ticks() // 180
    for moeda in moedas:
        sprite = _sprite(moeda["tipo"], quadro + moeda["fase_animacao"])
        tela.blit(sprite, moeda["rect"])

    fonte = pygame.font.Font(None, 25)
    cores_efeitos = {
        "comum": (255, 225, 76),
        "rapida": (125, 220, 255),
        "especial": (247, 192, 255),
    }
    for efeito in efeitos:
        cor = cores_efeitos.get(efeito["tipo"], (255, 225, 76))
        texto = fonte.render(f"+{efeito['pontos']}", False, cor)
        texto = pygame.transform.scale(
            texto, (texto.get_width() * 2, texto.get_height() * 2)
        )
        tela.blit(texto, texto.get_rect(center=(efeito["x"], round(efeito["y"]))))
