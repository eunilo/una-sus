# 🏗️ ESTRUTURA PRINCIPAL - PROJETO UNA-SUS

## 🎯 **VISÃO GERAL**

Este documento define a nova estrutura principal do projeto UNA-SUS, organizando os componentes de forma mais profissional e escalável.

## 📁 **ESTRUTURA PROPOSTA**

```
una-sus/
├── 🎯 src/                           # CÓDIGO PRINCIPAL
│   ├── __init__.py
│   ├── core/                         # Núcleo do sistema
│   │   ├── __init__.py
│   │   ├── database.py               # Sistema de database
│   │   ├── scraper.py                # Scrapers principais
│   │   └── analyzer.py               # Análises e estatísticas
│   ├── scrapers/                     # Módulos de coleta
│   │   ├── __init__.py
│   │   ├── basic.py                  # scraper_unasus.py
│   │   ├── enhanced.py               # scraper_unasus_melhorado.py
│   │   └── utils.py                  # Utilitários de scraping
│   └── utils/                        # Utilitários gerais
│       ├── __init__.py
│       ├── logger.py                 # Sistema de logging
│       └── config.py                 # Configurações
├── 📊 data/                          # DADOS
│   ├── raw/                          # Dados brutos
│   │   └── unasus_ofertas_detalhadas.csv
│   ├── processed/                    # Dados processados
│   └── exports/                      # Exports gerados
├── 📚 docs/                          # DOCUMENTAÇÃO
│   ├── README.md                     # Documentação principal
│   ├── MANUAL.md                     # Manual de uso
│   ├── API.md                        # Documentação da API
│   └── CHANGELOG.md                  # Histórico de mudanças
├── 🧪 tests/                         # TESTES
│   ├── __init__.py
│   ├── test_scrapers.py
│   ├── test_database.py
│   └── test_analyzer.py
├── 📦 scripts/                       # SCRIPTS DE EXECUÇÃO
│   ├── run_scraper.py                # Executar scraper
│   ├── run_database.py               # Executar database
│   └── run_analysis.py               # Executar análises
├── 🐳 docker/                        # CONTAINERIZAÇÃO
│   ├── Dockerfile
│   └── docker-compose.yml
├── ⚙️ config/                        # CONFIGURAÇÕES
│   ├── settings.py                   # Configurações principais
│   └── logging.conf                  # Configuração de logs
├── 📋 requirements/                  # DEPENDÊNCIAS
│   ├── requirements.txt              # Produção
│   ├── requirements-dev.txt          # Desenvolvimento
│   └── requirements-test.txt         # Testes
├── 🗂️ archive/                       # ARQUIVO HISTÓRICO
│   └── [componentes obsoletos]
└── 📄 Arquivos de configuração
    ├── pyproject.toml
    ├── setup.py
    ├── .gitignore
    └── LICENSE
```

## 🎯 **BENEFÍCIOS DA NOVA ESTRUTURA**

### **📦 Organização Modular**
- **Separação clara** entre código, dados e documentação
- **Módulos especializados** para cada funcionalidade
- **Fácil manutenção** e escalabilidade

### **🧪 Testabilidade**
- **Testes organizados** por funcionalidade
- **Cobertura de código** estruturada
- **Qualidade garantida**

### **📚 Documentação Profissional**
- **Documentação centralizada** em `docs/`
- **Manual de uso** claro e completo
- **Histórico de mudanças** organizado

### **🚀 Deploy Simplificado**
- **Scripts de execução** padronizados
- **Containerização** pronta
- **Configurações** centralizadas

## 🔄 **PLANO DE MIGRAÇÃO**

### **Fase 1: Estrutura Base**
1. Criar diretórios principais
2. Mover arquivos existentes
3. Criar `__init__.py` files

### **Fase 2: Refatoração**
1. Modularizar código existente
2. Criar sistema de configuração
3. Implementar logging centralizado

### **Fase 3: Testes e Documentação**
1. Criar testes unitários
2. Atualizar documentação
3. Criar scripts de execução

### **Fase 4: Deploy e CI/CD**
1. Configurar Docker
2. Implementar CI/CD
3. Deploy automatizado

## 📊 **MÉTRICAS DE SUCESSO**

- ✅ **Código modular** e reutilizável
- ✅ **Testes cobrindo** 80%+ do código
- ✅ **Documentação** completa e atualizada
- ✅ **Deploy automatizado** e confiável
- ✅ **Performance** mantida ou melhorada

## 🎯 **PRÓXIMOS PASSOS**

1. **Aprovação** da estrutura proposta
2. **Criação** dos diretórios base
3. **Migração** gradual dos arquivos
4. **Refatoração** do código existente
5. **Implementação** de testes
6. **Atualização** da documentação 