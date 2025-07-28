# 🧠 Grounded Theory - Metodologia de Pesquisa Qualitativa

> **📚 Pasta Especializada para Pesquisa Qualitativa**  
> Esta pasta contém versões modificáveis do scraper para aplicação da metodologia **Grounded Theory** em pesquisas educacionais.

---

## 🎯 **O que é Grounded Theory?**

A **Grounded Theory** é uma metodologia qualitativa desenvolvida por Glaser e Strauss (1967) que permite:

- 🔬 **Desenvolver teorias** a partir dos dados coletados
- 📊 **Análise sistemática** através de codificação
- 🔄 **Processo iterativo** de coleta e análise
- 🎯 **Saturação teórica** como critério de parada

### **🧠 Princípios Fundamentais:**

1. **Coleta e Análise Simultâneas** - Os dados são coletados e analisados ao mesmo tempo
2. **Codificação Aberta** - Identificação de conceitos nos dados
3. **Codificação Axial** - Relacionamento entre categorias
4. **Codificação Seletiva** - Integração das categorias em uma teoria
5. **Comparação Constante** - Comparação contínua entre dados

---

## 📁 **Estrutura da Pasta**

```
Grounded Theory/
├── 🐍 scraper_unasus_grounded.py     # Versão modificável para pesquisa
├── 🐍 scraper_unasus_backup_original.py # Backup fiel do código original
├── 🧠 grounded_theory_runner.py      # Orquestrador principal do processo
├── 🔄 coleta_e_processamento_separados.py # Coleta + Processamento separados
├── 📦 modulos/                       # Módulos modulares da metodologia
│   ├── 📋 __init__.py               # Configuração do pacote
│   ├── 📊 coleta_dados.py           # Módulo de coleta de dados
│   ├── 📊 coletor_unasus_completo.py # Coletor completo sem filtros
│   ├── 🔍 processador_deia.py       # Processador DEIA não-destrutivo
│   ├── 🔍 codificacao_aberta.py     # Módulo de codificação aberta
│   ├── 🔗 codificacao_axial.py      # Módulo de codificação axial
│   └── 🎯 codificacao_seletiva.py   # Módulo de codificação seletiva
└── 📋 README_Grounded_Theory.md      # Esta documentação
```

### **🎯 Propósito de Cada Arquivo:**

#### **`scraper_unasus_grounded.py`**
- ✅ **Versão modificável** para sua pesquisa
- 🔬 **Adapte critérios** conforme necessidades
- 📝 **Adicione campos** específicos
- 🔄 **Processo iterativo** de refinamento

#### **`scraper_unasus_backup_original.py`**
- 💾 **Backup fiel** do código original
- 🛡️ **Segurança** contra perda de código
- 🔄 **Ponto de retorno** se necessário
- 📋 **Referência** para comparações

#### **`grounded_theory_runner.py`**
- 🧠 **Orquestrador principal** do processo completo
- 🔄 **Gerenciamento automático** de iterações
- 🎯 **Controle de saturação** teórica
- 📊 **Geração automática** de relatórios
- 🔗 **Integração** de todos os módulos

#### **📦 Pasta `modulos/`**
- 📊 **`coleta_dados.py`**: Coleta sistemática e iterativa
- 📊 **`coletor_unasus_completo.py`**: Coleta completa sem filtros
- 🔍 **`processador_deia.py`**: Processamento DEIA não-destrutivo
- 🔍 **`codificacao_aberta.py`**: Identificação de conceitos básicos
- 🔗 **`codificacao_axial.py`**: Relacionamento entre categorias
- 🎯 **`codificacao_seletiva.py`**: Integração em teoria unificada

#### **🔄 `coleta_e_processamento_separados.py`**
- 🔄 **Orquestrador principal** de coleta e processamento
- 📊 **Coleta completa** sem filtros ou processamentos
- 💾 **Database fiel** e preservado
- 🔍 **Processamento DEIA** não-destrutivo
- 📈 **Relatórios separados** para cada etapa

---

## 🔬 **Como Usar para Pesquisa Grounded Theory**

### **🔄 Opção 1: Coleta e Processamento Separados (RECOMENDADO)**

#### **Arquitetura Segura - Database Fiel:**
```bash
# Execute o orquestrador principal
cd "Grounded Theory"
python coleta_e_processamento_separados.py
```

#### **Vantagens da Nova Arquitetura:**
- ✅ **Coleta Completa**: Todos os dados UNA-SUS sem filtros
- ✅ **Database Intacto**: Dados originais preservados
- ✅ **Processamento Não-Destrutivo**: Análises sem modificar fonte
- ✅ **Separação Clara**: Coleta e processamento independentes
- ✅ **Relatórios Separados**: Resultados organizados por etapa

#### **Fluxo de Trabalho:**
1. **📊 Coleta Completa** → Database fiel e atualizado
2. **💾 Preservação** → Dados originais mantidos
3. **🔍 Processamento DEIA** → Análise não-destrutiva
4. **📈 Relatórios** → Resultados separados e organizados

### **🚀 Opção 2: Processo Automatizado Grounded Theory**

#### **Usando o Grounded Theory Runner:**
```bash
# Execute o processo completo automatizado
cd "Grounded Theory"
python grounded_theory_runner.py
```

#### **Configuração Personalizada:**
```python
# Em grounded_theory_runner.py, modifique a configuração
config = {
    'criterios_iniciais': {
        'descritores': ['diversidade', 'equidade', 'inclusão', 'acessibilidade', 'saúde mental'],
        'filtros': {},
        'max_iteracoes': 5
    },
    'configuracoes_analise': {
        'min_frequencia_conceito': 3,
        'min_categorias': 3,
        'criterio_saturacao': 0.1
    }
}
```

### **🔧 Opção 2: Processo Manual**

#### **Usando Módulos Individualmente:**
```python
from modulos.coleta_dados import ColetorDadosGroundedTheory
from modulos.codificacao_aberta import CodificacaoAberta
from modulos.codificacao_axial import CodificacaoAxial
from modulos.codificacao_seletiva import CodificacaoSeletiva

# 1. Coleta de dados
coletor = ColetorDadosGroundedTheory(config, logger)
dados = coletor.coleta_inicial()

# 2. Codificação aberta
cod_aberta = CodificacaoAberta(logger)
resultados_aberta = cod_aberta.codificar_dados(dados)

# 3. Codificação axial
cod_axial = CodificacaoAxial(logger)
resultados_axial = cod_axial.codificar_axial(resultados_aberta)

# 4. Codificação seletiva
cod_seletiva = CodificacaoSeletiva(logger)
teoria_final = cod_seletiva.codificar_seletiva(resultados_aberta, resultados_axial)
```

### **📝 Passo 1: Modificação do Código**

#### **Exemplo 1: Adicionar Novos Descritores DEIA**
```python
# Em scraper_unasus_grounded.py
# Adicione descritores específicos da sua pesquisa

DESCRITORES_DEIA.extend([
    "Saúde Mental Comunitária",
    "Terapia Ocupacional",
    "Psicologia Social",
    "Saúde Coletiva",
    "Promoção da Saúde"
])
```

#### **Exemplo 2: Modificar Campos Coletados**
```python
def extrair_dados_especificos(curso):
    """Extrai dados específicos para sua pesquisa."""
    
    # Adicione campos específicos
    curso["area_pesquisa"] = "Saúde Mental"
    curso["metodologia"] = "Educação a Distância"
    curso["publico_especifico"] = "Profissionais de Saúde"
    
    return curso
```

#### **Exemplo 3: Filtrar por Critérios Específicos**
```python
def filtrar_por_criterios(curso):
    """Filtra cursos por critérios da pesquisa."""
    
    # Exemplo: apenas cursos de saúde mental
    if "saúde mental" in curso.get("no_curso", "").lower():
        return True
    
    # Exemplo: apenas cursos com carga horária > 40h
    if curso.get("qt_carga_horaria_total", 0) > 40:
        return True
    
    return False
```

### **🔄 Passo 2: Processo Iterativo**

#### **Ciclo de Pesquisa Grounded Theory:**

1. **📊 Coleta Inicial**
   ```bash
   python scraper_unasus_grounded.py
   ```

2. **🔍 Análise dos Dados**
   ```bash
   python ../analisar_dados_coletados.py
   ```

3. **📝 Identificação de Padrões**
   - Examine os resultados
   - Identifique categorias emergentes
   - Documente insights

4. **🔧 Modificação dos Critérios**
   - Ajuste descritores DEIA
   - Modifique campos coletados
   - Refine filtros

5. **🔄 Nova Coleta**
   - Execute novamente com critérios refinados
   - Compare com resultados anteriores

6. **📈 Saturação Teórica**
   - Continue até não encontrar novos padrões
   - Documente a teoria emergente

### **📊 Passo 3: Análise Qualitativa**

#### **Usando o Script de Análise:**
```bash
# Analise os dados coletados
python ../analisar_dados_coletados.py

# Examine padrões específicos
python ../testar_busca_deia.py
```

#### **Identificando Categorias:**
- **Códigos Abertos**: Conceitos básicos nos dados
- **Códigos Axiais**: Relacionamentos entre conceitos
- **Códigos Seletivos**: Integração em teoria

---

## 💾 **Sistema de Backup e Segurança**

### **🎯 Estratégia de Backup:**

#### **1. Backup Automático**
```bash
# Antes de fazer modificações
cp scraper_unasus_grounded.py scraper_unasus_grounded_backup_$(date +%Y%m%d).py
```

#### **2. Restauração Segura**
```bash
# Se algo der errado, restaure do backup
cp scraper_unasus_backup_original.py scraper_unasus_grounded.py
```

#### **3. Versionamento Git**
```bash
# Commit suas modificações
git add "Grounded Theory/"
git commit -m "Modificações para pesquisa Grounded Theory"
```

### **🔄 Fluxo de Trabalho Seguro:**

```bash
# 1. Sempre trabalhe na versão grounded
cd "Grounded Theory"
python scraper_unasus_grounded.py

# 2. Teste suas modificações
python ../testar_busca_deia.py

# 3. Analise os resultados
python ../analisar_dados_coletados.py

# 4. Se necessário, volte ao backup
cp scraper_unasus_backup_original.py scraper_unasus_grounded.py
```

---

## 📋 **Boas Práticas para Pesquisa**

### **✅ Documentação:**
- 📝 **Registre** cada modificação no código
- 📋 **Documente** insights e descobertas
- 📊 **Mantenha** logs de análise
- 📚 **Crie** relatórios de progresso

### **✅ Testes:**
- 🧪 **Teste** pequenas mudanças antes de grandes modificações
- 🔍 **Valide** resultados após cada modificação
- 📊 **Compare** com dados anteriores
- ⚠️ **Verifique** integridade dos dados

### **✅ Segurança:**
- 💾 **Mantenha** o backup original sempre intacto
- 🔄 **Faça** backups regulares das modificações
- 🛡️ **Use** controle de versão (Git)
- 📁 **Organize** arquivos de dados por data

### **✅ Análise:**
- 🔬 **Use** o sistema de análise para validar mudanças
- 📈 **Identifique** padrões emergentes
- 🎯 **Foque** na saturação teórica
- 📊 **Documente** a teoria desenvolvida

---

## 🎓 **Exemplos de Pesquisa**

### **🔬 Exemplo 1: Saúde Mental na Educação**
```python
# Descritores específicos para saúde mental
DESCRITORES_DEIA = [
    "Saúde Mental",
    "Psicologia",
    "Psiquiatria",
    "Transtornos Mentais",
    "Bem-estar Psicológico",
    "Saúde Mental Comunitária"
]

# Campos específicos
def extrair_dados_saude_mental(curso):
    curso["area_saude_mental"] = "Sim" if any(
        termo in curso.get("no_curso", "").lower() 
        for termo in ["mental", "psicologia", "psiquiatria"]
    ) else "Não"
    return curso
```

### **🏥 Exemplo 2: Populações Vulneráveis**
```python
# Descritores para populações vulneráveis
DESCRITORES_DEIA = [
    "População em Situação de Rua",
    "População Privada de Liberdade",
    "População Indígena",
    "População Negra",
    "Pessoas com Deficiência",
    "População LGBTQI+"
]
```

### **👥 Exemplo 3: Equidade em Saúde**
```python
# Descritores para equidade
DESCRITORES_DEIA = [
    "Equidade",
    "Equidade em Saúde",
    "Determinantes Sociais",
    "Vulnerabilidade Social",
    "Iniquidades",
    "Justiça Social"
]
```

---

## 📚 **Recursos Adicionais**

### **📖 Literatura Recomendada:**
- **Glaser, B. G., & Strauss, A. L.** (1967). The Discovery of Grounded Theory
- **Strauss, A., & Corbin, J.** (1990). Basics of Qualitative Research
- **Charmaz, K.** (2006). Constructing Grounded Theory

### **🔗 Links Úteis:**
- **Metodologia Qualitativa**: https://www.qualitative-research.net/
- **Grounded Theory**: https://groundedtheoryreview.com/
- **Análise de Dados**: https://www.qsrinternational.com/

---

## 🆘 **Suporte e Dúvidas**

### **❓ Perguntas Frequentes:**

#### **Q: Como saber se atingi saturação teórica?**
**A:** Quando novos dados não revelam novas categorias ou propriedades das categorias existentes.

#### **Q: Quantas iterações são necessárias?**
**A:** Não há número fixo. Continue até a saturação teórica.

#### **Q: Como documentar a teoria desenvolvida?**
**A:** Use o script de análise e mantenha registros detalhados de cada modificação.

#### **Q: Posso usar dados de diferentes fontes?**
**A:** Sim! Grounded Theory permite triangulação de dados.

---

**🧠 Desenvolvido para facilitar pesquisas qualitativas em educação em saúde!**

*Última atualização: Julho 2025* 