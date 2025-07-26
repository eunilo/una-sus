# 🏥 Scraper UNA-SUS - Coleta Inteligente de Dados Educacionais

> **📚 Projeto Educacional para Pesquisa em Saúde Pública**  
> Um sistema inteligente e didático para coletar e analisar dados de cursos da Universidade Aberta do SUS (UNA-SUS), com foco especial em **Diversidade, Equidade, Inclusão e Acessibilidade (DEIA)**.

## 🎯 Sobre Este Projeto

### 💡 **O que é?**
Este é um **scraper** (coletor automático de dados) que extrai informações detalhadas de cursos da plataforma UNA-SUS. Ele foi desenvolvido para facilitar pesquisas acadêmicas e análises sobre educação em saúde pública.

### 🎓 **Para quem é?**
- **Pesquisadores** em saúde pública e educação
- **Estudantes** de graduação e pós-graduação
- **Desenvolvedores** interessados em web scraping
- **Analistas de dados** em saúde
- **Qualquer pessoa** interessada em dados educacionais

### 🚀 **Por que usar?**
- ✅ **Automatiza** a coleta de dados que seria manual
- ✅ **Identifica** cursos com foco em DEIA automaticamente
- ✅ **Organiza** dados em formato estruturado (CSV)
- ✅ **Facilita** análises estatísticas e qualitativas
- ✅ **Economiza tempo** para pesquisas acadêmicas

---

## 📊 Dados Coletados

### 🎓 **Informações dos Cursos**
| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `co_seq_curso` | ID único do curso | `44538` |
| `no_curso` | Nome do curso | `"Atenção à Saúde da População Negra"` |
| `qt_carga_horaria_total` | Carga horária | `60 horas` |
| `ds_curso` | Descrição completa | `"Curso focado em..."` |
| `palavras_chave_curso` | Palavras-chave | `"saúde, população negra, equidade"` |

### 🎯 **Informações das Ofertas**
| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `id_oferta` | ID da oferta | `416264` |
| `vagas` | Número de vagas | `1000` |
| `publico_alvo` | Público-alvo | `"Profissionais de saúde"` |
| `local_oferta` | Local | `"EAD"` |
| `formato` | Formato | `"Ensino a Distância"` |

### 🌈 **Análise DEIA (Diversidade, Equidade, Inclusão e Acessibilidade)**
| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `tem_deia` | Possui conteúdo DEIA | `"Sim"` ou `"Não"` |
| `deia_encontrado` | Descritor específico | `"Saúde da População Negra"` |
| `texto_analisado_deia` | Texto analisado | `"Título: Curso... + Descrição:..."` |

---

## 🛠️ Como Usar (Guia Passo a Passo)

### 📋 **Pré-requisitos**
Antes de começar, você precisa ter:
- **Python 3.8 ou superior** instalado
- **Conexão com a internet** estável
- **Conhecimento básico** de linha de comando

### 🔧 **Instalação**

#### 1️⃣ **Clone o projeto**
```bash
git clone https://github.com/seu-usuario/una-sus.git
cd una-sus
```

#### 2️⃣ **Instale as dependências**
```bash
pip install -r requirements.txt
```

#### 3️⃣ **Verifique se tudo está funcionando**
```bash
python --version
pip list | grep -E "(requests|pandas|beautifulsoup)"
```

### 🚀 **Execução**

#### 🎯 **Opção 1: Coleta Completa (Recomendado)**
```bash
python scraper_unasus_melhorado.py
```

**O que acontece:**
- 🔍 **Busca** todos os cursos da UNA-SUS
- 📊 **Coleta** dados detalhados de cada curso
- 🌈 **Analisa** conteúdo DEIA automaticamente
- 💾 **Salva** progresso a cada 10 cursos
- 📈 **Mostra** estatísticas em tempo real

#### 🔄 **Opção 2: Reanálise de Dados Existentes**
Se você já tem dados coletados e quer apenas atualizar a análise DEIA:
```bash
python reanalisar_deia_existente.py
```

#### 🧪 **Opção 3: Teste da Busca DEIA**
Para validar se a busca DEIA está funcionando:
```bash
python testar_busca_deia.py
```

---

## 📈 Monitoramento e Logs

### 👀 **Como Acompanhar o Progresso**

Durante a execução, você verá mensagens como:
```
2025-07-26 15:30:15 - INFO - === PROCESSANDO PÁGINA 5 ===
2025-07-26 15:30:16 - INFO - Processando curso 44538: Atenção à Saúde da População Negra
2025-07-26 15:30:16 - INFO - 🌈 DEIA encontrado no curso 44538: População Negra
2025-07-26 15:30:17 - INFO - Buscando ofertas do curso 44538...
2025-07-26 15:30:17 - INFO -   ✅ Oferta encontrada: 416264
2025-07-26 15:30:18 - INFO -   🔍 Extraindo dados da oferta 416264...
2025-07-26 15:30:18 - INFO -     ✅ Dados obtidos via API REST
2025-07-26 15:30:18 - INFO -     ✅ Vagas extraídas: 1000
```

### 🎨 **Significado dos Emojis nos Logs**

| Emoji | Significado | Exemplo |
|-------|-------------|---------|
| 🌈 | **DEIA detectado** | `🌈 DEIA encontrado: População Negra` |
| ✅ | **Sucesso** | `✅ Oferta encontrada: 416264` |
| 🔍 | **Processando** | `🔍 Extraindo dados...` |
| 📊 | **Estatísticas** | `📊 Total de registros: 1656` |
| 💾 | **Salvando** | `💾 Progresso salvo` |
| ⚠️ | **Aviso** | `⚠️ Curso sem ofertas` |
| ❌ | **Erro** | `❌ Erro na conexão` |

### 📊 **Estatísticas Finais**
Ao final da execução, você verá:
```
=== RELATÓRIO FINAL ===
📊 Total de registros: 1656
🌈 Cursos com DEIA: 604 (36.5%)
📚 Cursos sem DEIA: 1052 (63.5%)
📁 Arquivo salvo: unasus_ofertas_melhoradas.csv
```

---

## 📁 Estrutura do Projeto

```
una-sus/
├── 🐍 scraper_unasus_melhorado.py    # Scraper principal (MAIS RECENTE)
├── 🐍 scraper_unasus.py              # Scraper original (referência)
├── 🐍 reanalisar_deia_existente.py   # Reanálise DEIA
├── 🐍 testar_busca_deia.py           # Testes DEIA
├── 📊 unasus_ofertas_melhoradas.csv  # Dados coletados
├── 📚 README.md                      # Esta documentação
├── 📚 README_MELHORIAS_DEIA.md       # Detalhes das melhorias
├── 📋 requirements.txt               # Dependências
├── ⚙️ pyproject.toml                 # Configuração do projeto
├── 🐳 Dockerfile                     # Containerização
├── 🐳 docker-compose.yml             # Orquestração
└── 📄 LICENSE                        # Licença MIT
```

---

## 🌈 Análise DEIA - Explicação Detalhada

### 🎯 **O que é DEIA?**
**DEIA** significa **Diversidade, Equidade, Inclusão e Acessibilidade**. É um conceito fundamental para:
- 🏥 **Saúde pública** inclusiva
- 🎓 **Educação** acessível a todos
- 🤝 **Sociedade** mais justa e equitativa

### 🔍 **Como Funciona a Detecção?**

O sistema analisa **todos os campos** coletados:
1. **Título do curso** (`no_curso`)
2. **Descrição do curso** (`ds_curso`)
3. **Descrição da oferta** (`descricao_oferta`)
4. **Palavras-chave** (`palavras_chave`)
5. **Público-alvo** (`publico_alvo`)
6. **Temas** (`temas`)
7. **DeCs** (`decs`)
8. **Programas de governo** (`programas_governo`)
9. **Texto da página inicial** (`texto_pagina_inicial`)

### 📝 **Exemplos de Descritores DEIA**

#### 👥 **Populações Específicas**
- População Negra, População Indígena
- População LGBTQI+, Trans, Transgênero
- População em Situação de Rua
- População Privada de Liberdade

#### 🏥 **Saúde Específica**
- Saúde Mental, Saúde da Mulher
- Saúde da Criança, Saúde do Idoso
- Saúde da População Negra
- Saúde Indígena

#### 🌍 **Conceitos DEIA**
- Diversidade, Equidade, Inclusão
- Acessibilidade, Pertencimento
- Direitos Humanos, Cidadania
- Vulnerabilidade, Discriminação

---

## 🚨 Solução de Problemas

### ❓ **Perguntas Frequentes**

#### **Q: O scraper parou no meio. O que fazer?**
**A:** Não se preocupe! O sistema tem **checkpoint automático**. Basta executar novamente:
```bash
python scraper_unasus_melhorado.py
```
Ele continuará de onde parou.

#### **Q: Não encontrou nenhum curso com DEIA. É normal?**
**A:** Se você está usando o scraper original (`scraper_unasus.py`), sim. Use o **melhorado**:
```bash
python scraper_unasus_melhorado.py
```

#### **Q: O arquivo CSV está muito grande. É normal?**
**A:** Sim! O arquivo pode ter **8+ MB** porque contém:
- 1.656 registros de ofertas
- 30 colunas de dados
- Textos completos dos cursos

#### **Q: Como saber se está funcionando?**
**A:** Observe os logs:
- ✅ **Verde** = funcionando
- ⚠️ **Amarelo** = aviso (normal)
- ❌ **Vermelho** = erro (raro)

### 🔧 **Problemas Técnicos**

#### **Erro de Conexão**
```bash
# Tente novamente em alguns minutos
python scraper_unasus_melhorado.py
```

#### **Erro de Dependências**
```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

#### **Erro de Permissão**
```bash
# No Windows, execute como administrador
# No Linux/Mac, use sudo se necessário
```

---

## 📊 Análise dos Resultados

### 📈 **Estatísticas Típicas**
- **Total de cursos**: ~550 cursos únicos
- **Total de ofertas**: ~1.650 ofertas
- **Cursos com DEIA**: ~600 (36%)
- **Cursos sem DEIA**: ~1.050 (64%)

### 🔍 **Como Analisar os Dados**

#### **1. Abrir no Excel/LibreOffice**
```bash
# O arquivo é compatível com Excel
unasus_ofertas_melhoradas.csv
```

#### **2. Filtrar por DEIA**
- Coluna `tem_deia` = "Sim"
- Ver coluna `deia_encontrado` para detalhes

#### **3. Análise por Tema**
- Coluna `temas` para categorização
- Coluna `decs` para classificação médica

#### **4. Análise Geográfica**
- Coluna `local_oferta` para distribuição
- Coluna `no_orgao` para instituições

---

## 🤝 Contribuição

### 💡 **Como Contribuir**

1. **🔍 Encontrou um bug?**
   - Abra uma **Issue** no GitHub
   - Descreva o problema detalhadamente

2. **✨ Tem uma ideia?**
   - Sugira melhorias via **Issue**
   - Proponha novos descritores DEIA

3. **💻 Quer programar?**
   - Faça um **Fork** do projeto
   - Crie uma **Pull Request**

### 📝 **Padrões do Projeto**

#### **Emojis Educativos**
Use emojis para facilitar a compreensão:
- 🎓 = Educação/Academia
- 🏥 = Saúde
- 🌈 = DEIA/Diversidade
- 📊 = Dados/Estatísticas
- 🔍 = Busca/Análise
- ✅ = Sucesso
- ❌ = Erro

#### **Comentários no Código**
```python
# 🌈 Busca por descritores DEIA no texto
def encontrar_descritor_deia_melhorado(texto_completo):
    """
    📝 Analisa texto completo em busca de descritores DEIA
    
    Args:
        texto_completo (str): Texto combinado de todos os campos
        
    Returns:
        str: Descritor DEIA encontrado ou None
    """
```

---

## 📚 Recursos Educativos

### 🎓 **Para Estudantes**
- **Web Scraping**: Aprenda a coletar dados da web
- **Análise de Dados**: Trabalhe com datasets reais
- **Python**: Pratique programação em Python
- **Saúde Pública**: Entenda dados educacionais em saúde

### 🔬 **Para Pesquisadores**
- **Metodologia**: Exemplo de coleta sistemática de dados
- **DEIA**: Framework para análise de diversidade
- **Estatísticas**: Dados quantitativos para pesquisas
- **Qualidade**: Dados validados e estruturados

### 💻 **Para Desenvolvedores**
- **Clean Code**: Código bem estruturado e documentado
- **Error Handling**: Tratamento robusto de erros
- **Logging**: Sistema de logs detalhado
- **Modularização**: Funções bem separadas

---

## 📄 Licença

Este projeto está sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

**O que isso significa?**
- ✅ **Pode usar** livremente
- ✅ **Pode modificar** o código
- ✅ **Pode distribuir** o projeto
- ✅ **Pode usar comercialmente**
- ❌ **Não precisa** dar crédito (mas é apreciado!)

---

## 🙏 Agradecimentos

- 🏥 **UNA-SUS** pela disponibilização dos dados
- 🐍 **Comunidade Python** pelos recursos utilizados
- 🌈 **Comunidade DEIA** pela inspiração
- 👥 **Contribuidores** do projeto

---

## 📞 Suporte

### 🆘 **Precisa de Ajuda?**

1. **📖 Leia** esta documentação completa
2. **🔍 Verifique** as seções de solução de problemas
3. **💬 Abra** uma Issue no GitHub
4. **📧 Entre em contato** com os mantenedores

### 📚 **Recursos Adicionais**

- 📖 **Documentação Python**: https://docs.python.org/
- 🐍 **Tutorial Requests**: https://requests.readthedocs.io/
- 🍲 **BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/
- 📊 **Pandas**: https://pandas.pydata.org/

---

**🎯 Desenvolvido com ❤️ para facilitar pesquisas em saúde pública e promover educação inclusiva!**

*Última atualização: Julho 2025*
