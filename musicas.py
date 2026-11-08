"""Trilhas do Drive Race com carregamento antecipado e crossfade sem bloqueio."""

from pathlib import Path
import pygame

PASTA_MUSICAS = Path(__file__).resolve().parent / "assets" / "musicas"
TRILHAS = {
    "rural": "dust_diesel.wav",
    "urbano": "concrete_chaos.wav",
    "extremo": "redline_fury.wav",
}
VOLUME_MUSICA = 0.30

_sons = {}
_canais = []
_trilha_atual = None
_canal_atual = None
_transicoes = []  # [canal, volume_inicial, volume_final, inicio_ms, duracao_ms, parar]


def inicializar_musicas():
    """Carrega as faixas uma vez, após pygame.mixer.init()."""
    global _sons, _canais
    if pygame.mixer.get_init() is None:
        raise RuntimeError("Inicialize pygame.mixer antes das músicas")
    if _canais:
        return
    _sons = {}
    for nome, arquivo in TRILHAS.items():
        caminho = PASTA_MUSICAS / arquivo
        if caminho.is_file():
            _sons[nome] = pygame.mixer.Sound(str(caminho))
        else:
            print(f"Música não encontrada: {caminho}")
    # Reserva dois canais exclusivos, sem competir com moeda e colisão.
    pygame.mixer.set_num_channels(max(pygame.mixer.get_num_channels(), 10))
    _canais = [pygame.mixer.Channel(8), pygame.mixer.Channel(9)]
    for canal in _canais:
        canal.set_volume(0)


def _agendar(canal, volume_final, duracao_ms, parar=False):
    global _transicoes
    agora = pygame.time.get_ticks()
    _transicoes = [t for t in _transicoes if t[0] != canal]
    inicio = canal.get_volume()
    if duracao_ms <= 0:
        canal.set_volume(volume_final)
        if parar:
            canal.stop()
    else:
        _transicoes.append([canal, inicio, volume_final, agora, duracao_ms, parar])


def atualizar_musicas():
    """Chamar uma vez por frame para atualizar os volumes sem esperar."""
    global _transicoes
    agora = pygame.time.get_ticks()
    restantes = []
    for canal, inicio, fim, instante, duracao, parar in _transicoes:
        progresso = min(1.0, max(0.0, (agora - instante) / duracao))
        canal.set_volume(inicio + (fim - inicio) * progresso)
        if progresso >= 1.0:
            if parar:
                canal.stop()
        else:
            restantes.append([canal, inicio, fim, instante, duracao, parar])
    _transicoes = restantes


def tocar_trilha(nome, transicao_ms=1000):
    """Troca a faixa sem I/O de disco ou espera durante a partida."""
    global _trilha_atual, _canal_atual
    if nome == _trilha_atual:
        return
    if not _canais:
        inicializar_musicas()
    som = _sons.get(nome)
    if som is None:
        print(f"Trilha indisponível: {nome}")
        return
    proximo = _canais[0] if _canal_atual is not _canais[0] else _canais[1]
    # Interrompe qualquer faixa antiga no canal que será reutilizado.
    _transicoes[:] = [t for t in _transicoes if t[0] != proximo]
    proximo.stop()
    proximo.set_volume(0 if transicao_ms > 0 else VOLUME_MUSICA)
    proximo.play(som, loops=-1)
    if _canal_atual is not None:
        _agendar(_canal_atual, 0, transicao_ms, parar=True)
    _agendar(proximo, VOLUME_MUSICA, transicao_ms)
    _canal_atual = proximo
    _trilha_atual = nome


def parar_trilha(transicao_ms=500):
    """Encerra a trilha sem bloquear o loop."""
    global _trilha_atual, _canal_atual
    if not _canais:
        return
    for canal in _canais:
        if canal.get_busy():
            _agendar(canal, 0, transicao_ms, parar=True)
    _trilha_atual = None
    _canal_atual = None


def atualizar_trilha(cenario, indice_fase):
    """Seleciona a trilha com base no cenário e na fase (índice começa em 0)."""
    if indice_fase >= 12:
        nome = "extremo"
    elif cenario == "urbano":
        nome = "urbano"
    else:
        nome = "rural"
    tocar_trilha(nome)
