# proec_joaoestima
programa de acessbilidade para as páginas de pró-reitoria e extensão cultural da Unicamp

Como o programa está elaborado 'extractor_v6.py?
    - O arquivo 'extractor_v6.py' é responsável por extrair, organizar e salvar os dados das 
        páginas(URLs) designadas de forma a preencher o dataframe elaborado pelo Prof. José Martino
    - A maior parte dos sites não tem tanto conteúdo, toda a informação extraida tinha sido contabilizada 
        em 1380 linhas
Onde os dado ficam salvos?
    - Na pasta data, existem 4 diferentes formatos de dados, conforme o trabalho foi executado,
    algumas restrições foram percebidas e cada versão tenta abarcar as sugestões e mudanças necessárias.


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
