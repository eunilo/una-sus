<<<<<<< HEAD
# Scraper UNA-SUS - Coleta de Dados de Cursos e Ofertas

Um scraper robusto e eficiente para coletar dados detalhados de cursos e ofertas da Universidade Aberta do SUS (UNA-SUS), incluindo informações sobre vagas, público-alvo, formato, e análise de descritores DEIA.

## 🚀 Funcionalidades Principais

### ✅ **Extração Completa de Dados**
- **Cursos**: Informações básicas, descrições, carga horária, órgãos responsáveis
- **Ofertas**: Dados detalhados de cada oferta de curso
- **Vagas**: Número de vagas disponíveis (extraído via API REST)
- **Público-alvo**: Perfil dos participantes
- **Formato**: Modalidade de ensino (EAD, presencial, etc.)
- **Programas de governo**: Iniciativas associadas
- **Temas e DeCs**: Classificações temáticas
- **Palavras-chave**: Termos de indexação
=======
# Scraper UNA-SUS - Cursos e Ofertas

Um scraper robusto e eficiente para coletar dados de cursos e ofertas da plataforma UNA-SUS (Universidade Aberta do SUS), com foco especial na identificação de conteúdos relacionados a DEIA (Diversidade, Equidade, Inclusão e Acessibilidade).
>>>>>>> a2555d3 (feat: implementação completa com clean code e melhorias robustas)

### ✅ **Análise DEIA (Diversidade, Equidade, Inclusão e Acessibilidade)**
- Detecção automática de descritores DEIA nos cursos
- Análise de título e descrição para identificar iniciativas inclusivas
- Mapeamento de cursos com foco em diversidade e equidade

<<<<<<< HEAD
### ✅ **Extração Inteligente de Ofertas**
- **Ofertas ativas**: Busca automática de ofertas em andamento
- **Ofertas encerradas**: Detecção e extração de ofertas finalizadas
- **API REST**: Uso de API oficial para dados precisos
- **Fallback HTML**: Extração alternativa via parsing de páginas

### ✅ **Sistema Robusto de Coleta**
- **Salvamento incremental**: Dados salvos a cada lote processado
- **Checkpoint automático**: Retoma de onde parou em caso de interrupção
- **Logs detalhados**: Monitoramento em tempo real do progresso
- **Tratamento de erros**: Recuperação automática de falhas

## 📊 Dados Coletados

### Colunas do Dataset Final

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| `co_seq_curso` | ID único do curso | `44538` |
| `no_curso` | Nome do curso | `"1º Formação de Preceptores para o SUS"` |
| `qt_carga_horaria_total` | Carga horária total | `195` |
| `co_seq_orgao` | ID do órgão responsável | `13` |
| `sg_orgao` | Sigla do órgão | `"UNIFESP"` |
| `no_orgao` | Nome completo do órgão | `"Universidade Federal de São Paulo"` |
| `no_formato` | Formato do curso | `"Ensino a Distância"` |
| `no_nivel` | Nível educacional | `"Extensão"` |
| `no_modalidade` | Modalidade | `"Aperfeiçoamento"` |
| `ds_imagem` | URL da imagem do curso | `"https://..."` |
| `status` | Status atual | `"Oferta encerrada"` |
| `status_ordem` | Ordem do status | `3` |
| `tem_deia` | Possui descritores DEIA | `"Sim"` / `"Não"` |
| `deia_encontrado` | Descritor DEIA específico | `"Diversidade, Equidade e Inclusão"` |
| `id_oferta` | ID único da oferta | `416264` |
| `codigo_oferta` | Código da oferta | `416264` |
| **`vagas`** | **Número de vagas disponíveis** | **`195`** |
| `publico_alvo` | Público-alvo da oferta | `"Profissionais da saúde..."` |
| `local_oferta` | Local da oferta | `"EAD"` |
| `formato` | Formato da oferta | `"Ensino a Distância"` |
| `programas_governo` | Programas de governo associados | `"UNA-SUS, Especialização"` |
| `temas` | Temas abordados | `"Saúde Pública"` |
| `decs` | Classificação DeCs | `"Medicina"` |
| `descricao_oferta` | Descrição detalhada da oferta | `"1ª Oferta - Formação..."` |
| `palavras_chave` | Palavras-chave da oferta | `"Formação de Preceptores"` |
| `url_oferta` | URL da página da oferta | `"https://..."` |
| `erro` | Erro durante coleta (se houver) | `"Sem ofertas encontradas"` |
=======
### ✨ Principais Recursos
- **Scraping Inteligente**: Coleta dados de cursos e ofertas da UNA-SUS
- **Análise DEIA**: Identifica automaticamente conteúdos relacionados a Diversidade, Equidade, Inclusão e Acessibilidade
- **Processamento Incremental**: Salva dados progressivamente para evitar perda de informações
- **Sistema de Checkpoint**: Permite retomar o scraping de onde parou
- **Logging Detalhado**: Acompanhamento completo do progresso
- **Validação de Dados**: Verifica integridade e qualidade dos dados coletados
- **Extração de Descrições**: Busca descrições completas em páginas individuais dos cursos
- **Busca por Ofertas Encerradas**: Inclui ofertas que podem estar ocultas

### 🔧 Ferramentas Auxiliares
- **Monitor em Tempo Real**: Acompanhe o progresso do scraper
- **Validador de Dados**: Analise e limpe os dados coletados
- **Teste de Paginação**: Debug da API da UNA-SUS

## 📊 Dados Coletados

### Informações dos Cursos
- **Identificação**: `co_seq_curso`, `id_curso`, `co_curso`
- **Dados Básicos**: `no_curso` (nome), `qt_carga_horaria_total`
- **Organização**: `co_seq_orgao`, `sg_orgao`, `no_orgao`
- **Características**: `no_formato`, `no_nivel`, `no_modalidade`
- **Mídia**: `ds_imagem`
- **Status**: `status`, `status_ordem`
- **Descrição**: `ds_curso` (extraída da página do curso quando necessário)
- **Qualidade**: `curso_incompleto` (marca cursos sem descrição)

### Informações das Ofertas
- **Identificação**: `id_oferta`, `codigo_oferta`
- **Detalhes**: `vagas`, `publico_alvo`, `local_oferta`
- **Formato**: `formato`
- **Programas**: `programas_governo`
- **Classificação**: `temas`, `decs`, `palavras_chave`
- **Descrição**: `descricao_oferta`

### Análise DEIA
- **Indicador**: `tem_deia` (Sim/Não)
- **Descritor**: `deia_encontrado` (descritor específico encontrado)

### Campos de Controle
- **URL**: `url_oferta`
- **Erros**: `erro` (quando aplicável)

## 🎯 Descritores DEIA

O sistema identifica automaticamente conteúdos relacionados a:
- Diversidade, Equidade e Integração
- Diversidade, Equidade, Inclusão e Pertencimento
- Diversidade, Equidade, Inclusão, Acessibilidade
- Diversidade, Equidade, Inclusão, Pertencimento
- Diversidade, Igualdade e Inclusão
- Diversidade, Igualdade, Inclusão e Acessibilidade
- Diversidade, Igualdade, Inclusão, Pertencimento
- Equidade, Diversidade e Inclusão
- Inclusão, Diversidade, Equidade e Acessibilidade
- Inclusão, Diversidade, Equidade, Acessibilidade
>>>>>>> a2555d3 (feat: implementação completa com clean code e melhorias robustas)

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Instalação das Dependências
```bash
pip install -r requirements.txt
```

## 🚀 Como Usar

<<<<<<< HEAD
### Execução Básica
```bash
python scraper_unasus.py
```

### Monitoramento em Tempo Real
O scraper exibe logs detalhados durante a execução:
```
Cursos já processados: 19
Arquivo de saída: unasus_ofertas_detalhadas.csv
Buscando ofertas do curso 44566...
  ✅ Oferta encontrada: 416699
  ✅ Oferta encontrada: 416329
  📋 Encontrados 2 links de ofertas encerradas
  ✅ Total de ofertas únicas encontradas: 2
  🔍 Extraindo dados da oferta 416699...
    ✅ Dados obtidos via API REST
    ✅ Vagas extraídas: 10000
```

### Verificação dos Resultados
```bash
python verificar_vagas.py
```

## 📈 Funcionalidades Avançadas

### 🔍 **Extração de Ofertas Encerradas**
O scraper automaticamente:
- Detecta links para ofertas encerradas
- Acessa páginas específicas de ofertas finalizadas
- Extrai dados completos mesmo de ofertas não ativas

### 🎯 **API REST para Dados Precisos**
- Utiliza a API oficial da UNA-SUS (`/rest/oferta/{id}`)
- Extrai dados estruturados em JSON
- Fallback para parsing HTML em caso de falha da API
- Headers otimizados para simular navegador real

### 📊 **Análise DEIA Automática**
Detecta automaticamente descritores como:
- "Diversidade, Equidade e Integração"
- "Diversidade, Equidade, Inclusão e Pertencimento"
- "Inclusão, Diversidade, Equidade e Acessibilidade"
- E outros 7 descritores relacionados

### 💾 **Sistema de Checkpoint**
- Salva progresso a cada 10 cursos processados
- Retoma automaticamente de onde parou
- Evita reprocessamento de dados já coletados

## 📁 Estrutura do Projeto

```
una-sus/
├── scraper_unasus.py                # Scraper principal
├── requirements.txt                 # Dependências
├── README.md                        # Documentação
├── .gitignore                       # Arquivos ignorados
└── unasus_ofertas_detalhadas.csv    # Dataset gerado
```

## 🔧 Configurações

### Variáveis Principais
```python
# Configurações de coleta
lote = 10                    # Salva a cada 10 cursos
timeout = 30                 # Timeout das requisições
delay = 1                    # Delay entre requisições

# Headers para API REST
api_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": url_oferta
}
=======
### 1. Scraper Principal
```bash
python scraper_unasus_incremental.py
```

**Características:**
- Processamento incremental (salva a cada 10 registros)
- Sistema de checkpoint automático
- Logging detalhado em `logs/scraper_YYYYMMDD_HHMMSS.log`
- Arquivo de saída: `unasus_ofertas_detalhadas.csv`

### 2. Monitor em Tempo Real
```bash
python monitor_scraper.py
```

**Funcionalidades:**
- Status atual do scraper
- Estatísticas do arquivo CSV
- Últimas entradas do log
- Informações do checkpoint

### 3. Validador de Dados
```bash
python validar_dados.py
```

**Análises:**
- Estrutura dos dados
- Validação de cursos e ofertas
- Estatísticas DEIA
- Remoção de duplicatas
- Limpeza de registros vazios
- Análise de cursos incompletos

### 4. Teste de Paginação
```bash
python teste_paginacao.py
```

**Debug:**
- Testa diferentes tokens de paginação
- Compara resultados entre páginas
- Identifica problemas de paginação

## 📁 Estrutura do Projeto

```
unsa-sus/
├── scraper_unasus_incremental.py  # Scraper principal
├── monitor_scraper.py             # Monitor em tempo real
├── validar_dados.py               # Validador de dados
├── teste_paginacao.py             # Teste de paginação
├── requirements.txt               # Dependências Python
├── README.md                      # Documentação
├── LICENSE                        # Licença MIT
├── setup.py                       # Configuração do pacote
├── pyproject.toml                 # Configuração moderna
├── .gitignore                     # Arquivos ignorados pelo Git
├── logs/                          # Logs do scraper
├── .github/workflows/             # CI/CD GitHub Actions
├── .vscode/                       # Configurações VS Code
├── Dockerfile                     # Containerização
├── docker-compose.yml             # Orquestração Docker
└── .dockerignore                  # Arquivos ignorados no Docker
```

## 🔧 Configurações

### Variáveis de Ambiente (Opcional)
```bash
# Configurações de logging
LOG_LEVEL=INFO
LOG_DIR=logs

# Configurações do scraper
BATCH_SIZE=10
REQUEST_TIMEOUT=30
RETRY_DELAY=30
```

### Arquivos de Configuração
- **checkpoint.json**: Progresso do scraper
- **unasus_ofertas_detalhadas.csv**: Dados coletados
- **logs/**: Arquivos de log com timestamp

## 🚀 Execução com Docker

### Usando Docker Compose
```bash
docker-compose up scraper
```

### Usando Docker diretamente
```bash
docker build -t unasus-scraper .
docker run -v $(pwd):/app unasus-scraper
>>>>>>> a2555d3 (feat: implementação completa com clean code e melhorias robustas)
```

## 📊 Exemplo de Saída

<<<<<<< HEAD
```csv
co_seq_curso,no_curso,qt_carga_horaria_total,vagas,publico_alvo,local_oferta,formato,programas_governo
44538,"1º Formação de Preceptores para o SUS",195,195,"Profissionais da saúde...",EAD,"Ensino a Distância","UNA-SUS, Especialização"
44540,"2º Formação de Preceptores para o SUS",195,195,"Profissionais da saúde...",EAD,"Ensino a Distância","UNA-SUS, Especialização"
```

## 🚨 Tratamento de Erros

O scraper inclui tratamento robusto de erros:
- **Timeout de conexão**: Retry automático após 30 segundos
- **Falha na API**: Fallback para parsing HTML
- **Dados ausentes**: Campos preenchidos com string vazia
- **Ofertas sem vagas**: Log de aviso mantido

## 📈 Estatísticas de Coleta

### Métricas Finais (Execução Completa)
- **Cursos processados**: 552 cursos únicos (99.6% dos 554 disponíveis)
- **Ofertas encontradas**: 1,656 ofertas
- **Taxa de sucesso vagas**: 100% (1,656/1,656)
- **Tempo de execução**: ~2 horas
- **Arquivo final**: 1.28 MB com dados completos

### Logs de Progresso
```
Página 1 processada.
Página 2 processada.
...
Progresso salvo após 20 cursos em unasus_ofertas_detalhadas.csv
```
=======
### Logs
- **Arquivo**: `logs/scraper_YYYYMMDD_HHMMSS.log`
- **Níveis**: INFO, WARNING, ERROR, DEBUG
- **Formato**: Timestamp - Nível - Mensagem

### Checkpoint
- **Arquivo**: `checkpoint.json`
- **Dados**: Página atual, cursos processados, ofertas processadas, último token

### Estatísticas
- Total de cursos processados
- Total de ofertas encontradas
- Cursos com/sem DEIA
- Cursos incompletos (sem descrição)

## 🔍 Exemplo de Dados

```csv
co_seq_curso,no_curso,qt_carga_horaria_total,ds_curso,tem_deia,deia_encontrado,id_oferta,vagas,publico_alvo,curso_incompleto
12345,Curso de Atenção à Diversidade,60,"Curso focado em atenção à diversidade...",Sim,"Diversidade, Equidade e Inclusão",67890,100,"Profissionais de saúde",Não
```

## 🛡️ Tratamento de Erros

### Recuperação Automática
- **Timeout de requisições**: 30 segundos
- **Retry automático**: 30 segundos de espera
- **Checkpoint**: Salva progresso a cada lote
- **Validação**: Verifica dados antes de salvar

### Logs de Erro
- **Erros de conexão**: Registrados com retry automático
- **Dados inválidos**: Marcados como "erro" no CSV
- **Cursos sem ofertas**: Registrados com flag específico
>>>>>>> a2555d3 (feat: implementação completa com clean code e melhorias robustas)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

<<<<<<< HEAD
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- UNA-SUS pela disponibilização dos dados
- Comunidade Python pelos recursos utilizados
- Contribuidores do projeto
=======
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

### Problemas Comuns
1. **Erro de paginação**: Use `teste_paginacao.py` para debug
2. **Dados incompletos**: Execute `validar_dados.py` para análise
3. **Scraper travado**: Verifique logs e checkpoint

### Logs Importantes
- **"Nenhum item encontrado"**: Fim dos dados
- **"Curso sem descrição"**: Curso marcado como incompleto
- **"Sem ofertas encontradas"**: Curso sem ofertas ativas/encerradas

## 🔄 Atualizações
>>>>>>> a2555d3 (feat: implementação completa com clean code e melhorias robustas)

### Versão Atual
- **Clean Code**: Código refatorado seguindo boas práticas
- **Funções Modulares**: Separação clara de responsabilidades
- **Tratamento Robusto**: Melhor gestão de erros e exceções
- **Documentação Completa**: README atualizado com todas as funcionalidades

<<<<<<< HEAD
**Desenvolvido com ❤️ para facilitar a análise de dados educacionais em saúde pública.** 
=======
### Próximas Melhorias
- Interface web para monitoramento
- API REST para consulta dos dados
- Dashboard com visualizações
- Integração com bases de dados 
>>>>>>> a2555d3 (feat: implementação completa com clean code e melhorias robustas)
