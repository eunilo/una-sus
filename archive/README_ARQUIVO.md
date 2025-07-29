# 📦 ARQUIVO - COMPONENTES OBSOLETOS

## 📋 **DESCRIÇÃO**

Esta pasta contém arquivos que foram **obsoletos** ou **substituídos** durante o desenvolvimento do projeto, mas são mantidos para referência histórica e possíveis consultas futuras.

## 📁 **ESTRUTURA**

```
arquivo/
├── 📄 README_ARQUIVO.md              # Este arquivo
├── 📄 coletor_database_geral.py      # Versão anterior do database
├── 📄 analisar_dados_coletados.py    # Análise básica (substituída)
├── 📄 analisar_dados_existentes.py   # Análise básica (substituída)
├── 📄 ESTADO_ORIGINAL_LIMPO.md       # Estado anterior do projeto
├── 📄 PLANO_DATABASE_GERAL.md        # Plano anterior do database
└── 📁 examples_deia/                 # Exemplos DEIA (removidos)
    ├── testar_busca_deia.py
    └── reanalisar_deia_existente.py
```

## 🔄 **MOTIVOS DO ARQUIVAMENTO**

### **1. Substituição por Versões Melhoradas**
- `coletor_database_geral.py` → `database_geral.py` (versão completa)
- `analisar_dados_*.py` → Funcionalidade integrada no database_geral.py

### **2. Mudança de Metodologia**
- Exemplos DEIA removidos (foco em dados completos)
- Documentação de estado anterior

### **3. Simplificação do Projeto**
- Remoção de funcionalidades desnecessárias
- Foco no database completo e funcional

## ⚠️ **IMPORTANTE**

- **NÃO EXECUTE** estes arquivos no projeto atual
- Use apenas para **referência histórica**
- O sistema atual está em `database_geral.py`

## 📅 **DATA DE ARQUIVAMENTO**

29/07/2025 - Durante a implementação do database completo 