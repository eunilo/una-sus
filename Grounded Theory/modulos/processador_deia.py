#!/usr/bin/env python3
"""
🔍 Processador DEIA - Análise Separada de Dados
==============================================

Este módulo implementa processamento DEIA (Diversidade, Equidade, 
Inclusão e Acessibilidade) em dados já coletados, mantendo a 
integridade do database original.

🎯 PRINCÍPIOS:
- Trabalha com dados já coletados
- NÃO modifica dados originais
- Cria cópias para análise
- Preserva database fiel
- Análise não-destrutiva

🔬 METODOLOGIA:
- Carregamento de dados existentes
- Análise DEIA não-destrutiva
- Geração de relatórios específicos
- Filtros e categorizações
- Estatísticas detalhadas
"""

import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd


class ProcessadorDEIA:
    """
    🔍 Processador DEIA para Análise de Dados

    Processa dados já coletados para análise DEIA sem modificar originais.
    """

    def __init__(self, logger: logging.Logger = None):
        """
        Inicializa o processador DEIA.

        Args:
            logger: Logger para acompanhamento
        """
        self.logger = logger or self._configurar_logger()
        self.dados_originais = []
        self.dados_processados = []
        self.resultados_deia = {}

        # Descritores DEIA expandidos
        self.descritores_deia = {
            "diversidade": [
                "diversidade",
                "diverso",
                "pluralidade",
                "multicultural",
                "intercultural",
                "transcultural",
                "multirracial",
            ],
            "equidade": [
                "equidade",
                "equitativo",
                "justiça social",
                "igualdade",
                "paridade",
                "equilibrio",
                "redistribuição",
            ],
            "inclusão": [
                "inclusão",
                "inclusivo",
                "acolhimento",
                "integração",
                "participação",
                "pertencimento",
                "comunidade",
            ],
            "acessibilidade": [
                "acessibilidade",
                "acessível",
                "acesso",
                "barreiras",
                "adaptação",
                "tecnologia assistiva",
                "design universal",
            ],
            "populações_específicas": [
                "população negra",
                "população indígena",
                "pessoa com deficiência",
                "lgbtqi+",
                "mulheres",
                "idosos",
                "crianças",
                "adolescentes",
                "população em situação de rua",
                "população privada de liberdade",
            ],
            "saúde_mental": [
                "saúde mental",
                "psicologia",
                "psiquiatria",
                "bem-estar psicológico",
                "transtornos mentais",
                "saúde mental comunitária",
                "psicossocial",
            ],
            "vulnerabilidade": [
                "vulnerabilidade",
                "vulnerável",
                "risco social",
                "proteção social",
                "assistência social",
                "políticas públicas",
                "direitos humanos",
            ],
        }

    def _configurar_logger(self) -> logging.Logger:
        """
        📝 Configura o logger para o processador.

        Returns:
            Logger configurado
        """
        # Criar pasta de logs se não existir
        os.makedirs("logs", exist_ok=True)

        # Configurar logger
        logger = logging.getLogger("ProcessadorDEIA")
        logger.setLevel(logging.INFO)

        # Handler para arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fh = logging.FileHandler(
            f"logs/processador_deia_{timestamp}.log", encoding="utf-8"
        )
        fh.setLevel(logging.INFO)

        # Handler para console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
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
        📂 Carrega dados para análise DEIA.

        Args:
            caminho_arquivo: Caminho para o arquivo de dados

        Returns:
            True se carregado com sucesso, False caso contrário
        """
        self.logger.info(f"📂 Carregando dados para análise DEIA: {caminho_arquivo}")

        try:
            if caminho_arquivo.endswith(".json"):
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    self.dados_originais = json.load(f)
            elif caminho_arquivo.endswith(".csv"):
                df = pd.read_csv(caminho_arquivo, encoding="utf-8")
                self.dados_originais = df.to_dict("records")
            elif caminho_arquivo.endswith(".xlsx"):
                try:
                    import openpyxl

                    df = pd.read_excel(caminho_arquivo)
                    self.dados_originais = df.to_dict("records")
                except ImportError:
                    raise ValueError(
                        "Para ler arquivos .xlsx, instale openpyxl: pip install openpyxl"
                    )
            else:
                raise ValueError(f"Formato de arquivo não suportado: {caminho_arquivo}")

            self.logger.info(
                f"✅ Dados carregados: {len(self.dados_originais)} registros"
            )
            return True

        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar dados: {str(e)}")
            return False

    def processar_analise_deia(self) -> Dict:
        """
        🔍 Processa análise DEIA completa.

        Returns:
            Resultados da análise DEIA
        """
        self.logger.info("🔍 INICIANDO ANÁLISE DEIA")
        self.logger.info(
            f"📊 Dados para análise: {len(self.dados_originais)} registros"
        )

        if not self.dados_originais:
            self.logger.error("❌ Nenhum dado carregado para análise")
            return {}

        # Criar cópia para processamento
        self.dados_processados = self.dados_originais.copy()

        # Realizar análises
        resultados = {
            "resumo_geral": self._gerar_resumo_geral(),
            "analise_por_categoria": self._analisar_por_categoria_deia(),
            "cursos_deia_identificados": self._identificar_cursos_deia(),
            "estatisticas_detalhadas": self._gerar_estatisticas_detalhadas(),
            "padroes_identificados": self._identificar_padroes(),
            "recomendacoes": self._gerar_recomendacoes(),
            "timestamp_analise": datetime.now().isoformat(),
        }

        self.resultados_deia = resultados

        # Salvar resultados
        self._salvar_resultados_analise()

        self.logger.info("✅ ANÁLISE DEIA CONCLUÍDA")
        return resultados

    def _gerar_resumo_geral(self) -> Dict:
        """
        📊 Gera resumo geral da análise.

        Returns:
            Resumo geral
        """
        total_cursos = len(self.dados_processados)

        # Contar cursos com elementos DEIA
        cursos_deia = 0
        for curso in self.dados_processados:
            if self._curso_contem_elementos_deia(curso):
                cursos_deia += 1

        resumo = {
            "total_cursos_analisados": total_cursos,
            "cursos_com_elementos_deia": cursos_deia,
            "percentual_deia": (
                (cursos_deia / total_cursos * 100) if total_cursos > 0 else 0
            ),
            "categorias_deia_identificadas": list(self.descritores_deia.keys()),
            "total_descritores": sum(
                len(desc) for desc in self.descritores_deia.values()
            ),
        }

        return resumo

    def _analisar_por_categoria_deia(self) -> Dict:
        """
        📊 Analisa dados por categoria DEIA.

        Returns:
            Análise por categoria
        """
        analise_categorias = {}

        for categoria, descritores in self.descritores_deia.items():
            cursos_categoria = []
            contagem_descritores = {}

            for curso in self.dados_processados:
                curso_contem_categoria = False

                for descritor in descritores:
                    if self._texto_contem_descritor(curso, descritor):
                        curso_contem_categoria = True
                        contagem_descritores[descritor] = (
                            contagem_descritores.get(descritor, 0) + 1
                        )

                if curso_contem_categoria:
                    cursos_categoria.append(curso)

            analise_categorias[categoria] = {
                "total_cursos": len(cursos_categoria),
                "percentual_total": (
                    (len(cursos_categoria) / len(self.dados_processados) * 100)
                    if self.dados_processados
                    else 0
                ),
                "descritores_mais_frequentes": sorted(
                    contagem_descritores.items(), key=lambda x: x[1], reverse=True
                )[:5],
                "cursos_identificados": [
                    curso.get("id", curso.get("titulo", "N/A"))
                    for curso in cursos_categoria[:10]
                ],
            }

        return analise_categorias

    def _identificar_cursos_deia(self) -> List[Dict]:
        """
        🎯 Identifica cursos com elementos DEIA.

        Returns:
            Lista de cursos DEIA
        """
        cursos_deia = []

        for curso in self.dados_processados:
            elementos_deia = self._extrair_elementos_deia_curso(curso)

            if elementos_deia:
                curso_deia = {
                    "id": curso.get("id"),
                    "titulo": curso.get("titulo"),
                    "descricao": curso.get("descricao"),
                    "categoria": curso.get("categoria"),
                    "status": curso.get("status"),
                    "elementos_deia": elementos_deia,
                    "score_deia": len(elementos_deia),
                    "categorias_deia": list(
                        set([elem["categoria"] for elem in elementos_deia])
                    ),
                }
                cursos_deia.append(curso_deia)

        # Ordenar por score DEIA
        cursos_deia.sort(key=lambda x: x["score_deia"], reverse=True)

        return cursos_deia

    def _gerar_estatisticas_detalhadas(self) -> Dict:
        """
        📈 Gera estatísticas detalhadas.

        Returns:
            Estatísticas detalhadas
        """
        df = pd.DataFrame(self.dados_processados)

        estatisticas = {
            "distribuicao_por_status": (
                df["status"].value_counts().to_dict() if "status" in df.columns else {}
            ),
            "distribuicao_por_categoria": (
                df["categoria"].value_counts().to_dict()
                if "categoria" in df.columns
                else {}
            ),
            "carga_horaria_estatisticas": {},
            "campos_preenchidos": {},
        }

        # Estatísticas de carga horária
        if "carga_horaria" in df.columns:
            try:
                cargas = pd.to_numeric(df["carga_horaria"], errors="coerce")
                estatisticas["carga_horaria_estatisticas"] = {
                    "media": float(cargas.mean()),
                    "mediana": float(cargas.median()),
                    "minima": float(cargas.min()),
                    "maxima": float(cargas.max()),
                    "desvio_padrao": float(cargas.std()),
                }
            except:
                pass

        # Campos preenchidos
        for coluna in df.columns:
            nao_nulos = df[coluna].notna().sum()
            estatisticas["campos_preenchidos"][coluna] = {
                "preenchidos": int(nao_nulos),
                "vazios": int(len(df) - nao_nulos),
                "percentual": float(nao_nulos / len(df) * 100),
            }

        return estatisticas

    def _identificar_padroes(self) -> Dict:
        """
        🔍 Identifica padrões nos dados DEIA.

        Returns:
            Padrões identificados
        """
        padroes = {
            "categorias_mais_frequentes": [],
            "descritores_mais_efetivos": [],
            "correlacoes": {},
            "tendencias": [],
        }

        # Categorias mais frequentes
        analise_categorias = self._analisar_por_categoria_deia()
        categorias_ordenadas = sorted(
            analise_categorias.items(), key=lambda x: x[1]["total_cursos"], reverse=True
        )

        padroes["categorias_mais_frequentes"] = [
            {"categoria": cat, "total": info["total_cursos"]}
            for cat, info in categorias_ordenadas[:5]
        ]

        # Descritores mais efetivos
        todos_descritores = {}
        for categoria, descritores in self.descritores_deia.items():
            for descritor in descritores:
                contagem = 0
                for curso in self.dados_processados:
                    if self._texto_contem_descritor(curso, descritor):
                        contagem += 1
                todos_descritores[descritor] = contagem

        padroes["descritores_mais_efetivos"] = sorted(
            todos_descritores.items(), key=lambda x: x[1], reverse=True
        )[:10]

        return padroes

    def _gerar_recomendacoes(self) -> List[str]:
        """
        💡 Gera recomendações baseadas na análise.

        Returns:
            Lista de recomendações
        """
        recomendacoes = []

        # Análise de cobertura
        resumo = self._gerar_resumo_geral()
        if resumo["percentual_deia"] < 20:
            recomendacoes.append("Aumentar cobertura de elementos DEIA nos cursos")

        # Análise de categorias
        analise_categorias = self._analisar_por_categoria_deia()
        categorias_baixas = [
            cat for cat, info in analise_categorias.items() if info["total_cursos"] < 10
        ]

        if categorias_baixas:
            recomendacoes.append(
                f"Fortalecer categorias com baixa representação: {', '.join(categorias_baixas)}"
            )

        # Recomendações gerais
        recomendacoes.extend(
            [
                "Implementar indicadores DEIA nos processos de criação de cursos",
                "Desenvolver capacitação sobre DEIA para equipes de desenvolvimento",
                "Estabelecer metas de inclusão DEIA nos planejamentos educacionais",
                "Criar sistema de monitoramento contínuo de elementos DEIA",
            ]
        )

        return recomendacoes

    def _curso_contem_elementos_deia(self, curso: Dict) -> bool:
        """
        🔍 Verifica se curso contém elementos DEIA.

        Args:
            curso: Dados do curso

        Returns:
            True se contém elementos DEIA
        """
        for categoria, descritores in self.descritores_deia.items():
            for descritor in descritores:
                if self._texto_contem_descritor(curso, descritor):
                    return True
        return False

    def _texto_contem_descritor(self, curso: Dict, descritor: str) -> bool:
        """
        🔍 Verifica se texto do curso contém descritor.

        Args:
            curso: Dados do curso
            descritor: Descritor a procurar

        Returns:
            True se contém descritor
        """
        campos_texto = ["titulo", "descricao", "palavras_chave", "publico_alvo"]
        texto_completo = ""

        for campo in campos_texto:
            if curso.get(campo):
                texto_completo += f" {str(curso[campo])}"

        texto_completo = texto_completo.lower()
        return descritor.lower() in texto_completo

    def _extrair_elementos_deia_curso(self, curso: Dict) -> List[Dict]:
        """
        🔍 Extrai elementos DEIA específicos do curso.

        Args:
            curso: Dados do curso

        Returns:
            Lista de elementos DEIA encontrados
        """
        elementos = []

        for categoria, descritores in self.descritores_deia.items():
            for descritor in descritores:
                if self._texto_contem_descritor(curso, descritor):
                    elementos.append(
                        {
                            "categoria": categoria,
                            "descritor": descritor,
                            "contexto": self._extrair_contexto(curso, descritor),
                        }
                    )

        return elementos

    def _extrair_contexto(self, curso: Dict, descritor: str) -> str:
        """
        📝 Extrai contexto do descritor no curso.

        Args:
            curso: Dados do curso
            descritor: Descritor encontrado

        Returns:
            Contexto extraído
        """
        campos_texto = ["titulo", "descricao", "palavras_chave", "publico_alvo"]

        for campo in campos_texto:
            if curso.get(campo):
                texto = str(curso[campo])
                if descritor.lower() in texto.lower():
                    # Extrair frase ao redor do descritor
                    palavras = texto.split()
                    for i, palavra in enumerate(palavras):
                        if descritor.lower() in palavra.lower():
                            inicio = max(0, i - 5)
                            fim = min(len(palavras), i + 6)
                            return " ".join(palavras[inicio:fim])

        return "Contexto não disponível"

    def _salvar_resultados_analise(self):
        """
        💾 Salva resultados da análise DEIA.
        """
        if not self.resultados_deia:
            self.logger.warning("⚠️ Nenhum resultado para salvar")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Salvar JSON
        caminho_json = f"resultados/analise_deia_{timestamp}.json"
        os.makedirs("resultados", exist_ok=True)

        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(self.resultados_deia, f, ensure_ascii=False, indent=2)

        # Salvar CSV dos cursos DEIA
        caminho_csv = None
        if self.resultados_deia.get("cursos_deia_identificados"):
            df_cursos = pd.DataFrame(self.resultados_deia["cursos_deia_identificados"])
            caminho_csv = f"resultados/cursos_deia_{timestamp}.csv"
            df_cursos.to_csv(caminho_csv, index=False, encoding="utf-8")

        # Gerar relatório em Markdown
        relatorio_md = self._gerar_relatorio_markdown()
        caminho_md = f"resultados/relatorio_deia_{timestamp}.md"

        with open(caminho_md, "w", encoding="utf-8") as f:
            f.write(relatorio_md)

        self.logger.info(f"💾 Resultados salvos:")
        self.logger.info(f"   📄 JSON: {caminho_json}")
        if caminho_csv:
            self.logger.info(f"   📊 CSV: {caminho_csv}")
        self.logger.info(f"   📋 Markdown: {caminho_md}")

    def _gerar_relatorio_markdown(self) -> str:
        """
        📋 Gera relatório em formato Markdown.

        Returns:
            Relatório em Markdown
        """
        relatorio = f"""# 🔍 Relatório de Análise DEIA - UNA-SUS

## 📊 Resumo Geral

- **Total de Cursos Analisados**: {self.resultados_deia['resumo_geral']['total_cursos_analisados']}
- **Cursos com Elementos DEIA**: {self.resultados_deia['resumo_geral']['cursos_com_elementos_deia']}
- **Percentual DEIA**: {self.resultados_deia['resumo_geral']['percentual_deia']:.2f}%
- **Categorias DEIA Identificadas**: {len(self.resultados_deia['resumo_geral']['categorias_deia_identificadas'])}

## 📈 Análise por Categoria DEIA

"""

        for categoria, info in self.resultados_deia["analise_por_categoria"].items():
            relatorio += f"""
### {categoria.replace('_', ' ').title()}
- **Total de Cursos**: {info['total_cursos']}
- **Percentual**: {info['percentual_total']:.2f}%
- **Descritores Mais Frequentes**: {', '.join([f"{d[0]} ({d[1]})" for d in info['descritores_mais_frequentes'][:3]])}

"""

        relatorio += f"""
## 🎯 Cursos com Maior Score DEIA

"""

        for i, curso in enumerate(
            self.resultados_deia["cursos_deia_identificados"][:10], 1
        ):
            relatorio += f"""
{i}. **{curso['titulo']}**
   - Score DEIA: {curso['score_deia']}
   - Categorias: {', '.join(curso['categorias_deia'])}
   - Status: {curso['status']}

"""

        relatorio += f"""
## 💡 Recomendações

"""

        for i, recomendacao in enumerate(self.resultados_deia["recomendacoes"], 1):
            relatorio += f"{i}. {recomendacao}\n"

        relatorio += f"""

---
*Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*
"""

        return relatorio


def main():
    """
    🚀 Função principal para executar análise DEIA.
    """
    print("🔍 INICIANDO PROCESSADOR DEIA")

    # Criar processador
    processador = ProcessadorDEIA()

    # Carregar dados (exemplo)
    # processador.carregar_dados_para_analise("dados/unasus_dados_completos_20250101_120000.json")

    # Executar análise
    # resultados = processador.processar_analise_deia()

    print("✅ PROCESSADOR DEIA CONFIGURADO")
    print("📁 Use carregar_dados_para_analise() e processar_analise_deia()")


if __name__ == "__main__":
    main()
