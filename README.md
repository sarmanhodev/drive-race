<div align="center">

# 🚛 DRIVE RACE

### A estrada não perdoa. Seu recorde também não.

**Um arcade de sobrevivência sobre rodas, desenvolvido em Python e Pygame, com visual inspirado nos clássicos de 8 bits.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-1B8D49?style=for-the-badge)
![Pixel Art](https://img.shields.io/badge/Estilo-Pixel%20Art-FFCC33?style=for-the-badge&labelColor=172033)
![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento-2389DA?style=for-the-badge)

**[Gameplay](#-o-jogo-em-ação) · [Recursos](#-o-que-te-espera-na-pista) · [Como jogar](#-como-jogar) · [Instalação](#-instalação-e-execução)**

</div>

---

## 🎮 O jogo em ação

> **Capturas reais do Drive Race**, feitas durante a execução do jogo. Não são artes conceituais.

### 🌲 Estrada rural

O início da jornada: asfalto, árvores pixeladas, moedas e tráfego. À direita, o HUD mostra **pontos, fase, velocidade e recorde**.

![Captura real do Drive Race no cenário rural, com caminhão e painel arcade](assets/screenshots/drive-race-rural.png)

### 🌃 Cidade noturna e Game Over

Com a progressão, a paisagem muda para a cidade. O desafio continua — até a próxima colisão!

![Captura real do Drive Race na cidade noturna, com tela de Game Over e quatro cards do HUD](assets/screenshots/drive-race-cidade-game-over.png)

---

## 🏁 Sobre o Drive Race

Você dirige um **caminhão** em uma estrada de três faixas. Desvie de carros e motos, evite buracos e colete moedas para aumentar a pontuação. A dificuldade cresce conforme você avança, e alguns veículos podem surpreender com mudanças de faixa.

**Atenção:** ultrapassar veículos não dá pontos. Para subir no placar, é preciso **coletar moedas e sobreviver**.

## ✨ O que te espera na pista

| Recurso | Como funciona |
| :--- | :--- |
| 🚛 **Caminhão controlável** | Movimentação lateral entre as faixas da estrada. |
| 🚗 **Carros vermelhos** | Obstáculos que seguem em linha reta. |
| 🚙 **Carros azuis** | Podem mudar de faixa e sinalizam a manobra. |
| 🏍️ **Motocicletas** | Passam a realizar manobras nas etapas mais avançadas. |
| 🕳️ **Buracos** | Novos perigos que exigem atenção à pista. |
| 🪙 **Moedas** | Coletáveis de diferentes valores, inclusive especiais. |
| 🌲 **Cenário rural** | Vegetação e árvores em pixel art. |
| 🌃 **Cenário urbano** | Cidade noturna com edifícios, calçadas e postes. |
| 📊 **HUD arcade** | Cards de pontos, fase, velocidade e recorde. |
| 🏆 **Recorde local** | Melhor pontuação armazenada entre partidas. |

## 🕹️ Como jogar

| Tecla | Ação |
| :---: | :--- |
| `←` / `→` | Mover o caminhão para a esquerda ou direita |
| `Enter` | Iniciar pelo menu |
| `R` | Reiniciar após o Game Over |
| `Esc` | Voltar ao menu após o Game Over |

**Objetivo:** desviar dos perigos e coletar o máximo de moedas possível. Uma colisão encerra a partida.

## 📈 Progressão do desafio

O jogo tem **16 fases**, com mudança de etapa a cada **250 pontos**. Entre os marcos de jogabilidade:

| Pontuação | O que muda |
| :---: | :--- |
| **0–249** | Primeiros obstáculos: carros vermelhos. |
| **250–499** | Carros azuis começam a mudar de faixa. |
| **500–749** | Motocicletas entram no trânsito. |
| **750–999** | Buracos e chegada ao ambiente urbano. |
| **1.000–1.249** | Carros azuis aparecem com mais frequência. |
| **1.250+** | Motocicletas também passam a mudar de faixa. |

A dificuldade segue evoluindo nas fases posteriores. **A 16ª fase é a última configuração de dificuldade**, mas a partida pode continuar enquanto você conseguir sobreviver.

## 🛠️ Tecnologias

- **Python 3** — lógica e organização modular do jogo.
- **Pygame** — renderização, eventos, movimentação, colisões e interface.
- **JSON** — persistência do recorde local.

## 🚀 Instalação e execução

**Pré-requisitos:** Python 3 instalado e acesso a um terminal.

### 1. Clonar o projeto

```bash
git clone https://github.com/sarmanhodev/drive-race.git
cd drive-race
```

### 2. Criar um ambiente virtual

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Iniciar o jogo

```bash
python main.py
```

> O jogo utiliza o arquivo `assets/icone.png` como ícone da janela. Mantenha a pasta `assets` junto aos arquivos Python.

## 📁 Estrutura do projeto

```text
drive-race/
├── assets/              # Ícone e recursos visuais
│   └── screenshots/     # Capturas reais usadas neste README
├── caminhao.py          # Desenho e movimento do caminhão
├── colisao.py           # Verificação de colisões
├── cores.py             # Paleta de cores
├── dificuldade.py       # Configuração das 16 fases
├── interface.py         # Placar, recorde e telas de aviso
├── main.py              # Inicialização e loop do jogo
├── menu.py              # Menu inicial
├── moedas.py            # Coleta e desenho das moedas
├── obstaculos.py        # Carros, motos e buracos
├── pista.py             # Pista, floresta e cidade
├── pontuacao.py         # Pontuação e persistência
├── recorde.json         # Recorde salvo localmente
├── requirements.txt     # Dependências
├── velocidade.py        # Progressão da velocidade
└── velocimetro.py       # Cards de fase e velocidade
```

## 🔮 Próximos passos

O Drive Race continua em desenvolvimento. Algumas ideias para futuras versões são novos cenários, ajustes de equilíbrio e distribuição de um executável para Windows.

---

<div align="center">

### 🏆 Até onde você consegue chegar?

**Desenvolvido por [sarmanhodev](https://github.com/sarmanhodev) com Python, Pygame e muita vontade de sobreviver ao trânsito.** 🚛💨

</div>
