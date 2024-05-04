# proec_joaoestima
# Introduction
- programa de acessbilidade/libras para as páginas de pró-reitoria e extensão cultural da Unicamp

## Index

- [About](#about)
- [Usage](#usage)
- [Development](#development)
  - [Pre-Requisites](#pre-requisites)
  - [Developmen Environment](#development-environment)
  - [File Structure](#file-structure)
  - [Build](#build)  
  - [Deployment](#deployment)  
- [FAQ](#faq)
- [Credit/Acknowledgment](#creditacknowledgment)

### Development Environment


### File Structure

| No | File Name | Details 
|----|-------------------|---------||---------||-----------||-----------------||----------------||-------||----------------|
['URL', 'Parágrafo/Bloco', 'Index', 'Sentença', 'Português', 'Resp. Português','Rev. Português', 'Glosas', 'Resp. Glosas', 'Arquivo Vídeo','Resp. Vídeo', 'Rev. Tradução', 'Mocap', 'Vídeo Mocap','Elan', 'Resp.  Elan','Rev. Elan'])

### Build


### Deployment


**Steps to work with feature branch**
1. Para começar a trabalhar em um novo recurso, crie um novo branch prefixado com `feat` e seguido pelo nome do recurso. (ou seja, `feat-FEATURE-NAME`)
2. Depois de concluir as alterações, você pode aumentar o PR.
3. 
**Steps to create a pull request**

1. Faça um PR para o branch `stage`.
2. Cumpra as melhores práticas e diretrizes, por exemplo. quando o PR disser respeito a elementos visuais deverá ter uma imagem que mostre o efeito.
3. Deve passar por todas as verificações de integração contínua e obter avaliações positivas.

Depois disso, as alterações serão mescladas.



## FAQ
Como o programa está elaborado 'extractor_v6.py?
    - O arquivo 'extractor_v6.py' é responsável por extrair, organizar e salvar os dados das 
        páginas(URLs) designadas de forma a preencher o dataframe elaborado pelo Prof. José Martino
    - A maior parte dos sites não tem tanto conteúdo, toda a informação extraida tinha sido contabilizada 
        em 1380 linhas
Onde os dado ficam salvos?
    - Na pasta data, existem 4 diferentes formatos de dados, conforme o trabalho foi executado,
    algumas restrições foram percebidas e cada versão tenta abarcar as sugestões e mudanças necessárias.

## Credit/Acknowledgment
João Pedro Estima Machado e Prof. Dr. José Mario Martino

Próximos passos:
    - Extrair conteúdo de imagens das páginas
    - Implementar o talita_web_plugin
    - 
================================================================================================================
As tarefas executadas ao longo do ano foram as seguintes:

1. Ler o conteúdo de página Web identificando parágrafos e sentenças.
2. Gerar arquivo no formato csv para ser importado no Excel contendo as seguintes colunas:
a. URL da página Web e id numérico interno (Página);
b. 10 do parágrafo (Parágrafo/Bloco);
€. 1Dda sentença (Sentença);
d. Texto em português da sentença (Português);
e. Nome do responsável pela transcrição do texto em português para a planilha (Resp.
Português) (conteúdo: tweb — transcrição Web)
Responsável pela revisão do texto (Rev. Português)
Tradução para representação por glosas da sentença (Glosas);
Responsável pela tradução (Resp. Glosas);
Link para o vídeo de referência da sinalização da tradução (Vídeo);
Responsável pelo vídeo (Resp. Vídeo);
Revisor da Tradução (Ver. Tradução);
Data e nome do intérprete da gravação Mocap (Mocap)
. Link para arquivo vídeo Mocap-vue (Vídeo Mocap)
Link para o arquivo de anotação (Elan)
Nome do responsável pela anotação Elan (Resp. Elan)
Nome do responsável pela revisão da anotação ELAN (Rev. Elan)
Link para o vídeo com a animação do avatar sinalizando a sentença
3. Inserir na página Web o nome do arquivo do vídeo contendo o animação do avatar. Os vídeos
receberão nome segundo o formato: web UuAAA pXXX sYYY 277; onde AAA, XXX, YYY e 777 são
números (exemplo web u01 pO01 s2 1 (web indica que conteúdo foi extraído da WEB, uO1 indica
prim '| processada — manter uma tabela com a url e esse identificador numérico; por
página — página 1 ( será sempre 01??); s2 1 indica que é a sentença 1 do

If it's open-source, talk about the community here, ask social media links and other links.

 > If you are new to open-source, make sure to check read more about it [here](https://www.digitalocean.com/community/tutorial_series/an-introduction-to-open-source) and learn more about creating a pull request [here](https://www.digitalocean.com/community/tutorials/how-to-create-a-pull-request-on-github).
