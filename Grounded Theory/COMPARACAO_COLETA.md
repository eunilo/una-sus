# 🔍 COMPARAÇÃO: Metodologia de Coleta - Atual vs Backup Original

## 📊 **RESUMO EXECUTIVO**

**PROBLEMA IDENTIFICADO**: A metodologia de coleta atual está **INCOMPATÍVEL** com o backup original, causando erro 404 na API.

## 🚨 **DIFERENÇAS CRÍTICAS ENCONTRADAS**

### **1. 🔗 URL da API**
| **Backup Original** | **Sistema Atual** |
|---------------------|-------------------|
| `https://www.unasus.gov.br/cursos/rest/busca` | `https://unasus.gov.br/api/cursos` |

### **2. 📋 Headers HTTP**
| **Backup Original** | **Sistema Atual** |
|---------------------|-------------------|
| ```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.unasus.gov.br",
    "Referer": "https://www.unasus.gov.br/cursos/busca?status=todos&busca=&ordenacao=Relev%C3%A2ncia%20na%20busca",
}
``` | ```python
self.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
``` |

### **3. 🍪 Cookies**
| **Backup Original** | **Sistema Atual** |
|---------------------|-------------------|
| ```python
COOKIES = {
    "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
    "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
    "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272": "_329a72cffc11d2904ae393c82d0cfb72",
}
``` | **❌ NENHUM COOKIE** |

### **4. 📦 Payload da Requisição**
| **Backup Original** | **Sistema Atual** |
|---------------------|-------------------|
| ```python
PAYLOAD_INICIAL = {
    "busca": "",
    "ordenacao": "Por nome",
    "status": "Todos",
    "proximo": 0,
}
``` | ```python
payload = {
    "page": 1,
    "size": 50,
    "sort": "rank,asc",
}
``` |

### **5. 🔄 Método de Envio**
| **Backup Original** | **Sistema Atual** |
|---------------------|-------------------|
| `requests.post(URL, data=payload, headers=HEADERS, cookies=COOKIES)` | `requests.post(self.url, json=payload, headers=self.headers)` |

## ⚠️ **PROBLEMAS IDENTIFICADOS**

### **❌ Problema 1: URL Incorreta**
- **Backup**: `https://www.unasus.gov.br/cursos/rest/busca`
- **Atual**: `https://unasus.gov.br/api/cursos`
- **Impacto**: Erro 404 - endpoint não existe

### **❌ Problema 2: Headers Incompletos**
- **Backup**: Headers completos com Content-Type, Accept, Origin, etc.
- **Atual**: Apenas User-Agent básico
- **Impacto**: API pode rejeitar requisições

### **❌ Problema 3: Cookies Ausentes**
- **Backup**: Cookies específicos do portal UNA-SUS
- **Atual**: Nenhum cookie
- **Impacto**: Autenticação/sessão pode falhar

### **❌ Problema 4: Payload Incompatível**
- **Backup**: Parâmetros específicos da API original
- **Atual**: Parâmetros genéricos
- **Impacto**: API não reconhece parâmetros

### **❌ Problema 5: Método de Envio**
- **Backup**: `data=payload` (form-encoded)
- **Atual**: `json=payload` (JSON)
- **Impacto**: Formato de dados incorreto

## 🔧 **SOLUÇÃO PROPOSTA**

### **1. Corrigir Configurações da API**
```python
# URL correta
self.url = "https://www.unasus.gov.br/cursos/rest/busca"

# Headers completos
self.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.unasus.gov.br",
    "Referer": "https://www.unasus.gov.br/cursos/busca?status=todos&busca=&ordenacao=Relev%C3%A2ncia%20na%20busca",
}

# Cookies necessários
self.cookies = {
    "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
    "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
    "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272": "_329a72cffc11d2904ae393c82d0cfb72",
}
```

### **2. Corrigir Payload**
```python
payload = {
    "busca": "",
    "ordenacao": "Por nome",
    "status": "Todos",
    "proximo": pagina,
}
```

### **3. Corrigir Método de Envio**
```python
response = requests.post(
    self.url, 
    data=payload, 
    headers=self.headers, 
    cookies=self.cookies, 
    timeout=30
)
```

## ✅ **CORREÇÕES APLICADAS COM SUCESSO**

### **1. ✅ Configurações da API Corrigidas**
- **URL**: `https://www.unasus.gov.br/cursos/rest/busca` ✅
- **Headers**: Completos com Content-Type, Accept, Origin, etc. ✅
- **Cookies**: Implementados corretamente ✅

### **2. ✅ Payload Corrigido**
- **Formato**: `data=payload` (form-encoded) ✅
- **Parâmetros**: Compatíveis com API original ✅
- **Paginação**: Usando `proximo` em vez de `page` ✅

### **3. ✅ Teste de Validação**
- **Resultado**: 420 registros coletados com sucesso ✅
- **Metadados**: Rastreabilidade completa ✅
- **Sem filtros**: Coleta inicial completa funcionando ✅

## 📊 **RESULTADOS DO TESTE**

```
✅ COLETA COMPLETA BEM-SUCEDIDA!
📊 Total de registros coletados: 420
📋 Exemplos de dados coletados:
1. 1º Formação de Preceptores para o SUS - Universidade Federal de São Paulo
2. 2º Formação de Preceptores para o SUS - Universidade Federal de São Paulo
3. Abordagem Clínica de Zika na Atenção Primária à Saúde - Fundação Oswaldo Cruz
```

## 🎯 **STATUS ATUAL**

**✅ SISTEMA FUNCIONANDO PERFEITAMENTE**
- Coleta inicial completa sem filtros ✅
- Compatibilidade total com backup original ✅
- Metodologia validada e testada ✅

## 🎯 **OBJETIVO**

Garantir que a coleta inicial completa funcione corretamente, seguindo exatamente a metodologia testada e validada do backup original, mas mantendo o princípio de **coleta sem filtros** para preservar a integridade completa do banco de dados. 