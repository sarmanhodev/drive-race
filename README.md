🚛 Drive Race
Um jogo arcade de direção feito em Python e Pygame, inspirado nos clássicos de 8 bits.

Assuma o volante de um caminhão, desvie do trânsito, colete moedas e tente superar seu recorde. Quanto mais pontos você conquista, mais imprevisível a estrada fica!
🎮 Sobre o jogo
O Drive Race é um jogo de corrida e sobrevivência com visão de cima, gráficos em pixel art e dificuldade progressiva. A pontuação vem da coleta de moedas: ultrapassar veículos não rende pontos.
✨ Funcionalidades
- 🚛 Caminhão controlado pelo jogador.
- 🚗 Carros vermelhos que seguem em linha reta.
- 🚙 Carros azuis que mudam de faixa e sinalizam antes da manobra.
- 🏍️ Motos que inicialmente seguem reto e, nas fases mais avançadas, começam a trocar de faixa.
- 🕳️ Buracos na pista.
- 🪙 Moedas de diferentes valores, incluindo moedas especiais.
- 📈 Progressão de dificuldade por pontuação.
- 🌳🌃 Cenários em pixel art, incluindo estrada rural e cidade noturna.
- 🚦 Indicadores de direção em estilo 8 bits.
- 🏆 Sistema de recorde local.
- 🎨 Interface e velocímetro com estética retrô.
🕹️ Controles
Tecla	Ação
← / →	Mover o caminhão para os lados


🏁 Progressão
O jogo evolui em fases de 250 pontos. Alguns marcos importantes:
Pontuação	Novidade
0–249	Apenas carros vermelhos
250–499	Carros azuis começam a mudar de faixa
500–749	Motos aparecem, inicialmente seguindo reto
750–999	Entrada na cidade noturna e surgimento de buracos
1.000–1.249	Carros azuis mais frequentes
1.250+	Motos começam a mudar de faixa


A dificuldade continua aumentando conforme a partida avança.
🛠️ Tecnologias
- Python 3
- Pygame
🚀 Como executar
1. Clone o repositório
git clone https://github.com/sarmanhodev/drive-race.git
cd drive-race

2. Crie um ambiente virtual
Windows (PowerShell):
py -m venv .venv
.\.venv\Scripts\Activate.ps1
Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate
3. Instale as dependências
python -m pip install -r requirements.txt
4. Inicie o jogo
python main.py
📁 Estrutura do projeto
py_game/
├── assets/             # Imagens e outros recursos visuais
├── caminhao.py         # Caminhão do jogador
├── colisao.py          # Regras de colisão
├── cores.py            # Cores e paletas
├── dificuldade.py      # Progressão de dificuldade
├── interface.py        # Elementos visuais da interface
├── main.py             # Inicialização e loop principal
├── menu.py             # Menu do jogo
├── moedas.py           # Moedas e coleta
├── obstaculos.py       # Carros, motos e buracos
├── pista.py            # Pista e cenários
├── pontuacao.py        # Pontuação e recorde
├── recorde.json        # Recorde local
├── requirements.txt    # Dependências Python
├── velocidade.py       # Regras de velocidade
└── velocimetro.py      # Velocímetro
As pastas de ambiente virtual (env/, .venv/) e cache (__pycache__/) são locais e não devem ser versionadas.

🔮 Próximas ideias
- Novos cenários, como deserto, chuva e rodovia noturna.
- Transições mais elaboradas entre ambientes.
- Ajustes de equilíbrio da dificuldade.
- Distribuição de uma versão executável para Windows.

Desenvolvido com Python, Pygame e muita vontade de sobreviver aos motoqueiros! 🏍️💨