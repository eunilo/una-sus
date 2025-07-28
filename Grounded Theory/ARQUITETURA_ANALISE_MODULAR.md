# 🏗️ Arquitetura de Análise Modular - UNA-SUS

## 📋 Visão Geral

A nova arquitetura implementa uma **separação completa** entre coleta de dados e análises, garantindo a integridade do database original e permitindo análises flexíveis e não-destrutivas.

## 🎯 Princípios Fundamentais

### 1. 📊 **Coleta Completa e Fiel**
- Coleta **TODOS** os dados disponíveis da UNA-SUS
- **NÃO** aplica filtros durante a coleta
- Preserva integridade dos dados originais
- Database fiel e atualizado

### 2. 🔍 **Análises Separadas e Flexíveis**
- Análises executadas **após** a coleta
- **NÃO** modificam dados originais
- Múltiplos tipos de análise disponíveis
- Resultados independentes

### 3. 🧩 **Modularidade Total**
- Cada tipo de análise em módulo separado
- Fácil adição de novas análises
- Reutilização de código
- Manutenção simplificada

## 🏛️ Arquitetura do Sistema

```
📁 UNA-SUS Project
├── 📊 COLETA COMPLETA
│   ├── coletor_unasus_completo.py
│   └── dados/ (database fiel)
│
├── 🔍 ANÁLISES MODULARES
│   ├── processador_deia.py (análise DEIA)
│   ├── analisador_geral.py (análises flexíveis)
│   └── [futuros analisadores]
│
└── 🔄 ORQUESTRADOR
    └── coleta_e_processamento_separados.py
```

## 📦 Módulos Disponíveis

### 1. 📊 **Coletor Completo** (`coletor_unasus_completo.py`)
```python
# Coleta TODOS os dados sem filtros
coletor = ColetorUnasusCompleto()
dados = coletor.coletar_dados_completos()
```

**Características:**
- ✅ Coleta completa de dados UNA-SUS
- ✅ Preserva todos os campos originais
- ✅ Checkpointing robusto
- ✅ Logs detalhados
- ✅ Validação de integridade

### 2. 🔍 **Processador DEIA** (`processador_deia.py`)
```python
# Análise específica DEIA
processador = ProcessadorDEIA()
processador.dados_originais = dados_coletados
resultados = processador.processar_analise_deia()
```

**Características:**
- ✅ Análise DEIA não-destrutiva
- ✅ Descritores expandidos
- ✅ Categorização automática
- ✅ Relatórios específicos
- ✅ Estatísticas detalhadas

### 3. 📊 **Analisador Geral** (`analisador_geral.py`)
```python
# Análises flexíveis e configuráveis
analisador = AnalisadorGeral()
analisador.configurar_analise('estatistica')
resultados = analisador.executar_analise()
```

**Tipos de Análise Disponíveis:**
- 📈 **Estatística**: Análise geral dos dados
- 📂 **Categoria**: Análise por categorias específicas
- 📅 **Temporal**: Análise de datas e períodos
- 🌍 **Geográfica**: Análise de localização
- 📝 **Conteúdo**: Análise de textos e conteúdo
- ⚖️ **Comparativa**: Análise comparativa entre campos
- 🔧 **Customizada**: Análise com parâmetros específicos

## 🔄 Fluxo de Trabalho

### **Opção 1: Workflow Completo**
```
1. 📊 Coleta Completa → Database Fiel
2. 🔍 Processamento DEIA → Análise DEIA
3. 📈 Análise Geral → Estatísticas Gerais
```

### **Opção 2: Análises Independentes**
```
Database Fiel → [Análise DEIA] [Análise Geral] [Análise Customizada]
```

### **Opção 3: Análises Sequenciais**
```
Database Fiel → Análise A → Análise B → Análise C
```

## 🎛️ Como Usar

### **1. Coleta Completa**
```bash
cd "Grounded Theory"
python coleta_e_processamento_separados.py
# Opção 1: Workflow completo
# Opção 3: Apenas coleta
```

### **2. Análise DEIA**
```bash
# Opção 4: Apenas processamento DEIA
# Opção 2: Dados existentes + DEIA
```

### **3. Análise Geral**
```bash
# Opção 5: Análise estatística
# Opção 6: Análise customizada
```

### **4. Análise Customizada**
```python
from modulos.analisador_geral import AnalisadorGeral

analisador = AnalisadorGeral()
analisador.carregar_dados_para_analise("dados/unasus_dados_completos.json")

# Análise por categoria
analisador.configurar_analise('categoria', {'campo_categoria': 'area_tematica'})
resultados = analisador.executar_analise()

# Análise temporal
analisador.configurar_analise('temporal')
resultados = analisador.executar_analise()

# Análise customizada
parametros = {
    'filtros': {'status': 'Ativo'},
    'campos_analise': ['titulo', 'area_tematica']
}
analisador.configurar_analise('customizada', parametros)
resultados = analisador.executar_analise()
```

## 📊 Estrutura de Dados

### **Database Original (Fiel)**
```json
{
  "id": "curso_123",
  "titulo": "Nome do Curso",
  "descricao": "Descrição completa",
  "area_tematica": "Saúde Pública",
  "status": "Ativo",
  "vagas": 100,
  "data_inicio": "2025-01-15",
  "instituicao": "UNA-SUS",
  "modalidade": "EAD",
  "carga_horaria": 60,
  "publico_alvo": "Profissionais de saúde",
  "objetivos": "Objetivos do curso",
  "metodologia": "Metodologia utilizada",
  "avaliacao": "Critérios de avaliação",
  "certificacao": "Tipo de certificação"
}
```

### **Resultados DEIA**
```json
{
  "resumo_geral": {
    "total_cursos": 150,
    "cursos_com_elementos_deia": 45,
    "percentual_deia": 30.0
  },
  "categorias_deia": {
    "diversidade": 15,
    "equidade": 12,
    "inclusao": 18,
    "acessibilidade": 8
  },
  "cursos_deia": [...]
}
```

### **Resultados Análise Geral**
```json
{
  "resumo_geral": {
    "total_cursos": 150,
    "campos_disponiveis": ["titulo", "descricao", ...],
    "campos_preenchidos": {"titulo": 150, "descricao": 145, ...}
  },
  "estatisticas_numericas": {
    "vagas": {
      "media": 85.5,
      "mediana": 80,
      "min": 10,
      "max": 500
    }
  },
  "estatisticas_categoricas": {
    "area_tematica": {
      "valores_unicos": 8,
      "top_valores": {"Saúde Pública": 45, ...}
    }
  }
}
```

## 🎯 Vantagens da Nova Arquitetura

### ✅ **Integridade de Dados**
- Database original sempre preservado
- Coleta fiel e completa
- Sem perda de informações

### ✅ **Flexibilidade**
- Múltiplos tipos de análise
- Análises independentes
- Fácil customização

### ✅ **Modularidade**
- Módulos independentes
- Fácil manutenção
- Reutilização de código

### ✅ **Escalabilidade**
- Novos analisadores fáceis de adicionar
- Análises em paralelo
- Processamento otimizado

### ✅ **Rastreabilidade**
- Logs detalhados
- Checkpoints
- Relatórios completos

## 🚀 Próximos Passos

### **1. Novos Analisadores**
- 📊 Analisador de Tendências
- 🎯 Analisador de Qualidade
- 📈 Analisador de Performance
- 🔍 Analisador de Padrões

### **2. Melhorias**
- ⚡ Processamento paralelo
- 🎨 Visualizações gráficas
- 📱 Interface web
- 🔗 API REST

### **3. Integrações**
- 🗄️ Banco de dados
- ☁️ Cloud storage
- 📊 Dashboards
- 🔄 ETL automatizado

## 📚 Documentação Relacionada

- `MODELO_TEORIA_FUNDAMENTADA.md` - Metodologia completa
- `GUIA_RAPIDO.md` - Guia de uso rápido
- `README.md` - Documentação geral
- `CORRECAO_OPENPYXL.md` - Correções técnicas

---

*Arquitetura modular implementada com sucesso! 🎉* 