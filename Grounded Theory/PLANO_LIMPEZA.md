# 🧹 PLANO DE LIMPEZA - DIRETÓRIO GROUNDED THEORY

## 📋 **ESTRATÉGIA DE LIMPEZA**

### **🎯 OBJETIVOS:**
- Manter apenas arquivos essenciais para funcionamento
- Organizar estrutura de diretórios
- Remover arquivos temporários e duplicados
- Preservar funcionalidade do código

## 📁 **ARQUIVOS A MANTER (ESSENCIAIS)**

### **🔧 Código Principal**
- `grounded_theory_metodologica.py` - Sistema principal ✅
- `orquestrador_grounded_theory.py` - Orquestrador ✅
- `modulos/` - Módulos de codificação ✅

### **📋 Documentação Principal**
- `README.md` - Documentação principal ✅
- `GUIA_WORKFLOW_LOGICO.md` - Guia do workflow ✅
- `RESUMO_FINAL_IMPLEMENTACAO.md` - Resumo da implementação ✅
- `COMPARACAO_COLETA.md` - Análise técnica ✅

### **🧪 Testes Essenciais**
- `teste_coleta_completa.py` - Teste da coleta ✅
- `teste_codificacao_simples.py` - Teste da codificação ✅

### **💾 Dados e Resultados**
- `dados/` - Dados coletados ✅
- `relatorios/` - Relatórios (manter apenas os mais recentes) ✅
- `checkpoints/` - Checkpoints ✅

## 🗑️ **ARQUIVOS A REMOVER**

### **📄 Relatórios Antigos (Manter apenas os 3 mais recentes)**
- `relatorio_workflow_grounded_theory_20250728_185437.md` ✅
- `relatorio_workflow_grounded_theory_20250728_185248.md` ✅
- `relatorio_workflow_grounded_theory_20250728_185117.md` ✅
- `relatorio_workflow_grounded_theory_20250728_184408.md` ❌ REMOVER
- `relatorio_workflow_grounded_theory_20250728_184224.md` ❌ REMOVER
- `relatorio_workflow_grounded_theory_20250728_184049.md` ❌ REMOVER
- `relatorio_grounded_theory_20250728_182132.md` ❌ REMOVER
- `relatorio_grounded_theory_20250728_181201.md` ❌ REMOVER

### **📊 Sistemas Antigos/Obsoletos**
- `workflow_completo_separado.py` ❌ REMOVER (substituído)
- `analise_posterior_dados.py` ❌ REMOVER (substituído)
- `coleta_aberta_grounded_theory.py` ❌ REMOVER (substituído)
- `executar_grounded_theory_dados_reais.py` ❌ REMOVER (substituído)
- `coleta_e_processamento_separados.py` ❌ REMOVER (substituído)
- `grounded_theory_runner.py` ❌ REMOVER (substituído)
- `iniciar_pesquisa.py` ❌ REMOVER (substituído)
- `scraper_unasus_grounded.py` ❌ REMOVER (substituído)

### **📋 Documentação Antiga**
- `GUIA_WORKFLOW_SEPARADO.md` ❌ REMOVER (substituído)
- `ARQUITETURA_ANALISE_MODULAR.md` ❌ REMOVER (obsoleto)
- `RELATORIO_TESTES.md` ❌ REMOVER (obsoleto)
- `GUIA_RAPIDO.md` ❌ REMOVER (obsoleto)
- `MODELO_TEORIA_FUNDAMENTADA.md` ❌ REMOVER (obsoleto)

### **🗂️ Arquivos Temporários**
- `__pycache__/` ❌ REMOVER (cache Python)
- Logs antigos (manter apenas os 5 mais recentes) ❌ REMOVER

## 📁 **ESTRUTURA FINAL DESEJADA**

```
Grounded Theory/
├── 📄 grounded_theory_metodologica.py
├── 📄 orquestrador_grounded_theory.py
├── 📄 scraper_unasus_backup_original.py
├── 📄 README.md
├── 📄 GUIA_WORKFLOW_LOGICO.md
├── 📄 RESUMO_FINAL_IMPLEMENTACAO.md
├── 📄 COMPARACAO_COLETA.md
├── 📄 teste_coleta_completa.py
├── 📄 teste_codificacao_simples.py
├── 📁 modulos/
├── 📁 dados/
├── 📁 relatorios/ (apenas 3 mais recentes)
├── 📁 logs/ (apenas 5 mais recentes)
└── 📁 checkpoints/
```

## ⚠️ **PRECAUÇÕES**

1. **Backup**: Manter `scraper_unasus_backup_original.py` como referência
2. **Dados**: Não remover pasta `dados/` com dados coletados
3. **Módulos**: Não remover pasta `modulos/` com código essencial
4. **Checkpoints**: Manter para recuperação de estado

## 🚀 **EXECUÇÃO**

1. Remover arquivos obsoletos
2. Limpar logs antigos
3. Manter apenas relatórios recentes
4. Verificar funcionamento após limpeza 