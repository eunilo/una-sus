# Melhorias na Busca DEIA - UNA-SUS

## Resumo das Melhorias Implementadas

Este documento descreve as melhorias implementadas no sistema de busca de descritores relacionados a **Diversidade, Equidade, Inclusão e Acessibilidade (DEIA)** nos cursos da UNA-SUS.

## Problemas Identificados

1. **Busca limitada**: A busca DEIA estava restrita apenas ao título e descrição básica do curso
2. **Campos não coletados**: Faltavam campos importantes como descrição completa do curso, palavras-chave e texto da página inicial
3. **Descritores insuficientes**: Lista limitada de descritores DEIA
4. **Nenhum curso com DEIA encontrado**: Resultado que indica subdetecção

## Melhorias Implementadas

### 1. Novos Campos Coletados

#### `scraper_unasus_melhorado.py`
- **Descrição do curso** (`ds_curso`): Extração robusta da descrição completa do curso
- **Palavras-chave do curso** (`palavras_chave_curso`): Palavras-chave específicas do curso
- **Texto da página inicial** (`texto_pagina_inicial`): Todo o texto da página do curso
- **Texto analisado DEIA** (`texto_analisado_deia`): Texto usado para análise DEIA (para debug)

### 2. Descritores DEIA Expandidos

A lista de descritores foi expandida de **10 para mais de 150** termos, incluindo:

#### Descritores Originais
- Diversidade, Equidade e Integração
- Diversidade, Equidade, Inclusão e Pertencimento
- Diversidade, Equidade, Inclusão, Acessibilidade
- etc.

#### Novos Descritores
- **Termos individuais**: Diversidade, Equidade, Inclusão, Acessibilidade, Pertencimento
- **Variações**: Inclusivo, Inclusiva, Diverso, Diversa, Equitativo, Equitativa, Acessível
- **Saúde específica**: Saúde Mental, Saúde da População Negra, Saúde Indígena, Saúde LGBTQI+
- **Populações vulneráveis**: População em Situação de Rua, População Privada de Liberdade
- **Identidades**: Trans, Transgênero, Não-binário, Gay, Lésbica, Bissexual, Pansexual
- **Etnias**: Negro, Negra, Indígena, Quilombola, Ribeirinho, Extrativista
- **Vulnerabilidades**: Vítima de Violência, Vítima de Discriminação, Vítima de Racismo
- **E muito mais...**

### 3. Busca DEIA Melhorada

#### `encontrar_descritor_deia_melhorado()`
- Analisa **todos os campos coletados** do curso
- Combina título, descrição do curso, descrição da oferta, palavras-chave, público-alvo, temas, DeCs, programas de governo
- Retorna o descritor **mais específico** encontrado (mais longo)
- Inclui texto da página inicial na análise

### 4. Scripts Adicionais

#### `reanalisar_deia_existente.py`
- Reanalisa dados existentes com a busca DEIA melhorada
- Não precisa fazer nova coleta de dados
- Gera novo arquivo com resultados atualizados

#### `testar_busca_deia.py`
- Testa a busca DEIA com exemplos controlados
- Valida a eficácia dos novos descritores
- Gera relatório de testes

## Como Usar

### 1. Nova Coleta de Dados
```bash
python scraper_unasus_melhorado.py
```

### 2. Reanálise de Dados Existentes
```bash
python reanalisar_deia_existente.py
```

### 3. Teste da Busca DEIA
```bash
python testar_busca_deia.py
```

## Arquivos Gerados

### `scraper_unasus_melhorado.py`
- Scraper principal com todas as melhorias
- Coleta dados completos incluindo novos campos
- Análise DEIA abrangente

### `unasus_ofertas_melhoradas.csv`
- Arquivo de saída do scraper melhorado
- Inclui todos os novos campos
- Análise DEIA em todos os registros

### `unasus_ofertas_reanalisadas_deia.csv`
- Dados existentes reanalisados
- Mesma estrutura, mas com DEIA atualizado

### `teste_busca_deia_resultados.csv`
- Resultados dos testes de validação
- Mostra eficácia da busca DEIA

## Campos Adicionados

| Campo | Descrição | Fonte |
|-------|-----------|-------|
| `ds_curso` | Descrição completa do curso | Página do curso |
| `palavras_chave_curso` | Palavras-chave do curso | Página do curso |
| `texto_pagina_inicial` | Todo o texto da página | Página do curso |
| `texto_analisado_deia` | Texto usado para análise DEIA | Combinação de campos |
| `tem_deia` | Indica se tem DEIA (Sim/Não) | Análise |
| `deia_encontrado` | Descritor DEIA específico encontrado | Análise |

## Resultados Esperados

Com essas melhorias, esperamos:

1. **Maior detecção**: Identificar cursos que abordam DEIA mas não eram detectados
2. **Análise mais precisa**: Considerar todos os campos relevantes
3. **Cobertura ampliada**: Incluir mais variações de descritores DEIA
4. **Dados mais completos**: Informações adicionais para análise

## Próximos Passos

1. Executar o scraper melhorado para coleta completa
2. Ou reanalisar dados existentes
3. Validar resultados com testes
4. Analisar estatísticas de detecção DEIA
5. Refinar descritores se necessário

## Contato

Para dúvidas ou sugestões sobre as melhorias implementadas, consulte a documentação ou os logs gerados pelos scripts. 