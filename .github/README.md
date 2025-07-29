# 🏥 UNA-SUS - Sistema de Coleta e Análise de Dados Educacionais

> **📚 Projeto Educacional para Pesquisa em Saúde Pública**  
> Sistema modular e profissional para coletar e analisar dados de cursos da Universidade Aberta do SUS (UNA-SUS).

## 🎯 **Sobre Este Projeto**

Este é o **projeto principal** do sistema UNA-SUS, desenvolvido com arquitetura modular e profissional para coleta automática de dados educacionais.

### 🚀 **Funcionalidades Principais**

- **🎯 Sistema de Database**: Database SQLite completo com 1.656 registros
- **🕷️ Scrapers Testados**: Coleta confiável de dados UNA-SUS
- **📊 Análises Automáticas**: Estatísticas e relatórios estruturados
- **🧪 Testes Automatizados**: Qualidade garantida
- **📚 Documentação Completa**: Manual e guias detalhados

### 📁 **Estrutura do Projeto**

```
una-sus/
├── 🎯 src/                           # CÓDIGO PRINCIPAL
│   ├── core/                         # Núcleo do sistema
│   ├── scrapers/                     # Módulos de coleta
│   └── utils/                        # Utilitários gerais
├── 📊 data/                          # DADOS
├── 📚 docs/                          # DOCUMENTAÇÃO
├── 🧪 tests/                         # TESTES
├── 📦 scripts/                       # SCRIPTS DE EXECUÇÃO
└── 🗂️ archive/                       # ARQUIVO HISTÓRICO
```

## 🚀 **Como Usar**

### **📋 Instalação Rápida**

```bash
# Clone o repositório
git clone https://github.com/eunilo/una-sus.git
cd una-sus

# Instale as dependências
pip install -r requirements/requirements.txt

# Execute o sistema principal
python src/core/database.py
```

### **🎯 Execução Rápida**

```bash
# Sistema de database
python src/core/database.py

# Scrapers
python src/scrapers/basic.py
python src/scrapers/enhanced.py

# Exemplo de uso
python scripts/run_example.py
```

## 📊 **Dados Disponíveis**

- **1.656 registros** de cursos e ofertas
- **27 campos** originais preservados
- **Database SQLite** completo
- **Exports** em CSV e JSON
- **Análises estatísticas** automáticas

## 🧪 **Testes**

```bash
# Executar todos os testes
python -m pytest tests/

# Testes específicos
python -m pytest tests/test_database.py
python -m pytest tests/test_scrapers.py
```

## 📚 **Documentação**

- **📖 [Documentação Principal](docs/README.md)** - Visão geral completa
- **📋 [Manual de Uso](docs/MANUAL.md)** - Guia detalhado
- **🗂️ [Arquivo Histórico](archive/)** - Componentes obsoletos

## 🤝 **Contribuição**

1. **Fork** o projeto
2. **Crie** uma branch para sua feature
3. **Commit** suas mudanças
4. **Push** para a branch
5. **Abra** um Pull Request

## 📄 **Licença**

Este projeto está licenciado sob a [MIT License](LICENSE).

---

**🎉 Projeto UNA-SUS - Sistema Profissional de Coleta e Análise de Dados Educacionais** 