# Scraper UNA-SUS - Cursos e Ofertas

Um scraper robusto e eficiente para coletar dados de cursos e ofertas da plataforma UNA-SUS (Universidade Aberta do SUS), com foco especial na identificação de conteúdos relacionados a DEIA (Diversidade, Equidade, Inclusão e Acessibilidade).

## 🚀 Funcionalidades

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

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Instalação das Dependências
```bash
pip install -r requirements.txt
```

## 📖 Como Usar

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
```

## 📈 Monitoramento

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

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

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

### Versão Atual
- **Clean Code**: Código refatorado seguindo boas práticas
- **Funções Modulares**: Separação clara de responsabilidades
- **Tratamento Robusto**: Melhor gestão de erros e exceções
- **Documentação Completa**: README atualizado com todas as funcionalidades

### Próximas Melhorias
- Interface web para monitoramento
- API REST para consulta dos dados
- Dashboard com visualizações
- Integração com bases de dados 