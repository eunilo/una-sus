# 🏥 UNA-SUS - Sistema de Coleta e Análise de Dados Educacionais

> **📚 Projeto Educacional para Pesquisa em Saúde Pública**  
> Sistema modular e profissional para coletar e analisar dados de cursos da Universidade Aberta do SUS (UNA-SUS).

## 🎯 **Sobre Este Projeto**

### 💡 **O que é?**
Sistema **modular e escalável** para coleta automática de dados educacionais da plataforma UNA-SUS, desenvolvido com arquitetura profissional e foco em manutenibilidade.

### 🎓 **Para quem é?**
- **Pesquisadores** em saúde pública e educação
- **Desenvolvedores** interessados em web scraping
- **Analistas de dados** em saúde
- **Estudantes** de graduação e pós-graduação

### 🚀 **Por que usar?**
- ✅ **Arquitetura modular** e profissional
- ✅ **Sistema de database** completo e robusto
- ✅ **Scrapers testados** e confiáveis
- ✅ **Documentação** completa e atualizada
- ✅ **Testes automatizados** para qualidade

---

## 📁 **Estrutura do Projeto**

```
una-sus/
├── 🎯 src/                           # CÓDIGO PRINCIPAL
│   ├── core/                         # Núcleo do sistema
│   │   ├── database.py               # Sistema de database
│   │   ├── scraper.py                # Scrapers principais
│   │   └── analyzer.py               # Análises e estatísticas
│   ├── scrapers/                     # Módulos de coleta
│   │   ├── basic.py                  # Scraper básico
│   │   ├── enhanced.py               # Scraper melhorado
│   │   └── utils.py                  # Utilitários
│   └── utils/                        # Utilitários gerais
│       ├── logger.py                 # Sistema de logging
│       └── config.py                 # Configurações
├── 📊 data/                          # DADOS
│   ├── raw/                          # Dados brutos
│   ├── processed/                    # Dados processados
│   └── exports/                      # Exports gerados
├── 📚 docs/                          # DOCUMENTAÇÃO
│   ├── README.md                     # Documentação principal
│   └── MANUAL.md                     # Manual de uso
├── 🧪 tests/                         # TESTES
├── 📦 scripts/                       # SCRIPTS DE EXECUÇÃO
├── 🐳 docker/                        # CONTAINERIZAÇÃO
├── ⚙️ config/                        # CONFIGURAÇÕES
├── 📋 requirements/                  # DEPENDÊNCIAS
└── 🗂️ archive/                       # ARQUIVO HISTÓRICO
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

### **🎯 Execução Rápida**

#### **1. Inicialização Simples (Recomendado)**
```bash
# Script principal com menu interativo
python start.py
```

#### **2. Coletor Database Geral (Principal)**
```bash
# Executar coletor principal
python coletor_database_geral.py
```

#### **3. Sistema de Database (Menu Interativo)**
```bash
# Executar sistema principal com menu
python run_database.py
```

#### **4. Scrapers Diretos**
```bash
# Scraper básico
python run_scraper_basic.py

# Scraper melhorado
python run_scraper_enhanced.py
```

#### **5. Scripts de Exemplo**
```bash
# Exemplo de uso
python scripts/run_example.py
```

#### **6. Execução Direta (Alternativa)**
```bash
# Sistema de database
python src/core/database.py

# Scrapers
python src/scrapers/basic.py
python src/scrapers/enhanced.py
```

### **🐳 Docker (Opcional)**
```bash
# Construir e executar
docker-compose -f docker/docker-compose.yml up --build
```

---

## 📊 **Funcionalidades Principais**

### **🎯 Coletor Database Geral**
- **Coleta completa** de dados UNA-SUS
- **Database SQLite** robusto e atualizado
- **1.656 registros** de cursos e ofertas
- **27 campos** originais preservados
- **Checkpointing** e logs detalhados
- **Exports** em CSV e JSON
- **Análises estatísticas** automáticas

### **🕷️ Scrapers**
- **Scraper Básico**: Coleta fundamental e confiável
- **Scraper Melhorado**: Funcionalidades avançadas
- **Sistema de logging** detalhado
- **Tratamento de erros** robusto

### **📈 Análises**
- **Estatísticas completas** dos dados
- **Análises por instituição** e modalidade
- **Exports estruturados** para outras aplicações
- **Relatórios automáticos**

---

## 🧪 **Testes**

```bash
# Executar todos os testes
python -m pytest tests/

# Testes específicos
python -m pytest tests/test_database.py
python -m pytest tests/test_scrapers.py
```

---

## 📚 **Documentação**

- **📖 [Documentação Principal](docs/README.md)** - Visão geral completa
- **📋 [Manual de Uso](docs/MANUAL.md)** - Guia detalhado
- **🗂️ [Arquivo Histórico](archive/)** - Componentes obsoletos

---

## 🔧 **Desenvolvimento**

### **📁 Estrutura de Desenvolvimento**
```
src/
├── core/          # Funcionalidades principais
├── scrapers/      # Módulos de coleta
└── utils/         # Utilitários gerais
```

### **🧪 Testes**
```
tests/
├── test_database.py    # Testes do database
├── test_scrapers.py    # Testes dos scrapers
└── test_analyzer.py    # Testes das análises
```

### **📦 Scripts**
```
scripts/
├── run_example.py      # Exemplo de uso
├── run_scraper.py      # Executar scraper
└── run_database.py     # Executar database
```

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

**🎉 Projeto UNA-SUS - Sistema Profissional de Coleta e Análise de Dados Educacionais** 