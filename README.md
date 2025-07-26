# 🏥 Scraper UNA-SUS - Coleta Inteligente de Dados Educacionais

> **📚 Projeto Educacional para Pesquisa em Saúde Pública**  
> Um sistema inteligente e didático para coletar e analisar dados de cursos da Universidade Aberta do SUS (UNA-SUS), com foco especial em **Diversidade, Equidade, Inclusão e Acessibilidade (DEIA)**.

## 🎯 Sobre Este Projeto

### 💡 **O que é?**
Este é um **scraper** (coletor automático de dados) que extrai informações detalhadas de cursos da plataforma UNA-SUS. Ele foi desenvolvido para facilitar pesquisas acadêmicas e análises sobre educação em saúde pública.

### 🎓 **Para quem é?**
- **Pesquisadores** em saúde pública e educação
- **Estudantes** de graduação e pós-graduação
- **Desenvolvedores** interessados em web scraping
- **Analistas de dados** em saúde
- **Qualquer pessoa** interessada em dados educacionais

### 🚀 **Por que usar?**
- ✅ **Automatiza** a coleta de dados que seria manual
- ✅ **Identifica** cursos com foco em DEIA automaticamente
- ✅ **Organiza** dados em formato estruturado (CSV)
- ✅ **Facilita** análises estatísticas e qualitativas
- ✅ **Economiza tempo** para pesquisas acadêmicas

---

## 🏗️ Como o Código Funciona (Arquitetura Detalhada)

### 🧠 **Visão Geral da Arquitetura**

O sistema é composto por **módulos especializados** que trabalham em conjunto para coletar, processar e analisar dados:

```
🌐 UNA-SUS Website
    ↓
🔍 Scraper Principal (scraper_unasus_melhorado.py)
    ↓
📊 Processadores Especializados
    ↓
💾 Sistema de Persistência
    ↓
📈 Análise DEIA
    ↓
📁 Arquivo CSV Final
```

### 🔧 **Componentes Principais**

#### 1️⃣ **Módulo de Conexão e Autenticação**
```python
# 🌐 Configurações de rede
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

COOKIES = {
    "JSESSIONID": "sessão_ativa",
    "BIGipServer": "balanceamento_de_carga"
}

# 📋 Payload para requisições POST
PAYLOAD_INICIAL = {
    "draw": "1",
    "columns[0][data]": "0",
    "columns[0][name]": "",
    "columns[0][searchable]": "true",
    "columns[0][orderable]": "true",
    "start": "0",
    "length": "10",
    "search[value]": "",
    "search[regex]": "false"
}
```

**🎯 Função**: Estabelece conexão segura com o servidor UNA-SUS, simulando um navegador real.

#### 2️⃣ **Módulo de Paginação Inteligente**
```python
def processar_pagina(pagina, logger):
    """
    📄 Processa uma página de resultados da UNA-SUS
    
    🔄 Fluxo:
    1. Faz requisição POST com parâmetros de paginação
    2. Extrai dados JSON da resposta
    3. Processa cada curso encontrado
    4. Retorna dados estruturados
    """
    # 📊 Parâmetros de paginação
    payload = PAYLOAD_INICIAL.copy()
    payload["start"] = str(pagina * 10)
    
    # 🌐 Requisição HTTP
    response = requests.post(URL, data=payload, headers=HEADERS, cookies=COOKIES)
    
    # 📋 Extração de dados JSON
    dados = response.json()
    cursos = dados.get("data", [])
    
    return cursos
```

**🎯 Função**: Navega pelas páginas de resultados, extraindo dados de forma sistemática.

#### 3️⃣ **Módulo de Extração de Dados de Cursos**
```python
def extrair_dados_curso(curso, logger):
    """
    🎓 Extrai dados completos de um curso individual
    
    📊 Campos extraídos:
    - Informações básicas (ID, nome, carga horária)
    - Dados organizacionais (órgão responsável)
    - Características (formato, nível, modalidade)
    - Descrição completa e palavras-chave
    - Análise DEIA inicial
    """
    # 🆔 Dados básicos
    co_seq_curso = curso[0]
    no_curso = curso[1]
    qt_carga_horaria_total = curso[2]
    
    # 🏢 Dados organizacionais
    co_seq_orgao = curso[3]
    sg_orgao = curso[4]
    no_orgao = curso[5]
    
    # 📝 Descrição completa (nova funcionalidade)
    ds_curso = extrair_descricao_curso(co_seq_curso, logger)
    
    # 🌈 Análise DEIA inicial
    tem_deia, deia_encontrado = analisar_deia_inicial(no_curso, ds_curso)
    
    return {
        "co_seq_curso": co_seq_curso,
        "no_curso": no_curso,
        "ds_curso": ds_curso,
        "tem_deia": tem_deia,
        "deia_encontrado": deia_encontrado,
        # ... outros campos
    }
```

**🎯 Função**: Extrai e estrutura todos os dados de um curso individual.

#### 4️⃣ **Módulo de Extração de Descrição Completa**
```python
def extrair_descricao_curso(id_curso, logger):
    """
    📄 Extrai descrição completa da página individual do curso
    
    🔍 Estratégias de extração:
    1. Busca por seletores CSS específicos
    2. Fallback para busca por texto
    3. Limpeza e formatação do conteúdo
    """
    url_curso = f"https://unasus.gov.br/cursos/{id_curso}"
    
    try:
        # 🌐 Requisição à página do curso
        response = requests.get(url_curso, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 🔍 Busca por descrição
        descricao = None
        
        # Estratégia 1: Seletor CSS específico
        desc_element = soup.select_one('.curso-descricao, .descricao-curso, .content-description')
        if desc_element:
            descricao = desc_element.get_text(strip=True)
        
        # Estratégia 2: Busca por texto
        if not descricao:
            for element in soup.find_all(['p', 'div']):
                text = element.get_text(strip=True)
                if len(text) > 100 and 'curso' in text.lower():
                    descricao = text
                    break
        
        return descricao or ""
        
    except Exception as e:
        logger.warning(f"❌ Erro ao extrair descrição do curso {id_curso}: {e}")
        return ""
```

**🎯 Função**: Acessa páginas individuais dos cursos para extrair descrições completas.

#### 5️⃣ **Módulo de Busca de Ofertas**
```python
def extrair_ofertas_do_curso(id_curso, logger):
    """
    🎯 Extrai todas as ofertas de um curso (ativas e encerradas)
    
    🔍 Estratégias:
    1. Busca ofertas ativas na página principal
    2. Identifica links para ofertas encerradas
    3. Extrai dados de cada oferta individual
    """
    url_curso = f"https://unasus.gov.br/cursos/{id_curso}"
    
    try:
        response = requests.get(url_curso, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        ofertas_encontradas = []
        
        # 🔍 Busca ofertas ativas
        links_ofertas = soup.find_all('a', href=re.compile(r'/oferta/\d+'))
        for link in links_ofertas:
            id_oferta = re.search(r'/oferta/(\d+)', link['href']).group(1)
            ofertas_encontradas.append(id_oferta)
        
        # 📋 Busca ofertas encerradas
        ofertas_encerradas = buscar_ofertas_encerradas(soup, url_curso, logger)
        ofertas_encontradas.extend(ofertas_encerradas)
        
        return list(set(ofertas_encontradas))  # Remove duplicatas
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar ofertas do curso {id_curso}: {e}")
        return []
```

**🎯 Função**: Identifica e coleta todas as ofertas disponíveis para um curso.

#### 6️⃣ **Módulo de Extração de Dados de Ofertas**
```python
def extrair_dados_oferta(id_oferta, logger):
    """
    📊 Extrai dados detalhados de uma oferta específica
    
    🎯 Estratégia híbrida:
    1. Tenta API REST primeiro (mais rápido e preciso)
    2. Fallback para parsing HTML se API falhar
    3. Extração robusta de todos os campos
    """
    url_oferta = f"https://unasus.gov.br/oferta/{id_oferta}"
    url_api = f"https://unasus.gov.br/cursos/rest/oferta/{id_oferta}"
    
    dados_oferta = {}
    
    # 🚀 Tentativa 1: API REST
    try:
        api_headers = HEADERS.copy()
        api_headers.update({
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": url_oferta
        })
        
        response = requests.get(url_api, headers=api_headers, timeout=30)
        if response.status_code == 200:
            dados_json = response.json()
            
            # 📊 Extração de dados da API
            dados_oferta = {
                "vagas": dados_json.get("vagas", ""),
                "publico_alvo": dados_json.get("publico_alvo", ""),
                "local_oferta": dados_json.get("local_oferta", ""),
                "formato": dados_json.get("formato", ""),
                "programas_governo": dados_json.get("programas_governo", ""),
                "temas": dados_json.get("temas", ""),
                "decs": dados_json.get("decs", ""),
                "descricao_oferta": dados_json.get("descricao_oferta", ""),
                "palavras_chave": dados_json.get("palavras_chave", "")
            }
            
            logger.info("    ✅ Dados obtidos via API REST")
            return dados_oferta
            
    except Exception as e:
        logger.warning(f"    ⚠️ API falhou, tentando HTML: {e}")
    
    # 🌐 Tentativa 2: Parsing HTML
    try:
        response = requests.get(url_oferta, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 🔍 Extração via HTML
        dados_oferta = extrair_dados_html_oferta(soup, logger)
        logger.info("    ✅ Dados obtidos via HTML")
        
    except Exception as e:
        logger.error(f"    ❌ Erro na extração HTML: {e}")
    
    return dados_oferta
```

**🎯 Função**: Extrai dados detalhados de ofertas usando API REST e fallback HTML.

#### 7️⃣ **Módulo de Análise DEIA Avançada**
```python
def encontrar_descritor_deia_melhorado(texto_completo):
    """
    🌈 Análise avançada de conteúdo DEIA
    
    🧠 Lógica:
    1. Combina todos os campos relevantes
    2. Busca por 150+ descritores diferentes
    3. Retorna o descritor mais específico encontrado
    4. Prioriza descritores mais longos (mais específicos)
    """
    # 🌈 Lista expandida de descritores DEIA (150+ termos)
    DESCRITORES_DEIA = [
        # 👥 Populações específicas
        "Saúde da População Negra",
        "Saúde da População Indígena",
        "População LGBTQI+",
        "População Trans",
        "População em Situação de Rua",
        
        # 🏥 Saúde específica
        "Saúde Mental",
        "Saúde da Mulher",
        "Saúde da Criança",
        "Saúde do Idoso",
        
        # 🌍 Conceitos DEIA
        "Diversidade, Equidade e Inclusão",
        "Diversidade, Equidade, Inclusão e Acessibilidade",
        "Inclusão, Diversidade, Equidade",
        
        # 🎓 Educação inclusiva
        "Educação Inclusiva",
        "Educação Popular",
        "Formação Continuada",
        
        # ... 150+ descritores
    ]
    
    # 🔍 Busca pelo descritor mais específico
    descritor_encontrado = None
    for descritor in sorted(DESCRITORES_DEIA, key=len, reverse=True):
        if descritor.lower() in texto_completo.lower():
            descritor_encontrado = descritor
            break
    
    return descritor_encontrado
```

**🎯 Função**: Analisa texto completo em busca de conteúdo relacionado a DEIA.

#### 8️⃣ **Módulo de Sistema de Checkpoint**
```python
def salvar_checkpoint(pagina_atual, cursos_processados, logger):
    """
    💾 Sistema de checkpoint para recuperação automática
    
    📊 Salva:
    - Página atual sendo processada
    - Número de cursos processados
    - Timestamp da última execução
    - Dados parciais coletados
    """
    checkpoint = {
        "pagina_atual": pagina_atual,
        "cursos_processados": cursos_processados,
        "timestamp": datetime.now().isoformat(),
        "status": "em_andamento"
    }
    
    with open("checkpoint.json", "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)
    
    logger.info(f"💾 Progresso salvo: {cursos_processados} cursos processados")

def carregar_checkpoint():
    """
    🔄 Carrega checkpoint para retomar execução
    """
    try:
        with open("checkpoint.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"pagina_atual": 0, "cursos_processados": 0}
```

**🎯 Função**: Permite retomar a execução de onde parou em caso de interrupção.

### 🔄 **Fluxo de Execução Detalhado**

#### 📋 **Fase 1: Inicialização**
```python
def main():
    """
    🚀 Função principal - orquestra todo o processo
    """
    # 🔧 Configuração inicial
    logger = setup_logging()
    logger.info("🚀 Iniciando scraper UNA-SUS melhorado")
    
    # 🔄 Carrega checkpoint se existir
    checkpoint = carregar_checkpoint()
    pagina_atual = checkpoint["pagina_atual"]
    cursos_processados = checkpoint["cursos_processados"]
    
    # 📊 Inicializa estrutura de dados
    todos_dados = []
```

#### 📄 **Fase 2: Processamento de Páginas**
```python
    # 🔄 Loop principal de páginas
    while True:
        logger.info(f"=== PROCESSANDO PÁGINA {pagina_atual + 1} ===")
        
        # 📄 Extrai cursos da página atual
        cursos_pagina = processar_pagina(pagina_atual, logger)
        
        if not cursos_pagina:
            logger.info("📋 Nenhum curso encontrado - fim dos dados")
            break
        
        # 🎓 Processa cada curso da página
        for curso in cursos_pagina:
            dados_curso = extrair_dados_curso(curso, logger)
            ofertas = extrair_ofertas_do_curso(dados_curso["co_seq_curso"], logger)
            
            # 🎯 Processa cada oferta
            for oferta in ofertas:
                dados_oferta = extrair_dados_oferta(oferta, logger)
                
                # 🔗 Combina dados do curso e da oferta
                registro_completo = {**dados_curso, **dados_oferta}
                todos_dados.append(registro_completo)
            
            cursos_processados += 1
```

#### 💾 **Fase 3: Persistência e Checkpoint**
```python
        # 💾 Salva progresso a cada lote
        if cursos_processados % 10 == 0:
            salvar_dados_parciais(todos_dados, logger)
            salvar_checkpoint(pagina_atual, cursos_processados, logger)
        
        pagina_atual += 1
```

#### 📊 **Fase 4: Finalização e Relatório**
```python
    # 📊 Salva dados finais
    salvar_dados_finais(todos_dados, logger)
    
    # 📈 Gera relatório final
    gerar_relatorio_final(todos_dados, logger)
    
    logger.info("🎉 Scraper finalizado com sucesso!")
```

### 🛡️ **Sistema de Tratamento de Erros**

#### 🔄 **Recuperação Automática**
```python
def executar_com_retry(funcao, max_tentativas=3, delay=30):
    """
    🔄 Executa função com retry automático em caso de erro
    
    🎯 Estratégias:
    1. Tentativa imediata
    2. Retry com delay crescente
    3. Log detalhado de erros
    4. Fallback para métodos alternativos
    """
    for tentativa in range(max_tentativas):
        try:
            return funcao()
        except requests.exceptions.RequestException as e:
            if tentativa < max_tentativas - 1:
                logger.warning(f"⚠️ Tentativa {tentativa + 1} falhou: {e}")
                time.sleep(delay * (tentativa + 1))
            else:
                logger.error(f"❌ Todas as tentativas falharam: {e}")
                raise
```

#### 📊 **Validação de Dados**
```python
def validar_dados_curso(dados):
    """
    ✅ Valida integridade dos dados coletados
    
    🔍 Verificações:
    - Campos obrigatórios presentes
    - Tipos de dados corretos
    - Valores dentro de ranges esperados
    - Consistência entre campos relacionados
    """
    campos_obrigatorios = ["co_seq_curso", "no_curso", "id_oferta"]
    
    for campo in campos_obrigatorios:
        if campo not in dados or not dados[campo]:
            return False, f"Campo obrigatório ausente: {campo}"
    
    # Validações específicas
    if dados.get("vagas") and not str(dados["vagas"]).isdigit():
        return False, "Vagas deve ser um número"
    
    return True, "Dados válidos"
```

### 🎯 **Otimizações de Performance**

#### ⚡ **Concorrência Controlada**
```python
# 🚦 Controle de taxa de requisições
time.sleep(1)  # Delay entre requisições para não sobrecarregar servidor

# 📊 Processamento em lotes
if len(todos_dados) % 10 == 0:
    salvar_dados_parciais(todos_dados, logger)
```

#### 💾 **Gerenciamento de Memória**
```python
# 🧹 Limpeza periódica de dados em memória
if len(todos_dados) > 1000:
    salvar_dados_parciais(todos_dados, logger)
    todos_dados = []  # Libera memória
```

#### 🔍 **Cache Inteligente**
```python
# 📋 Cache de requisições para evitar duplicatas
cache_requisicoes = {}

def fazer_requisicao_cachead(url):
    if url in cache_requisicoes:
        return cache_requisicoes[url]
    
    response = requests.get(url, headers=HEADERS, timeout=30)
    cache_requisicoes[url] = response
    return response
```

---

## 📊 Dados Coletados

### 🎓 **Informações dos Cursos**
| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `co_seq_curso` | ID único do curso | `44538` |
| `no_curso` | Nome do curso | `"Atenção à Saúde da População Negra"` |
| `qt_carga_horaria_total` | Carga horária | `60 horas` |
| `ds_curso` | Descrição completa | `"Curso focado em..."` |
| `palavras_chave_curso` | Palavras-chave | `"saúde, população negra, equidade"` |

### 🎯 **Informações das Ofertas**
| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `id_oferta` | ID da oferta | `416264` |
| `vagas` | Número de vagas | `1000` |
| `publico_alvo` | Público-alvo | `"Profissionais de saúde"` |
| `local_oferta` | Local | `"EAD"` |
| `formato` | Formato | `"Ensino a Distância"` |

### 🌈 **Análise DEIA (Diversidade, Equidade, Inclusão e Acessibilidade)**
| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `tem_deia` | Possui conteúdo DEIA | `"Sim"` ou `"Não"` |
| `deia_encontrado` | Descritor específico | `"Saúde da População Negra"` |
| `texto_analisado_deia` | Texto analisado | `"Título: Curso... + Descrição:..."` |

---

## 🛠️ Como Usar (Guia Passo a Passo)

### 📋 **Pré-requisitos**
Antes de começar, você precisa ter:
- **Python 3.8 ou superior** instalado
- **Conexão com a internet** estável
- **Conhecimento básico** de linha de comando

### 🔧 **Instalação**

#### 1️⃣ **Clone o projeto**
```bash
git clone https://github.com/seu-usuario/una-sus.git
cd una-sus
```

#### 2️⃣ **Instale as dependências**
```bash
pip install -r requirements.txt
```

#### 3️⃣ **Verifique se tudo está funcionando**
```bash
python --version
pip list | grep -E "(requests|pandas|beautifulsoup)"
```

### 🚀 **Execução**

#### 🎯 **Opção 1: Coleta Completa (Recomendado)**
```bash
python scraper_unasus_melhorado.py
```

**O que acontece:**
- 🔍 **Busca** todos os cursos da UNA-SUS
- 📊 **Coleta** dados detalhados de cada curso
- 🌈 **Analisa** conteúdo DEIA automaticamente
- 💾 **Salva** progresso a cada 10 cursos
- 📈 **Mostra** estatísticas em tempo real

#### 🔄 **Opção 2: Reanálise de Dados Existentes**
Se você já tem dados coletados e quer apenas atualizar a análise DEIA:
```bash
python reanalisar_deia_existente.py
```

#### 🧪 **Opção 3: Teste da Busca DEIA**
Para validar se a busca DEIA está funcionando:
```bash
python testar_busca_deia.py
```

---

## 📈 Monitoramento e Logs

### 👀 **Como Acompanhar o Progresso**

Durante a execução, você verá mensagens como:
```
2025-07-26 15:30:15 - INFO - === PROCESSANDO PÁGINA 5 ===
2025-07-26 15:30:16 - INFO - Processando curso 44538: Atenção à Saúde da População Negra
2025-07-26 15:30:16 - INFO - 🌈 DEIA encontrado no curso 44538: População Negra
2025-07-26 15:30:17 - INFO - Buscando ofertas do curso 44538...
2025-07-26 15:30:17 - INFO -   ✅ Oferta encontrada: 416264
2025-07-26 15:30:18 - INFO -   🔍 Extraindo dados da oferta 416264...
2025-07-26 15:30:18 - INFO -     ✅ Dados obtidos via API REST
2025-07-26 15:30:18 - INFO -     ✅ Vagas extraídas: 1000
```

### 🎨 **Significado dos Emojis nos Logs**

| Emoji | Significado | Exemplo |
|-------|-------------|---------|
| 🌈 | **DEIA detectado** | `🌈 DEIA encontrado: População Negra` |
| ✅ | **Sucesso** | `✅ Oferta encontrada: 416264` |
| 🔍 | **Processando** | `🔍 Extraindo dados...` |
| 📊 | **Estatísticas** | `📊 Total de registros: 1656` |
| 💾 | **Salvando** | `💾 Progresso salvo` |
| ⚠️ | **Aviso** | `⚠️ Curso sem ofertas` |
| ❌ | **Erro** | `❌ Erro na conexão` |

### 📊 **Estatísticas Finais**
Ao final da execução, você verá:
```
=== RELATÓRIO FINAL ===
📊 Total de registros: 1656
🌈 Cursos com DEIA: 604 (36.5%)
📚 Cursos sem DEIA: 1052 (63.5%)
📁 Arquivo salvo: unasus_ofertas_melhoradas.csv
```

---

## 📁 Estrutura do Projeto

```
una-sus/
├── 🐍 scraper_unasus_melhorado.py    # Scraper principal (MAIS RECENTE)
├── 🐍 scraper_unasus.py              # Scraper original (referência)
├── 🐍 reanalisar_deia_existente.py   # Reanálise DEIA
├── 🐍 testar_busca_deia.py           # Testes DEIA
├── 📊 unasus_ofertas_melhoradas.csv  # Dados coletados
├── 📚 README.md                      # Esta documentação
├── 📚 README_MELHORIAS_DEIA.md       # Detalhes das melhorias
├── 📋 requirements.txt               # Dependências
├── ⚙️ pyproject.toml                 # Configuração do projeto
├── 🐳 Dockerfile                     # Containerização
├── 🐳 docker-compose.yml             # Orquestração
└── 📄 LICENSE                        # Licença MIT
```

---

## 🌈 Análise DEIA - Explicação Detalhada

### 🎯 **O que é DEIA?**
**DEIA** significa **Diversidade, Equidade, Inclusão e Acessibilidade**. É um conceito fundamental para:
- 🏥 **Saúde pública** inclusiva
- 🎓 **Educação** acessível a todos
- 🤝 **Sociedade** mais justa e equitativa

### 🔍 **Como Funciona a Detecção?**

O sistema analisa **todos os campos** coletados:
1. **Título do curso** (`no_curso`)
2. **Descrição do curso** (`ds_curso`)
3. **Descrição da oferta** (`descricao_oferta`)
4. **Palavras-chave** (`palavras_chave`)
5. **Público-alvo** (`publico_alvo`)
6. **Temas** (`temas`)
7. **DeCs** (`decs`)
8. **Programas de governo** (`programas_governo`)
9. **Texto da página inicial** (`texto_pagina_inicial`)

### 📝 **Exemplos de Descritores DEIA**

#### 👥 **Populações Específicas**
- População Negra, População Indígena
- População LGBTQI+, Trans, Transgênero
- População em Situação de Rua
- População Privada de Liberdade

#### 🏥 **Saúde Específica**
- Saúde Mental, Saúde da Mulher
- Saúde da Criança, Saúde do Idoso
- Saúde da População Negra
- Saúde Indígena

#### 🌍 **Conceitos DEIA**
- Diversidade, Equidade, Inclusão
- Acessibilidade, Pertencimento
- Direitos Humanos, Cidadania
- Vulnerabilidade, Discriminação

---

## 🚨 Solução de Problemas

### ❓ **Perguntas Frequentes**

#### **Q: O scraper parou no meio. O que fazer?**
**A:** Não se preocupe! O sistema tem **checkpoint automático**. Basta executar novamente:
```bash
python scraper_unasus_melhorado.py
```
Ele continuará de onde parou.

#### **Q: Não encontrou nenhum curso com DEIA. É normal?**
**A:** Se você está usando o scraper original (`scraper_unasus.py`), sim. Use o **melhorado**:
```bash
python scraper_unasus_melhorado.py
```

#### **Q: O arquivo CSV está muito grande. É normal?**
**A:** Sim! O arquivo pode ter **8+ MB** porque contém:
- 1.656 registros de ofertas
- 30 colunas de dados
- Textos completos dos cursos

#### **Q: Como saber se está funcionando?**
**A:** Observe os logs:
- ✅ **Verde** = funcionando
- ⚠️ **Amarelo** = aviso (normal)
- ❌ **Vermelho** = erro (raro)

### 🔧 **Problemas Técnicos**

#### **Erro de Conexão**
```bash
# Tente novamente em alguns minutos
python scraper_unasus_melhorado.py
```

#### **Erro de Dependências**
```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

#### **Erro de Permissão**
```bash
# No Windows, execute como administrador
# No Linux/Mac, use sudo se necessário
```

---

## 📊 Análise dos Resultados

### 📈 **Estatísticas Típicas**
- **Total de cursos**: ~550 cursos únicos
- **Total de ofertas**: ~1.650 ofertas
- **Cursos com DEIA**: ~600 (36%)
- **Cursos sem DEIA**: ~1.050 (64%)

### 🔍 **Como Analisar os Dados**

#### **1. Abrir no Excel/LibreOffice**
```bash
# O arquivo é compatível com Excel
unasus_ofertas_melhoradas.csv
```

#### **2. Filtrar por DEIA**
- Coluna `tem_deia` = "Sim"
- Ver coluna `deia_encontrado` para detalhes

#### **3. Análise por Tema**
- Coluna `temas` para categorização
- Coluna `decs` para classificação médica

#### **4. Análise Geográfica**
- Coluna `local_oferta` para distribuição
- Coluna `no_orgao` para instituições

---

## 🤝 Contribuição

### 💡 **Como Contribuir**

1. **🔍 Encontrou um bug?**
   - Abra uma **Issue** no GitHub
   - Descreva o problema detalhadamente

2. **✨ Tem uma ideia?**
   - Sugira melhorias via **Issue**
   - Proponha novos descritores DEIA

3. **💻 Quer programar?**
   - Faça um **Fork** do projeto
   - Crie uma **Pull Request**

### 📝 **Padrões do Projeto**

#### **Emojis Educativos**
Use emojis para facilitar a compreensão:
- 🎓 = Educação/Academia
- 🏥 = Saúde
- 🌈 = DEIA/Diversidade
- 📊 = Dados/Estatísticas
- 🔍 = Busca/Análise
- ✅ = Sucesso
- ❌ = Erro

#### **Comentários no Código**
```python
# 🌈 Busca por descritores DEIA no texto
def encontrar_descritor_deia_melhorado(texto_completo):
    """
    📝 Analisa texto completo em busca de descritores DEIA
    
    Args:
        texto_completo (str): Texto combinado de todos os campos
        
    Returns:
        str: Descritor DEIA encontrado ou None
    """
```

---

## 📚 Recursos Educativos

### 🎓 **Para Estudantes**
- **Web Scraping**: Aprenda a coletar dados da web
- **Análise de Dados**: Trabalhe com datasets reais
- **Python**: Pratique programação em Python
- **Saúde Pública**: Entenda dados educacionais em saúde

### 🔬 **Para Pesquisadores**
- **Metodologia**: Exemplo de coleta sistemática de dados
- **DEIA**: Framework para análise de diversidade
- **Estatísticas**: Dados quantitativos para pesquisas
- **Qualidade**: Dados validados e estruturados

### 💻 **Para Desenvolvedores**
- **Clean Code**: Código bem estruturado e documentado
- **Error Handling**: Tratamento robusto de erros
- **Logging**: Sistema de logs detalhado
- **Modularização**: Funções bem separadas

---

## 📄 Licença

Este projeto está sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

**O que isso significa?**
- ✅ **Pode usar** livremente
- ✅ **Pode modificar** o código
- ✅ **Pode distribuir** o projeto
- ✅ **Pode usar comercialmente**
- ❌ **Não precisa** dar crédito (mas é apreciado!)

---

## 🙏 Agradecimentos

- 🏥 **UNA-SUS** pela disponibilização dos dados
- 🐍 **Comunidade Python** pelos recursos utilizados
- 🌈 **Comunidade DEIA** pela inspiração
- 👥 **Contribuidores** do projeto

---

## 📞 Suporte

### 🆘 **Precisa de Ajuda?**

1. **📖 Leia** esta documentação completa
2. **🔍 Verifique** as seções de solução de problemas
3. **💬 Abra** uma Issue no GitHub
4. **📧 Entre em contato** com os mantenedores

### 📚 **Recursos Adicionais**

- 📖 **Documentação Python**: https://docs.python.org/
- 🐍 **Tutorial Requests**: https://requests.readthedocs.io/
- 🍲 **BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/
- 📊 **Pandas**: https://pandas.pydata.org/

---

**🎯 Desenvolvido com ❤️ para facilitar pesquisas em saúde pública e promover educação inclusiva!**

*Última atualização: Julho 2025*
