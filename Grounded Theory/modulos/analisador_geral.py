#!/usr/bin/env python3
"""
📊 Analisador Geral - Análises Flexíveis de Dados
=================================================

Este módulo implementa análises gerais e flexíveis dos dados coletados,
permitindo diferentes tipos de análise sem comprometer a integridade
dos dados originais.

🎯 PRINCÍPIOS:
- Trabalha com dados já coletados
- NÃO modifica dados originais
- Análises flexíveis e configuráveis
- Preserva database fiel
- Múltiplos tipos de análise

🔬 TIPOS DE ANÁLISE:
- Análise estatística geral
- Análise por categorias
- Análise temporal
- Análise geográfica
- Análise de conteúdo
- Análise comparativa
- Análise customizada
"""

import json
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


class AnalisadorGeral:
    """
    📊 Analisador Geral para Dados UNA-SUS

    Realiza análises flexíveis e configuráveis dos dados coletados.
    """

    def __init__(self, logger: logging.Logger = None):
        """
        Inicializa o analisador geral.

        Args:
            logger: Logger para acompanhamento
        """
        self.logger = logger or self._configurar_logger()
        self.dados_originais = []
        self.dados_processados = []
        self.resultados_analise = {}
        self.configuracoes_analise = {}

    def _configurar_logger(self) -> logging.Logger:
        """
        📝 Configura o logger para o analisador.

        Returns:
            Logger configurado
        """
        # Criar pasta de logs se não existir
        os.makedirs("logs", exist_ok=True)

        # Configurar logger
        logger = logging.getLogger("AnalisadorGeral")
        logger.setLevel(logging.INFO)

        # Handler para arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fh = logging.FileHandler(
            f"logs/analisador_geral_{timestamp}.log", encoding="utf-8"
        )
        fh.setLevel(logging.INFO)

        # Handler para console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formato
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Adicionar handlers
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def carregar_dados_para_analise(self, caminho_arquivo: str) -> bool:
        """
        📂 Carrega dados para análise.

        Args:
            caminho_arquivo: Caminho para o arquivo de dados

        Returns:
            True se carregado com sucesso
        """
        try:
            self.logger.info(f"🔄 Carregando dados de: {caminho_arquivo}")

            # Tentar carregar CSV primeiro
            if caminho_arquivo.endswith(".csv"):
                df = pd.read_csv(caminho_arquivo, encoding="utf-8")
                self.dados_originais = df.to_dict("records")

            # Tentar carregar JSON
            elif caminho_arquivo.endswith(".json"):
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    self.dados_originais = json.load(f)

            # Tentar carregar Excel (se disponível)
            elif caminho_arquivo.endswith((".xlsx", ".xls")):
                try:
                    df = pd.read_excel(caminho_arquivo)
                    self.dados_originais = df.to_dict("records")
                except ImportError:
                    raise ValueError(
                        "❌ openpyxl não está instalado. "
                        "Instale com: pip install openpyxl"
                    )

            else:
                raise ValueError(
                    f"❌ Formato de arquivo não suportado: {caminho_arquivo}"
                )

            self.logger.info(
                f"✅ Dados carregados: {len(self.dados_originais)} registros"
            )
            return True

        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar dados: {str(e)}")
            return False

    def configurar_analise(self, tipo_analise: str, parametros: Dict = None):
        """
        ⚙️ Configura o tipo de análise a ser realizada.

        Args:
            tipo_analise: Tipo de análise ('estatistica', 'categoria', 'temporal', etc.)
            parametros: Parâmetros específicos da análise
        """
        self.configuracoes_analise = {
            "tipo": tipo_analise,
            "parametros": parametros or {},
            "timestamp": datetime.now().isoformat(),
        }

        self.logger.info(f"⚙️ Análise configurada: {tipo_analise}")

    def executar_analise(self) -> Dict:
        """
        🚀 Executa a análise configurada.

        Returns:
            Resultados da análise
        """
        if not self.dados_originais:
            self.logger.error("❌ Nenhum dado carregado para análise")
            return {}

        tipo_analise = self.configuracoes_analise.get("tipo", "estatistica")

        self.logger.info(f"🚀 Executando análise: {tipo_analise}")

        if tipo_analise == "estatistica":
            return self._analise_estatistica_geral()
        elif tipo_analise == "categoria":
            return self._analise_por_categoria()
        elif tipo_analise == "temporal":
            return self._analise_temporal()
        elif tipo_analise == "geografica":
            return self._analise_geografica()
        elif tipo_analise == "conteudo":
            return self._analise_conteudo()
        elif tipo_analise == "comparativa":
            return self._analise_comparativa()
        elif tipo_analise == "customizada":
            return self._analise_customizada()
        else:
            self.logger.warning(f"⚠️ Tipo de análise não reconhecido: {tipo_analise}")
            return self._analise_estatistica_geral()

    def _analise_estatistica_geral(self) -> Dict:
        """
        📊 Análise estatística geral dos dados.

        Returns:
            Estatísticas gerais
        """
        self.logger.info("📊 Executando análise estatística geral")

        if not self.dados_originais:
            return {}

        df = pd.DataFrame(self.dados_originais)

        estatisticas = {
            "resumo_geral": {
                "total_cursos": len(df),
                "campos_disponiveis": list(df.columns),
                "campos_preenchidos": df.count().to_dict(),
                "percentual_preenchimento": (df.count() / len(df) * 100).to_dict(),
            },
            "estatisticas_numericas": {},
            "estatisticas_categoricas": {},
            "valores_unicos": {},
        }

        # Análise de campos numéricos
        campos_numericos = df.select_dtypes(include=["number"]).columns
        for campo in campos_numericos:
            estatisticas["estatisticas_numericas"][campo] = {
                "media": df[campo].mean(),
                "mediana": df[campo].median(),
                "min": df[campo].min(),
                "max": df[campo].max(),
                "desvio_padrao": df[campo].std(),
            }

            # Análise de campos categóricos
        campos_categoricos = df.select_dtypes(include=["object"]).columns
        for campo in campos_categoricos:
            # Pular campos que contêm dicionários ou objetos complexos
            if campo == "metadata_coleta":
                estatisticas["estatisticas_categoricas"][campo] = {
                    "valores_unicos": "N/A (campo com dicionários)",
                    "top_valores": {},
                    "valores_nulos": df[campo].isnull().sum(),
                    "tipo": "metadata_complexa",
                }
                continue

            try:
                valores_unicos = df[campo].nunique()
                top_valores = df[campo].value_counts().head(10).to_dict()
            except (TypeError, ValueError):
                # Se o campo contém objetos não-hashable (como dicionários)
                valores_unicos = len(df[campo].dropna().unique())
                top_valores = {}

            estatisticas["estatisticas_categoricas"][campo] = {
                "valores_unicos": valores_unicos,
                "top_valores": top_valores,
                "valores_nulos": df[campo].isnull().sum(),
            }

        # Valores únicos por campo
        for campo in df.columns:
            if campo == "metadata_coleta":
                estatisticas["valores_unicos"][campo] = "N/A (campo com dicionários)"
                continue

            try:
                estatisticas["valores_unicos"][campo] = df[campo].nunique()
            except (TypeError, ValueError):
                # Se o campo contém objetos não-hashable
                estatisticas["valores_unicos"][campo] = len(df[campo].dropna().unique())

        self.resultados_analise = estatisticas
        return estatisticas

    def _analise_por_categoria(self) -> Dict:
        """
        📂 Análise por categorias específicas.

        Returns:
            Análise por categorias
        """
        self.logger.info("📂 Executando análise por categoria")

        parametros = self.configuracoes_analise.get("parametros", {})
        campo_categoria = parametros.get("campo_categoria", "area_tematica")

        df = pd.DataFrame(self.dados_originais)

        if campo_categoria not in df.columns:
            self.logger.warning(
                f"⚠️ Campo de categoria não encontrado: {campo_categoria}"
            )
            return {}

        try:
            categorias_encontradas = df[campo_categoria].value_counts().to_dict()
        except (TypeError, ValueError):
            # Se o campo contém objetos não-hashable
            categorias_encontradas = {}

        analise_categoria = {
            "campo_analisado": campo_categoria,
            "categorias_encontradas": categorias_encontradas,
            "estatisticas_por_categoria": {},
        }

        # Estatísticas por categoria
        try:
            categorias_unicas = df[campo_categoria].unique()
        except (TypeError, ValueError):
            # Se o campo contém objetos não-hashable
            categorias_unicas = df[campo_categoria].dropna().unique()

        for categoria in categorias_unicas:
            if pd.isna(categoria):
                continue

            dados_categoria = df[df[campo_categoria] == categoria]
            analise_categoria["estatisticas_por_categoria"][str(categoria)] = {
                "quantidade": len(dados_categoria),
                "percentual": len(dados_categoria) / len(df) * 100,
            }

        self.resultados_analise = analise_categoria
        return analise_categoria

    def _analise_temporal(self) -> Dict:
        """
        📅 Análise temporal dos dados.

        Returns:
            Análise temporal
        """
        self.logger.info("📅 Executando análise temporal")

        df = pd.DataFrame(self.dados_originais)

        # Identificar campos de data
        campos_data = []
        for coluna in df.columns:
            if any(
                palavra in coluna.lower()
                for palavra in ["data", "inicio", "fim", "ano", "mes"]
            ):
                campos_data.append(coluna)

        analise_temporal = {
            "campos_data_encontrados": campos_data,
            "analise_por_campo": {},
        }

        for campo in campos_data:
            try:
                # Tentar converter para datetime
                df[campo] = pd.to_datetime(df[campo], errors="coerce")

                analise_temporal["analise_por_campo"][campo] = {
                    "primeira_data": df[campo].min(),
                    "ultima_data": df[campo].max(),
                    "periodo_dias": (df[campo].max() - df[campo].min()).days,
                    "distribuicao_anual": df[campo].dt.year.value_counts().to_dict(),
                }
            except:
                analise_temporal["analise_por_campo"][campo] = {
                    "erro": "Não foi possível converter para data"
                }

        self.resultados_analise = analise_temporal
        return analise_temporal

    def _analise_geografica(self) -> Dict:
        """
        🌍 Análise geográfica dos dados.

        Returns:
            Análise geográfica
        """
        self.logger.info("🌍 Executando análise geográfica")

        df = pd.DataFrame(self.dados_originais)

        # Identificar campos geográficos
        campos_geo = []
        for coluna in df.columns:
            if any(
                palavra in coluna.lower()
                for palavra in ["estado", "cidade", "regiao", "uf", "local"]
            ):
                campos_geo.append(coluna)

        analise_geografica = {
            "campos_geograficos_encontrados": campos_geo,
            "distribuicao_geografica": {},
        }

        for campo in campos_geo:
            analise_geografica["distribuicao_geografica"][campo] = {
                "valores_unicos": df[campo].nunique(),
                "top_localizacoes": df[campo].value_counts().head(10).to_dict(),
                "valores_nulos": df[campo].isnull().sum(),
            }

        self.resultados_analise = analise_geografica
        return analise_geografica

    def _analise_conteudo(self) -> Dict:
        """
        📝 Análise de conteúdo dos dados.

        Returns:
            Análise de conteúdo
        """
        self.logger.info("📝 Executando análise de conteúdo")

        df = pd.DataFrame(self.dados_originais)

        # Identificar campos de texto
        campos_texto = []
        for coluna in df.columns:
            if any(
                palavra in coluna.lower()
                for palavra in ["descricao", "titulo", "nome", "texto", "conteudo"]
            ):
                campos_texto.append(coluna)

        analise_conteudo = {
            "campos_texto_encontrados": campos_texto,
            "analise_por_campo": {},
        }

        for campo in campos_texto:
            textos = df[campo].dropna().astype(str)

            analise_conteudo["analise_por_campo"][campo] = {
                "total_textos": len(textos),
                "media_caracteres": textos.str.len().mean(),
                "min_caracteres": textos.str.len().min(),
                "max_caracteres": textos.str.len().max(),
                "palavras_mais_comuns": self._extrair_palavras_comuns(textos),
            }

        self.resultados_analise = analise_conteudo
        return analise_conteudo

    def _analise_comparativa(self) -> Dict:
        """
        ⚖️ Análise comparativa dos dados.

        Returns:
            Análise comparativa
        """
        self.logger.info("⚖️ Executando análise comparativa")

        parametros = self.configuracoes_analise.get("parametros", {})
        campos_comparacao = parametros.get("campos_comparacao", [])

        df = pd.DataFrame(self.dados_originais)

        analise_comparativa = {
            "campos_comparacao": campos_comparacao,
            "comparacoes": {},
        }

        for campo in campos_comparacao:
            if campo in df.columns:
                analise_comparativa["comparacoes"][campo] = {
                    "valores_unicos": df[campo].nunique(),
                    "distribuicao": df[campo].value_counts().to_dict(),
                    "correlacoes": self._calcular_correlacoes(df, campo),
                }

        self.resultados_analise = analise_comparativa
        return analise_comparativa

    def _analise_customizada(self) -> Dict:
        """
        🔧 Análise customizada baseada em parâmetros específicos.

        Returns:
            Análise customizada
        """
        self.logger.info("🔧 Executando análise customizada")

        parametros = self.configuracoes_analise.get("parametros", {})
        filtros = parametros.get("filtros", {})
        campos_analise = parametros.get("campos_analise", [])

        df = pd.DataFrame(self.dados_originais)

        # Aplicar filtros
        for campo, valor in filtros.items():
            if campo in df.columns:
                df = df[df[campo] == valor]

        analise_customizada = {
            "filtros_aplicados": filtros,
            "registros_filtrados": len(df),
            "analise_campos": {},
        }

        for campo in campos_analise:
            if campo in df.columns:
                analise_customizada["analise_campos"][campo] = {
                    "valores_unicos": df[campo].nunique(),
                    "distribuicao": df[campo].value_counts().to_dict(),
                }

        self.resultados_analise = analise_customizada
        return analise_customizada

    def _extrair_palavras_comuns(self, textos: pd.Series, top_n: int = 10) -> Dict:
        """
        📚 Extrai palavras mais comuns dos textos.

        Args:
            textos: Série com textos
            top_n: Número de palavras mais comuns

        Returns:
            Dicionário com palavras e frequências
        """
        todas_palavras = []
        for texto in textos:
            palavras = re.findall(r"\b\w+\b", texto.lower())
            todas_palavras.extend(palavras)

        from collections import Counter

        contador = Counter(todas_palavras)
        return dict(contador.most_common(top_n))

    def _calcular_correlacoes(self, df: pd.DataFrame, campo: str) -> Dict:
        """
        📈 Calcula correlações para um campo específico.

        Args:
            df: DataFrame com dados
            campo: Campo para análise

        Returns:
            Correlações encontradas
        """
        correlacoes = {}

        # Tentar calcular correlações com campos numéricos
        campos_numericos = df.select_dtypes(include=["number"]).columns
        for campo_num in campos_numericos:
            if campo_num != campo:
                try:
                    correlacao = (
                        df[campo].astype("category").cat.codes.corr(df[campo_num])
                    )
                    if not pd.isna(correlacao):
                        correlacoes[campo_num] = correlacao
                except:
                    continue

        return correlacoes

    def salvar_resultados(self, caminho_saida: str = None):
        """
        💾 Salva os resultados da análise.

        Args:
            caminho_saida: Caminho para salvar os resultados
        """
        if not self.resultados_analise:
            self.logger.warning("⚠️ Nenhum resultado para salvar")
            return

        # Criar pasta de relatórios se não existir
        os.makedirs("relatorios", exist_ok=True)

        # Gerar nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tipo_analise = self.configuracoes_analise.get("tipo", "geral")

        if not caminho_saida:
            caminho_saida = f"relatorios/analise_{tipo_analise}_{timestamp}"

        # Salvar JSON
        caminho_json = f"{caminho_saida}.json"
        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(
                self.resultados_analise, f, indent=2, ensure_ascii=False, default=str
            )

        # Salvar CSV (se aplicável)
        if (
            isinstance(self.resultados_analise, dict)
            and "resumo_geral" in self.resultados_analise
        ):
            caminho_csv = f"{caminho_saida}.csv"
            df_resultado = pd.DataFrame([self.resultados_analise["resumo_geral"]])
            df_resultado.to_csv(caminho_csv, index=False, encoding="utf-8")

        # Gerar relatório Markdown
        caminho_md = f"{caminho_saida}.md"
        self._gerar_relatorio_markdown(caminho_md)

        self.logger.info(f"✅ Resultados salvos em: {caminho_saida}.*")

    def _gerar_relatorio_markdown(self, caminho_arquivo: str):
        """
        📄 Gera relatório em Markdown.

        Args:
            caminho_arquivo: Caminho para o arquivo Markdown
        """
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tipo_analise = self.configuracoes_analise.get("tipo", "geral")

        relatorio = f"""# 📊 Relatório de Análise Geral - UNA-SUS

## 📅 Informações Gerais
- **Data da Análise**: {timestamp}
- **Tipo de Análise**: {tipo_analise}
- **Total de Registros**: {len(self.dados_originais)}

## 🎯 Resultados da Análise

### 📈 Resumo Geral
"""

        if "resumo_geral" in self.resultados_analise:
            resumo = self.resultados_analise["resumo_geral"]
            relatorio += f"""
- **Total de Cursos**: {resumo.get('total_cursos', 'N/A')}
- **Campos Disponíveis**: {len(resumo.get('campos_disponiveis', []))}
- **Campos com Dados**: {sum(1 for v in resumo.get('campos_preenchidos', {}).values() if v > 0)}
"""

        if "estatisticas_numericas" in self.resultados_analise:
            relatorio += "\n### 📊 Estatísticas Numéricas\n"
            for campo, stats in self.resultados_analise[
                "estatisticas_numericas"
            ].items():
                relatorio += f"""
#### {campo}
- **Média**: {stats.get('media', 'N/A'):.2f}
- **Mediana**: {stats.get('mediana', 'N/A'):.2f}
- **Mínimo**: {stats.get('min', 'N/A')}
- **Máximo**: {stats.get('max', 'N/A')}
- **Desvio Padrão**: {stats.get('desvio_padrao', 'N/A'):.2f}
"""

        if "estatisticas_categoricas" in self.resultados_analise:
            relatorio += "\n### 📂 Estatísticas Categóricas\n"
            for campo, stats in self.resultados_analise[
                "estatisticas_categoricas"
            ].items():
                relatorio += f"""
#### {campo}
- **Valores Únicos**: {stats.get('valores_unicos', 'N/A')}
- **Valores Nulos**: {stats.get('valores_nulos', 'N/A')}
- **Top 5 Valores**: {list(stats.get('top_valores', {}).keys())[:5]}
"""

        relatorio += f"""

## 🔧 Configurações da Análise
```json
{json.dumps(self.configuracoes_analise, indent=2, ensure_ascii=False)}
```

---
*Relatório gerado automaticamente pelo Analisador Geral UNA-SUS*
"""

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(relatorio)

        self.logger.info(f"📄 Relatório Markdown gerado: {caminho_arquivo}")


def main():
    """
    🚀 Função principal para teste do analisador.
    """
    print("🔍 Analisador Geral UNA-SUS")
    print("=" * 50)

    # Exemplo de uso
    analisador = AnalisadorGeral()

    # Carregar dados (exemplo)
    # analisador.carregar_dados_para_analise("dados/unasus_dados_completos.json")

    # Configurar análise
    analisador.configurar_analise("estatistica")

    # Executar análise
    # resultados = analisador.executar_analise()

    # Salvar resultados
    # analisador.salvar_resultados()

    print("✅ Analisador configurado e pronto para uso!")


if __name__ == "__main__":
    main()
