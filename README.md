# proec_joaoestima
## Introduction
Programa de acessibilidade/Libras para as páginas da Pró-Reitoria de Cultura e Extensão (PROEC) da Unicamp.

## Index
- [About](#about)
- [Usage](#usage)
- [Development](#development)
  - [Pre-Requisites](#pre-requisites)
  - [Development Environment](#development-environment)
  - [File Structure](#file-structure)
  - [Build](#build)  
  - [Deployment](#deployment)  
- [FAQ](#faq)
- [Credit/Acknowledgment](#creditacknowledgment)

## About
Este projeto tem como objetivo implementar um programa de acessibilidade para as páginas web da Pró-Reitoria de Cultura e Extensão (PROEC) da Unicamp, traduzindo o conteúdo das páginas para Libras (Língua Brasileira de Sinais).

## Usage
O algoritmo extrai e organiza dados das páginas web designadas, gerando um arquivo CSV contendo informações estruturadas sobre parágrafos e sentenças, além de adicionar tags de acessibilidade ao HTML das páginas.

### Passos para utilização:
1. **Configurar os caminhos dos arquivos:**
   - Defina os caminhos `urls_path`, `output_folder` e `template_path` no script conforme necessário.

2. **Executar o script:**
   - Execute o script para extrair conteúdo das URLs especificadas, organizá-lo e salvar em arquivos CSV no diretório de saída.

3. **Modificar o HTML:**
   - O script também modifica arquivos HTML para adicionar tags de acessibilidade, utilizando os dados extraídos e salvos nos arquivos CSV.

## Development

### Pré-requisitos
- **Python 3.x**: Linguagem de programação utilizada para desenvolver o script.
- **pandas**: Biblioteca utilizada para manipulação e análise de dados, especialmente para trabalhar com DataFrames.
- **requests**: Biblioteca para fazer requisições HTTP e obter o conteúdo das páginas web.
- **beautifulsoup4**: Biblioteca para análise de documentos HTML e extração de dados das páginas web.
- **re**: Módulo de expressões regulares para trabalhar com padrões de texto.

### Ambiente de Desenvolvimento
Certifique-se de ter um ambiente Python configurado com as bibliotecas necessárias instaladas.

### Estrutura dos arquivos
Estrutura de diretórios do projeto:
proec_joaoestima
│
├── .git
├── app
├── coletor_paragrafos
│ ├── parser.py
├── pagina_sobre_teste
└── README.md

## Build
Para construir e preparar o ambiente, siga os passos abaixo:

1. **Instalar Git:**
   - **Windows:**
     - Baixe o instalador do Git em: https://gitforwindows.org/
     - Execute o instalador e siga as instruções na tela.
   - **Linux:**
     - Ubuntu: `sudo apt-get install git`
     - Fedora: `sudo dnf install git`
     - Arch: `sudo pacman -S git`

2. **Clonar o repositório:**
	git clone https://github.com/joaoestima/proec_joaoestima.git

3. **Navegar até o diretório do projeto:**
	cd proec_joaoestima

4. **Instalar as dependências:**
	pip install -r requirements.txt
## Deployment
### Passos para utilização:
1. **Configurar os caminhos dos arquivos:**
   - Defina os caminhos `urls_path`, `output_folder` e `template_path` no script conforme necessário.

2. **Executar o script:**
   - Execute o script `parser.py` para extrair conteúdo das URLs especificadas, organizá-lo e salvar em arquivos CSV no diretório de saída.

3. **Modificar o HTML:**
   - O script também modifica arquivos HTML para adicionar tags de acessibilidade, utilizando os dados extraídos e salvos nos arquivos CSV.

1. Para implantar o projeto, siga os passos abaixo:

Certifique-se de que todas as dependências estão instaladas.
Configure os caminhos dos arquivos no script.
Execute o script principal parser.py.
### Passos para trabalhar em outra branch

	Para começar a trabalhar em um novo recurso, crie um novo branch prefixado com feat e seguido pelo nome do recurso (ex.: feat-FEATURE-NAME).
	Depois de concluir as alterações, faça um Pull Request (PR).
	Passos para criar um pull request

Faça um PR para o branch stage.
Siga as melhores práticas e diretrizes (ex.: se o PR se refere a elementos visuais, inclua uma imagem mostrando o efeito).
Certifique-se de que o PR passe por todas as verificações de integração contínua e obtenha avaliações positivas.
## FAQ
1. Como o programa está estruturado no parser.py?

	O arquivo parser.py é responsável por extrair, organizar e salvar os dados das páginas (URLs) designadas, preenchendo o DataFrame elaborado pelo Prof. José Martino.
	A maior parte dos sites não tem tanto conteúdo, toda a informação extraída foi contabilizada em 1380 linhas.
Onde os dados são salvos?

	Na pasta data, existem diferentes formatos de dados conforme o trabalho foi executado. Algumas restrições foram percebidas e cada versão tenta abarcar as sugestões e mudanças necessárias.
2. Onde os dados são salvos?
	Na pasta data, existem diferentes formatos de dados conforme o trabalho foi executado. Algumas restrições foram percebidas e cada versão tenta abarcar as sugestões e mudanças necessárias.

## Credit/Acknowledgment
João Pedro Estima Machado e Prof. Dr. José Mario Martino

================================================================================================================
As tarefas executadas ao longo do ano foram as seguintes:

1. Ler o conteúdo de página Web identificando parágrafos e sentenças.
2. Gerar arquivo no formato CSV para ser importado no Excel contendo as seguintes colunas:
   - URL da página Web e id numérico interno (Página);
   - ID do parágrafo (Parágrafo/Bloco);
   - ID da sentença (Sentença);
   - Texto em português da sentença (Português);
   - Nome do responsável pela transcrição do texto em português (Resp. Português);
   - Responsável pela revisão do texto (Rev. Português);
   - Tradução para representação por glosas da sentença (Glosas);
   - Responsável pela tradução (Resp. Glosas);
   - Link para o vídeo de referência da sinalização da tradução (Vídeo);
   - Responsável pelo vídeo (Resp. Vídeo);
   - Revisor da tradução (Rev. Tradução);
   - Data e nome do intérprete da gravação Mocap (Mocap);
   - Link para o arquivo de vídeo Mocap (Vídeo Mocap);
   - Link para o arquivo de anotação (Elan);
   - Nome do responsável pela anotação Elan (Resp. Elan);
   - Nome do responsável pela revisão da anotação Elan (Rev. Elan);
   - Link para o vídeo com a animação do avatar sinalizando a sentença.

3. Inserir na página Web o nome do arquivo do vídeo contendo a animação do avatar. Os vídeos recebem nome no formato: `web_uAAA_pXXX_sYYY_talita.vp9.webm`; onde AAA, XXX e YYY são números (exemplo: `web_u01_p001_s001_talita.vp9.webm`).

If it's open-source, talk about the community here, ask social media links and other links.

> If you are new to open-source, make sure to check read more about it [here](https://www.digitalocean.com/community/tutorial_series/an-introduction-to-open-source) and learn more about creating a pull request [here](https://www.digitalocean.com/community/tutorials/how-to-create-a-pull-request-on-github).
