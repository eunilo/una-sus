# 🔄 GUIA DO WORKFLOW INTERATIVO

## 🎯 **OBJETIVO**

Este workflow interativo permite uma abordagem controlada e analítica da pesquisa, onde você pode:

1. **Coletar dados completos** sem filtros
2. **Analisar os dados** coletados em detalhes
3. **Tomar decisões** baseadas na análise
4. **Fazer ramificações** específicas da pesquisa
5. **Executar Grounded Theory** de forma controlada

## 📋 **OPÇÕES DISPONÍVEIS**

### **🔄 Workflow Interativo Completo**
```bash
python executar_workflow_interativo.py
```

### **🔍 Análise Exploratória Detalhada**
```bash
python analise_exploratoria_dados.py
```

## 🚀 **COMO USAR**

### **PASSO 1: Executar Workflow Interativo**

1. **Execute o workflow:**
   ```bash
   python executar_workflow_interativo.py
   ```

2. **O sistema irá:**
   - Verificar se existem dados coletados
   - Perguntar se você quer usar dados existentes ou coletar novos
   - Coletar dados completos (se necessário)
   - Fazer análise exploratória
   - Permitir escolher próximos passos

### **PASSO 2: Escolher Próximos Passos**

Após a análise exploratória, você pode escolher:

1. **Executar Grounded Theory completa**
2. **Focar em análise DEIA específica**
3. **Analisar apenas cursos de formação**
4. **Investigar padrões por instituição**
5. **Sair do workflow**

### **PASSO 3: Análise Exploratória Detalhada**

Para uma análise mais profunda:

```bash
python analise_exploratoria_dados.py
```

Esta análise irá gerar:
- 📊 Estatísticas detalhadas dos dados
- 🏛️ Análise de instituições
- 🎓 Distribuição de cursos
- 🌈 Elementos DEIA encontrados
- 📚 Modalidades de ensino
- ⏰ Análise de carga horária

## 📁 **ARQUIVOS GERADOS**

### **Relatórios JSON**
- `relatorios/analise_exploratoria_YYYYMMDD_HHMMSS.json`
- `relatorios/workflow_interativo_YYYYMMDD_HHMMSS.json`

### **Relatórios Markdown**
- `relatorios/analise_exploratoria_YYYYMMDD_HHMMSS.md`
- `relatorios/relatorio_workflow_interativo_YYYYMMDD_HHMMSS.md`

### **Logs**
- `logs/workflow_interativo_YYYYMMDD_HHMMSS.log`

## 🔍 **ANÁLISES DISPONÍVEIS**

### **📊 Análise Estrutural**
- Total de registros
- Campos disponíveis
- Campos com dados vs. vazios
- Estrutura dos dados

### **🏛️ Análise Institucional**
- Total de instituições
- Top 15 instituições
- Distribuição por instituição

### **🎓 Análise de Cursos**
- Distribuição por nível
- Modalidades de ensino
- Formatos de curso
- Carga horária

### **🌈 Análise DEIA**
- Cursos com elementos DEIA
- Elementos mais frequentes
- Exemplos de cursos
- Percentual de cobertura

### **🎓 Análise de Formação**
- Cursos de formação/preceptoria
- Palavras-chave identificadas
- Exemplos de cursos

## 💡 **VANTAGENS DO WORKFLOW INTERATIVO**

### **✅ Controle Total**
- Você decide quando parar e analisar
- Pode fazer decisões baseadas nos dados
- Controle sobre as ramificações

### **🔍 Análise Detalhada**
- Análise exploratória completa
- Estatísticas detalhadas
- Identificação de padrões

### **📋 Documentação**
- Relatórios automáticos
- Logs detalhados
- Rastreabilidade completa

### **🎯 Foco Específico**
- Pode focar em aspectos específicos
- Análises customizadas
- Ramificações controladas

## 🛠️ **CUSTOMIZAÇÃO**

### **Adicionar Novas Análises**
Você pode adicionar novas análises editando:
- `analise_exploratoria_dados.py`
- `workflow_interativo.py`

### **Modificar Palavras-Chave**
Para DEIA ou formação, edite as listas em:
- `analise_exploratoria_dados.py`

### **Adicionar Novos Campos**
Para analisar novos campos, modifique:
- `extrair_texto_curso()` em `analise_exploratoria_dados.py`

## 📊 **EXEMPLO DE USO**

```bash
# 1. Executar workflow interativo
python executar_workflow_interativo.py

# 2. Responder às perguntas:
# - Usar dados existentes? (s/n)
# - Escolher próximo passo (1-5)

# 3. Verificar relatórios gerados
ls relatorios/

# 4. Executar análise exploratória detalhada
python analise_exploratoria_dados.py
```

## 🎯 **PRÓXIMOS PASSOS SUGERIDOS**

1. **Execute o workflow interativo**
2. **Analise os dados coletados**
3. **Identifique padrões interessantes**
4. **Escolha focos específicos**
5. **Execute análises detalhadas**
6. **Baseie decisões nos dados**
7. **Faça ramificações da pesquisa**

## 📞 **SUPORTE**

Se encontrar problemas:
1. Verifique os logs em `logs/`
2. Confirme que os dados foram coletados
3. Verifique as permissões de escrita
4. Consulte os relatórios gerados

---

**🎉 Agora você tem controle total sobre sua pesquisa!** 