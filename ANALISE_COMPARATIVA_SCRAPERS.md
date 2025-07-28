# 🔍 Análise Comparativa: Scraper Original vs. Modelo Modular

## 📋 Visão Geral da Comparação

Esta análise compara o **`scraper_unasus.py`** (versão original robusta) com o **sistema modular de coleta** implementado na pasta `Grounded Theory`, especificamente o **`coletor_unasus_completo.py`**.

---

## 🎯 Objetivos da Comparação

### **Scraper Original (`scraper_unasus.py`)**
- ✅ **Coleta básica** de dados UNA-SUS
- ✅ **Análise DEIA integrada** durante a coleta
- ✅ **Extração de ofertas** detalhadas
- ✅ **Salvamento incremental** em CSV
- ✅ **Controle de duplicatas** por ID

### **Sistema Modular (`coletor_unasus_completo.py`)**
- ✅ **Coleta completa** sem filtros
- ✅ **Separação** entre coleta e análise
- ✅ **Database fiel** preservado
- ✅ **Sistema robusto** de logging
- ✅ **Checkpointing avançado**

---

## 🏗️ Arquitetura Comparativa

### **1. Estrutura de Código**

#### **A. Scraper Original (Monolítico)**
```python
# Estrutura monolítica - tudo em um arquivo
├── Configurações (URL, headers, cookies, payload)
├── Funções de análise DEIA
├── Funções de extração de ofertas
├── Loop principal de coleta
└── Salvamento incremental
```

**Características:**
- 📁 **1 arquivo** com todas as funcionalidades
- 🔄 **Coleta + Análise** integradas
- 📊 **Filtros DEIA** aplicados durante coleta
- 💾 **Salvamento direto** em CSV

#### **B. Sistema Modular (Separado)**
```python
# Estrutura modular - separação de responsabilidades
├── ColetorUnasusCompleto (coleta pura)
├── ProcessadorDEIA (análise separada)
├── AnalisadorGeral (análises flexíveis)
└── Orquestrador (coordenação)
```

**Características:**
- 📁 **Múltiplos módulos** especializados
- 🔄 **Coleta independente** da análise
- 📊 **Análises não-destrutivas**
- 💾 **Múltiplos formatos** de saída

---

## 🔧 Comparação Técnica Detalhada

### **1. Configurações de Rede**

#### **A. Scraper Original**
```python
# Configurações básicas
url = "https://www.unasus.gov.br/cursos/rest/busca"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.unasus.gov.br",
    "Referer": "https://www.unasus.gov.br/cursos/busca?status=todos&busca=&ordenacao=Relev%C3%A2ncia%20na%20busca"
}

cookies = {
    "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
    "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
    "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272": "_329a72cffc11d2904ae393c82d0cfb72"
}

payload = {"busca": "", "ordenacao": "Por nome", "status": "Todos", "proximo": 0}
```

#### **B. Sistema Modular**
```python
# Configurações idênticas (baseadas no backup original)
self.url_base = "https://www.unasus.gov.br/cursos/rest/busca"
self.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.unasus.gov.br",
    "Referer": "https://www.unasus.gov.br/cursos/busca?status=todos&busca=&ordenacao=Relev%C3%A2ncia%20na%20busca"
}

self.cookies = {
    "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
    "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
    "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272": "_329a72cffc11d2904ae393c82d0cfb72"
}

self.payload = {
    "busca": "",
    "ordenacao": "Por nome", 
    "status": "Todos",
    "proximo": 0
}
```

**✅ Conclusão**: Configurações **idênticas** - ambos usam o mesmo modelo de requisição.

### **2. Descritores DEIA**

#### **A. Scraper Original (Limitado)**
```python
descritores = [
    "Diversidade, Equidade e Integração",
    "Diversidade, Equidade, Inclusão e Pertencimento",
    "Diversidade, Equidade, Inclusão, Acessibilidade",
    "Diversidade, Igualdade e Inclusão",
    "Diversidade, Igualdade, Inclusão e Acessibilidade",
    "Diversidade, Igualdade, Inclusão, Pertencimento",
    "Equidade, Diversidade e Inclusão",
    "Inclusão, Diversidade, Equidade e Acessibilidade",
    "Inclusão, Diversidade, Equidade, Acessibilidade"
]
```

**Características:**
- 📝 **10 descritores** específicos
- 🎯 **Foco em frases completas**
- 🔍 **Aplicado durante coleta**

#### **B. Sistema Modular (Expandido)**
```python
DESCRITORES_DEIA = {
    "diversidade": [
        "diversidade", "diverso", "pluralidade", "multicultural",
        "intercultural", "transcultural", "multirracial", "heterogeneidade"
    ],
    "equidade": [
        "equidade", "equitativo", "justiça social", "igualdade",
        "paridade", "equilibrio", "redistribuição", "justiça"
    ],
    "inclusão": [
        "inclusão", "inclusivo", "acolhimento", "integração",
        "participação", "pertencimento", "comunidade", "aceitação"
    ],
    "acessibilidade": [
        "acessibilidade", "acessível", "acesso", "barreiras",
        "adaptação", "tecnologia assistiva", "design universal"
    ],
    "populações_específicas": [
        "população negra", "indígena", "quilombola", "ribeirinha",
        "pessoas com deficiência", "LGBTQIA+", "mulheres", "idosos"
    ]
}
```

**Características:**
- 📝 **50+ descritores** organizados por categoria
- 🎯 **Foco em palavras-chave**
- 🔍 **Aplicado após coleta** (não-destrutivo)

### **3. Processamento de Dados**

#### **A. Scraper Original**
```python
def encontrar_descritor(titulo, descricao, descritores):
    """Encontra descritores DEIA no título e descrição do curso."""
    texto = (titulo or "") + " " + (descricao or "")
    for descritor in descritores:
        if descritor.lower() in texto.lower():
            return descritor
    return ""

# Aplicação durante coleta
encontrado = encontrar_descritor(titulo, descricao, descritores)
curso["tem_deia"] = "Sim" if encontrado else "Não"
curso["deia_encontrado"] = encontrado
```

**Características:**
- 🔍 **Análise simples** (busca exata)
- 📊 **Integrada** na coleta
- 🎯 **Apenas título e descrição**

#### **B. Sistema Modular**
```python
def _identificar_elementos_deia(self, texto: str) -> List[Dict]:
    """Identifica elementos DEIA com contexto."""
    elementos_encontrados = []
    
    for categoria, descritores in self.descritores_deia.items():
        for descritor in descritores:
            if descritor.lower() in texto.lower():
                # Encontrar contexto
                contexto = self._extrair_contexto(texto, descritor)
                elementos_encontrados.append({
                    "categoria": categoria,
                    "descritor": descritor,
                    "contexto": contexto,
                    "campo": campo_origem
                })
    
    return elementos_encontrados
```

**Características:**
- 🔍 **Análise avançada** com contexto
- 📊 **Separada** da coleta
- 🎯 **Múltiplos campos** analisados

### **4. Extração de Ofertas**

#### **A. Scraper Original (Detalhada)**
```python
def extrair_ofertas_do_curso(id_curso):
    """Extrai ofertas de um curso específico com logs detalhados."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"
    
    # Busca ofertas ativas
    for link in soup.find_all("a", href=True):
        if any(pattern in href for pattern in ["/cursos/oferta/", "../oferta/", "oferta/"]):
            id_oferta = href.split("/")[-1]
            if id_oferta.isdigit():
                ofertas.append(id_oferta)
    
    # Busca ofertas encerradas
    botoes_encerradas = soup.find_all("a", string=lambda t: t and "encerrada" in t.lower())
    
    return ofertas

def extrair_dados_oferta(id_oferta):
    """Extrai dados detalhados de uma oferta."""
    # Extração de 20+ campos específicos
    dados = {
        "id_oferta": id_oferta,
        "titulo_oferta": "",
        "carga_horaria": "",
        "vagas": "",
        "inscricoes_abertas": "",
        "data_inicio": "",
        "data_fim": "",
        "coordenador": "",
        "tutores": "",
        "certificacao": "",
        "pre_requisitos": "",
        "objetivos": "",
        "metodologia": "",
        "avaliacao": "",
        "bibliografia": "",
        "temas": "",
        "decs": "",
        "descricao_oferta": "",
        "palavras_chave": ""
    }
```

**Características:**
- 🔍 **Extração detalhada** de ofertas
- 📊 **20+ campos** específicos
- 🎯 **Foco em ofertas** individuais

#### **B. Sistema Modular (Simplificada)**
```python
def _processar_curso_completo(self, curso: Dict) -> Dict:
    """Processa um curso mantendo TODOS os dados originais."""
    curso_processado = curso.copy()
    
    # Adicionar metadados de coleta
    curso_processado["metadata_coleta"] = {
        "timestamp_coleta": datetime.now().isoformat(),
        "pagina_coleta": self.pagina_atual,
        "versao_coletor": "1.0.0",
        "tipo_coleta": "completa_sem_filtros"
    }
    
    # Garantir campos obrigatórios
    campos_obrigatorios = [
        "id", "titulo", "descricao", "carga_horaria", "status",
        "categoria", "publico_alvo", "palavras_chave", "link",
        "vagas", "numero_vagas", "qt_vagas", "vagas_disponiveis",
        "inicio_inscricao", "fim_inscricao", "data_inicio", "data_fim",
        "modalidade", "tipo_curso", "nivel", "area_tematica",
        "instituicao", "coordenador", "tutores", "certificacao",
        "pre_requisitos", "objetivos", "metodologia", "avaliacao",
        "bibliografia"
    ]
```

**Características:**
- 🔍 **Preservação completa** dos dados originais
- 📊 **Metadados** de coleta
- 🎯 **Foco na integridade** dos dados

### **5. Salvamento de Dados**

#### **A. Scraper Original**
```python
# Salvamento incremental
csv_path = "unasus_ofertas_detalhadas.csv"
lote = 10  # Salva a cada 10 cursos

if len(todos_detalhes) >= lote:
    if os.path.exists(csv_path):
        df_existente = pd.read_csv(csv_path, encoding="utf-8-sig")
        df_novo = pd.DataFrame(todos_detalhes)
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
    else:
        df_final = pd.DataFrame(todos_detalhes)
    df_final.to_csv(csv_path, index=False, encoding="utf-8-sig")
```

**Características:**
- 💾 **Apenas CSV**
- 🔄 **Salvamento incremental**
- 📊 **Controle de duplicatas**

#### **B. Sistema Modular**
```python
def _salvar_dados_completos(self):
    """Salva dados em múltiplos formatos."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Salvar em JSON
    json_path = f"dados/unasus_dados_completos_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(self.dados_coletados, f, ensure_ascii=False, indent=2)
    
    # Salvar em CSV
    csv_path = f"dados/unasus_dados_completos_{timestamp}.csv"
    df = pd.DataFrame(self.dados_coletados)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    
    # Salvar em Excel (opcional)
    try:
        excel_path = f"dados/unasus_dados_completos_{timestamp}.xlsx"
        df.to_excel(excel_path, index=False)
    except ImportError:
        self.logger.info("openpyxl não instalado. Pulando salvamento Excel.")
```

**Características:**
- 💾 **Múltiplos formatos** (JSON, CSV, Excel)
- 🔄 **Checkpointing robusto**
- 📊 **Logs detalhados**

### **6. Logging e Monitoramento**

#### **A. Scraper Original**
```python
# Logs básicos com print
print(f"Buscando ofertas do curso {id_curso}...")
print(f"  ✅ Oferta encontrada: {id_oferta}")
print(f"Progresso salvo após {len(cursos_processados)} cursos")
print(f"Página {pagina} processada.")
```

**Características:**
- 📝 **Logs básicos** com print
- 🔄 **Sem persistência** de logs
- 📊 **Informações limitadas**

#### **B. Sistema Modular**
```python
def _configurar_logger(self) -> logging.Logger:
    """Configura o logger para o coletor."""
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger("ColetorUnasusCompleto")
    logger.setLevel(logging.INFO)
    
    # Handler para arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fh = logging.FileHandler(f"logs/coletor_unasus_{timestamp}.log", encoding="utf-8")
    
    # Handler para console
    ch = logging.StreamHandler()
    
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

**Características:**
- 📝 **Logs estruturados** com logging
- 🔄 **Persistência** em arquivos
- 📊 **Informações detalhadas**

---

## 📊 Comparação de Funcionalidades

### **1. Escopo de Coleta**

| Aspecto | Scraper Original | Sistema Modular |
|---------|------------------|-----------------|
| **Dados Coletados** | Cursos + Ofertas | Apenas Cursos |
| **Campos Extraídos** | 20+ campos específicos | Todos os campos originais |
| **Integridade** | Processamento durante coleta | Preservação completa |
| **Filtros** | DEIA aplicado durante coleta | Sem filtros na coleta |

### **2. Análise DEIA**

| Aspecto | Scraper Original | Sistema Modular |
|---------|------------------|-----------------|
| **Descritores** | 10 frases específicas | 50+ palavras-chave |
| **Aplicação** | Durante coleta | Após coleta |
| **Campos Analisados** | Título + Descrição | Múltiplos campos |
| **Contexto** | Não | Sim |
| **Categorização** | Sim/Não | Categorias detalhadas |

### **3. Persistência de Dados**

| Aspecto | Scraper Original | Sistema Modular |
|---------|------------------|-----------------|
| **Formatos** | CSV apenas | JSON, CSV, Excel |
| **Checkpointing** | Básico | Robusto |
| **Controle de Duplicatas** | Por ID de curso | Por ID de curso |
| **Metadados** | Não | Sim |

### **4. Monitoramento**

| Aspecto | Scraper Original | Sistema Modular |
|---------|------------------|-----------------|
| **Logs** | Print básico | Logging estruturado |
| **Persistência** | Não | Sim |
| **Níveis** | Apenas info | Debug, Info, Warning, Error |
| **Relatórios** | Não | Sim |

---

## 🎯 Vantagens e Desvantagens

### **Scraper Original**

#### **✅ Vantagens:**
- 🚀 **Simplicidade**: Código monolítico fácil de entender
- 🔍 **Detalhamento**: Extração detalhada de ofertas
- 📊 **Análise integrada**: DEIA aplicado durante coleta
- 💾 **Salvamento direto**: CSV pronto para uso

#### **❌ Desvantagens:**
- 🔄 **Acoplamento**: Coleta e análise misturadas
- 📊 **Filtros**: Dados filtrados durante coleta
- 💾 **Formato único**: Apenas CSV
- 📝 **Logs limitados**: Sem persistência

### **Sistema Modular**

#### **✅ Vantagens:**
- 🧩 **Modularidade**: Separação clara de responsabilidades
- 📊 **Integridade**: Database fiel preservado
- 🔍 **Flexibilidade**: Análises não-destrutivas
- 💾 **Múltiplos formatos**: JSON, CSV, Excel
- 📝 **Logs robustos**: Persistência e estruturação
- 🔄 **Checkpointing**: Recuperação de falhas

#### **❌ Desvantagens:**
- 🏗️ **Complexidade**: Múltiplos módulos
- 🔍 **Escopo limitado**: Sem extração de ofertas
- 📚 **Curva de aprendizado**: Mais arquivos para entender

---

## 🔄 Fluxos de Trabalho Comparativos

### **1. Scraper Original**
```
🌐 Conexão UNA-SUS
    ↓
📄 Paginação automática
    ↓
🔍 Extração de cursos
    ↓
📊 Análise DEIA (durante coleta)
    ↓
🔍 Extração de ofertas
    ↓
💾 Salvamento CSV incremental
```

### **2. Sistema Modular**
```
🌐 Conexão UNA-SUS
    ↓
📄 Paginação automática
    ↓
🔍 Coleta completa (sem filtros)
    ↓
💾 Salvamento múltiplos formatos
    ↓
📊 Análise DEIA (separada)
    ↓
📈 Análise geral (separada)
```

---

## 🎯 Recomendações de Uso

### **Use Scraper Original quando:**
- 🎯 **Precisa de ofertas detalhadas**
- 🚀 **Quer simplicidade**
- 📊 **Análise DEIA básica é suficiente**
- 💾 **CSV é o formato desejado**

### **Use Sistema Modular quando:**
- 🎯 **Precisa de database fiel**
- 🔍 **Quer análises flexíveis**
- 📊 **Pesquisa acadêmica rigorosa**
- 💾 **Múltiplos formatos de saída**
- 📝 **Logs detalhados necessários**

---

## 🔮 Evolução e Integração

### **Possível Integração:**
```python
# Combinar o melhor dos dois mundos
class ScraperUnasusIntegrado:
    def __init__(self):
        self.coletor = ColetorUnasusCompleto()  # Coleta fiel
        self.extrator_ofertas = ExtratorOfertas()  # Extração detalhada
        self.analisador_deia = ProcessadorDEIA()  # Análise avançada
    
    def executar_coleta_completa(self):
        # 1. Coleta fiel de cursos
        cursos = self.coletor.coletar_dados_completos()
        
        # 2. Extração detalhada de ofertas
        ofertas = self.extrator_ofertas.extrair_ofertas_detalhadas(cursos)
        
        # 3. Análise DEIA não-destrutiva
        analise_deia = self.analisador_deia.processar_analise_deia(cursos)
        
        return cursos, ofertas, analise_deia
```

---

## 📋 Conclusão

### **Resumo da Comparação:**

1. **🔍 Escopo**: Scraper original foca em ofertas detalhadas, sistema modular foca em integridade de dados
2. **📊 Análise**: Scraper original integra DEIA, sistema modular separa análises
3. **💾 Persistência**: Scraper original usa CSV incremental, sistema modular usa múltiplos formatos
4. **📝 Monitoramento**: Scraper original usa logs básicos, sistema modular usa logging estruturado
5. **🏗️ Arquitetura**: Scraper original é monolítico, sistema modular é separado

### **Recomendação Final:**
- **Para pesquisa acadêmica rigorosa**: Use o sistema modular
- **Para análise rápida com ofertas**: Use o scraper original
- **Para desenvolvimento futuro**: Considere integrar as melhores características de ambos

**Ambos os sistemas são válidos e complementares, servindo a diferentes propósitos de pesquisa e análise.** 🎯 