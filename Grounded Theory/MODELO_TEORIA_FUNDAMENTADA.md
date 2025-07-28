# 🧠 **MODELO DE TEORIA FUNDAMENTADA - UNA-SUS**

## 📚 **O QUE É ESTE MODELO?**

Este é um **sistema completo de pesquisa qualitativa** que implementa a metodologia **Grounded Theory (Teoria Fundamentada)** para analisar cursos da UNA-SUS e identificar elementos de **DEIA (Diversidade, Equidade, Inclusão e Acessibilidade)**.

### 🎯 **Objetivo Principal:**
Desenvolver uma **teoria fundamentada** sobre como a UNA-SUS aborda temas de DEIA em seus cursos, gerando insights para políticas públicas e melhorias na formação em saúde.

---

## 🏗️ **ARQUITETURA DO MODELO**

### **📊 PRINCÍPIO FUNDAMENTAL:**
**"Coleta Completa + Processamento Inteligente"**

O modelo funciona em **duas etapas separadas** para garantir integridade dos dados:

```
📥 ETAPA 1: COLETA COMPLETA
├── Coleta TODOS os dados da UNA-SUS
├── Sem filtros ou processamentos
├── Preserva integridade original
└── Salva dados brutos

🔍 ETAPA 2: PROCESSAMENTO DEIA
├── Analisa dados coletados
├── Identifica elementos DEIA
├── Categoriza e classifica
└── Gera insights e relatórios
```

---

## 📁 **ESTRUTURA ORGANIZACIONAL**

### **🎯 ARQUIVOS ESSENCIAIS:**

```
Grounded Theory/
├── 🚀 iniciar_pesquisa.py              # PONTO DE ENTRADA PRINCIPAL
├── 📋 MODELO_TEORIA_FUNDAMENTADA.md    # ESTE DOCUMENTO
├── 🔄 coleta_e_processamento_separados.py # ORQUESTRADOR PRINCIPAL
├── 🧠 grounded_theory_runner.py        # METODOLOGIA COMPLETA
├── 📊 scraper_unasus_grounded.py       # VERSÃO MODIFICÁVEL
├── 💾 scraper_unasus_backup_original.py # BACKUP SEGURO
├── 📁 modulos/                         # MÓDULOS MODULARES
│   ├── 📥 coletor_unasus_completo.py   # COLETA COMPLETA
│   ├── 🔍 processador_deia.py          # PROCESSAMENTO DEIA
│   ├── 🔓 codificacao_aberta.py        # CODIFICAÇÃO ABERTA
│   ├── 🔗 codificacao_axial.py         # CODIFICAÇÃO AXIAL
│   ├── 🎯 codificacao_seletiva.py      # CODIFICAÇÃO SELETIVA
│   └── 📊 coleta_dados.py              # COLETA DE DADOS
├── 📁 dados/                           # DADOS COLETADOS
├── 📁 logs/                            # LOGS DE EXECUÇÃO
└── 📁 checkpoints/                     # PONTOS DE SALVAMENTO
```

---

## 🎯 **OPÇÕES DE USO DO MODELO**

### **🚀 OPÇÃO 1: COLETA COMPLETA + PROCESSAMENTO DEIA**
**Recomendado para maioria dos usuários**

```bash
python iniciar_pesquisa.py
# Escolher opção 1
```

**O que faz:**
- ✅ Coleta todos os cursos da UNA-SUS
- ✅ Identifica elementos DEIA automaticamente
- ✅ Gera relatórios e estatísticas
- ✅ Salva dados em múltiplos formatos

**Tempo estimado:** 30-60 minutos

**Resultados:**
- `dados_completos.json` - Todos os cursos
- `analise_deia.json` - Análise DEIA
- `relatorio_deia.md` - Relatório detalhado

---

### **📥 OPÇÃO 2: APENAS COLETA COMPLETA**
**Para análise manual posterior**

```bash
python iniciar_pesquisa.py
# Escolher opção 2
```

**O que faz:**
- ✅ Coleta todos os dados sem processamento
- ✅ Salva dados brutos para análise personalizada
- ✅ Útil para pesquisas específicas

**Tempo estimado:** 20-40 minutos

---

### **🔍 OPÇÃO 3: PROCESSAMENTO DEIA**
**Para dados já coletados**

```bash
python iniciar_pesquisa.py
# Escolher opção 3
```

**O que faz:**
- ✅ Usa dados existentes
- ✅ Aplica análise DEIA
- ✅ Gera relatórios

**Tempo estimado:** 5-10 minutos

---

### **🧠 OPÇÃO 4: METODOLOGIA GROUNDED THEORY COMPLETA**
**Para pesquisa acadêmica completa**

```bash
python iniciar_pesquisa.py
# Escolher opção 4
```

**O que faz:**
- ✅ Executa todas as etapas da metodologia
- ✅ Codificação aberta, axial e seletiva
- ✅ Desenvolvimento de teoria
- ✅ Relatório final completo

**Tempo estimado:** 2-4 horas

---

## 🔬 **METODOLOGIA GROUNDED THEORY**

### **📚 O QUE É GROUNDED THEORY?**

A **Teoria Fundamentada** é uma metodologia de pesquisa qualitativa que permite desenvolver teorias a partir dos dados coletados, de forma sistemática e iterativa.

#### **🎯 Princípios Fundamentais:**
1. **📊 Coleta de Dados**: Recolher informações sem preconceitos
2. **🔍 Análise Contínua**: Analisar dados enquanto coleta
3. **🔄 Iteração**: Repetir o processo até saturação
4. **🏗️ Construção de Teoria**: Desenvolver teoria baseada nos dados

---

### **🏗️ ETAPAS DA METODOLOGIA**

#### **1️⃣ ETAPA 1: Coleta de Dados**
**📥 Objetivo**: Coletar TODOS os dados disponíveis sem filtros

**🔧 Como funciona:**
- **Coleta Completa**: Pega todos os cursos da UNA-SUS
- **Sem Filtros**: Não aplica critérios DEIA inicialmente
- **Dados Brutos**: Mantém fidelidade aos dados originais
- **Checkpoints**: Salva progresso para evitar perda

**📊 Dados Coletados:**
```python
# Campos básicos
- id, titulo, descricao, status, categoria
- vagas, numero_vagas, carga_horaria
- modalidade, tipo_curso, nivel
- inicio_inscricao, fim_inscricao
- area_tematica, instituicao
- publico_alvo, palavras_chave
```

---

#### **2️⃣ ETAPA 2: Processamento DEIA**
**🔍 Objetivo**: Analisar dados coletados para elementos DEIA

**🧠 O que é DEIA:**
- **D**iversidade - Diferenças entre pessoas
- **E**quidade - Tratamento justo e imparcial
- **I**nclusão - Participação plena de todos
- **A**cessibilidade - Acesso para pessoas com deficiência

**🔍 Análise realizada:**
- **Palavras-chave**: Busca termos relacionados a DEIA
- **Categorização**: Classifica cursos por temas DEIA
- **Estatísticas**: Gera relatórios quantitativos
- **Relatórios**: Cria documentos de análise

---

#### **3️⃣ ETAPA 3: Codificação Aberta**
**🔓 Objetivo**: Identificar conceitos e categorias iniciais

**🔍 Processo:**
1. **Leitura dos Dados**: Analisar textos dos cursos
2. **Identificação de Conceitos**: Encontrar palavras-chave
3. **Categorização Inicial**: Agrupar conceitos similares
4. **Criação de Memos**: Documentar insights

**📝 Exemplo de codificação:**
```python
# Texto original: "Curso sobre inclusão de PCDs no ambiente de trabalho"
# Conceitos identificados:
- "inclusão"
- "PCDs" 
- "ambiente de trabalho"
# Categoria: "Inclusão Laboral"
```

---

#### **4️⃣ ETAPA 4: Codificação Axial**
**🔗 Objetivo**: Conectar categorias e identificar relações

**🔗 Paradigma de Strauss e Corbin:**
- **Condições Causais**: O que causa o fenômeno
- **Fenômeno Central**: O que está sendo estudado
- **Contexto**: Onde acontece
- **Condições Intervenientes**: Fatores que influenciam
- **Estratégias**: Como lidar com o fenômeno
- **Consequências**: Resultados das ações

**📊 Exemplo de análise axial:**
```python
# Fenômeno: "Falta de formação em DEIA"
# Condição Causal: "Ausência de cursos específicos"
# Contexto: "Instituições de saúde"
# Estratégia: "Criar cursos de capacitação"
# Consequência: "Profissionais mais preparados"
```

---

#### **5️⃣ ETAPA 5: Codificação Seletiva**
**🎯 Objetivo**: Integrar tudo em uma teoria coerente

**🏗️ Processo:**
1. **Integração**: Conectar todas as categorias
2. **Fenômeno Central**: Identificar o tema principal
3. **Teoria**: Desenvolver explicação teórica
4. **Validação**: Verificar se a teoria faz sentido

**📚 Resultado Final:**
- **Teoria Fundamentada**: Explicação baseada nos dados
- **Modelo Teórico**: Representação visual da teoria
- **Relatório Final**: Documentação completa

---

## 🔧 **MÓDULOS DO SISTEMA**

### **📥 MÓDULO 1: Coletor UNA-SUS Completo**
**Arquivo**: `modulos/coletor_unasus_completo.py`

**🎯 Função**: Coleta TODOS os dados da UNA-SUS sem filtros

**🔧 Características:**
- Coleta fiel e completa
- Preserva integridade dos dados
- Sistema de checkpoints
- Logs detalhados
- Múltiplos formatos de saída

**📊 Dados coletados:**
- Informações básicas dos cursos
- Detalhes de vagas e inscrições
- Dados institucionais
- Metadados de coleta

---

### **🔍 MÓDULO 2: Processador DEIA**
**Arquivo**: `modulos/processador_deia.py`

**🎯 Função**: Analisa dados coletados para elementos DEIA

**🔧 Características:**
- Análise não-destrutiva
- Categorização automática
- Estatísticas quantitativas
- Relatórios detalhados
- Múltiplos formatos de saída

**📊 Análises realizadas:**
- Identificação de elementos DEIA
- Categorização por temas
- Estatísticas de distribuição
- Relatórios qualitativos

---

### **🔓 MÓDULO 3: Codificação Aberta**
**Arquivo**: `modulos/codificacao_aberta.py`

**🎯 Função**: Identifica conceitos e categorias iniciais

**🔧 Características:**
- Análise de texto
- Identificação de conceitos
- Categorização inicial
- Criação de memos
- Documentação de insights

---

### **🔗 MÓDULO 4: Codificação Axial**
**Arquivo**: `modulos/codificacao_axial.py`

**🎯 Função**: Conecta categorias e identifica relações

**🔧 Características:**
- Aplicação do paradigma de Strauss e Corbin
- Identificação de relações
- Análise de condições
- Desenvolvimento de estratégias
- Documentação de consequências

---

### **🎯 MÓDULO 5: Codificação Seletiva**
**Arquivo**: `modulos/codificacao_seletiva.py`

**🎯 Função**: Integra tudo em uma teoria coerente

**🔧 Características:**
- Integração de categorias
- Identificação do fenômeno central
- Construção do modelo teórico
- Geração da teoria final
- Documentação completa

---

## 📊 **DADOS E RESULTADOS**

### **📁 ARQUIVOS GERADOS**

#### **📊 Dados Brutos:**
- `dados_completos.json` - Todos os cursos em JSON
- `dados_completos.csv` - Dados em formato tabular
- `dados_completos.xlsx` - Dados em Excel

#### **🔍 Análises DEIA:**
- `analise_deia.json` - Resultados da análise DEIA
- `relatorio_deia.md` - Relatório detalhado
- `estatisticas_deia.json` - Estatísticas quantitativas

#### **🧠 Codificação (Grounded Theory):**
- `codificacao_aberta.json` - Resultados da codificação aberta
- `codificacao_axial.json` - Resultados da codificação axial
- `codificacao_seletiva.json` - Resultados da codificação seletiva

#### **📚 Teoria Final:**
- `teoria_fundamentada.md` - Teoria desenvolvida
- `modelo_teorico.md` - Modelo visual da teoria
- `relatorio_final.md` - Relatório completo

---

### **📈 EXEMPLOS DE ANÁLISE**

#### **📊 Estatísticas DEIA:**
```json
{
  "total_cursos": 1500,
  "cursos_com_deia": 45,
  "percentual_deia": 3.0,
  "categorias_deia": {
    "diversidade": 15,
    "equidade": 12,
    "inclusão": 25,
    "acessibilidade": 8
  }
}
```

#### **🔍 Exemplos de Cursos DEIA:**
```json
{
  "titulo": "Saúde Mental e Inclusão Social",
  "categoria_deia": "inclusão",
  "elementos_encontrados": ["inclusão", "saúde mental", "social"],
  "descricao": "Curso sobre saúde mental e inclusão social..."
}
```

---

## 🚀 **COMO USAR O MODELO**

### **🎯 PASSO A PASSO COMPLETO**

#### **Passo 1: Preparação**
```bash
cd "Grounded Theory"
python iniciar_pesquisa.py
```

#### **Passo 2: Escolher Opção**
- **Opção 1**: Coleta completa + Processamento DEIA (Recomendado)
- **Opção 2**: Apenas coleta completa
- **Opção 3**: Processamento DEIA (dados existentes)
- **Opção 4**: Metodologia Grounded Theory completa

#### **Passo 3: Acompanhar Execução**
- Monitore os logs em tempo real
- Dados são salvos automaticamente
- Progresso salvo em checkpoints

#### **Passo 4: Analisar Resultados**
- Verifique arquivos gerados
- Leia relatórios em Markdown
- Analise dados em Excel

---

### **🔧 CONFIGURAÇÕES AVANÇADAS**

#### **⚙️ Configurações do Coletor:**
```python
# Em modulos/coletor_unasus_completo.py
URL_BASE = "https://www.unasus.gov.br/cursos/rest/busca"
DELAY_ENTRE_REQUESTS = 1  # segundos
```

#### **🔍 Configurações DEIA:**
```python
# Em modulos/processador_deia.py
DESCRITORES_DEIA = [
    "diversidade", "equidade", "inclusão", "acessibilidade",
    "PCD", "deficiência", "gênero", "raça", "etnia"
]
```

---

## 🆘 **SOLUÇÃO DE PROBLEMAS**

### **❌ Problemas Comuns:**

#### **Erro 404:**
- **Causa**: Curso não encontrado
- **Solução**: Normal, alguns cursos podem ter sido removidos

#### **Erro de Conexão:**
- **Causa**: Problema de internet ou servidor
- **Solução**: Verificar conexão e tentar novamente

#### **Erro de Importação:**
- **Causa**: Módulos não encontrados
- **Solução**: Verificar se está na pasta correta

#### **Erro de Permissão:**
- **Causa**: Sem permissão para criar arquivos
- **Solução**: Verificar permissões da pasta

---

### **🔍 Como obter ajuda:**
1. **📖 Ler documentação**: Este documento
2. **📊 Verificar logs**: Analisar arquivos em logs/
3. **🔄 Tentar novamente**: Muitos erros são temporários
4. **📞 Suporte**: Criar issue no GitHub

---

## 📚 **APLICAÇÕES DO MODELO**

### **🎓 Pesquisa Acadêmica:**
- Desenvolvimento de teorias sobre formação em saúde
- Análise de políticas públicas em DEIA
- Estudos sobre inclusão na educação

### **🏢 Políticas Públicas:**
- Identificação de lacunas na formação
- Desenvolvimento de estratégias de inclusão
- Avaliação de programas existentes

### **📊 Análise de Dados:**
- Estatísticas sobre cursos DEIA
- Tendências na formação em saúde
- Comparação entre instituições

---

## 🎯 **PRÓXIMOS PASSOS**

### **🚀 Para começar agora:**
1. **📖 Ler este documento** completamente
2. **🚀 Executar** `python iniciar_pesquisa.py`
3. **🎯 Escolher opção 1** (Recomendado)
4. **📊 Analisar resultados** gerados

### **📚 Para aprofundar:**
1. **🧪 Personalizar configurações** conforme necessidade
2. **📊 Analisar dados** com ferramentas estatísticas
3. **📝 Documentar insights** em memos
4. **🏗️ Desenvolver teoria** baseada nos dados

---

## 📞 **SUPORTE E CONTATO**

### **🔍 Como obter ajuda:**
- **📖 Documentação**: Este documento
- **📊 Logs**: Analisar arquivos em logs/
- **🔄 Tentativas**: Muitos problemas são temporários

---

**🎉 Parabéns! Você está pronto para usar o modelo de Teoria Fundamentada para pesquisa qualitativa!**

---

*📅 Última atualização: 27/07/2025*
*📝 Versão: 1.0*
*👨‍💻 Desenvolvido para pesquisa UNA-SUS*
*🧠 Metodologia Grounded Theory* 