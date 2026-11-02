import pygame
from pathlib import Path
import obstaculos
import moedas

from pontuacao import Pontuacao
from dificuldade import obter_dificuldade
from velocimetro import desenhar_velocimetro

from menu import desenhar_menu, processar_evento_menu

from velocidade import atualizar_velocidade

from pista import (
    atualizar_pista,
    desenhar_pista,
    definir_cenario,
    PISTA_X,
    PISTA_LARGURA
)

from caminhao import (
    desenhar_caminhao,
    movimentar_caminhao
)

from obstaculos import (
    criar_obstaculo,
    movimentar_obstaculos,
    desenhar_obstaculos
)

from colisao import verificar_colisao

from interface import (
    desenhar_game_over,
    desenhar_pontuacao,
    desenhar_aviso_fase
)


# ==========================================================
# 1 - INICIALIZAÇÃO DO PYGAME
# ==========================================================

pygame.init()


# ==========================================================
# 2 - CONFIGURAÇÕES DA JANELA
# ==========================================================

largura = 620
altura = 700

# Mantém a área original do jogo (pista + margens)
LARGURA_AREA_JOGO = 500

tela = pygame.display.set_mode((largura, altura))

pygame.display.set_caption("Drive Race")

# Ícone personalizado da janela
CAMINHO_ICONE = Path(__file__).resolve().parent / "assets" / "icone.png"

icone = pygame.image.load(str(CAMINHO_ICONE)).convert_alpha()
pygame.display.set_icon(icone)

# ==========================================================
# 3 - CONFIGURAÇÕES DO CAMINHÃO
# ==========================================================

caminhao_largura = 60
caminhao_altura = 120

velocidade_caminhao = 5

# Cria o retângulo do caminhão
caminhao = pygame.Rect(
    0,
    0,
    caminhao_largura,
    caminhao_altura
)

# Centraliza o caminhão na pista
caminhao.centerx = round(
    PISTA_X + PISTA_LARGURA / 2
)

# Posiciona o caminhão na parte inferior
caminhao.bottom = altura - 50


# ==========================================================
# 4 - CONTROLE DE FPS
# ==========================================================

relogio = pygame.time.Clock()

FPS = 60


# ==========================================================
# 5 - SISTEMA DE PONTUAÇÃO
# ==========================================================

pontuacao = Pontuacao()


# ==========================================================
# 6 - SISTEMA DE DIFICULDADE
# ==========================================================

# Obtém a dificuldade inicial
dificuldade_atual = obter_dificuldade(0)

# ==========================================================
# CONTROLE DE VELOCIDADE PROGRESSIVA
# ==========================================================

# Velocidade inicial do jogo
velocidade_atual = float(
    dificuldade_atual["velocidade"]
)

# Velocidade que desejamos alcançar
velocidade_alvo = velocidade_atual


# ==========================================================
# 7 - EVENTO DE CRIAÇÃO DOS CARROS
# ==========================================================

EVENTO_CARRO = pygame.USEREVENT + 1
EVENTO_MOEDA = pygame.USEREVENT + 2
INTERVALO_MOEDAS = 1400

# O temporizador só será ligado quando a partida começar.
pygame.time.set_timer(EVENTO_CARRO, 0)
pygame.time.set_timer(EVENTO_MOEDA, 0)


# ==========================================================
# 8 - CONTROLE DO AVISO DE DIFICULDADE
# ==========================================================

mostrar_aviso = False

tempo_aviso = 0

# Duração do aviso em milissegundos
DURACAO_AVISO = 2000


# ==========================================================
# 9 - ESTADO DO JOGO
# ==========================================================

# MENU -> JOGANDO -> GAME_OVER
estado = "MENU"
game_over = False

executando = True


def iniciar_partida():
    """Reinicia a partida sem apagar o recorde."""
    global dificuldade_atual, velocidade_atual, velocidade_alvo
    global mostrar_aviso, tempo_aviso, game_over, estado

    obstaculos.obstaculos.clear()
    moedas.reiniciar_moedas()
    caminhao.centerx = round(PISTA_X + PISTA_LARGURA / 2)
    caminhao.bottom = altura - 50
    pontuacao.reiniciar()

    dificuldade_atual = obter_dificuldade(0)
    velocidade_atual = float(dificuldade_atual["velocidade"])
    velocidade_alvo = velocidade_atual
    mostrar_aviso = False
    tempo_aviso = 0
    game_over = False
    estado = "JOGANDO"

    # Descarta eventos antigos de criação antes de reiniciar os timers.
    pygame.event.clear((EVENTO_CARRO, EVENTO_MOEDA))

    # Recomeça a contagem do tempo para gerar obstáculos.
    pygame.time.set_timer(EVENTO_CARRO, dificuldade_atual["intervalo"])
    pygame.time.set_timer(EVENTO_MOEDA, INTERVALO_MOEDAS)
    moedas.criar_moeda(obstaculos.obstaculos, pontuacao.pontos)



# ==========================================================
# 10 - GAME LOOP
# ==========================================================

while executando:

    # ------------------------------------------------------
    # CONTROLE DE FPS
    # ------------------------------------------------------

    delta_time = relogio.tick(FPS) / 1000.0


    # ------------------------------------------------------
    # EVENTOS DO PYGAME
    # ------------------------------------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            executando = False
            continue

        # Menu inicial: Enter começa; Esc encerra o programa.
        if estado == "MENU":
            comando = processar_evento_menu(evento)
            if comando == "jogar":
                iniciar_partida()
            elif comando == "sair":
                executando = False
            continue

        # Os obstáculos só nascem durante a partida.
        if evento.type == EVENTO_CARRO:
            if estado == "JOGANDO":
                criar_obstaculo(pontuacao.pontos)
            continue

        if evento.type == EVENTO_MOEDA:
            if estado == "JOGANDO":
                moedas.criar_moeda(obstaculos.obstaculos, pontuacao.pontos)
            continue

        if evento.type == pygame.KEYDOWN and estado == "GAME_OVER":
            if evento.key == pygame.K_r:
                iniciar_partida()
            elif evento.key == pygame.K_ESCAPE:
                # Volta ao menu sem criar novos obstáculos.
                pygame.time.set_timer(EVENTO_CARRO, 0)
                pygame.time.set_timer(EVENTO_MOEDA, 0)
                obstaculos.obstaculos.clear()
                moedas.reiniciar_moedas()
                pygame.event.clear((EVENTO_CARRO, EVENTO_MOEDA))
                estado = "MENU"
                game_over = False


    # ======================================================
    # 11 - ATUALIZAÇÃO DO JOGO
    # ======================================================

    if estado == "JOGANDO" and executando:

        # --------------------------------------------------
        # VERIFICA A DIFICULDADE ATUAL
        # --------------------------------------------------

        nova_dificuldade = obter_dificuldade(
            pontuacao.pontos
        )

        # Verifica se houve mudança de fase
        if nova_dificuldade != dificuldade_atual:

            dificuldade_atual = nova_dificuldade
            
            # Define a nova velocidade desejada
            velocidade_alvo = float(
                dificuldade_atual["velocidade"]
            )

            # Atualiza a frequência dos carros
            pygame.time.set_timer(
                EVENTO_CARRO,
                dificuldade_atual["intervalo"]
            )

            # Ativa o aviso da nova fase
            mostrar_aviso = True

            # Registra o momento da mudança
            tempo_aviso = pygame.time.get_ticks()

            # Exibe a fase no terminal
            print(
                f"Nova fase: {dificuldade_atual['nome']}"
            )

        # --------------------------------------------------
        # ACELERAÇÃO E DESACELERAÇÃO PROGRESSIVAS
        # --------------------------------------------------

        velocidade_atual = atualizar_velocidade(
            velocidade_atual,
            velocidade_alvo,
            delta_time
        )

        # --------------------------------------------------
        # MOVIMENTAÇÃO DO CAMINHÃO
        # --------------------------------------------------

        movimentar_caminhao(
            caminhao,
            velocidade_caminhao,
            PISTA_X,
            PISTA_LARGURA
        )


        # --------------------------------------------------
        # MOVIMENTAÇÃO DA PISTA
        # --------------------------------------------------

        atualizar_pista(
            velocidade_atual
        )


        # --------------------------------------------------
        # MOVIMENTAÇÃO DOS OBSTÁCULOS
        # --------------------------------------------------

        movimentar_obstaculos(
            altura,
            caminhao,
            pontuacao,
            velocidade_atual
        )


        # --------------------------------------------------
        # VERIFICAÇÃO DE COLISÕES (ANTES DA COLETA)
        # --------------------------------------------------

        if verificar_colisao(caminhao, obstaculos.obstaculos):
            game_over = True
            estado = "GAME_OVER"
            pygame.time.set_timer(EVENTO_CARRO, 0)
            pygame.time.set_timer(EVENTO_MOEDA, 0)
            mostrar_aviso = False

        # --------------------------------------------------
        # MOEDAS: SÓ COLETA SE O CAMINHÃO NÃO BATEU
        # --------------------------------------------------

        if not game_over:
            moedas.movimentar_moedas(
                altura,
                caminhao,
                pontuacao,
                velocidade_atual,
                delta_time,
                obstaculos.obstaculos
            )

        # --------------------------------------------------
        # REAVALIA A DIFICULDADE APÓS A PONTUAÇÃO
        # --------------------------------------------------

        # A pontuação pode ter aumentado com a coleta de moedas.
        # A nova fase será aplicada no próximo quadro.


    # ======================================================
    # 12 - DESENHO DOS ELEMENTOS
    # ======================================================

    if estado == "MENU":
        desenhar_menu(tela, largura, altura, pontuacao.recorde)
    else:
        # ------------------------------------------------------
        # DESENHA A PISTA
        # ------------------------------------------------------
        
        # Seleciona o cenário conforme a pontuação
        definir_cenario(pontuacao.pontos)

        desenhar_pista(
            tela,
            largura,
            altura
        )


        # ------------------------------------------------------
        # DESENHA OS OBSTÁCULOS
        # ------------------------------------------------------

        desenhar_obstaculos(tela)
        moedas.desenhar_moedas(tela)


        # ------------------------------------------------------
        # DESENHA O CAMINHÃO
        # ------------------------------------------------------

        desenhar_caminhao(
            tela,
            caminhao
        )


        # ------------------------------------------------------
        # DESENHA A PONTUAÇÃO
        # ------------------------------------------------------

        desenhar_pontuacao(
            tela,
            pontuacao
        )
    
        # ------------------------------------------------------
        # DESENHA O VELOCÍMETRO
        # ------------------------------------------------------

        desenhar_velocimetro(
            tela,
            largura,
            velocidade_atual,
            dificuldade_atual["nome"]
        )


        # ------------------------------------------------------
        # DESENHA O AVISO DE DIFICULDADE
        # ------------------------------------------------------

        if mostrar_aviso and not game_over:

            tempo_atual = pygame.time.get_ticks()

            tempo_decorrido = tempo_atual - tempo_aviso

            if tempo_decorrido < DURACAO_AVISO:

                desenhar_aviso_fase(
                    tela,
                    LARGURA_AREA_JOGO,
                    dificuldade_atual["nome"]
                )

            else:

                mostrar_aviso = False


        # ------------------------------------------------------
        # DESENHA O GAME OVER
        # ------------------------------------------------------

        if game_over:

            desenhar_game_over(
                tela,
                LARGURA_AREA_JOGO,
                altura,
                pontuacao
            )



    # ======================================================
    # 13 - ATUALIZAÇÃO DA TELA
    # ======================================================

    pygame.display.update()


# ==========================================================
# 14 - FINALIZAÇÃO DO PYGAME
# ==========================================================

pygame.quit()