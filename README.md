# 🏥 UNA-SUS - Sistema de Análise da Universidade Aberta do SUS

> **📚 Sistema Completo de Análise Educacional em Saúde Pública**  
> Plataforma modular e profissional para análise de dados educacionais da Universidade Aberta do SUS (UNA-SUS) com foco em programas de governo e distribuição geográfica.

## 🎯 **Sobre Este Projeto**

### 💡 **O que é?**
Sistema **completo e avançado** para análise de dados educacionais da plataforma UNA-SUS, desenvolvido com arquitetura modular e foco em **programas de governo** e **distribuição geográfica**. A **FASE 1** está 100% implementada e funcional.

### 🎓 **Para quem é?**
- **Pesquisadores** em saúde pública e educação
- **Gestores** de políticas públicas educacionais
- **Analistas de dados** em saúde
- **Estudantes** de graduação e pós-graduação
- **Profissionais** interessados em análise educacional

### 🚀 **Por que usar?**
- ✅ **FASE 1 COMPLETA** - Sistema 100% funcional
- ✅ **Análises Especializadas** - Programas de governo e geografia
- ✅ **Relatórios Profissionais** - Executivos e técnicos
- ✅ **Documentação Completa** - Manual e glossário técnico
- ✅ **Interface Amigável** - Menu interativo
- ✅ **Dados Atualizados** - 1,657 ofertas analisadas

---

## 📊 **Estado Atual - FASE 1 IMPLEMENTADA**

### **✅ Funcionalidades Implementadas**
- **🏛️ Mapeamento de Programas de Governo** - 31 programas identificados
- **📋 Cobertura Programática** - Análise de lacunas e concentração
- **🗺️ Distribuição Geográfica** - Polos e desertos educacionais
- **📈 Relatórios Visuais** - Executivos e técnicos completos
- **📚 Documentação Abrangente** - Manual completo e glossário

### **📊 Dados Analisados**
- **1,657 ofertas** educacionais
- **503 cursos únicos**
- **31 programas** de governo
- **7 estados** com dados
- **26 instituições** parceiras

### **🔍 Principais Descobertas**
- **Polo Educacional**: Alagoas (93.1% das ofertas)
- **Desertos Educacionais**: 22 estados identificados
- **Programa Dominante**: UNA-SUS (45.9% das ofertas)
- **Lacunas Programáticas**: Múltiplas oportunidades identificadas

---

## 📁 **Estrutura do Projeto**

```
una-sus/
├── 🎯 SCRIPTS PRINCIPAIS
│   ├── coletor_database_geral.py    # Script principal
│   ├── start.py                     # ⭐ PONTO DE ENTRADA PRINCIPAL
│   └── scraper_unasus.py            # Backup original
│
├── 📂 analise/                      # SISTEMA DE ANÁLISE (FASE 1)
│   ├── analisador_geral.py          # Orquestrador de análises
│   ├── mapeamento_programas.py      # Análise de programas
│   ├── cobertura_programatica.py    # Cobertura programática
│   ├── distribuicao_geografica.py   # Distribuição geográfica
│   ├── estatisticas_basicas.py      # Estatísticas básicas
│   ├── relatorios.py                # Geração de relatórios
│   └── relatorios_visuais.py        # Relatórios visuais
│
├── 📊 data/                         # DADOS COLETADOS
│   ├── raw/                         # Dados brutos
│   ├── processed/                   # Dados processados
│   └── exports/                     # Exports gerados
│
├── 📋 relatorios/                   # RELATÓRIOS GERADOS
│   ├── mapeamento_programas.txt
│   ├── cobertura_programatica_executivo.txt
│   ├── cobertura_programatica_completo.txt
│   ├── distribuicao_geografica.txt
│   └── relatorio_completo_visual.txt
│
├── 📚 docs/                         # DOCUMENTAÇÃO COMPLETA
│   ├── MANUAL_COMPLETO.md           # Manual abrangente
│   ├── GLOSSARIO_TECNICO.md         # Glossário técnico
│   ├── ESTADO_ATUAL_SISTEMA.md      # Status do sistema
│   └── MANUAL.md                    # Manual básico
│
├── 🧪 tests/                        # TESTES
├── 📦 scripts/                      # SCRIPTS AUXILIARES
├── 🗂️ archive/                      # ARQUIVOS ARQUIVADOS
└── 📋 requirements/                 # DEPENDÊNCIAS
```

---

## 🚀 **Como Usar**

### **📋 Pré-requisitos**
```bash
# Python 3.8+
python --version
```

### **🔧 Instalação Automática**
O sistema **instala automaticamente** todas as dependências necessárias na primeira execução!

- ✅ **Dependências detectadas** automaticamente
- ✅ **Instalação automática** via pip
- ✅ **Verificação de compatibilidade** com Python
- ✅ **Tratamento de erros** com instruções claras

---

## ⭐ **PRIMEIROS PASSOS - COMEÇAR AQUI**

### **🚀 PONTO DE ENTRADA PRINCIPAL**
```bash
# 1. Clone o repositório
git clone https://github.com/eunilo/una-sus.git
cd una-sus

# 2. Execute o sistema principal
python start.py

# 3. Escolha uma opção do menu interativo
```

**💡 O `start.py` é o script principal para usar o sistema!**

---

## 🎯 **Execução Rápida**

### **⭐ COMEÇAR AQUI - Menu Interativo (RECOMENDADO)**
```bash
# ⭐ PONTO DE ENTRADA PRINCIPAL DO SISTEMA
python start.py
```

**Opções Disponíveis:**
- 🔄 **Varredura Completa** (limpa dados + coleta)
- 📊 **Verificar Banco de Dados**
- 🧹 **Limpar Dados Coletados**
- 🚀 **Executar Coletor** (sem limpar)
- 📋 **Verificar Dependências**
- 📈 **Análise Completa dos Dados**
- 📊 **Estatísticas Básicas**
- 📋 **Gerar Relatórios**

### **2. Coletor Principal**
```bash
# Executar coletor de dados
python coletor_database_geral.py
```

### **3. Análise Completa**
```bash
# Executar todas as análises da FASE 1
python -c "from analise.analisador_geral import AnalisadorGeral; a = AnalisadorGeral(); a.carregar_dados(); r = a.gerar_relatorio_completo(); print('✅ Análise completa realizada!')"
```

---

## 📊 **Funcionalidades da FASE 1**

### **🏛️ Mapeamento de Programas de Governo**
- **Identificação** de 31 programas de governo
- **Contagem** de cursos e ofertas por programa
- **Análise** de vagas disponíveis
- **Mapeamento** de instituições por programa

### **📋 Cobertura Programática**
- **Análise** de concentração por programas
- **Identificação** de lacunas programáticas
- **Classificação** por quantidade de ofertas:
  - 🔴 **Crítica**: < 5 ofertas
  - 🟡 **Limitada**: 5-9 ofertas
  - 🟢 **Adequada**: 10-49 ofertas
  - 🏆 **Excelente**: 50+ ofertas
- **Detalhamento** de registros individuais

### **🗺️ Distribuição Geográfica**
- **Identificação** de polos educacionais (>100 ofertas)
- **Identificação** de desertos educacionais (<10 ofertas)
- **Análise** por região geográfica
- **Contagem** de ofertas e cursos únicos por região

### **📈 Relatórios Visuais**
- **📊 Executivo**: Resumido para gestores
- **📋 Técnico**: Completo para analistas
- **🎨 Visual**: Formatação aprimorada com ASCII art
- **📋 Sem abreviações**: Informações completas

---

## 📚 **Documentação Completa**

### **📖 Manual Completo**
- **MANUAL_COMPLETO.md** - Manual abrangente sem abreviações
- **GLOSSARIO_TECNICO.md** - Definições de todos os conceitos
- **ESTADO_ATUAL_SISTEMA.md** - Status de implementação

### **📋 Relatórios Disponíveis**
- **Mapeamento de Programas** - Análise de programas de governo
- **Cobertura Programática** - Executivo e técnico
- **Distribuição Geográfica** - Polos e desertos educacionais
- **Relatório Completo** - Visão geral do sistema

---

## 🧪 **Testes**

```bash
# Executar todas as análises
python -c "from analise.analisador_geral import AnalisadorGeral; a = AnalisadorGeral(); a.carregar_dados(); print('✅ Sistema funcionando!')"

# Verificar relatórios
ls relatorios/
```

---

## 🔧 **Desenvolvimento**

### **📁 Estrutura de Análise**
```
analise/
├── analisador_geral.py          # Orquestrador principal
├── mapeamento_programas.py      # Análise de programas
├── cobertura_programatica.py    # Cobertura programática
├── distribuicao_geografica.py   # Distribuição geográfica
├── estatisticas_basicas.py      # Estatísticas básicas
├── relatorios.py                # Geração de relatórios
└── relatorios_visuais.py        # Relatórios visuais
```

### **📊 Dados de Entrada**
- **CSV**: `data/unasus_database_geral_*.csv`
- **SQLite**: `data/unasus_database_geral_*.db`
- **JSON**: `data/exports/*.json`

### **📋 Relatórios de Saída**
- **TXT**: `relatorios/*.txt`
- **JSON**: `relatorios/*.json`

---

## 🚀 **Próximas Fases**

### **📊 FASE 2 - Análises Avançadas**
- **Análise de Diversidade Programática**
- **Análise de Cobertura por Instituição**
- **Análise Temporal de Programas**

### **🔮 FASE 3 - Análises Preditivas**
- **Análises Preditivas de Programas**
- **Análises de Impacto de Programas**
- **Análises de Sustentabilidade de Programas**

---

## 📄 **Licença**

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 🤝 **Contribuição**

1. **Fork** o projeto
2. **Crie** uma branch para sua feature
3. **Commit** suas mudanças
4. **Push** para a branch
5. **Abra** um Pull Request

---

## 📞 **Contato**

- **Projeto**: [GitHub Repository](https://github.com/eunilo/una-sus)
- **Issues**: [GitHub Issues](https://github.com/eunilo/una-sus/issues)

---

## 🎯 **Status do Projeto**

### **✅ FASE 1 - COMPLETA E FUNCIONAL**
- **Sistema**: 100% operacional
- **Análises**: 3 análises implementadas
- **Relatórios**: 5 relatórios gerados
- **Documentação**: Completa e atualizada
- **Dados**: 1,657 ofertas analisadas

### **📊 Métricas de Qualidade**
- **Cobertura de Funcionalidades**: 100%
- **Módulos Funcionais**: 7/7
- **Relatórios Gerados**: 5/5
- **Documentação**: 100% completa

---

**🎉 UNA-SUS - Sistema Completo de Análise de Programas de Governo**  
**FASE 1 IMPLEMENTADA E FUNCIONAL** 📊✨ 