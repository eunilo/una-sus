# RELATO DA CONSTRUÇÃO DO SISTEMA UNA-SUS

---

## 1 INTRODUÇÃO E OBJETIVOS

Este documento descreve, em registro acadêmico, o processo de construção do sistema
de coleta e análise de dados educacionais da UNA-SUS, desde a concepção até o
estágio atual de desenvolvimento. O propósito é explicitar o percurso metodológico,
as decisões técnicas e as adaptações realizadas, assegurando rastreabilidade e
reprodutibilidade, elementos essenciais à pesquisa de mestrado.

O sistema foi concebido para consolidar dados públicos de ofertas educacionais,
programas e instituições, transformando-os em bases estruturadas e relatórios
analíticos. Para tal, adotaram-se princípios de modularidade, transparência e
preservação da integridade dos dados.

---

## 2 CONCEPÇÃO INICIAL E PLANEJAMENTO METODOLÓGICO

O ponto de partida consistiu no levantamento das necessidades centrais da pesquisa,
que podem ser sintetizadas em quatro eixos: (i) coleta automatizada e completa de
dados, (ii) preservação do conteúdo original, (iii) estruturação adequada para
análises quantitativas e qualitativas e (iv) produção de relatórios destinados a
diferentes públicos, mantendo a consistência metodológica.

Essa etapa orientou a escolha por uma arquitetura em camadas (coleta, armazenamento,
análise e geração de relatórios), permitindo desenvolvimento incremental, validação
por módulo e possibilidade de extensão para novos descritores.

---

## 3 IMPLEMENTAÇÃO DA COLETA DE DADOS

A implementação inicial concentrou-se no coletor principal, responsável por acessar
a API da UNA-SUS e obter o conjunto completo de ofertas disponíveis, sem filtros.
O coletor foi desenvolvido com foco em confiabilidade e consistência, incorporando:

1) Requisições HTTP com tratamento de falhas;
2) Persistência em formatos CSV, JSON e SQLite;
3) Checkpoints para recuperação de execução;
4) Registro fiel dos campos originais.

Diante de instabilidades da API, foi incorporada lógica de retentativas, de modo a
reduzir perdas de dados e aumentar a resiliência do processo de coleta.

---

## 4 ESTRUTURAÇÃO DOS DADOS E ARMAZENAMENTO

Com a coleta operante, o sistema passou a garantir padronização de diretórios,
versionamento de resultados e integridade dos dados. Definiram-se diretórios
estruturantes (`data`, `logs`, `checkpoints`) e fluxos de exportação com metadados.
O armazenamento em SQLite permitiu consultas mais eficientes para análise posterior.

Essa organização foi decisiva para evitar falhas relacionadas à ausência de arquivos
ou inconsistências de caminhos, especialmente em ambientes heterogêneos.

---

## 5 MÓDULOS DE ANÁLISE E INTEGRAÇÃO

A etapa seguinte consistiu na implementação de módulos analíticos especializados,
coordenados por um analisador geral. Os principais módulos incluem:

1) Mapeamento de programas de governo;
2) Cobertura programática dos cursos;
3) Distribuição geográfica das ofertas;
4) Relatórios visuais e executivos.

Cada módulo foi mantido independente, assegurando evolução incremental sem impacto
em outras partes do sistema.

---

## 6 PRODUÇÃO DE RELATÓRIOS E COMUNICAÇÃO CIENTÍFICA

Para garantir a comunicação dos resultados, o sistema passou a gerar relatórios em
níveis distintos de detalhamento, adequados a leitores técnicos e executivos. Foram
produzidos relatórios completos, resumos executivos e versões visuais (ASCII).

Por demanda metodológica, foi incorporada seção específica para cursos sem cobertura
programática, posicionada antes da análise completa. Adicionalmente, implementou-se
um relatório geográfico completo com detalhamento por estado, permitindo comparações
regionais e análises de concentração de ofertas.

---

## 7 ROBUSTEZ, PORTABILIDADE E USO POR TERCEIROS

Durante o processo, ocorreram falhas típicas de ambiente, sobretudo em Windows, como
problemas de encoding e instalação de dependências. Para assegurar a execução por
qualquer usuário, foram implementadas medidas estruturantes:

1) Saída em UTF-8 no Windows para evitar erros de caracteres especiais;
2) Detecção de ambiente virtual (venv) e reexecução automática;
3) Instalação automática de dependências ausentes;
4) Diagnóstico integrado com verificação de dados e diretórios básicos.

Além disso, foram adicionados itens de menu para diagnóstico, limpeza de relatórios e
pesquisa transversal no banco de dados, com filtros, a fim de viabilizar ciclos de
análise repetíveis e ampliar a exploração temática.

---

## 8 INTEGRAÇÃO COM O FLUXO DA PESQUISA

O sistema foi continuamente ajustado a partir das necessidades empíricas da pesquisa.
Esses ajustes incluíram modificações de relatórios, correções em processos de coleta
e ampliação da documentação técnica. Em paralelo, foram produzidos documentos de
arquitetura, proposta modular e documentação de dissertação, reforçando o rigor e a
transparência metodológica.

---

## 9 ESTADO ATUAL E CAPACIDADE OPERACIONAL

Atualmente, o sistema é capaz de:

1) Executar varredura completa com limpeza e checkpoints;
2) Realizar análises consolidadas a partir dos dados coletados;
3) Gerar relatórios técnicos, executivos e visuais;
4) Produzir relatórios completos de cobertura programática e distribuição geográfica;
5) Efetuar diagnóstico automatizado e instalação de dependências;
6) Limpar relatórios por menu ou script dedicado;
7) Pesquisar termos no banco em qualquer coluna, com filtros adicionais.

Esse conjunto de funcionalidades evidencia a maturidade do sistema, que evoluiu de
uma coleta básica para uma plataforma modular e documentada, adequada ao contexto
da pesquisa de mestrado.

---

## 10 CONSIDERAÇÕES FINAIS

O processo de construção foi iterativo, demandando ciclos de validação e ajustes
metodológicos. A convergência entre engenharia de software e pesquisa aplicada
resultou em uma solução robusta, documentada e alinhada às exigências acadêmicas.

O sistema, em sua forma atual, fornece base sólida para análises e para a
reprodutibilidade do estudo, permitindo que outros pesquisadores compreendam o
processo, reproduzam os resultados e ampliem o escopo das investigações.

---

Documento acadêmico incorporado ao repositório da pesquisa de mestrado.
