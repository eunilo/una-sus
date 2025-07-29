# 🤝 Guia de Contribuição - UNA-SUS

Obrigado por considerar contribuir com o projeto UNA-SUS! Este documento fornece diretrizes para contribuições.

## 🎯 **Como Contribuir**

### **📋 Pré-requisitos**

- Python 3.8+
- Git
- Conhecimento básico de Python

### **🚀 Configuração Inicial**

```bash
# Clone o repositório
git clone https://github.com/eunilo/una-sus.git
cd una-sus

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements/requirements.txt
pip install -r requirements/requirements-dev.txt
```

## 🔄 **Fluxo de Trabalho**

### **1. Fork e Clone**
```bash
# Faça fork do repositório no GitHub
# Clone seu fork
git clone https://github.com/SEU_USUARIO/una-sus.git
cd una-sus
```

### **2. Crie uma Branch**
```bash
# Crie uma branch para sua feature
git checkout -b feature/nova-funcionalidade
# ou para correção de bug
git checkout -b fix/correcao-bug
```

### **3. Desenvolva**
- Siga as convenções de código
- Escreva testes para novas funcionalidades
- Atualize a documentação quando necessário

### **4. Teste**
```bash
# Execute os testes
python -m pytest tests/

# Verifique a cobertura
python -m pytest tests/ --cov=src --cov-report=html

# Execute o linting
flake8 src/
black --check src/
isort --check-only src/
```

### **5. Commit e Push**
```bash
# Adicione suas mudanças
git add .

# Faça commit com mensagem descritiva
git commit -m "feat: adiciona nova funcionalidade de análise"

# Push para sua branch
git push origin feature/nova-funcionalidade
```

### **6. Pull Request**
- Crie um Pull Request no GitHub
- Descreva suas mudanças detalhadamente
- Aguarde a revisão e feedback

## 📝 **Convenções de Código**

### **🎨 Formatação**
- Use **Black** para formatação automática
- Use **isort** para ordenação de imports
- Use **flake8** para linting

### **📝 Mensagens de Commit**
Use o padrão **Conventional Commits**:

```
tipo(escopo): descrição

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas de manutenção

**Exemplos:**
```bash
feat(database): adiciona suporte a PostgreSQL
fix(scraper): corrige timeout em requisições
docs(readme): atualiza instruções de instalação
```

### **🏗️ Estrutura de Código**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: Descrição do módulo
==========================

Descrição detalhada do módulo e suas funcionalidades.
"""

import logging
from typing import Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class MinhaClasse:
    """Descrição da classe."""
    
    def __init__(self, parametro: str) -> None:
        """Inicializa a classe.
        
        Args:
            parametro: Descrição do parâmetro
        """
        self.parametro = parametro
    
    def meu_metodo(self, valor: int) -> str:
        """Descrição do método.
        
        Args:
            valor: Descrição do valor
            
        Returns:
            Descrição do retorno
            
        Raises:
            ValueError: Quando valor é inválido
        """
        if valor < 0:
            raise ValueError("Valor deve ser positivo")
        return f"Resultado: {valor}"
```

## 🧪 **Testes**

### **📋 Escrevendo Testes**
```python
import pytest
from src.core.database import DatabaseCompleto


class TestDatabaseCompleto:
    """Testes para a classe DatabaseCompleto."""
    
    def test_inicializacao(self):
        """Testa a inicialização da classe."""
        db = DatabaseCompleto()
        assert db is not None
        assert hasattr(db, 'db_path')
    
    def test_carregar_dados(self):
        """Testa o carregamento de dados."""
        db = DatabaseCompleto()
        # Implementar teste
        pass
```

### **🚀 Executando Testes**
```bash
# Todos os testes
python -m pytest

# Testes específicos
python -m pytest tests/test_database.py

# Com cobertura
python -m pytest --cov=src --cov-report=html

# Testes marcados
python -m pytest -m "not slow"
```

## 📚 **Documentação**

### **📝 Atualizando Documentação**
- Mantenha o README.md atualizado
- Documente novas funcionalidades
- Atualize exemplos de uso
- Adicione docstrings em funções e classes

### **🔗 Links Úteis**
- [Documentação Principal](docs/README.md)
- [Manual de Uso](docs/MANUAL.md)
- [Estrutura do Projeto](ESTRUTURA_PRINCIPAL.md)

## 🐛 **Reportando Bugs**

### **📋 Template de Bug Report**
```markdown
**Descrição do Bug**
Descrição clara e concisa do bug.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

**Comportamento Esperado**
Descrição do que deveria acontecer.

**Comportamento Atual**
Descrição do que está acontecendo.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
- OS: [ex: Windows 10]
- Python: [ex: 3.11.0]
- Versão: [ex: 2.0.0]

**Informações Adicionais**
Qualquer outra informação relevante.
```

## 💡 **Sugerindo Funcionalidades**

### **📋 Template de Feature Request**
```markdown
**Problema/Necessidade**
Descrição clara do problema que a funcionalidade resolveria.

**Solução Proposta**
Descrição da solução que você gostaria de ver implementada.

**Alternativas Consideradas**
Outras soluções que você considerou.

**Informações Adicionais**
Qualquer contexto adicional.
```

## 🏆 **Reconhecimento**

Contribuições significativas serão reconhecidas no README.md e na documentação do projeto.

## 📞 **Contato**

- **Issues**: [GitHub Issues](https://github.com/eunilo/una-sus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/eunilo/una-sus/discussions)

---

**Obrigado por contribuir com o projeto UNA-SUS! 🎉** 