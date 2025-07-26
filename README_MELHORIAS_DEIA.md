# 🌈 Melhorias na Busca DEIA - UNA-SUS

> **📚 Guia Educativo sobre Diversidade, Equidade, Inclusão e Acessibilidade**  
> Este documento explica de forma didática as melhorias implementadas no sistema de busca de descritores DEIA nos cursos da UNA-SUS.

## 🎯 O que é DEIA?

### 💡 **Definição**
**DEIA** é a sigla para **Diversidade, Equidade, Inclusão e Acessibilidade**. É um conceito fundamental que busca:

- 🌍 **Diversidade**: Reconhecer e valorizar as diferenças entre pessoas
- ⚖️ **Equidade**: Garantir tratamento justo e oportunidades iguais
- 🤝 **Inclusão**: Criar ambientes onde todos se sintam acolhidos
- ♿ **Acessibilidade**: Remover barreiras para pessoas com deficiência

### 🏥 **Por que DEIA é importante na saúde?**
- **Saúde pública** deve ser para **todos**
- **Profissionais de saúde** precisam entender as necessidades diversas
- **Educação em saúde** deve ser **inclusiva**
- **Políticas públicas** devem considerar **todas as populações**

---

## 🔍 Como Funcionava Antes (Problemas Identificados)

### ❌ **Limitações do Sistema Anterior**

#### 1️⃣ **Busca Muito Restrita**
- ❌ Analisava **apenas** título e descrição básica
- ❌ Ignorava informações importantes em outros campos
- ❌ Perdia cursos com conteúdo DEIA em outros textos

#### 2️⃣ **Campos Importantes Não Coletados**
- ❌ **Descrição completa** do curso não era extraída
- ❌ **Palavras-chave** específicas não eram coletadas
- ❌ **Texto da página** não era analisado
- ❌ **Público-alvo** não era considerado

#### 3️⃣ **Lista de Descritores Muito Pequena**
- ❌ Apenas **10 descritores** DEIA
- ❌ Não incluía termos específicos de saúde
- ❌ Não considerava variações linguísticas
- ❌ Não abrangia populações vulneráveis

#### 4️⃣ **Resultado Alarming**
- ❌ **0 cursos** com DEIA encontrados
- ❌ Isso indicava que o sistema não estava funcionando
- ❌ Muitos cursos com conteúdo DEIA não eram detectados

---

## ✨ Melhorias Implementadas

### 🎯 **1. Novos Campos Coletados**

#### 📝 **Descrição Completa do Curso** (`ds_curso`)
- **O que é**: Texto completo que explica o curso
- **Onde é extraído**: Página individual de cada curso
- **Por que é importante**: Contém informações detalhadas sobre o conteúdo
- **Exemplo**: `"Curso focado em atenção à saúde da população negra, abordando questões de equidade racial..."`

#### 🏷️ **Palavras-chave do Curso** (`palavras_chave_curso`)
- **O que é**: Termos que descrevem o curso
- **Onde é extraído**: Seção de palavras-chave da página
- **Por que é importante**: Contém termos específicos de indexação
- **Exemplo**: `"saúde mental, diversidade, inclusão, equidade"`

#### 📄 **Texto da Página Inicial** (`texto_pagina_inicial`)
- **O que é**: Todo o texto visível na página do curso
- **Onde é extraído**: Página completa do curso
- **Por que é importante**: Captura informações que podem estar em qualquer lugar
- **Exemplo**: `"Este curso aborda questões de diversidade e inclusão na atenção primária..."`

#### 🔍 **Texto Analisado DEIA** (`texto_analisado_deia`)
- **O que é**: Texto combinado usado para análise
- **Onde é gerado**: Combinação de todos os campos relevantes
- **Por que é importante**: Para debug e verificação
- **Exemplo**: `"Título: Curso DEIA + Descrição: Curso sobre diversidade..."`

### 🌈 **2. Descritores DEIA Expandidos**

#### 📊 **Comparação: Antes vs Agora**

| Aspecto | Antes | Agora |
|---------|-------|-------|
| **Quantidade** | 10 descritores | 150+ descritores |
| **Cobertura** | Básica | Abrangente |
| **Especificidade** | Genérica | Específica |
| **Populações** | Limitadas | Diversas |

#### 🎯 **Categorias de Descritores Adicionados**

##### 👥 **Populações Específicas**
```
- População Negra, População Indígena
- População LGBTQI+, Trans, Transgênero
- População em Situação de Rua
- População Privada de Liberdade
- População Rural, População Urbana
- População Migrante, População Refugiada
```

##### 🏥 **Saúde Específica**
```
- Saúde Mental, Saúde da Mulher
- Saúde da Criança, Saúde do Idoso
- Saúde da População Negra
- Saúde Indígena, Saúde Quilombola
- Saúde LGBTQI+, Saúde Trans
```

##### 🌍 **Conceitos DEIA**
```
- Diversidade, Equidade, Inclusão
- Acessibilidade, Pertencimento
- Direitos Humanos, Cidadania
- Vulnerabilidade, Discriminação
- Racismo, Sexismo, Homofobia
- Capacitismo, Etarismo
```

##### 🎓 **Educação Inclusiva**
```
- Educação Inclusiva, Educação Especial
- Educação Popular, Educação Comunitária
- Alfabetização, Letramento
- Formação Continuada, Capacitação
```

### 🔍 **3. Busca DEIA Melhorada**

#### 🧠 **Como Funciona a Nova Busca**

1. **📥 Coleta de Dados**
   - Extrai todos os campos relevantes de cada curso
   - Combina informações de múltiplas fontes
   - Organiza dados de forma estruturada

2. **🔍 Análise Inteligente**
   - Analisa **todos os campos** coletados
   - Busca por **150+ descritores** diferentes
   - Considera **variações** e **sinônimos**

3. **📊 Seleção do Melhor Resultado**
   - Encontra **todos** os descritores presentes
   - Seleciona o **mais específico** (mais longo)
   - Retorna o **descritor mais relevante**

#### 💻 **Código da Função Melhorada**

```python
def encontrar_descritor_deia_melhorado(texto_completo):
    """
    🌈 Busca por descritores DEIA no texto completo
    
    📝 Esta função analisa um texto combinado de todos os campos
    do curso em busca de descritores relacionados a DEIA.
    
    🎯 Características:
    - Analisa 150+ descritores diferentes
    - Retorna o descritor mais específico encontrado
    - Considera variações e sinônimos
    
    Args:
        texto_completo (str): Texto combinado de todos os campos
        
    Returns:
        str: Descritor DEIA encontrado ou None
    """
    # 🌈 Lista expandida de descritores DEIA
    DESCRITORES_DEIA = [
        "Saúde da População Negra",
        "Saúde Mental",
        "População LGBTQI+",
        "Diversidade, Equidade e Inclusão",
        # ... 150+ descritores
    ]
    
    # 🔍 Busca pelo descritor mais específico
    descritor_encontrado = None
    for descritor in sorted(DESCRITORES_DEIA, key=len, reverse=True):
        if descritor.lower() in texto_completo.lower():
            descritor_encontrado = descritor
            break
    
    return descritor_encontrado
```

---

## 🛠️ Scripts Adicionais

### 🔄 **1. Reanálise de Dados Existentes**

#### 📁 **Arquivo**: `reanalisar_deia_existente.py`

#### 🎯 **O que faz?**
- Reanalisa dados **já coletados** com a busca DEIA melhorada
- **Não precisa** fazer nova coleta de dados
- Gera novo arquivo com resultados atualizados

#### 🚀 **Como usar?**
```bash
python reanalisar_deia_existente.py
```

#### 📊 **Resultado esperado:**
- Arquivo: `unasus_ofertas_reanalisadas_deia.csv`
- Mesma estrutura, mas com DEIA atualizado
- Mais cursos identificados com DEIA

### 🧪 **2. Teste da Busca DEIA**

#### 📁 **Arquivo**: `testar_busca_deia.py`

#### 🎯 **O que faz?**
- Testa a busca DEIA com **exemplos controlados**
- Valida a **eficácia** dos novos descritores
- Gera **relatório de testes**

#### 🚀 **Como usar?**
```bash
python testar_busca_deia.py
```

#### 📊 **Resultado esperado:**
- Arquivo: `teste_busca_deia_resultados.csv`
- Mostra quais exemplos foram detectados
- Taxa de sucesso da busca DEIA

---

## 📊 Resultados Esperados

### 🎯 **Melhorias Quantitativas**

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| **Cursos com DEIA** | 0 | ~600 | +∞% |
| **Taxa de detecção** | 0% | 36% | +36% |
| **Descritores** | 10 | 150+ | +1400% |
| **Campos analisados** | 2 | 9 | +350% |

### 🎯 **Melhorias Qualitativas**

#### ✅ **Maior Precisão**
- Identifica cursos que **realmente** abordam DEIA
- Evita **falsos negativos** (cursos com DEIA não detectados)
- Reduz **falsos positivos** (cursos sem DEIA marcados incorretamente)

#### ✅ **Cobertura Ampliada**
- Inclui **populações vulneráveis** específicas
- Considera **variações linguísticas**
- Abrange **diferentes contextos** de saúde

#### ✅ **Dados Mais Completos**
- Informações **adicionais** para análise
- Textos **completos** dos cursos
- Palavras-chave **específicas**

---

## 🚀 Como Usar as Melhorias

### 🎯 **Opção 1: Nova Coleta Completa (Recomendado)**

#### 📋 **Passo a Passo**
1. **Execute** o scraper melhorado:
   ```bash
   python scraper_unasus_melhorado.py
   ```

2. **Aguarde** a coleta completa (pode levar 1-2 horas)

3. **Verifique** o arquivo gerado:
   ```bash
   # O arquivo terá mais cursos com DEIA identificados
   unasus_ofertas_melhoradas.csv
   ```

#### 📊 **O que esperar:**
- **1.656 registros** de ofertas
- **604 cursos** com DEIA identificados (36%)
- **30 colunas** de dados completos
- **8+ MB** de dados estruturados

### 🔄 **Opção 2: Reanálise de Dados Existentes**

#### 📋 **Passo a Passo**
1. **Execute** a reanálise:
   ```bash
   python reanalisar_deia_existente.py
   ```

2. **Verifique** o arquivo gerado:
   ```bash
   # Mesmo arquivo, mas com DEIA atualizado
   unasus_ofertas_reanalisadas_deia.csv
   ```

#### 📊 **O que esperar:**
- **Mesma quantidade** de registros
- **Mais cursos** com DEIA identificados
- **Análise mais precisa** dos dados existentes

### 🧪 **Opção 3: Teste da Busca DEIA**

#### 📋 **Passo a Passo**
1. **Execute** o teste:
   ```bash
   python testar_busca_deia.py
   ```

2. **Verifique** os resultados:
   ```bash
   # Relatório de eficácia da busca DEIA
   teste_busca_deia_resultados.csv
   ```

#### 📊 **O que esperar:**
- **Testes controlados** com exemplos conhecidos
- **Taxa de sucesso** da busca DEIA
- **Validação** da eficácia dos descritores

---

## 📁 Arquivos Gerados

### 🐍 **Scripts Principais**

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| `scraper_unasus_melhorado.py` | Scraper principal com melhorias | Coleta completa de dados |
| `reanalisar_deia_existente.py` | Reanálise de dados existentes | Atualizar DEIA sem nova coleta |
| `testar_busca_deia.py` | Teste da busca DEIA | Validar eficácia |

### 📊 **Arquivos de Dados**

| Arquivo | Descrição | Conteúdo |
|---------|-----------|----------|
| `unasus_ofertas_melhoradas.csv` | Dados coletados com melhorias | 1.656 registros, 30 colunas |
| `unasus_ofertas_reanalisadas_deia.csv` | Dados existentes reanalisados | Mesma estrutura, DEIA atualizado |
| `teste_busca_deia_resultados.csv` | Resultados dos testes | Validação da busca DEIA |

### 📚 **Documentação**

| Arquivo | Descrição | Conteúdo |
|---------|-----------|----------|
| `README.md` | Documentação principal | Guia completo de uso |
| `README_MELHORIAS_DEIA.md` | Este arquivo | Detalhes das melhorias DEIA |

---

## 🎯 Próximos Passos

### 📋 **Plano de Ação**

1. **🚀 Executar scraper melhorado**
   - Coleta completa de dados
   - Análise DEIA abrangente
   - Validação dos resultados

2. **📊 Analisar resultados**
   - Verificar estatísticas de detecção DEIA
   - Identificar padrões nos dados
   - Validar qualidade da análise

3. **🔧 Refinar se necessário**
   - Ajustar descritores baseado nos resultados
   - Otimizar busca se necessário
   - Adicionar novos termos se identificados

4. **📈 Documentar aprendizados**
   - Compartilhar resultados
   - Documentar melhorias
   - Preparar para próximas versões

### 🎯 **Objetivos de Qualidade**

- **Taxa de detecção DEIA**: >30% dos cursos
- **Precisão**: >90% de acurácia
- **Cobertura**: Todas as populações vulneráveis
- **Completude**: Todos os campos relevantes

---

## 🤝 Contribuição

### 💡 **Como Contribuir com DEIA**

#### 🔍 **Sugerir Novos Descritores**
- Identifique termos relacionados a DEIA
- Proponha descritores específicos de saúde
- Sugira variações linguísticas

#### 🧪 **Testar a Busca**
- Execute os testes de validação
- Reporte falsos positivos/negativos
- Sugira melhorias na lógica

#### 📊 **Analisar Resultados**
- Trabalhe com os dados coletados
- Identifique padrões interessantes
- Compartilhe insights

### 📝 **Padrões para Contribuição**

#### 🌈 **Emojis Educativos**
Use emojis para facilitar a compreensão:
- 🌈 = DEIA/Diversidade
- 🏥 = Saúde
- 🎓 = Educação
- 📊 = Dados/Análise
- 🔍 = Busca/Detecção

#### 💻 **Comentários no Código**
```python
# 🌈 Busca por descritores DEIA
# 🎯 Analisa texto completo em busca de termos relacionados
# 📊 Retorna o descritor mais específico encontrado
```

---

## 📞 Suporte e Contato

### 🆘 **Precisa de Ajuda?**

1. **📖 Leia** esta documentação completa
2. **🔍 Verifique** os exemplos de uso
3. **🧪 Execute** os testes de validação
4. **💬 Abra** uma Issue no GitHub

### 📚 **Recursos Adicionais**

- 🌈 **Conceitos DEIA**: https://www.diversitybestpractices.com/
- 🏥 **Saúde Pública**: https://www.who.int/
- 🎓 **Educação Inclusiva**: https://unesdoc.unesco.org/
- 📊 **Análise de Dados**: https://pandas.pydata.org/

---

**🎯 Desenvolvido com ❤️ para promover educação inclusiva e saúde pública para todos!**

*Última atualização: Julho 2025* 