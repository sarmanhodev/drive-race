
import math
import random
import struct
import pygame


# Configurações do áudio
TAXA_AMOSTRAGEM = 44100
VOLUME_EFEITOS = 0.35

som_moeda = None
som_colisao = None


def gerar_som_moeda():
    """Gera um efeito de moeda no estilo arcade 8 bits."""

    duracao = 0.18
    quantidade = int(TAXA_AMOSTRAGEM * duracao)

    dados = bytearray()

    for i in range(quantidade):
        tempo = i / TAXA_AMOSTRAGEM

        # Duas notas ascendentes
        frequencia = 880 if tempo < 0.08 else 1320

        # Onda quadrada característica dos jogos retrô
        onda = 1 if math.sin(
            2 * math.pi * frequencia * tempo
        ) >= 0 else -1

        # Volume diminui suavemente no final
        envelope = (1 - tempo / duracao) ** 1.5

        amplitude = int(12000 * onda * envelope)

        dados.extend(struct.pack("<h", amplitude))

    return pygame.mixer.Sound(buffer=bytes(dados))


def gerar_som_colisao():
    """Gera uma explosão eletrônica retrô com queda de frequência."""

    duracao = 0.42
    quantidade = int(TAXA_AMOSTRAGEM * duracao)

    dados = bytearray()
    gerador = random.Random(42)
    fase = 0.0

    for i in range(quantidade):
        tempo = i / TAXA_AMOSTRAGEM
        progresso = tempo / duracao

        # Frequência cai rapidamente, simulando uma batida
        frequencia = 380 * (1 - progresso) ** 2 + 45
        fase += 2 * math.pi * frequencia / TAXA_AMOSTRAGEM

        # Onda quadrada com ruído eletrônico
        onda = 1.0 if math.sin(fase) >= 0 else -1.0
        ruido = gerador.uniform(-1.0, 1.0)

        # Mistura o impacto com uma textura de explosão
        sinal = 0.55 * onda + 0.45 * ruido

        # Ataque forte e desaparecimento progressivo
        envelope = (1 - progresso) ** 2

        amplitude = int(18000 * sinal * envelope)
        amplitude = max(-32768, min(32767, amplitude))

        dados.extend(struct.pack("<h", amplitude))

    return pygame.mixer.Sound(buffer=bytes(dados))


def inicializar_sons():
    """Inicializa os efeitos sonoros do jogo."""
    global som_moeda, som_colisao

    if pygame.mixer.get_init() is None:
        pygame.mixer.init(
            frequency=TAXA_AMOSTRAGEM,
            size=-16,
            channels=1
        )

    som_moeda = gerar_som_moeda()
    som_moeda.set_volume(VOLUME_EFEITOS)

    som_colisao = gerar_som_colisao()
    som_colisao.set_volume(0.55)


def tocar_moeda():
    """Reproduz o som quando o caminhão coleta uma moeda."""
    if som_moeda is not None:
        som_moeda.play()


def tocar_colisao():
    """Reproduz o som quando o caminhão bate."""
    if som_colisao is not None:
        som_colisao.play()
