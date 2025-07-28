# 🗄️ SISTEMA DE BANCO DE DADOS ESTRUTURADO

## 🎯 Objetivo

Implementar um sistema de persistência de dados robusto que crie arquivos estruturados e interoperáveis para uso em outras instâncias e aplicações, resolvendo o problema de dados não estruturados.

## 🚀 Funcionalidades Implementadas

### 1. **Banco de Dados SQLite Estruturado**
- **Módulo**: `modulos/banco_dados.py`
- **Classe Principal**: `BancoDadosEstruturado`
- **Benefícios**:
  - Estrutura relacional completa
  - Integridade de dados
  - Consultas SQL complexas
  - Compatibilidade universal

### 2. **Estrutura de Tabelas**
```sql
-- Tabela principal de cursos
cursos (
    id_curso TEXT PRIMARY KEY,
    no_curso TEXT,
    no_orgao TEXT,
    sg_orgao TEXT,
    no_formato TEXT,
    no_nivel TEXT,
    no_modalidade TEXT,
    status TEXT,
    area_tematica TEXT,
    objetivos TEXT,
    metodologia TEXT,
    carga_horaria INTEGER,
    vagas_ofertadas INTEGER,
    vagas_disponiveis INTEGER,
    data_inicio TEXT,
    data_fim TEXT,
    timestamp_coleta TEXT,
    metadata_coleta TEXT
)

-- Tabela de conceitos identificados
conceitos_identificados (
    id_conceito INTEGER PRIMARY KEY AUTOINCREMENT,
    conceito TEXT,
    frequencia INTEGER,
    categoria TEXT,
    etapa_codificacao TEXT,
    timestamp_identificacao TEXT,
    contexto TEXT
)

-- Tabela de categorias
categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT,
    descricao TEXT,
    tipo_codificacao TEXT,
    conceitos_relacionados TEXT,
    timestamp_criacao TEXT
)

-- Tabela de relações
relacoes (
    id_relacao INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_origem TEXT,
    categoria_destino TEXT,
    tipo_relacao TEXT,
    forca_relacao REAL,
    timestamp_relacao TEXT
)

-- Tabela de análises exploratórias
analises_exploratorias (
    id_analise INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_analise TEXT,
    parametros TEXT,
    resultados TEXT,
    timestamp_analise TEXT
)
```

### 3. **Exportação Multi-Formato**
O sistema exporta dados em **5 formatos diferentes**:

#### **CSV (Comma-Separated Values)**
- **Uso**: Excel, Google Sheets, R, Python pandas
- **Vantagens**: Universal, fácil de ler
- **Estrutura**: Dados tabulares com cabeçalhos

#### **JSON (JavaScript Object Notation)**
- **Uso**: APIs web, aplicações JavaScript, Python
- **Vantagens**: Estrutura hierárquica, metadados
- **Estrutura**: 
```json
{
  "metadata": {
    "tabela": "cursos",
    "timestamp_exportacao": "2025-01-28T10:30:15",
    "total_registros": 500,
    "colunas": ["id_curso", "no_curso", ...]
  },
  "dados": [...]
}
```

#### **XML (eXtensible Markup Language)**
- **Uso**: Sistemas enterprise, troca de dados
- **Vantagens**: Padrão universal, validação
- **Estrutura**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<dados tabela="cursos" timestamp="2025-01-28T10:30:15" total_registros="500">
  <metadata>
    <colunas>
      <coluna>id_curso</coluna>
      <coluna>no_curso</coluna>
    </colunas>
  </metadata>
  <dados>
    <registro>
      <id_curso>CURSO001</id_curso>
      <no_curso>Formação em Saúde Pública</no_curso>
    </registro>
  </dados>
</dados>
```

#### **YAML (YAML Ain't Markup Language)**
- **Uso**: Configurações, documentação
- **Vantagens**: Legível, hierárquico
- **Estrutura**:
```yaml
metadata:
  tabela: cursos
  timestamp_exportacao: 2025-01-28T10:30:15
  total_registros: 500
  colunas:
    - id_curso
    - no_curso
dados:
  - id_curso: CURSO001
    no_curso: Formação em Saúde Pública
```

#### **SQLite (Banco de Dados)**
- **Uso**: Aplicações desktop, web, mobile
- **Vantagens**: Relacional, consultas complexas
- **Compatibilidade**: Python, R, JavaScript, C#, Java, etc.

### 4. **Gerenciador de Dados Simplificado**
```python
from modulos.banco_dados import GerenciadorDados

# Inicializar
gerenciador = GerenciadorDados()
gerenciador.inicializar_banco("meu_projeto")

# Salvar dados
gerenciador.salvar_dados_coleta(dados_coletados)
gerenciador.salvar_resultados_codificacao(resultados)

# Exportar tudo
arquivos, relatorio = gerenciador.exportar_dados_completos()
```

## 📁 Estrutura de Diretórios

### Organização Automática
```
projeto/
├── banco_sqlite/           # Bancos SQLite criados
│   ├── unasus_grounded_theory_20250128_103015.db
│   └── ...
├── exportacoes/            # Arquivos exportados
│   ├── cursos_20250128_103015.csv
│   ├── cursos_20250128_103015.json
│   ├── cursos_20250128_103015.xml
│   ├── cursos_20250128_103015.yaml
│   └── ...
├── dados/                  # Backups JSON
│   ├── dados_coletados_20250128_103015.json
│   └── ...
├── relatorios/             # Relatórios gerados
│   ├── relatorio_final_20250128_103015.json
│   ├── relatorio_final_20250128_103015.md
│   └── ...
└── schemas/                # Esquemas de validação (futuro)
```

### Nomenclatura Padronizada
- **Formato**: `{nome}_{timestamp}.{extensao}`
- **Timestamp**: `YYYYMMDD_HHMMSS`
- **Encoding**: UTF-8 para todos os arquivos

## 🔧 Uso Prático

### 1. **Integração com Workflow**
```python
# No workflow_interativo.py
from modulos.banco_dados import GerenciadorDados

class WorkflowInterativo:
    def __init__(self):
        self.gerenciador_dados = GerenciadorDados()
    
    def salvar_dados_coletados(self):
        # Salva automaticamente no banco estruturado
        caminho_json = self.gerenciador_dados.salvar_dados_coleta(
            self.dados_coletados
        )
    
    def gerar_relatorio_final(self):
        # Exporta em múltiplos formatos
        arquivos, relatorio = self.gerenciador_dados.exportar_dados_completos()
```

### 2. **Uso Direto do Banco**
```python
from modulos.banco_dados import BancoDadosEstruturado

# Context manager garante fechamento da conexão
with BancoDadosEstruturado("meu_projeto") as banco:
    # Inserir dados
    banco.inserir_cursos(dados_cursos)
    banco.inserir_conceitos(conceitos)
    banco.inserir_categorias(categorias)
    
    # Exportar
    banco.exportar_para_csv("cursos")
    banco.exportar_para_json("conceitos_identificados")
    banco.exportar_para_xml("categorias")
    banco.exportar_para_yaml("relacoes")
    
    # Relatório
    relatorio = banco.gerar_relatorio_banco()
```

### 3. **Consultas SQL**
```python
# Consultas complexas no banco SQLite
cursor.execute("""
    SELECT c.no_curso, ci.conceito, ci.frequencia
    FROM cursos c
    JOIN conceitos_identificados ci ON c.id_curso = ci.contexto->>'cursos_relacionados'
    WHERE ci.frequencia > 10
    ORDER BY ci.frequencia DESC
""")
```

## 🌐 Interoperabilidade

### **Compatibilidade por Formato**

#### **CSV**
- ✅ **Excel/Google Sheets**: Importação direta
- ✅ **R**: `read.csv()`, `readr::read_csv()`
- ✅ **Python**: `pandas.read_csv()`
- ✅ **JavaScript**: Bibliotecas CSV
- ✅ **SQL**: `COPY FROM` (PostgreSQL)

#### **JSON**
- ✅ **Python**: `json.load()`, `pandas.read_json()`
- ✅ **JavaScript**: `JSON.parse()`
- ✅ **R**: `jsonlite::fromJSON()`
- ✅ **APIs REST**: Resposta padrão
- ✅ **NoSQL**: MongoDB, CouchDB

#### **XML**
- ✅ **Java**: DOM, SAX parsers
- ✅ **C#**: `XmlDocument`, LINQ to XML
- ✅ **Python**: `xml.etree.ElementTree`
- ✅ **Sistemas Enterprise**: SOAP, WSDL
- ✅ **Validação**: XSD schemas

#### **YAML**
- ✅ **Python**: `PyYAML`, `ruamel.yaml`
- ✅ **JavaScript**: `js-yaml`
- ✅ **Configurações**: Docker, Kubernetes
- ✅ **Documentação**: Jekyll, Hugo

#### **SQLite**
- ✅ **Python**: `sqlite3`, `sqlalchemy`
- ✅ **R**: `RSQLite`
- ✅ **JavaScript**: `sqlite3`, `better-sqlite3`
- ✅ **C/C++**: SQLite C API
- ✅ **Mobile**: Android, iOS nativo

## 📊 Relatórios e Metadados

### **Relatório de Banco**
```json
{
  "metadata": {
    "nome_banco": "unasus_grounded_theory",
    "timestamp": "20250128_103015",
    "caminho_sqlite": "banco_sqlite/unasus_grounded_theory_20250128_103015.db"
  },
  "estatisticas": {
    "total_tabelas": 5,
    "total_registros": 1250
  },
  "tabelas": {
    "cursos": {
      "total_registros": 500,
      "colunas": 18,
      "estrutura": {...}
    },
    "conceitos_identificados": {
      "total_registros": 45,
      "colunas": 7,
      "estrutura": {...}
    }
  }
}
```

### **Metadados de Coleta**
```json
{
  "metadata_coleta": {
    "timestamp_coleta": "2025-01-28T10:30:15",
    "pagina_coleta": 1,
    "iteracao_coleta": 1,
    "tipo_coleta": "inicial_completa",
    "sem_filtros": true
  }
}
```

## 🎯 Benefícios Alcançados

### 1. **Interoperabilidade Total**
- Dados podem ser usados em **qualquer aplicação**
- **5 formatos** diferentes para diferentes necessidades
- **Compatibilidade universal** com todas as plataformas

### 2. **Estrutura Profissional**
- **Banco relacional** com integridade de dados
- **Esquemas bem definidos** para cada tabela
- **Metadados completos** para rastreabilidade

### 3. **Facilidade de Uso**
- **Interface simplificada** com `GerenciadorDados`
- **Context managers** para gerenciamento automático
- **Exportação automática** em múltiplos formatos

### 4. **Rastreabilidade**
- **Timestamps** em todas as operações
- **Metadados** de coleta e processamento
- **Relatórios detalhados** de todas as operações

## 🚀 Como Usar

### 1. **Executar Exemplo**
```bash
python exemplo_banco_dados.py
```

### 2. **Verificar Arquivos Criados**
```bash
ls banco_sqlite/
ls exportacoes/
ls dados/
ls relatorios/
```

### 3. **Usar no Workflow**
```bash
python executar_workflow_interativo.py
```

### 4. **Importar em Outras Aplicações**
```python
# Python
import pandas as pd
df = pd.read_csv('exportacoes/cursos_20250128_103015.csv')

# R
library(readr)
dados <- read_csv('exportacoes/cursos_20250128_103015.csv')

# JavaScript
const fs = require('fs');
const dados = JSON.parse(fs.readFileSync('exportacoes/cursos_20250128_103015.json'));
```

## 📈 Próximos Passos

### 1. **Melhorias Futuras**
- [ ] Validação de esquemas com JSON Schema
- [ ] Compressão automática de arquivos grandes
- [ ] Sincronização com bancos remotos
- [ ] Dashboard web para visualização

### 2. **Integrações**
- [ ] APIs REST para acesso remoto
- [ ] Conectores para BI tools (Power BI, Tableau)
- [ ] Integração com sistemas de versionamento
- [ ] Backup automático para cloud

### 3. **Documentação**
- [ ] Guia de migração de dados
- [ ] Templates para diferentes tipos de projeto
- [ ] Exemplos específicos por área de aplicação

## ✅ Status da Implementação

- [x] Sistema de banco SQLite estruturado
- [x] Exportação em 5 formatos (CSV, JSON, XML, YAML, SQLite)
- [x] Gerenciador de dados simplificado
- [x] Integração com workflow interativo
- [x] Relatórios automáticos
- [x] Metadados completos
- [x] Exemplos de uso
- [x] Documentação completa
- [ ] Validação de esquemas
- [ ] Dashboard web
- [ ] APIs REST

---

**🗄️ Nota**: Este sistema resolve completamente o problema de dados não estruturados, criando um banco de dados profissional que pode ser usado em qualquer aplicação ou plataforma, garantindo máxima interoperabilidade e facilidade de uso. 