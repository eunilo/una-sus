#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ANÁLISE EXPLORATÓRIA DOS DADOS
==================================

Script para análise detalhada dos dados coletados da UNA-SUS
antes de prosseguir com a Grounded Theory.
"""

import json
import os
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
from formatos_saida import (
    ConversorFormatos,
    GeradorSaida,
    ResultadoAnaliseExploratoria,
    TipoAnalise,
)


class AnaliseExploratoria:
    """
    🔍 Classe para análise exploratória dos dados UNA-SUS.
    """

    def __init__(self, arquivo_dados: str = None):
        """
        Inicializa a análise exploratória.

        Args:
            arquivo_dados: Caminho para o arquivo de dados JSON
        """
        self.arquivo_dados = arquivo_dados or self.encontrar_dados_mais_recentes()
        self.dados = self.carregar_dados()
        self.resultados = {}

    def encontrar_dados_mais_recentes(self) -> str:
        """Encontra o arquivo de dados mais recente."""
        dados_dir = "dados"
        if not os.path.exists(dados_dir):
            raise FileNotFoundError("Diretório 'dados' não encontrado")

        arquivos = [
            f
            for f in os.listdir(dados_dir)
            if f.endswith(".json") and "unasus_dados_completos" in f
        ]

        if not arquivos:
            raise FileNotFoundError("Nenhum arquivo de dados encontrado")

        arquivo_mais_recente = max(
            arquivos, key=lambda x: os.path.getctime(os.path.join(dados_dir, x))
        )

        return os.path.join(dados_dir, arquivo_mais_recente)

    def carregar_dados(self) -> List[Dict]:
        """Carrega os dados do arquivo JSON."""
        print(f"📁 Carregando dados de: {self.arquivo_dados}")

        with open(self.arquivo_dados, "r", encoding="utf-8") as f:
            dados = json.load(f)

        print(f"✅ Dados carregados: {len(dados)} registros")
        return dados

    def executar_analise_completa(self):
        """Executa análise exploratória completa."""
        print("\n🔍 INICIANDO ANÁLISE EXPLORATÓRIA COMPLETA")
        print("=" * 60)

        # Análises básicas
        self.analisar_estrutura_dados()
        self.analisar_campos_disponiveis()
        self.analisar_distribuicao_cursos()
        self.analisar_instituicoes()
        self.analisar_modalidades()
        self.analisar_carga_horaria()
        self.analisar_status_cursos()

        # Análises específicas
        self.analisar_padroes_texto()
        self.analisar_elementos_deia()
        self.analisar_cursos_formacao()

        # Salvar resultados
        self.salvar_resultados()

    def analisar_estrutura_dados(self):
        """Analisa a estrutura básica dos dados."""
        print("\n📊 ANÁLISE DA ESTRUTURA DOS DADOS")
        print("-" * 40)

        primeiro_registro = self.dados[0]

        print(f"• Total de registros: {len(self.dados):,}")
        print(f"• Campos por registro: {len(primeiro_registro)}")
        print(f"• Arquivo fonte: {os.path.basename(self.arquivo_dados)}")

        # Verificar metadata
        if "metadata_coleta" in primeiro_registro:
            metadata = primeiro_registro["metadata_coleta"]
            print(f"• Data da coleta: {metadata.get('timestamp_coleta', 'N/A')}")
            print(f"• Tipo de coleta: {metadata.get('tipo_coleta', 'N/A')}")

        self.resultados["estrutura"] = {
            "total_registros": len(self.dados),
            "campos_por_registro": len(primeiro_registro),
            "arquivo_fonte": os.path.basename(self.arquivo_dados),
        }

    def analisar_campos_disponiveis(self):
        """Analisa quais campos têm dados."""
        print("\n📋 ANÁLISE DOS CAMPOS DISPONÍVEIS")
        print("-" * 40)

        campos_com_dados = {}
        campos_vazios = {}

        for registro in self.dados:
            for campo, valor in registro.items():
                if campo not in ["metadata_coleta"]:
                    if valor and str(valor).lower() != "null":
                        campos_com_dados[campo] = campos_com_dados.get(campo, 0) + 1
                    else:
                        campos_vazios[campo] = campos_vazios.get(campo, 0) + 1

        total_registros = len(self.dados)

        print("✅ CAMPOS COM MAIS DADOS:")
        for campo, count in sorted(
            campos_com_dados.items(), key=lambda x: x[1], reverse=True
        )[:15]:
            percentual = (count / total_registros) * 100
            print(f"   • {campo}: {count:,} ({percentual:.1f}%)")

        print("\n❌ CAMPOS COMPLETAMENTE VAZIOS:")
        campos_todos_vazios = [
            campo for campo, count in campos_vazios.items() if count == total_registros
        ]
        for campo in campos_todos_vazios[:10]:  # Mostrar apenas os primeiros 10
            print(f"   • {campo}")

        if len(campos_todos_vazios) > 10:
            print(f"   ... e mais {len(campos_todos_vazios) - 10} campos")

        self.resultados["campos"] = {
            "com_dados": dict(list(campos_com_dados.items())[:15]),
            "vazios": campos_todos_vazios,
        }

    def analisar_distribuicao_cursos(self):
        """Analisa a distribuição dos cursos por nível."""
        print("\n🎓 DISTRIBUIÇÃO DOS CURSOS POR NÍVEL")
        print("-" * 40)

        niveis = Counter(registro.get("no_nivel", "N/A") for registro in self.dados)

        for nivel, count in niveis.most_common():
            percentual = (count / len(self.dados)) * 100
            print(f"• {nivel}: {count:,} ({percentual:.1f}%)")

        self.resultados["niveis"] = dict(niveis)

    def analisar_instituicoes(self):
        """Analisa as instituições participantes."""
        print("\n🏛️ INSTITUIÇÕES PARTICIPANTES")
        print("-" * 40)

        instituicoes = Counter(
            registro.get("no_orgao", "N/A") for registro in self.dados
        )

        print(f"• Total de instituições: {len(instituicoes)}")
        print("\n🏆 TOP 15 INSTITUIÇÕES:")

        for instituicao, count in instituicoes.most_common(15):
            percentual = (count / len(self.dados)) * 100
            print(f"   • {instituicao}: {count:,} ({percentual:.1f}%)")

        self.resultados["instituicoes"] = {
            "total": len(instituicoes),
            "top_15": dict(instituicoes.most_common(15)),
        }

    def analisar_modalidades(self):
        """Analisa as modalidades de ensino."""
        print("\n📚 MODALIDADES DE ENSINO")
        print("-" * 40)

        modalidades = Counter(
            registro.get("no_modalidade", "N/A") for registro in self.dados
        )
        formatos = Counter(registro.get("no_formato", "N/A") for registro in self.dados)

        print("📖 MODALIDADES:")
        for modalidade, count in modalidades.most_common():
            percentual = (count / len(self.dados)) * 100
            print(f"   • {modalidade}: {count:,} ({percentual:.1f}%)")

        print("\n💻 FORMATOS:")
        for formato, count in formatos.most_common():
            percentual = (count / len(self.dados)) * 100
            print(f"   • {formato}: {count:,} ({percentual:.1f}%)")

        self.resultados["modalidades"] = {
            "modalidades": dict(modalidades),
            "formatos": dict(formatos),
        }

    def analisar_carga_horaria(self):
        """Analisa a distribuição de carga horária."""
        print("\n⏰ ANÁLISE DE CARGA HORÁRIA")
        print("-" * 40)

        cargas_horarias = []
        for registro in self.dados:
            carga = registro.get("qt_carga_horaria_total")
            if carga and isinstance(carga, (int, float)):
                cargas_horarias.append(carga)

        if cargas_horarias:
            df_carga = pd.Series(cargas_horarias)

            print(f"• Total com carga horária: {len(cargas_horarias):,}")
            print(f"• Média: {df_carga.mean():.1f} horas")
            print(f"• Mediana: {df_carga.median():.1f} horas")
            print(f"• Mínimo: {df_carga.min():.1f} horas")
            print(f"• Máximo: {df_carga.max():.1f} horas")

            # Distribuição por faixas
            faixas = [(0, 30), (31, 60), (61, 120), (121, 240), (241, float("inf"))]
            nomes_faixas = ["0-30h", "31-60h", "61-120h", "121-240h", "240h+"]

            print("\n📊 DISTRIBUIÇÃO POR FAIXAS:")
            for (min_h, max_h), nome in zip(faixas, nomes_faixas):
                if max_h == float("inf"):
                    count = len(df_carga[df_carga >= min_h])
                else:
                    count = len(df_carga[(df_carga >= min_h) & (df_carga < max_h)])
                percentual = (count / len(cargas_horarias)) * 100
                print(f"   • {nome}: {count:,} ({percentual:.1f}%)")

            self.resultados["carga_horaria"] = {
                "total_com_carga": len(cargas_horarias),
                "estatisticas": {
                    "media": float(df_carga.mean()),
                    "mediana": float(df_carga.median()),
                    "minimo": float(df_carga.min()),
                    "maximo": float(df_carga.max()),
                },
            }
        else:
            print("• Nenhum dado de carga horária disponível")

    def analisar_status_cursos(self):
        """Analisa o status dos cursos."""
        print("\n📊 STATUS DOS CURSOS")
        print("-" * 40)

        status = Counter(registro.get("status", "N/A") for registro in self.dados)

        for stat, count in status.most_common():
            percentual = (count / len(self.dados)) * 100
            print(f"• {stat}: {count:,} ({percentual:.1f}%)")

        self.resultados["status"] = dict(status)

    def analisar_padroes_texto(self):
        """Analisa padrões no texto dos cursos."""
        print("\n🔍 ANÁLISE DE PADRÕES NO TEXTO")
        print("-" * 40)

        # Extrair texto dos cursos
        textos_cursos = []
        for registro in self.dados:
            texto = self.extrair_texto_curso(registro)
            if texto:
                textos_cursos.append(texto.lower())

        if not textos_cursos:
            print("• Nenhum texto disponível para análise")
            return

        # Análise de palavras mais comuns
        todas_palavras = []
        for texto in textos_cursos:
            palavras = texto.split()
            todas_palavras.extend(palavras)

        # Filtrar palavras comuns e muito curtas
        palavras_filtradas = [
            palavra
            for palavra in todas_palavras
            if len(palavra) > 3
            and palavra
            not in ["para", "com", "uma", "das", "dos", "que", "por", "são", "está"]
        ]

        palavras_comuns = Counter(palavras_filtradas)

        print("📝 PALAVRAS MAIS COMUNS NOS CURSOS:")
        for palavra, count in palavras_comuns.most_common(20):
            print(f"   • {palavra}: {count:,}")

        self.resultados["padroes_texto"] = {
            "total_textos": len(textos_cursos),
            "palavras_comuns": dict(palavras_comuns.most_common(20)),
        }

    def analisar_elementos_deia(self):
        """Analisa elementos DEIA nos cursos."""
        print("\n🌈 ANÁLISE DE ELEMENTOS DEIA")
        print("-" * 40)

        # Palavras-chave DEIA
        palavras_deia = [
            "diversidade",
            "equidade",
            "inclusão",
            "inclusivo",
            "inclusiva",
            "acessibilidade",
            "acessível",
            "equitativo",
            "equitativa",
            "população",
            "negro",
            "negra",
            "indígena",
            "lgbt",
            "lgbtqi",
            "deficiência",
            "deficiente",
            "idoso",
            "idosos",
            "criança",
            "crianças",
            "adolescente",
            "adolescentes",
            "mulher",
            "mulheres",
            "gestante",
            "gestantes",
            "trabalhador",
            "trabalhadores",
            "rural",
            "urbano",
            "vulnerabilidade",
            "vulnerável",
            "vulneráveis",
            "discriminação",
            "preconceito",
            "estigma",
            "marginalização",
            "exclusão",
            "desigualdade",
            "direitos",
            "humanos",
            "cidadania",
            "justiça",
            "social",
            "determinantes",
            "sociais",
        ]

        cursos_com_deia = []
        elementos_encontrados = Counter()

        for i, registro in enumerate(self.dados):
            texto = self.extrair_texto_curso(registro).lower()
            elementos_registro = []

            for palavra in palavras_deia:
                if palavra in texto:
                    elementos_registro.append(palavra)
                    elementos_encontrados[palavra] += 1

            if elementos_registro:
                cursos_com_deia.append(
                    {
                        "id": i,
                        "curso": registro.get("no_curso", "N/A"),
                        "elementos": elementos_registro,
                    }
                )

        print(
            f"• Cursos com elementos DEIA: {len(cursos_com_deia):,} ({len(cursos_com_deia)/len(self.dados)*100:.1f}%)"
        )

        if elementos_encontrados:
            print("\n🔍 ELEMENTOS DEIA MAIS FREQUENTES:")
            for elemento, count in elementos_encontrados.most_common(15):
                print(f"   • {elemento}: {count:,}")

        if cursos_com_deia:
            print(f"\n📋 EXEMPLOS DE CURSOS COM ELEMENTOS DEIA:")
            for curso in cursos_com_deia[:5]:
                print(f"   • {curso['curso']}: {', '.join(curso['elementos'])}")

        self.resultados["deia"] = {
            "cursos_com_deia": len(cursos_com_deia),
            "percentual": len(cursos_com_deia) / len(self.dados) * 100,
            "elementos_encontrados": dict(elementos_encontrados.most_common(15)),
            "exemplos": cursos_com_deia[:10],
        }

    def analisar_cursos_formacao(self):
        """Analisa cursos de formação/preceptoria."""
        print("\n🎓 ANÁLISE DE CURSOS DE FORMAÇÃO")
        print("-" * 40)

        palavras_formacao = [
            "formação",
            "capacitação",
            "treinamento",
            "preceptor",
            "preceptores",
            "tutor",
            "tutores",
            "educação",
            "ensino",
            "aprendizagem",
            "pedagogia",
            "didática",
        ]

        cursos_formacao = []

        for i, registro in enumerate(self.dados):
            texto = self.extrair_texto_curso(registro).lower()

            for palavra in palavras_formacao:
                if palavra in texto:
                    cursos_formacao.append(
                        {
                            "id": i,
                            "curso": registro.get("no_curso", "N/A"),
                            "palavra_chave": palavra,
                        }
                    )
                    break

        print(
            f"• Cursos de formação identificados: {len(cursos_formacao):,} ({len(cursos_formacao)/len(self.dados)*100:.1f}%)"
        )

        if cursos_formacao:
            print(f"\n📋 EXEMPLOS DE CURSOS DE FORMAÇÃO:")
            for curso in cursos_formacao[:10]:
                print(
                    f"   • {curso['curso']} (palavra-chave: {curso['palavra_chave']})"
                )

        self.resultados["formacao"] = {
            "cursos_formacao": len(cursos_formacao),
            "percentual": len(cursos_formacao) / len(self.dados) * 100,
            "exemplos": cursos_formacao[:15],
        }

    def extrair_texto_curso(self, registro: Dict) -> str:
        """Extrai texto completo do curso."""
        campos_texto = [
            "no_curso",
            "no_orgao",
            "no_formato",
            "no_nivel",
            "no_modalidade",
            "status",
            "titulo",
            "descricao",
            "palavras_chave",
            "publico_alvo",
            "area_tematica",
            "objetivos",
            "metodologia",
        ]

        texto_completo = ""
        for campo in campos_texto:
            valor = registro.get(campo)
            if valor and str(valor).lower() != "null":
                texto_completo += f" {str(valor)}"

        return texto_completo.strip()

    def salvar_resultados(self):
        """Salva os resultados da análise usando formatos padronizados."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Usar gerador de saída padronizada
        gerador = GeradorSaida()
        resultado_padronizado = gerador.gerar_saida_analise_exploratoria(
            self.resultados, len(self.dados)
        )

        # Salvar em diferentes formatos
        try:
            # JSON (formato principal)
            nome_json = f"relatorios/analise_exploratoria_{timestamp}.json"
            gerador.salvar_json(resultado_padronizado, nome_json)
            print(f"\n💾 Resultados JSON salvos: {nome_json}")

            # CSV (dados tabulares)
            nome_csv = f"relatorios/analise_exploratoria_{timestamp}.csv"
            ConversorFormatos.json_para_csv(
                [resultado_padronizado.metadata.__dict__], nome_csv
            )
            print(f"📊 Metadados CSV salvos: {nome_csv}")

            # YAML (configuração)
            nome_yaml = f"relatorios/analise_exploratoria_{timestamp}.yaml"
            ConversorFormatos.json_para_yaml(
                [resultado_padronizado.metadata.__dict__], nome_yaml
            )
            print(f"⚙️ Configuração YAML salva: {nome_yaml}")

        except Exception as e:
            print(f"❌ Erro ao salvar resultados: {e}")

        # Gerar relatório em Markdown
        self.gerar_relatorio_markdown(timestamp)

    def gerar_relatorio_markdown(self, timestamp: str):
        """Gera relatório em formato Markdown."""
        nome_arquivo = f"relatorios/analise_exploratoria_{timestamp}.md"

        relatorio = f"""# 🔍 RELATÓRIO DE ANÁLISE EXPLORATÓRIA

## 📋 RESUMO EXECUTIVO
- **Data da análise**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Arquivo analisado**: {os.path.basename(self.arquivo_dados)}
- **Total de registros**: {len(self.dados):,}

## 📊 ESTRUTURA DOS DADOS
- **Registros**: {self.resultados.get('estrutura', {}).get('total_registros', 0):,}
- **Campos por registro**: {self.resultados.get('estrutura', {}).get('campos_por_registro', 0)}

## 🏛️ INSTITUIÇÕES
- **Total de instituições**: {self.resultados.get('instituicoes', {}).get('total', 0)}

### Top 5 Instituições:
"""

        instituicoes = self.resultados.get("instituicoes", {}).get("top_15", {})
        for i, (inst, count) in enumerate(list(instituicoes.items())[:5]):
            percentual = (count / len(self.dados)) * 100
            relatorio += f"- **{inst}**: {count:,} ({percentual:.1f}%)\n"

        relatorio += f"""
## 🎓 NÍVEIS DE CURSO
"""

        niveis = self.resultados.get("niveis", {})
        for nivel, count in niveis.items():
            percentual = (count / len(self.dados)) * 100
            relatorio += f"- **{nivel}**: {count:,} ({percentual:.1f}%)\n"

        relatorio += f"""
## 📚 MODALIDADES
"""

        modalidades = self.resultados.get("modalidades", {})
        for modalidade, count in modalidades.get("modalidades", {}).items():
            percentual = (count / len(self.dados)) * 100
            relatorio += f"- **{modalidade}**: {count:,} ({percentual:.1f}%)\n"

        relatorio += f"""
## 🌈 ELEMENTOS DEIA
- **Cursos com elementos DEIA**: {self.resultados.get('deia', {}).get('cursos_com_deia', 0):,} ({self.resultados.get('deia', {}).get('percentual', 0):.1f}%)

### Elementos mais frequentes:
"""

        elementos = self.resultados.get("deia", {}).get("elementos_encontrados", {})
        for elemento, count in list(elementos.items())[:10]:
            relatorio += f"- **{elemento}**: {count:,}\n"

        relatorio += f"""
## 🎓 CURSOS DE FORMAÇÃO
- **Cursos de formação**: {self.resultados.get('formacao', {}).get('cursos_formacao', 0):,} ({self.resultados.get('formacao', {}).get('percentual', 0):.1f}%)

## 📊 CARGA HORÁRIA
"""

        carga_horaria = self.resultados.get("carga_horaria", {})
        if carga_horaria:
            stats = carga_horaria.get("estatisticas", {})
            relatorio += f"""
- **Média**: {stats.get('media', 0):.1f} horas
- **Mediana**: {stats.get('mediana', 0):.1f} horas
- **Mínimo**: {stats.get('minimo', 0):.1f} horas
- **Máximo**: {stats.get('maximo', 0):.1f} horas
"""

        relatorio += f"""
---
*Relatório gerado automaticamente pela Análise Exploratória*
"""

        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(relatorio)
            print(f"📄 Relatório Markdown salvo: {nome_arquivo}")
        except Exception as e:
            print(f"❌ Erro ao gerar relatório Markdown: {e}")


def main():
    """Função principal."""
    print("🔍 ANÁLISE EXPLORATÓRIA DOS DADOS UNA-SUS")
    print("=" * 50)

    try:
        analise = AnaliseExploratoria()
        analise.executar_analise_completa()

        print("\n✅ ANÁLISE EXPLORATÓRIA CONCLUÍDA!")
        print("📋 Verifique os relatórios gerados na pasta 'relatorios'")

    except Exception as e:
        print(f"❌ Erro durante a análise: {e}")


if __name__ == "__main__":
    main()
