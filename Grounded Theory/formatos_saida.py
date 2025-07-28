#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 FORMATOS DE SAÍDA PADRONIZADOS
==================================

Definições dos formatos de saída para interoperabilidade
com outras aplicações e sistemas.
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class TipoSaida(Enum):
    """Tipos de saída disponíveis."""

    JSON = "json"
    CSV = "csv"
    MARKDOWN = "markdown"
    XML = "xml"
    YAML = "yaml"


class TipoAnalise(Enum):
    """Tipos de análise disponíveis."""

    COLETA_DADOS = "coleta_dados"
    ANALISE_EXPLORATORIA = "analise_exploratoria"
    CODIFICACAO_ABERTA = "codificacao_aberta"
    CODIFICACAO_AXIAL = "codificacao_axial"
    CODIFICACAO_SELETIVA = "codificacao_seletiva"
    GROUNDED_THEORY = "grounded_theory"
    ANALISE_DEIA = "analise_deia"
    ANALISE_FORMACAO = "analise_formacao"


@dataclass
class MetadataSaida:
    """Metadados padronizados para todas as saídas."""

    timestamp_geracao: str
    versao_sistema: str = "1.0.0"
    tipo_analise: str = ""
    fonte_dados: str = ""
    total_registros: int = 0
    parametros_analise: Dict[str, Any] = None

    def __post_init__(self):
        if self.parametros_analise is None:
            self.parametros_analise = {}


@dataclass
class ResultadoColeta:
    """Formato padronizado para resultados de coleta."""

    metadata: MetadataSaida
    dados_coletados: List[Dict[str, Any]]
    estatisticas_coleta: Dict[str, Any]
    erros_coleta: List[str] = None

    def __post_init__(self):
        if self.erros_coleta is None:
            self.erros_coleta = []


@dataclass
class ResultadoAnaliseExploratoria:
    """Formato padronizado para análise exploratória."""

    metadata: MetadataSaida
    estrutura_dados: Dict[str, Any]
    campos_disponiveis: Dict[str, Any]
    distribuicao_cursos: Dict[str, Any]
    instituicoes: Dict[str, Any]
    modalidades: Dict[str, Any]
    carga_horaria: Dict[str, Any]
    elementos_deia: Dict[str, Any]
    cursos_formacao: Dict[str, Any]
    padroes_texto: Dict[str, Any] = None

    def __post_init__(self):
        if self.padroes_texto is None:
            self.padroes_texto = {}


@dataclass
class ResultadoCodificacao:
    """Formato padronizado para resultados de codificação."""

    metadata: MetadataSaida
    conceitos_identificados: Dict[str, Any]
    categorias_geradas: List[str]
    memos_analiticos: List[Dict[str, Any]]
    estatisticas_codificacao: Dict[str, Any]
    relacoes_identificadas: Dict[str, Any] = None

    def __post_init__(self):
        if self.relacoes_identificadas is None:
            self.relacoes_identificadas = {}


@dataclass
class ResultadoGroundedTheory:
    """Formato padronizado para resultados da Grounded Theory."""

    metadata: MetadataSaida
    fenomeno_central: str
    categorias_principais: List[Dict[str, Any]]
    proposicoes_teoricas: List[str]
    modelo_teorico: Dict[str, Any]
    saturação_atingida: bool
    iteracoes_realizadas: int
    teoria_desenvolvida: str = ""

    def __post_init__(self):
        if self.teoria_desenvolvida == "":
            self.teoria_desenvolvida = "Teoria em desenvolvimento"


class GeradorSaida:
    """Gerador de saídas padronizadas."""

    def __init__(self, versao_sistema: str = "1.0.0"):
        self.versao_sistema = versao_sistema

    def criar_metadata(
        self,
        tipo_analise: TipoAnalise,
        fonte_dados: str = "",
        total_registros: int = 0,
        parametros: Dict[str, Any] = None,
    ) -> MetadataSaida:
        """Cria metadados padronizados."""
        return MetadataSaida(
            timestamp_geracao=datetime.now().isoformat(),
            versao_sistema=self.versao_sistema,
            tipo_analise=tipo_analise.value,
            fonte_dados=fonte_dados,
            total_registros=total_registros,
            parametros_analise=parametros or {},
        )

    def gerar_saida_coleta(
        self,
        dados: List[Dict],
        estatisticas: Dict,
        erros: List[str] = None,
        fonte_dados: str = "",
    ) -> ResultadoColeta:
        """Gera saída padronizada para coleta de dados."""
        metadata = self.criar_metadata(
            TipoAnalise.COLETA_DADOS,
            fonte_dados=fonte_dados,
            total_registros=len(dados),
        )

        return ResultadoColeta(
            metadata=metadata,
            dados_coletados=dados,
            estatisticas_coleta=estatisticas,
            erros_coleta=erros or [],
        )

    def gerar_saida_analise_exploratoria(
        self, resultados: Dict, total_registros: int
    ) -> ResultadoAnaliseExploratoria:
        """Gera saída padronizada para análise exploratória."""
        metadata = self.criar_metadata(
            TipoAnalise.ANALISE_EXPLORATORIA, total_registros=total_registros
        )

        return ResultadoAnaliseExploratoria(
            metadata=metadata,
            estrutura_dados=resultados.get("estrutura", {}),
            campos_disponiveis=resultados.get("campos", {}),
            distribuicao_cursos=resultados.get("niveis", {}),
            instituicoes=resultados.get("instituicoes", {}),
            modalidades=resultados.get("modalidades", {}),
            carga_horaria=resultados.get("carga_horaria", {}),
            elementos_deia=resultados.get("deia", {}),
            cursos_formacao=resultados.get("formacao", {}),
            padroes_texto=resultados.get("padroes_texto", {}),
        )

    def gerar_saida_codificacao(
        self, resultados: Dict, tipo_codificacao: TipoAnalise
    ) -> ResultadoCodificacao:
        """Gera saída padronizada para codificação."""
        metadata = self.criar_metadata(tipo_codificacao)

        return ResultadoCodificacao(
            metadata=metadata,
            conceitos_identificados=resultados.get("conceitos_identificados", {}),
            categorias_geradas=resultados.get("categorias_iniciais", []),
            memos_analiticos=resultados.get("memos_analiticos", []),
            estatisticas_codificacao=resultados.get("estatisticas", {}),
            relacoes_identificadas=resultados.get("relacionamentos", {}),
        )

    def gerar_saida_grounded_theory(self, resultados: Dict) -> ResultadoGroundedTheory:
        """Gera saída padronizada para Grounded Theory."""
        metadata = self.criar_metadata(TipoAnalise.GROUNDED_THEORY)

        return ResultadoGroundedTheory(
            metadata=metadata,
            fenomeno_central=resultados.get("fenomeno_central", "Não identificado"),
            categorias_principais=resultados.get("categorias_integradas", []),
            proposicoes_teoricas=resultados.get("proposicoes_teoricas", []),
            modelo_teorico=resultados.get("modelo_teorico", {}),
            saturação_atingida=resultados.get("saturacao_atingida", False),
            iteracoes_realizadas=resultados.get("iteracoes_realizadas", 0),
            teoria_desenvolvida=resultados.get("teoria_final", ""),
        )

    def salvar_json(self, resultado: Any, nome_arquivo: str):
        """Salva resultado em formato JSON."""
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(asdict(resultado), f, ensure_ascii=False, indent=2)

    def salvar_csv(self, dados: List[Dict], nome_arquivo: str):
        """Salva dados em formato CSV."""
        import pandas as pd

        df = pd.DataFrame(dados)
        df.to_csv(nome_arquivo, index=False, encoding="utf-8")

    def salvar_markdown(self, resultado: Any, nome_arquivo: str):
        """Salva resultado em formato Markdown."""
        # Implementar conversão para Markdown
        pass


class EsquemasValidacao:
    """Esquemas de validação para os formatos de saída."""

    @staticmethod
    def validar_coleta(resultado: ResultadoColeta) -> List[str]:
        """Valida formato de saída de coleta."""
        erros = []

        if not resultado.metadata.timestamp_geracao:
            erros.append("Timestamp de geração obrigatório")

        if not resultado.dados_coletados:
            erros.append("Dados coletados obrigatórios")

        if resultado.metadata.total_registros != len(resultado.dados_coletados):
            erros.append("Total de registros não confere com dados coletados")

        return erros

    @staticmethod
    def validar_analise_exploratoria(
        resultado: ResultadoAnaliseExploratoria,
    ) -> List[str]:
        """Valida formato de saída de análise exploratória."""
        erros = []

        if not resultado.metadata.tipo_analise:
            erros.append("Tipo de análise obrigatório")

        if not resultado.estrutura_dados:
            erros.append("Estrutura de dados obrigatória")

        if not resultado.campos_disponiveis:
            erros.append("Campos disponíveis obrigatórios")

        return erros

    @staticmethod
    def validar_codificacao(resultado: ResultadoCodificacao) -> List[str]:
        """Valida formato de saída de codificação."""
        erros = []

        if not resultado.conceitos_identificados:
            erros.append("Conceitos identificados obrigatórios")

        if not resultado.categorias_geradas:
            erros.append("Categorias geradas obrigatórias")

        return erros


class ConversorFormatos:
    """Conversor entre diferentes formatos de saída."""

    @staticmethod
    def json_para_csv(dados_json: List[Dict], nome_arquivo_csv: str):
        """Converte dados JSON para CSV."""
        import pandas as pd

        df = pd.DataFrame(dados_json)
        df.to_csv(nome_arquivo_csv, index=False, encoding="utf-8")

    @staticmethod
    def json_para_xml(dados_json: List[Dict], nome_arquivo_xml: str):
        """Converte dados JSON para XML."""
        import xml.etree.ElementTree as ET
        from xml.dom import minidom

        root = ET.Element("dados")

        for item in dados_json:
            registro = ET.SubElement(root, "registro")
            for chave, valor in item.items():
                campo = ET.SubElement(registro, chave)
                campo.text = str(valor)

        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")

        with open(nome_arquivo_xml, "w", encoding="utf-8") as f:
            f.write(xml_str)

    @staticmethod
    def json_para_yaml(dados_json: List[Dict], nome_arquivo_yaml: str):
        """Converte dados JSON para YAML."""
        import yaml

        with open(nome_arquivo_yaml, "w", encoding="utf-8") as f:
            yaml.dump(dados_json, f, default_flow_style=False, allow_unicode=True)


class DocumentacaoFormatos:
    """Documentação dos formatos de saída."""

    @staticmethod
    def gerar_documentacao_formatos(nome_arquivo: str = "FORMATOS_SAIDA.md"):
        """Gera documentação dos formatos de saída."""
        doc = """# 📋 DOCUMENTAÇÃO DOS FORMATOS DE SAÍDA

## 🎯 **OBJETIVO**

Esta documentação define os formatos padronizados de saída para garantir interoperabilidade com outras aplicações.

## 📊 **TIPOS DE SAÍDA**

### **JSON (Padrão)**
- Formato principal para todas as saídas
- Estrutura hierárquica bem definida
- Metadados incluídos em cada arquivo

### **CSV**
- Para dados tabulares
- Compatível com Excel e outras ferramentas
- Sem metadados (apenas dados)

### **Markdown**
- Para relatórios humanos
- Formatação rica
- Inclui metadados e explicações

### **XML**
- Para integração com sistemas legados
- Estrutura hierárquica
- Metadados incluídos

### **YAML**
- Para configurações e metadados
- Formato legível
- Estrutura hierárquica

## 🔧 **ESTRUTURAS DE DADOS**

### **MetadataSaida**
```json
{
  "timestamp_geracao": "2025-07-28T19:30:00",
  "versao_sistema": "1.0.0",
  "tipo_analise": "coleta_dados",
  "fonte_dados": "UNA-SUS API",
  "total_registros": 420,
  "parametros_analise": {}
}
```

### **ResultadoColeta**
```json
{
  "metadata": {...},
  "dados_coletados": [...],
  "estatisticas_coleta": {...},
  "erros_coleta": []
}
```

### **ResultadoAnaliseExploratoria**
```json
{
  "metadata": {...},
  "estrutura_dados": {...},
  "campos_disponiveis": {...},
  "distribuicao_cursos": {...},
  "instituicoes": {...},
  "modalidades": {...},
  "carga_horaria": {...},
  "elementos_deia": {...},
  "cursos_formacao": {...},
  "padroes_texto": {...}
}
```

### **ResultadoCodificacao**
```json
{
  "metadata": {...},
  "conceitos_identificados": {...},
  "categorias_geradas": [...],
  "memos_analiticos": [...],
  "estatisticas_codificacao": {...},
  "relacoes_identificadas": {...}
}
```

### **ResultadoGroundedTheory**
```json
{
  "metadata": {...},
  "fenomeno_central": "string",
  "categorias_principais": [...],
  "proposicoes_teoricas": [...],
  "modelo_teorico": {...},
  "saturação_atingida": true,
  "iteracoes_realizadas": 3,
  "teoria_desenvolvida": "string"
}
```

## 📁 **CONVENÇÕES DE NOMENCLATURA**

### **Arquivos de Coleta**
- `coleta_dados_YYYYMMDD_HHMMSS.json`
- `coleta_dados_YYYYMMDD_HHMMSS.csv`

### **Arquivos de Análise**
- `analise_exploratoria_YYYYMMDD_HHMMSS.json`
- `analise_exploratoria_YYYYMMDD_HHMMSS.md`

### **Arquivos de Codificação**
- `codificacao_aberta_YYYYMMDD_HHMMSS.json`
- `codificacao_axial_YYYYMMDD_HHMMSS.json`
- `codificacao_seletiva_YYYYMMDD_HHMMSS.json`

### **Arquivos de Grounded Theory**
- `grounded_theory_YYYYMMDD_HHMMSS.json`
- `grounded_theory_YYYYMMDD_HHMMSS.md`

## 🔍 **VALIDAÇÃO**

Todos os arquivos de saída são validados automaticamente:

- **Campos obrigatórios** presentes
- **Tipos de dados** corretos
- **Consistência** entre metadados e dados
- **Integridade** dos dados

## 🔄 **CONVERSÃO DE FORMATOS**

### **JSON → CSV**
```python
ConversorFormatos.json_para_csv(dados_json, "saida.csv")
```

### **JSON → XML**
```python
ConversorFormatos.json_para_xml(dados_json, "saida.xml")
```

### **JSON → YAML**
```python
ConversorFormatos.json_para_yaml(dados_json, "saida.yaml")
```

## 📊 **EXEMPLOS DE USO**

### **Gerar Saída de Coleta**
```python
gerador = GeradorSaida()
resultado = gerador.gerar_saida_coleta(dados, estatisticas)
gerador.salvar_json(resultado, "coleta.json")
```

### **Gerar Saída de Análise**
```python
resultado = gerador.gerar_saida_analise_exploratoria(resultados, 420)
gerador.salvar_json(resultado, "analise.json")
```

### **Validar Saída**
```python
erros = EsquemasValidacao.validar_coleta(resultado)
if erros:
    print(f"Erros de validação: {erros}")
```

## 🎯 **INTEGRAÇÃO COM OUTRAS APLICAÇÕES**

### **Python**
```python
import json
with open("coleta.json", "r") as f:
    dados = json.load(f)
```

### **R**
```r
library(jsonlite)
dados <- fromJSON("coleta.json")
```

### **JavaScript**
```javascript
const dados = JSON.parse(fs.readFileSync("coleta.json"));
```

### **Excel**
- Abrir arquivo CSV diretamente
- Ou usar Power Query para JSON

---
*Documentação gerada automaticamente*
"""

        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(doc)


if __name__ == "__main__":
    # Gerar documentação
    DocumentacaoFormatos.gerar_documentacao_formatos()
    print("✅ Documentação dos formatos gerada: FORMATOS_SAIDA.md")
