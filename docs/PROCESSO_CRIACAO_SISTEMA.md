# 🔬 PROCESSO DE CRIAÇÃO DO SISTEMA UNA-SUS
## Documentação Extensa e Detalhada do Desenvolvimento

---

## 📋 **SUMÁRIO EXECUTIVO**

Este documento apresenta uma explicação extensa e detalhada do processo completo de criação do Sistema UNA-SUS, desde a concepção inicial até a implementação final. O documento aborda:

1. **Processo de Criação do Sistema**: Metodologia, arquitetura e decisões de design
2. **Cuidado com Falhas**: Sistemas de tratamento de erros, validação e recuperação
3. **Processo de Encontrar Resultados**: Metodologias de análise e descoberta de padrões
4. **Modulação para Outros Descritores**: Arquitetura extensível e adaptação para novos campos

---

## 🏗️ **PARTE 1: PROCESSO DE CRIAÇÃO DO SISTEMA**

### **1.1. Concepção e Planejamento Inicial**

#### **A. Identificação da Necessidade**

O sistema foi concebido para atender uma necessidade específica: **analisar dados educacionais da Universidade Aberta do SUS (UNA-SUS) de forma sistemática e reproduzível**. As necessidades identificadas foram:

- **Coleta Automatizada**: Necessidade de coletar dados de forma automatizada e confiável
- **Análise Estruturada**: Necessidade de análises padronizadas e reproduzíveis
- **Extensibilidade**: Necessidade de adaptar o sistema para diferentes tipos de análise
- **Reprodutibilidade Científica**: Necessidade de metodologia clara e documentada

#### **B. Definição de Objetivos**

Os objetivos principais foram definidos como:

1. **Coleta Completa**: Coletar todos os dados disponíveis sem filtros ou exclusões
2. **Preservação de Integridade**: Manter todos os campos originais sem modificações
3. **Análise Modular**: Criar módulos independentes para diferentes tipos de análise
4. **Documentação Completa**: Documentar todo o processo para reprodutibilidade

#### **C. Escolha de Tecnologias**

As tecnologias foram escolhidas com base em:

- **Python**: Linguagem de programação principal
  - **Razão**: Facilidade de uso, bibliotecas robustas, comunidade ativa
  - **Bibliotecas Principais**:
    - `requests`: Para requisições HTTP
    - `pandas`: Para manipulação de dados
    - `beautifulsoup4`: Para parsing HTML
    - `sqlite3`: Para armazenamento de dados

- **Estrutura de Dados**:
  - **CSV**: Formato principal para compatibilidade
  - **JSON**: Para metadados e relatórios
  - **SQLite**: Para consultas eficientes

### **1.2. Arquitetura do Sistema**

#### **A. Princípios de Design**

O sistema foi projetado seguindo princípios fundamentais:

1. **Modularidade**: Cada componente é independente e pode ser usado separadamente
2. **Separação de Responsabilidades**: Coleta, análise e relatórios são separados
3. **Extensibilidade**: Fácil adição de novos módulos de análise
4. **Robustez**: Tratamento de erros em todos os níveis
5. **Transparência**: Logging detalhado de todas as operações

#### **B. Estrutura de Camadas**

O sistema foi organizado em camadas bem definidas:

```
┌─────────────────────────────────────────────────────────────┐
│                    🌐 CAMADA DE COLETA                     │
│  - Requisições HTTP                                         │
│  - Parsing de dados                                        │
│  - Validação inicial                                       │
│  - Tratamento de erros de rede                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                💾 CAMADA DE ARMAZENAMENTO                  │
│  - Persistência em múltiplos formatos                      │
│  - Checkpointing automático                                │
│  - Validação de integridade                               │
│  - Backup e recuperação                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                🔍 CAMADA DE ANÁLISE                       │
│  - Módulos especializados                                 │
│  - Processamento de dados                                  │
│  - Identificação de padrões                                │
│  - Geração de estatísticas                                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                📈 CAMADA DE RELATÓRIOS                    │
│  - Formatação de resultados                                │
│  - Geração de relatórios                                   │
│  - Visualizações                                          │
│  - Exportação em múltiplos formatos                       │
└─────────────────────────────────────────────────────────────┘
```

#### **C. Componentes Principais**

##### **1. Coletor de Dados (`coletor_database_geral.py`)**

**Responsabilidades**:
- Coleta completa de dados da API UNA-SUS
- Extração de ofertas por curso
- Validação de dados coletados
- Persistência em múltiplos formatos

**Metodologia de Implementação**:

```python
class ColetorDatabaseGeral:
    """
    Processo de criação:
    1. Análise da API UNA-SUS
    2. Identificação de endpoints e parâmetros
    3. Implementação de requisições HTTP
    4. Parsing de respostas JSON
    5. Extração de dados de ofertas
    6. Validação e normalização
    7. Persistência em múltiplos formatos
    """
    
    def __init__(self):
        # 1. Configuração inicial
        # - Headers HTTP necessários
        # - Cookies de autenticação
        # - Payload para requisições
        # - Configuração de logging
        
    def coletar_dados_completos(self):
        # 2. Processo de coleta
        # - Loop paginado de requisições
        # - Processamento de cada página
        # - Extração de cursos
        # - Extração de ofertas por curso
        # - Validação incremental
        # - Checkpointing automático
```

**Decisões de Design**:

1. **Estrutura Plana**: Uma oferta = um registro
   - **Razão**: Facilita análises estatísticas
   - **Benefício**: Cada registro é independente e completo

2. **Preservação de Dados Originais**: Todos os campos mantidos
   - **Razão**: Permite análises futuras não previstas
   - **Benefício**: Dados completos para pesquisa

3. **Múltiplos Formatos de Saída**: CSV, JSON, SQLite
   - **Razão**: Diferentes ferramentas requerem diferentes formatos
   - **Benefício**: Flexibilidade de uso

##### **2. Sistema de Análise Modular (`analise/`)**

**Arquitetura Modular**:

```python
# Estrutura de módulos independentes
analise/
├── analisador_geral.py          # Orquestrador
├── mapeamento_programas.py      # Análise de programas
├── cobertura_programatica.py   # Cobertura programática
├── distribuicao_geografica.py   # Distribuição geográfica
├── estatisticas_basicas.py      # Estatísticas básicas
├── relatorios.py                # Geração de relatórios
└── relatorios_visuais.py        # Relatórios visuais
```

**Metodologia de Criação dos Módulos**:

1. **Identificação de Necessidade**: Cada módulo atende a uma necessidade específica
2. **Definição de Interface**: Interface padronizada entre módulos
3. **Implementação Independente**: Cada módulo pode ser desenvolvido separadamente
4. **Testes Unitários**: Testes específicos para cada módulo
5. **Integração**: Integração com o orquestrador principal

**Exemplo de Criação de Módulo**:

```python
class MapeamentoProgramas:
    """
    Processo de criação:
    1. Identificação do campo de programas nos dados
    2. Desenvolvimento de algoritmo de mapeamento
    3. Implementação de contagem e estatísticas
    4. Validação de resultados
    5. Integração com sistema de relatórios
    """
    
    def __init__(self):
        # Inicialização com dados vazios
        self.dados = None
        self.mapeamento = {}
    
    def carregar_dados(self, dados):
        # Carregamento de dados para análise
        # Validação de estrutura
        # Preparação para processamento
    
    def mapear_programas(self):
        # 1. Identificação de coluna de programas
        # 2. Extração de programas únicos
        # 3. Contagem de cursos e ofertas por programa
        # 4. Cálculo de estatísticas
        # 5. Ordenação e classificação
        # 6. Retorno de resultados estruturados
```

### **1.3. Processo de Desenvolvimento Iterativo**

#### **A. Fase 1: Prototipagem**

**Objetivo**: Validar a viabilidade da coleta de dados

**Atividades**:
1. Análise da API UNA-SUS
2. Testes de requisições HTTP
3. Parsing inicial de dados
4. Validação de estrutura de dados

**Resultados**:
- Confirmação da viabilidade
- Identificação de desafios técnicos
- Definição de requisitos técnicos

#### **B. Fase 2: Implementação Base**

**Objetivo**: Criar sistema funcional básico

**Atividades**:
1. Implementação do coletor principal
2. Sistema de logging básico
3. Persistência em CSV
4. Validação de dados básica

**Resultados**:
- Sistema funcional para coleta
- Primeiros dados coletados
- Identificação de melhorias necessárias

#### **C. Fase 3: Robustez e Confiabilidade**

**Objetivo**: Tornar o sistema robusto e confiável

**Atividades**:
1. Implementação de tratamento de erros
2. Sistema de checkpointing
3. Validação avançada de dados
4. Recuperação de falhas

**Resultados**:
- Sistema robusto para produção
- Capacidade de recuperação de erros
- Logging detalhado

#### **D. Fase 4: Análises Especializadas**

**Objetivo**: Criar módulos de análise especializados

**Atividades**:
1. Desenvolvimento de módulos de análise
2. Implementação de algoritmos específicos
3. Geração de relatórios
4. Validação de resultados

**Resultados**:
- Módulos de análise funcionais
- Relatórios gerados automaticamente
- Validação de metodologias

#### **E. Fase 5: Documentação e Refinamento**

**Objetivo**: Documentar e refinar o sistema

**Atividades**:
1. Documentação completa
2. Refinamento de código
3. Otimizações de performance
4. Testes finais

**Resultados**:
- Sistema documentado
- Código otimizado
- Sistema pronto para uso

---

## 🛡️ **PARTE 2: CUIDADO COM FALHAS**

### **2.1. Filosofia de Tratamento de Erros**

#### **A. Princípios Fundamentais**

O sistema foi desenvolvido com uma filosofia rigorosa de tratamento de erros:

1. **Nunca Falhar Silenciosamente**: Todos os erros são logados
2. **Recuperação Automática**: Tentativas automáticas de recuperação
3. **Preservação de Dados**: Dados coletados são sempre preservados
4. **Transparência**: Usuário sempre informado sobre o estado do sistema
5. **Graceful Degradation**: Sistema continua funcionando mesmo com falhas parciais

#### **B. Estratégias de Tratamento**

##### **1. Tratamento de Erros de Rede**

**Problema**: Requisições HTTP podem falhar por diversos motivos

**Solução Implementada**:

```python
def coletar_dados_completos(self):
    """
    Estratégia de tratamento de erros de rede:
    1. Tentativa inicial
    2. Verificação de status HTTP
    3. Retry automático com delay
    4. Logging detalhado
    5. Continuidade do processo
    """
    while True:
        try:
            response = requests.post(
                self.url_base,
                data=payload,
                headers=self.headers,
                cookies=self.cookies,
                timeout=30,  # Timeout explícito
            )
            
            # Verificação de status
            if response.status_code != 200:
                self.logger.warning(
                    f"⚠️ Status {response.status_code}. Tentando novamente..."
                )
                time.sleep(30)  # Delay antes de retry
                continue  # Retry automático
            
            # Processamento normal
            data = response.json()
            # ...
            
        except requests.exceptions.Timeout:
            self.logger.warning("⚠️ Timeout na requisição. Tentando novamente...")
            time.sleep(30)
            continue
            
        except requests.exceptions.ConnectionError:
            self.logger.warning("⚠️ Erro de conexão. Tentando novamente...")
            time.sleep(60)  # Delay maior para erros de conexão
            continue
            
        except Exception as e:
            self.logger.error(f"❌ Erro inesperado: {e}")
            # Salvar dados coletados até o momento
            self._salvar_dados_completos()
            raise  # Re-raise apenas após salvar dados
```

**Características**:
- **Timeout Explícito**: Evita travamentos indefinidos
- **Retry Automático**: Tentativas automáticas de recuperação
- **Delays Progressivos**: Delays maiores para erros mais graves
- **Preservação de Dados**: Dados sempre salvos antes de falhar

##### **2. Tratamento de Erros de Parsing**

**Problema**: Dados podem estar em formatos inesperados

**Solução Implementada**:

```python
def _processar_curso_completo(self, curso: Dict) -> List[Dict]:
    """
    Estratégia de tratamento de erros de parsing:
    1. Validação de estrutura
    2. Tratamento de campos ausentes
    3. Normalização de tipos
    4. Valores padrão para campos faltantes
    5. Logging de problemas
    """
    try:
        # Criar cópia para não modificar original
        curso_processado = curso.copy()
        
        # Validação de campos obrigatórios
        campos_obrigatorios = ["id", "titulo", "descricao"]
        for campo in campos_obrigatorios:
            if campo not in curso_processado:
                self.logger.warning(
                    f"⚠️ Campo obrigatório ausente: {campo}"
                )
                curso_processado[campo] = ""  # Valor padrão
        
        # Normalização de campos numéricos
        campos_numericos = ["vagas", "numero_vagas", "qt_vagas"]
        for campo in campos_numericos:
            if campo in curso_processado:
                try:
                    valor = curso_processado[campo]
                    if isinstance(valor, str) and valor.strip():
                        curso_processado[campo] = int(valor)
                    elif valor is None or valor == "":
                        curso_processado[campo] = 0
                except (ValueError, TypeError) as e:
                    self.logger.warning(
                        f"⚠️ Erro ao converter {campo}: {e}. Usando 0."
                    )
                    curso_processado[campo] = 0
        
        # Processamento normal
        # ...
        
    except Exception as e:
        self.logger.error(f"❌ Erro ao processar curso: {e}")
        # Retornar registro mínimo ao invés de falhar
        return [{
            "erro": str(e),
            "dados_originais": curso
        }]
```

**Características**:
- **Validação Preventiva**: Verificação antes de processar
- **Valores Padrão**: Valores seguros para campos faltantes
- **Conversão Segura**: Tratamento de erros de conversão
- **Preservação de Dados Originais**: Dados originais mantidos em caso de erro

##### **3. Tratamento de Erros de Extração de Ofertas**

**Problema**: Extração de ofertas pode falhar por diversos motivos

**Solução Implementada**:

```python
def _extrair_ofertas_do_curso(self, id_curso: str) -> List[Dict]:
    """
    Estratégia de tratamento de erros de extração:
    1. Múltiplas tentativas (API REST + HTML)
    2. Fallback para métodos alternativos
    3. Tratamento de erros específicos
    4. Retorno de lista vazia ao invés de falhar
    5. Logging detalhado
    """
    ofertas = []
    
    try:
        # Tentativa 1: API REST
        try:
            url_api = f"https://www.unasus.gov.br/cursos/rest/oferta/{id_oferta}"
            resp_api = requests.get(url_api, headers=api_headers, timeout=30)
            
            if resp_api.status_code == 200:
                response_data = resp_api.json()
                oferta_data = response_data.get("data", {})
                # Processamento normal
                return oferta_data
            else:
                self.logger.warning(
                    f"⚠️ API REST retornou status {resp_api.status_code}"
                )
        except Exception as e:
            self.logger.warning(f"⚠️ Erro na API REST: {e}")
        
        # Tentativa 2: Fallback HTML
        try:
            self.logger.info("🔄 Tentando extração da página HTML...")
            resp = requests.get(url_oferta, headers=self.headers, timeout=30)
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Extração via HTML
            oferta_quadro = soup.find("div", id="oferta_quadro")
            if oferta_quadro:
                # Processamento HTML
                dados = self._extrair_dados_html(oferta_quadro)
                return dados
        except Exception as e:
            self.logger.warning(f"⚠️ Erro na extração HTML: {e}")
        
        # Se todas as tentativas falharam
        self.logger.warning(
            f"⚠️ Não foi possível extrair dados da oferta {id_oferta}"
        )
        return {"id_oferta": id_oferta, "erro": "Extração falhou"}
        
    except Exception as e:
        self.logger.error(f"❌ Erro ao extrair ofertas do curso {id_curso}: {e}")
        return []  # Retornar lista vazia ao invés de falhar
```

**Características**:
- **Múltiplas Tentativas**: API REST primeiro, HTML como fallback
- **Fallback Automático**: Mudança automática de método
- **Retorno Seguro**: Lista vazia ao invés de exceção
- **Logging Detalhado**: Informações sobre cada tentativa

### **2.2. Sistema de Validação**

#### **A. Validação de Dados Coletados**

**Estratégia**: Validação em múltiplos níveis

```python
def _validar_dados_coletados(self):
    """
    Validação em múltiplos níveis:
    1. Validação de estrutura
    2. Validação de tipos
    3. Validação de valores
    4. Validação de consistência
    5. Relatório de problemas
    """
    problemas = []
    
    # 1. Validação de estrutura
    if not self.dados_coletados:
        problemas.append("Nenhum dado coletado")
        return problemas
    
    # 2. Validação de tipos
    for i, registro in enumerate(self.dados_coletados):
        # Verificar campos obrigatórios
        if "id_curso" not in registro:
            problemas.append(f"Registro {i}: Campo 'id_curso' ausente")
        
        # Verificar tipos
        if "vagas" in registro:
            try:
                int(registro["vagas"])
            except (ValueError, TypeError):
                problemas.append(f"Registro {i}: Campo 'vagas' inválido")
    
    # 3. Validação de valores
    for i, registro in enumerate(self.dados_coletados):
        if "vagas" in registro and registro["vagas"] < 0:
            problemas.append(f"Registro {i}: Vagas negativas")
    
    # 4. Relatório
    if problemas:
        self.logger.warning(f"⚠️ {len(problemas)} problemas encontrados")
        for problema in problemas[:10]:  # Limitar relatório
            self.logger.warning(f"  - {problema}")
    
    return problemas
```

#### **B. Validação de Integridade**

**Estratégia**: Verificação de integridade dos dados salvos

```python
def _verificar_integridade_dados(self, arquivo: str):
    """
    Verificação de integridade:
    1. Verificação de existência do arquivo
    2. Verificação de formato
    3. Verificação de estrutura
    4. Verificação de completude
    """
    try:
        # Carregar dados
        if arquivo.endswith('.csv'):
            df = pd.read_csv(arquivo)
        elif arquivo.endswith('.json'):
            with open(arquivo, 'r') as f:
                dados = json.load(f)
        
        # Verificações
        if len(df) == 0:
            self.logger.warning("⚠️ Arquivo vazio")
            return False
        
        # Verificar campos essenciais
        campos_essenciais = ['id_curso', 'no_curso']
        for campo in campos_essenciais:
            if campo not in df.columns:
                self.logger.warning(f"⚠️ Campo essencial ausente: {campo}")
                return False
        
        self.logger.info("✅ Integridade verificada")
        return True
        
    except Exception as e:
        self.logger.error(f"❌ Erro ao verificar integridade: {e}")
        return False
```

### **2.3. Sistema de Checkpointing**

#### **A. Objetivo**

O sistema de checkpointing permite recuperação de coletas interrompidas.

**Implementação**:

```python
def _salvar_checkpoint(self, pagina_atual: int):
    """
    Sistema de checkpointing:
    1. Salvamento periódico do estado
    2. Informações de progresso
    3. Dados coletados até o momento
    4. Possibilidade de retomada
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_data = {
        "timestamp": datetime.now().isoformat(),
        "pagina_atual": pagina_atual,
        "cursos_coletados": len(self.dados_coletados),
        "versao_coletor": "1.0.0",
        "tipo_coleta": "database_geral",
    }
    
    checkpoint_path = (
        f"checkpoints/coleta_database_geral_checkpoint_{timestamp}.json"
    )
    
    try:
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"💾 Checkpoint salvo: {checkpoint_path}")
        
        # Salvar também dados coletados
        if self.dados_coletados:
            dados_path = f"checkpoints/dados_checkpoint_{timestamp}.json"
            with open(dados_path, "w", encoding="utf-8") as f:
                json.dump(self.dados_coletados, f, ensure_ascii=False, indent=2)
    
    except Exception as e:
        self.logger.error(f"❌ Erro ao salvar checkpoint: {e}")
```

**Características**:
- **Salvamento Periódico**: Checkpoints a cada 10 páginas
- **Dados Preservados**: Dados coletados sempre salvos
- **Retomada Possível**: Possibilidade de continuar de onde parou
- **Metadata Completa**: Informações sobre o estado da coleta

### **2.4. Sistema de Logging**

#### **A. Estrutura de Logging**

**Implementação**:

```python
def _configurar_logger(self) -> logging.Logger:
    """
    Sistema de logging:
    1. Logging para arquivo
    2. Logging para console
    3. Formatação padronizada
    4. Níveis de log apropriados
    """
    logger = logging.getLogger("ColetorDatabaseGeral")
    logger.setLevel(logging.INFO)
    
    # Limpar handlers existentes
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Handler para arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fh = logging.FileHandler(
        f"logs/coletor_database_geral_{timestamp}.log",
        encoding="utf-8"
    )
    fh.setLevel(logging.INFO)
    
    # Handler para console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
```

**Características**:
- **Múltiplos Destinos**: Arquivo e console
- **Formatação Padronizada**: Fácil leitura e análise
- **Níveis Apropriados**: INFO, WARNING, ERROR
- **Encoding UTF-8**: Suporte a caracteres especiais

---

## 🔍 **PARTE 3: PROCESSO DE ENCONTRAR RESULTADOS**

### **3.1. Metodologia de Análise**

#### **A. Abordagem Exploratória**

O processo de encontrar resultados segue uma abordagem exploratória:

1. **Carregamento de Dados**: Dados coletados são carregados
2. **Exploração Inicial**: Análise exploratória dos dados
3. **Identificação de Padrões**: Identificação de padrões e tendências
4. **Validação**: Validação dos padrões identificados
5. **Geração de Resultados**: Geração de resultados estruturados

#### **B. Processo de Descoberta**

##### **1. Identificação de Campos Relevantes**

**Metodologia**:

```python
def identificar_campos_relevantes(self, dados):
    """
    Processo de identificação:
    1. Análise de todas as colunas disponíveis
    2. Identificação de campos relevantes para análise
    3. Verificação de completude dos campos
    4. Seleção de campos para análise
    """
    campos_relevantes = {}
    
    # Análise de cada coluna
    for coluna in dados.columns:
        # Verificar completude
        valores_nulos = dados[coluna].isnull().sum()
        percentual_nulos = (valores_nulos / len(dados)) * 100
        
        # Verificar valores únicos
        valores_unicos = dados[coluna].nunique()
        
        # Classificar relevância
        if percentual_nulos < 50 and valores_unicos > 1:
            campos_relevantes[coluna] = {
                "completude": 100 - percentual_nulos,
                "valores_unicos": valores_unicos,
                "relevante": True
            }
    
    return campos_relevantes
```

##### **2. Extração de Padrões**

**Metodologia**:

```python
def extrair_padroes(self, dados, campo):
    """
    Processo de extração de padrões:
    1. Agrupamento por campo
    2. Contagem de ocorrências
    3. Identificação de padrões
    4. Classificação de padrões
    """
    # Agrupamento
    grupos = dados.groupby(campo)
    
    # Contagem
    contagens = grupos.size().sort_values(ascending=False)
    
    # Identificação de padrões
    padroes = {}
    for valor, contagem in contagens.items():
        if contagem > 10:  # Threshold para padrão significativo
            padroes[valor] = {
                "contagem": contagem,
                "percentual": (contagem / len(dados)) * 100,
                "padrao": True
            }
    
    return padroes
```

### **3.2. Análises Especializadas**

#### **A. Mapeamento de Programas**

**Processo de Descoberta**:

```python
def mapear_programas(self):
    """
    Processo de mapeamento:
    1. Identificação da coluna de programas
    2. Extração de programas únicos
    3. Contagem de ocorrências por programa
    4. Cálculo de estatísticas
    5. Classificação e ordenação
    """
    # 1. Identificação da coluna
    coluna_programas = None
    for col in self.dados.columns:
        if "programa" in col.lower():
            coluna_programas = col
            break
    
    # 2. Extração de programas únicos
    programas_unicos = self.dados[coluna_programas].dropna().unique()
    
    # 3. Contagem por programa
    mapeamento = {}
    for programa in programas_unicos:
        dados_programa = self.dados[
            self.dados[coluna_programas] == programa
        ]
        
        mapeamento[programa] = {
            "quantidade_cursos": len(dados_programa),
            "cursos_unicos": dados_programa["no_curso"].nunique(),
            "ofertas_unicas": dados_programa["id_oferta"].nunique(),
            "instituicoes": dados_programa["no_orgao"].nunique(),
        }
    
    # 4. Ordenação
    programas_ordenados = dict(
        sorted(
            mapeamento.items(),
            key=lambda x: x[1]["quantidade_cursos"],
            reverse=True
        )
    )
    
    return programas_ordenados
```

#### **B. Análise de Cobertura Programática**

**Processo de Descoberta**:

```python
def analisar_cobertura(self):
    """
    Processo de análise de cobertura:
    1. Agrupamento por programa
    2. Contagem de ofertas por programa
    3. Classificação por quantidade
    4. Identificação de lacunas
    5. Geração de relatório
    """
    # 1. Agrupamento
    cobertura_por_programa = self.dados.groupby(
        "programas_governo"
    ).size()
    
    # 2. Classificação
    classificacao = {
        "critica": [],      # < 5 ofertas
        "limitada": [],     # 5-9 ofertas
        "adequada": [],     # 10-49 ofertas
        "excelente": []     # 50+ ofertas
    }
    
    for programa, quantidade in cobertura_por_programa.items():
        if quantidade < 5:
            classificacao["critica"].append(programa)
        elif quantidade < 10:
            classificacao["limitada"].append(programa)
        elif quantidade < 50:
            classificacao["adequada"].append(programa)
        else:
            classificacao["excelente"].append(programa)
    
    # 3. Identificação de lacunas
    lacunas = classificacao["critica"] + classificacao["limitada"]
    
    return {
        "classificacao": classificacao,
        "lacunas": lacunas,
        "total_programas": len(cobertura_por_programa)
    }
```

#### **C. Distribuição Geográfica**

**Processo de Descoberta**:

```python
def analisar_distribuicao(self):
    """
    Processo de análise geográfica:
    1. Extração de estados das instituições
    2. Agrupamento por estado
    3. Contagem de ofertas por estado
    4. Classificação (polos/desertos)
    5. Análise por região
    """
    # 1. Extração de estados
    estados = []
    for instituicao in self.dados["no_orgao"]:
        estado = self._extrair_estado(instituicao)
        estados.append(estado)
    
    self.dados["estado"] = estados
    
    # 2. Agrupamento
    distribuicao_por_estado = self.dados.groupby("estado").size()
    
    # 3. Classificação
    polos = []
    desertos = []
    
    for estado, quantidade in distribuicao_por_estado.items():
        if quantidade > 100:
            polos.append(estado)
        elif quantidade < 10:
            desertos.append(estado)
    
    # 4. Análise por região
    distribuicao_por_regiao = self._agrupar_por_regiao()
    
    return {
        "polos": polos,
        "desertos": desertos,
        "distribuicao_por_estado": distribuicao_por_estado.to_dict(),
        "distribuicao_por_regiao": distribuicao_por_regiao
    }
```

### **3.3. Validação de Resultados**

#### **A. Verificação de Consistência**

**Metodologia**:

```python
def validar_resultados(self, resultados):
    """
    Validação de resultados:
    1. Verificação de completude
    2. Verificação de consistência
    3. Verificação de valores esperados
    4. Comparação com dados originais
    """
    problemas = []
    
    # 1. Verificação de completude
    if "total_programas" not in resultados:
        problemas.append("Campo 'total_programas' ausente")
    
    # 2. Verificação de consistência
    total_esperado = len(self.dados)
    if resultados.get("total_registros") != total_esperado:
        problemas.append(
            f"Inconsistência: esperado {total_esperado}, "
            f"obtido {resultados.get('total_registros')}"
        )
    
    # 3. Verificação de valores esperados
    if resultados.get("total_programas", 0) < 0:
        problemas.append("Número de programas negativo")
    
    return problemas
```

---

## 🔧 **PARTE 4: MODULAÇÃO PARA OUTROS DESCRITORES**

### **4.1. Arquitetura Extensível**

#### **A. Princípios de Extensibilidade**

O sistema foi projetado para ser facilmente extensível:

1. **Interface Padronizada**: Todos os módulos seguem a mesma interface
2. **Independência**: Módulos são independentes e podem ser adicionados sem modificar outros
3. **Configuração Flexível**: Critérios e parâmetros são configuráveis
4. **Reutilização**: Componentes comuns são reutilizáveis

#### **B. Estrutura para Novos Descritores**

**Exemplo de Estrutura**:

```python
class AnaliseDescritor:
    """
    Estrutura base para análise de novos descritores:
    1. Interface padronizada
    2. Configuração flexível
    3. Processamento genérico
    4. Geração de relatórios
    """
    
    def __init__(self, nome_descritor, campo_dados, criterios=None):
        self.nome_descritor = nome_descritor
        self.campo_dados = campo_dados
        self.criterios = criterios or self._criterios_padrao()
        self.dados = None
        self.resultados = {}
    
    def carregar_dados(self, dados):
        """Carrega dados para análise"""
        self.dados = dados
    
    def executar_analise(self):
        """Executa análise específica do descritor"""
        # Implementação específica
        pass
    
    def gerar_relatorio(self):
        """Gera relatório da análise"""
        # Implementação específica
        pass
    
    def _criterios_padrao(self):
        """Define critérios padrão"""
        return {}
```

### **4.2. Processo de Adaptação**

#### **A. Identificação do Novo Descritor**

**Passos**:

1. **Identificação do Campo**: Identificar o campo nos dados que contém o descritor
2. **Análise de Estrutura**: Analisar a estrutura dos dados do descritor
3. **Definição de Critérios**: Definir critérios de análise específicos
4. **Validação**: Validar que o campo existe e tem dados suficientes

**Exemplo**:

```python
def identificar_novo_descritor(self, nome_campo):
    """
    Processo de identificação:
    1. Verificar existência do campo
    2. Analisar estrutura dos dados
    3. Verificar completude
    4. Definir critérios de análise
    """
    # 1. Verificar existência
    if nome_campo not in self.dados.columns:
        raise ValueError(f"Campo '{nome_campo}' não encontrado")
    
    # 2. Analisar estrutura
    valores_unicos = self.dados[nome_campo].nunique()
    valores_nulos = self.dados[nome_campo].isnull().sum()
    percentual_nulos = (valores_nulos / len(self.dados)) * 100
    
    # 3. Verificar completude
    if percentual_nulos > 90:
        raise ValueError(
            f"Campo '{nome_campo}' tem mais de 90% de valores nulos"
        )
    
    # 4. Definir critérios
    criterios = {
        "campo": nome_campo,
        "valores_unicos": valores_unicos,
        "completude": 100 - percentual_nulos,
        "tipo_analise": self._determinar_tipo_analise(nome_campo)
    }
    
    return criterios
```

#### **B. Criação de Módulo de Análise**

**Processo**:

1. **Criar Classe Baseada em Template**: Usar template de módulo existente
2. **Implementar Lógica Específica**: Implementar lógica de análise específica
3. **Integrar com Sistema**: Integrar com o orquestrador principal
4. **Testar e Validar**: Testar com dados reais

**Exemplo**:

```python
class AnaliseTemas(MapeamentoProgramas):
    """
    Exemplo de adaptação para análise de temas:
    - Reutiliza estrutura de MapeamentoProgramas
    - Adapta para campo 'temas'
    - Define critérios específicos
    """
    
    def __init__(self):
        super().__init__()
        self.campo_analise = "temas"
        self.nome_analise = "Análise de Temas"
    
    def mapear_temas(self):
        """
        Adaptação do mapeamento de programas para temas:
        1. Identificar coluna de temas
        2. Processar temas (podem ser listas)
        3. Contar ocorrências
        4. Classificar por frequência
        """
        # Identificar coluna
        coluna_temas = "temas"
        
        # Processar temas (podem estar como strings separadas por vírgula)
        todos_temas = []
        for temas_str in self.dados[coluna_temas].dropna():
            if isinstance(temas_str, str):
                temas = [t.strip() for t in temas_str.split(",")]
                todos_temas.extend(temas)
        
        # Contar ocorrências
        from collections import Counter
        contagem_temas = Counter(todos_temas)
        
        # Classificar
        temas_ordenados = dict(
            sorted(
                contagem_temas.items(),
                key=lambda x: x[1],
                reverse=True
            )
        )
        
        return temas_ordenados
```

#### **C. Configuração de Critérios**

**Processo**:

1. **Definir Critérios Específicos**: Critérios específicos para o descritor
2. **Criar Arquivo de Configuração**: Arquivo de configuração separado
3. **Integrar com Sistema**: Integrar critérios com o sistema

**Exemplo**:

```python
# config/analise_temas.yaml
analise_temas:
  campo: "temas"
  separador: ","
  min_ocorrencias: 5
  classificacao:
    muito_frequente: 50
    frequente: 20
    moderado: 10
    raro: 5
  
# Uso no código
def carregar_configuracao(self, arquivo_config):
    """Carrega configuração de arquivo YAML"""
    import yaml
    
    with open(arquivo_config, 'r') as f:
        config = yaml.safe_load(f)
    
    self.criterios = config.get('analise_temas', {})
    return self.criterios
```

### **4.3. Exemplo Prático: Adaptação para DEIA**

#### **A. Contexto**

DEIA (Diversidade, Equidade, Inclusão e Acessibilidade) é um exemplo de descritor que foi adaptado ao sistema.

#### **B. Processo de Adaptação**

**1. Identificação do Descritor**:

```python
DESCRITORES_DEIA = [
    "Diversidade, Equidade e Inclusão",
    "Diversidade, Equidade, Inclusão e Acessibilidade",
    "Inclusão, Diversidade, Equidade",
    # ... mais descritores
]
```

**2. Criação de Módulo de Análise**:

```python
class AnaliseDEIA:
    """
    Módulo específico para análise DEIA:
    - Busca descritores em múltiplos campos
    - Classifica por tipo de descritor
    - Gera estatísticas específicas
    """
    
    def __init__(self):
        self.descritores = DESCRITORES_DEIA
        self.dados = None
    
    def analisar_deia(self, dados):
        """
        Análise DEIA completa:
        1. Buscar descritores em todos os campos relevantes
        2. Classificar por tipo de descritor
        3. Contar ocorrências
        4. Gerar estatísticas
        """
        resultados = {
            "cursos_com_deia": 0,
            "cursos_sem_deia": 0,
            "descritores_encontrados": {},
            "campos_analisados": []
        }
        
        # Campos a analisar
        campos_analise = [
            "no_curso",
            "ds_curso",
            "descricao_oferta",
            "palavras_chave",
            "temas"
        ]
        
        for campo in campos_analise:
            if campo in dados.columns:
                resultados["campos_analisados"].append(campo)
                
                # Buscar descritores
                for descritor in self.descritores:
                    ocorrencias = dados[campo].str.contains(
                        descritor,
                        case=False,
                        na=False
                    ).sum()
                    
                    if ocorrencias > 0:
                        if descritor not in resultados["descritores_encontrados"]:
                            resultados["descritores_encontrados"][descritor] = 0
                        resultados["descritores_encontrados"][descritor] += ocorrencias
        
        # Contar cursos com/sem DEIA
        resultados["cursos_com_deia"] = sum(
            1 for desc in resultados["descritores_encontrados"].values()
            if desc > 0
        )
        resultados["cursos_sem_deia"] = len(dados) - resultados["cursos_com_deia"]
        
        return resultados
```

**3. Integração com Sistema Principal**:

```python
# No analisador_geral.py
def analisar_deia(self):
    """Integração da análise DEIA"""
    from analise.analise_deia import AnaliseDEIA
    
    analisador_deia = AnaliseDEIA()
    analisador_deia.carregar_dados(self.dados)
    resultados = analisador_deia.analisar_deia(self.dados)
    
    return resultados
```

### **4.4. Guia de Extensão para Novos Descritores**

#### **A. Passo a Passo**

**1. Identificar o Novo Descritor**:
   - Qual campo contém o descritor?
   - Qual é a estrutura dos dados?
   - Quais são os critérios de análise?

**2. Criar Módulo de Análise**:
   - Criar classe baseada em template
   - Implementar lógica específica
   - Definir critérios de análise

**3. Integrar com Sistema**:
   - Adicionar ao orquestrador
   - Criar função de geração de relatórios
   - Testar com dados reais

**4. Documentar**:
   - Documentar o novo descritor
   - Documentar critérios de análise
   - Documentar uso

#### **B. Template de Módulo**

```python
"""
Template para novo módulo de análise de descritor
"""
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime

class AnaliseNovoDescritor:
    """
    Template para análise de novo descritor.
    
    Substituir:
    - 'NovoDescritor' pelo nome do descritor
    - Implementar métodos específicos
    - Definir critérios de análise
    """
    
    def __init__(self, dados: pd.DataFrame = None):
        """
        Inicialização do módulo.
        
        Args:
            dados: DataFrame com os dados
        """
        self.dados = dados
        self.resultados = {}
        self.criterios = self._criterios_padrao()
    
    def _criterios_padrao(self) -> Dict:
        """
        Define critérios padrão para análise.
        
        Returns:
            Dicionário com critérios
        """
        return {
            "campo_analise": "campo_descritor",
            "min_ocorrencias": 1,
            "classificacao": {}
        }
    
    def carregar_dados(self, dados: pd.DataFrame):
        """
        Carrega dados para análise.
        
        Args:
            dados: DataFrame com os dados
        """
        self.dados = dados
    
    def executar_analise(self) -> Dict[str, Any]:
        """
        Executa análise específica do descritor.
        
        Returns:
            Dicionário com resultados da análise
        """
        if self.dados is None:
            return {}
        
        # Implementar lógica específica aqui
        resultados = {
            "total_registros": len(self.dados),
            "timestamp_analise": datetime.now().isoformat(),
            # Adicionar resultados específicos
        }
        
        self.resultados = resultados
        return resultados
    
    def validar_resultados(self) -> List[str]:
        """
        Valida resultados da análise.
        
        Returns:
            Lista de problemas encontrados (vazia se tudo OK)
        """
        problemas = []
        
        # Implementar validações específicas
        
        return problemas
    
    def gerar_relatorio(self) -> str:
        """
        Gera relatório textual da análise.
        
        Returns:
            String com relatório formatado
        """
        if not self.resultados:
            return "❌ Nenhum resultado disponível!"
        
        # Implementar geração de relatório
        
        return "Relatório gerado"
```

---

## 📊 **CONCLUSÃO**

Este documento apresentou uma explicação extensa e detalhada do processo completo de criação do Sistema UNA-SUS, abordando:

1. **Processo de Criação**: Desde a concepção até a implementação final
2. **Cuidado com Falhas**: Sistemas robustos de tratamento de erros e validação
3. **Processo de Encontrar Resultados**: Metodologias de análise e descoberta
4. **Modulação para Outros Descritores**: Arquitetura extensível e processo de adaptação

O sistema foi desenvolvido com foco em:
- **Robustez**: Tratamento completo de erros
- **Extensibilidade**: Fácil adaptação para novos descritores
- **Reprodutibilidade**: Metodologia clara e documentada
- **Transparência**: Logging e validação em todos os níveis

Esta arquitetura permite que o sistema seja facilmente adaptado para novos descritores e tipos de análise, mantendo a qualidade e confiabilidade dos resultados.

---

*Documento de Processo de Criação do Sistema UNA-SUS - Versão 1.0*  
*Última atualização: 2025-01-31*

