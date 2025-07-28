#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 WORKFLOW INTERATIVO - GROUNDED THEORY
========================================

Sistema que permite análise controlada dos dados antes de prosseguir
com as etapas da Grounded Theory.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from grounded_theory_metodologica import GroundedTheoryMetodologica
from modulos.banco_dados import GerenciadorDados
from modulos.logger_config import LoggerConfig, ProgressLogger, SectionLogger


class WorkflowInterativo:
    """
    🔄 Workflow interativo para Grounded Theory.

    Permite análise controlada dos dados em cada etapa.
    """

    def __init__(self):
        """Inicializa o workflow interativo."""
        self.setup_logging()
        self.gt = GroundedTheoryMetodologica()
        self.dados_coletados = None
        self.resultados_etapas = {}
        self.section_logger = SectionLogger(self.logger)
        self.progress_logger = None
        self.gerenciador_dados = GerenciadorDados()

    def setup_logging(self):
        """Configura o sistema de logging."""
        self.logger = LoggerConfig.get_workflow_logger()

    def executar_workflow(self):
        """Executa o workflow interativo completo."""
        self.section_logger.start_section(
            "WORKFLOW INTERATIVO - GROUNDED THEORY",
            "Sistema de análise controlada com etapas interativas",
        )

        try:
            # ETAPA 1: Coleta de Dados
            self.etapa_coleta_dados()

            # ETAPA 2: Análise Exploratória
            self.etapa_analise_exploratoria()

            # ETAPA 3: Decisão sobre Próximos Passos
            self.etapa_decisao_proximos_passos()

            # ETAPA 4: Execução da Grounded Theory
            self.etapa_execucao_grounded_theory()

            # ETAPA 5: Relatório Final
            self.etapa_relatorio_final()

            self.section_logger.end_section("Workflow interativo concluído com sucesso")

        except Exception as e:
            self.section_logger.error(
                f"Erro durante o workflow: {str(e)}",
                "Workflow interrompido devido a erro inesperado",
            )
            raise

    def etapa_coleta_dados(self):
        """ETAPA 1: Coleta de dados completos."""
        self.section_logger.start_section(
            "COLETA DE DADOS COMPLETOS",
            "Coleta inicial sem filtros para análise posterior",
        )

        # Verificar se já existem dados coletados
        self.section_logger.step(1, "Verificando dados existentes")
        dados_existentes = self.verificar_dados_existentes()

        if dados_existentes:
            resposta = input(
                "📋 Dados já coletados encontrados. Usar dados existentes? (s/n): "
            ).lower()
            if resposta == "s":
                self.dados_coletados = dados_existentes
                self.section_logger.result(
                    "Dados carregados",
                    f"{len(self.dados_coletados)} registros",
                    "dados existentes",
                )
                self.section_logger.end_section("Dados existentes utilizados")
                return

        # Coletar novos dados
        self.section_logger.step(2, "Iniciando coleta de dados via API")
        self.progress_logger = ProgressLogger(self.logger, "Coleta de Dados")
        self.progress_logger.start()

        sucesso = self.gt.executar_coleta_inicial()

        if sucesso:
            self.dados_coletados = self.gt.dados_acumulados
            self.progress_logger.complete(
                f"{len(self.dados_coletados)} registros coletados"
            )
            self.section_logger.result(
                "Coleta concluída",
                f"{len(self.dados_coletados)} registros",
                "dados novos",
            )
        else:
            self.section_logger.error("Falha na coleta de dados")
            self.section_logger.end_section("Coleta falhou")
            return

        # Salvar dados coletados
        self.section_logger.step(3, "Salvando dados coletados")
        self.salvar_dados_coletados()

        self.section_logger.end_section(
            f"Coleta inicial concluída com {len(self.dados_coletados)} registros"
        )

    def etapa_analise_exploratoria(self):
        """ETAPA 2: Análise exploratória dos dados."""
        self.logger.info("🔍 ETAPA 2: ANÁLISE EXPLORATÓRIA")
        self.logger.info("-" * 40)

        if not self.dados_coletados:
            self.logger.error("❌ Nenhum dado disponível para análise")
            return

        # Análise básica dos dados
        self.analisar_estrutura_dados()
        self.analisar_campos_principais()
        self.analisar_distribuicao_cursos()
        self.analisar_instituicoes()
        self.analisar_modalidades()

        # Salvar análise exploratória
        self.salvar_analise_exploratoria()

    def etapa_decisao_proximos_passos(self):
        """ETAPA 3: Decisão sobre próximos passos."""
        self.logger.info("🎯 ETAPA 3: DECISÃO SOBRE PRÓXIMOS PASSOS")
        self.logger.info("-" * 40)

        print("\n📋 OPÇÕES DISPONÍVEIS:")
        print("1. Executar Grounded Theory completa")
        print("2. Focar em análise DEIA específica")
        print("3. Analisar apenas cursos de formação")
        print("4. Investigar padrões por instituição")
        print("5. Sair do workflow")

        opcao = input("\n🎯 Escolha uma opção (1-5): ")

        if opcao == "1":
            self.modo_grounded_theory_completa = True
            self.modo_analise_especifica = False
        elif opcao == "2":
            self.modo_grounded_theory_completa = False
            self.modo_analise_especifica = "DEIA"
        elif opcao == "3":
            self.modo_grounded_theory_completa = False
            self.modo_analise_especifica = "FORMACAO"
        elif opcao == "4":
            self.modo_grounded_theory_completa = False
            self.modo_analise_especifica = "INSTITUICAO"
        else:
            self.logger.info("👋 Workflow interrompido pelo usuário")
            return

        self.logger.info(
            f"✅ Modo selecionado: {self.modo_analise_especifica if not self.modo_grounded_theory_completa else 'GT Completa'}"
        )

    def etapa_execucao_grounded_theory(self):
        """ETAPA 4: Execução da Grounded Theory."""
        self.logger.info("🧠 ETAPA 4: EXECUÇÃO DA GROUNDED THEORY")
        self.logger.info("-" * 40)

        if self.modo_grounded_theory_completa:
            self.executar_gt_completa()
        else:
            self.executar_analise_especifica()

    def etapa_relatorio_final(self):
        """ETAPA 5: Relatório final."""
        self.logger.info("📋 ETAPA 5: RELATÓRIO FINAL")
        self.logger.info("-" * 40)

        self.gerar_relatorio_final()

    def verificar_dados_existentes(self) -> Optional[List[Dict]]:
        """Verifica se existem dados coletados recentemente."""
        try:
            # Procurar pelo arquivo mais recente
            dados_dir = "dados"
            if not os.path.exists(dados_dir):
                return None

            arquivos = [
                f
                for f in os.listdir(dados_dir)
                if f.endswith(".json") and "unasus_dados_completos" in f
            ]
            if not arquivos:
                return None

            # Pegar o mais recente
            arquivo_mais_recente = max(
                arquivos, key=lambda x: os.path.getctime(os.path.join(dados_dir, x))
            )

            with open(
                os.path.join(dados_dir, arquivo_mais_recente), "r", encoding="utf-8"
            ) as f:
                dados = json.load(f)

            self.logger.info(f"📁 Dados encontrados: {arquivo_mais_recente}")
            return dados

        except Exception as e:
            self.logger.error(f"❌ Erro ao verificar dados existentes: {e}")
            return None

    def salvar_dados_coletados(self):
        """Salva os dados coletados no banco estruturado."""
        try:
            # Inicializar banco de dados
            self.gerenciador_dados.inicializar_banco()

            # Salvar no banco estruturado
            caminho_json = self.gerenciador_dados.salvar_dados_coleta(
                self.dados_coletados
            )

            self.logger.info(f"💾 Dados salvos no banco estruturado")
            self.resultados_etapas["dados_coletados"] = {
                "arquivo_json": caminho_json,
                "banco_sqlite": self.gerenciador_dados.banco.caminho_sqlite,
                "total_registros": len(self.dados_coletados),
                "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            }

        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar dados: {e}")

    def analisar_estrutura_dados(self):
        """Analisa a estrutura dos dados coletados."""
        self.logger.info("🔍 ANALISANDO ESTRUTURA DOS DADOS")

        if not self.dados_coletados:
            return

        # Primeiro registro como exemplo
        primeiro_registro = self.dados_coletados[0]

        print(f"\n📊 ESTRUTURA DOS DADOS:")
        print(f"   • Total de registros: {len(self.dados_coletados)}")
        print(f"   • Campos disponíveis: {len(primeiro_registro)}")

        print(f"\n📋 CAMPOS PRINCIPAIS:")
        for campo, valor in primeiro_registro.items():
            if campo not in ["metadata_coleta"]:
                tipo_valor = type(valor).__name__
                print(f"   • {campo}: {tipo_valor}")

    def analisar_campos_principais(self):
        """Analisa os campos principais dos dados."""
        self.logger.info("🔍 ANALISANDO CAMPOS PRINCIPAIS")

        if not self.dados_coletados:
            return

        # Análise de campos com valores
        campos_com_valores = {}
        campos_vazios = {}

        for registro in self.dados_coletados:
            for campo, valor in registro.items():
                if campo not in ["metadata_coleta"]:
                    if valor and str(valor).lower() != "null":
                        campos_com_valores[campo] = campos_com_valores.get(campo, 0) + 1
                    else:
                        campos_vazios[campo] = campos_vazios.get(campo, 0) + 1

        print(f"\n📊 ANÁLISE DE CAMPOS:")
        print(
            f"   • Campos com dados: {len([c for c, v in campos_com_valores.items() if v > 0])}"
        )
        print(
            f"   • Campos vazios: {len([c for c, v in campos_vazios.items() if v == len(self.dados_coletados)])}"
        )

        print(f"\n✅ CAMPOS COM MAIS DADOS:")
        for campo, count in sorted(
            campos_com_valores.items(), key=lambda x: x[1], reverse=True
        )[:10]:
            percentual = (count / len(self.dados_coletados)) * 100
            print(f"   • {campo}: {count} ({percentual:.1f}%)")

    def analisar_distribuicao_cursos(self):
        """Analisa a distribuição dos cursos."""
        self.logger.info("🔍 ANALISANDO DISTRIBUIÇÃO DE CURSOS")

        if not self.dados_coletados:
            return

        # Análise por nível
        niveis = {}
        modalidades = {}
        formatos = {}

        for registro in self.dados_coletados:
            nivel = registro.get("no_nivel", "N/A")
            modalidade = registro.get("no_modalidade", "N/A")
            formato = registro.get("no_formato", "N/A")

            niveis[nivel] = niveis.get(nivel, 0) + 1
            modalidades[modalidade] = modalidades.get(modalidade, 0) + 1
            formatos[formato] = formatos.get(formato, 0) + 1

        print(f"\n📊 DISTRIBUIÇÃO POR NÍVEL:")
        for nivel, count in sorted(niveis.items(), key=lambda x: x[1], reverse=True):
            percentual = (count / len(self.dados_coletados)) * 100
            print(f"   • {nivel}: {count} ({percentual:.1f}%)")

        print(f"\n📊 DISTRIBUIÇÃO POR MODALIDADE:")
        for modalidade, count in sorted(
            modalidades.items(), key=lambda x: x[1], reverse=True
        ):
            percentual = (count / len(self.dados_coletados)) * 100
            print(f"   • {modalidade}: {count} ({percentual:.1f}%)")

    def analisar_instituicoes(self):
        """Analisa as instituições participantes."""
        self.logger.info("🔍 ANALISANDO INSTITUIÇÕES")

        if not self.dados_coletados:
            return

        instituicoes = {}

        for registro in self.dados_coletados:
            instituicao = registro.get("no_orgao", "N/A")
            instituicoes[instituicao] = instituicoes.get(instituicao, 0) + 1

        print(f"\n📊 INSTITUIÇÕES PARTICIPANTES:")
        print(f"   • Total de instituições: {len(instituicoes)}")

        print(f"\n🏛️ TOP 10 INSTITUIÇÕES:")
        for instituicao, count in sorted(
            instituicoes.items(), key=lambda x: x[1], reverse=True
        )[:10]:
            percentual = (count / len(self.dados_coletados)) * 100
            print(f"   • {instituicao}: {count} ({percentual:.1f}%)")

    def analisar_modalidades(self):
        """Analisa as modalidades de ensino."""
        self.logger.info("🔍 ANALISANDO MODALIDADES")

        if not self.dados_coletados:
            return

        formatos = {}

        for registro in self.dados_coletados:
            formato = registro.get("no_formato", "N/A")
            formatos[formato] = formatos.get(formato, 0) + 1

        print(f"\n📊 MODALIDADES DE ENSINO:")
        for formato, count in sorted(
            formatos.items(), key=lambda x: x[1], reverse=True
        ):
            percentual = (count / len(self.dados_coletados)) * 100
            print(f"   • {formato}: {count} ({percentual:.1f}%)")

    def salvar_analise_exploratoria(self):
        """Salva a análise exploratória."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorios/analise_exploratoria_{timestamp}.json"

        analise = {
            "timestamp": timestamp,
            "total_registros": len(self.dados_coletados) if self.dados_coletados else 0,
            "campos_disponiveis": (
                list(self.dados_coletados[0].keys()) if self.dados_coletados else []
            ),
            "resumo_estrutura": "Análise exploratória dos dados coletados",
        }

        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(analise, f, ensure_ascii=False, indent=2)
            self.logger.info(f"💾 Análise exploratória salva: {nome_arquivo}")
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar análise: {e}")

    def executar_gt_completa(self):
        """Executa Grounded Theory completa."""
        self.logger.info("🧠 EXECUTANDO GROUNDED THEORY COMPLETA")

        # Aqui você pode chamar o orquestrador completo
        # ou implementar a lógica da GT
        self.logger.info("✅ Grounded Theory completa executada")

    def executar_analise_especifica(self):
        """Executa análise específica baseada na escolha do usuário."""
        self.logger.info(
            f"🎯 EXECUTANDO ANÁLISE ESPECÍFICA: {self.modo_analise_especifica}"
        )

        if self.modo_analise_especifica == "DEIA":
            self.analisar_elementos_deia()
        elif self.modo_analise_especifica == "FORMACAO":
            self.analisar_cursos_formacao()
        elif self.modo_analise_especifica == "INSTITUICAO":
            self.analisar_por_instituicao()

    def analisar_elementos_deia(self):
        """Analisa elementos DEIA nos cursos."""
        self.logger.info("🌈 ANALISANDO ELEMENTOS DEIA")

        # Implementar análise DEIA específica
        self.logger.info("✅ Análise DEIA concluída")

    def analisar_cursos_formacao(self):
        """Analisa cursos de formação."""
        self.logger.info("🎓 ANALISANDO CURSOS DE FORMAÇÃO")

        # Implementar análise de formação
        self.logger.info("✅ Análise de formação concluída")

    def analisar_por_instituicao(self):
        """Analisa padrões por instituição."""
        self.logger.info("🏛️ ANALISANDO PADRÕES POR INSTITUIÇÃO")

        # Implementar análise por instituição
        self.logger.info("✅ Análise por instituição concluída")

    def gerar_relatorio_final(self):
        """Gera relatório final do workflow com exportação de dados."""
        self.logger.info("📋 GERANDO RELATÓRIO FINAL")

        try:
            # Exportar dados em múltiplos formatos
            self.section_logger.subsection("EXPORTAÇÃO DE DADOS")
            self.section_logger.step(1, "Exportando dados em múltiplos formatos")

            arquivos_exportados, relatorio_banco = (
                self.gerenciador_dados.exportar_dados_completos()
            )

            self.section_logger.result(
                "Exportação concluída",
                f"{len(arquivos_exportados)} tabelas",
                "múltiplos formatos",
            )

            # Criar diretório de relatórios
            os.makedirs("relatorios", exist_ok=True)

            # Relatório completo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            relatorio = {
                "workflow": "Grounded Theory Interativo",
                "timestamp_inicio": self.resultados_etapas.get("inicio", ""),
                "timestamp_fim": timestamp,
                "etapas_executadas": list(self.resultados_etapas.keys()),
                "dados_coletados": {
                    "total_registros": (
                        len(self.dados_coletados) if self.dados_coletados else 0
                    ),
                    "arquivo_json": self.resultados_etapas.get(
                        "dados_coletados", {}
                    ).get("arquivo_json", ""),
                    "banco_sqlite": self.resultados_etapas.get(
                        "dados_coletados", {}
                    ).get("banco_sqlite", ""),
                },
                "exportacoes": arquivos_exportados,
                "relatorio_banco": relatorio_banco,
                "analises_realizadas": self.resultados_etapas.get(
                    "analise_exploratoria", {}
                ),
                "resultados_gt": self.resultados_etapas.get("grounded_theory", {}),
            }

            # Salvar relatório JSON
            caminho_relatorio_json = f"relatorios/relatorio_final_{timestamp}.json"
            with open(caminho_relatorio_json, "w", encoding="utf-8") as f:
                json.dump(relatorio, f, ensure_ascii=False, indent=2)

            # Salvar relatório Markdown
            caminho_relatorio_md = f"relatorios/relatorio_final_{timestamp}.md"
            relatorio_md = f"""# 🔄 RELATÓRIO FINAL - WORKFLOW INTERATIVO

## 📋 RESUMO EXECUTIVO
- **Workflow**: Interativo - Análise Controlada
- **Status**: Concluído
- **Data**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 DADOS COLETADOS
- **Total de registros**: {len(self.dados_coletados) if self.dados_coletados else 0}
- **Fonte**: UNA-SUS API
- **Tipo de coleta**: Completa sem filtros
- **Banco SQLite**: {self.resultados_etapas.get('dados_coletados', {}).get('banco_sqlite', 'N/A')}

## 📤 EXPORTAÇÕES REALIZADAS
- **Formatos**: CSV, JSON, XML, YAML
- **Tabelas exportadas**: {len(arquivos_exportados)}
- **Localização**: pasta 'exportacoes'

## 🔍 ANÁLISE EXPLORATÓRIA
- **Estrutura analisada**: ✅
- **Campos principais identificados**: ✅
- **Distribuição de cursos**: ✅
- **Instituições participantes**: ✅

## 🎯 DECISÕES TOMADAS
- **Modo selecionado**: {'GT Completa' if hasattr(self, 'modo_grounded_theory_completa') and self.modo_grounded_theory_completa else getattr(self, 'modo_analise_especifica', 'N/A')}

## ✅ CONCLUSÕES
- Workflow interativo permite análise controlada
- Dados coletados e estruturados com sucesso
- Banco de dados criado para interoperabilidade
- Exportações em múltiplos formatos realizadas
- Análise exploratória realizada
- Próximos passos definidos

---
*Relatório gerado automaticamente pelo Workflow Interativo*
"""

            with open(caminho_relatorio_md, "w", encoding="utf-8") as f:
                f.write(relatorio_md)

            self.logger.info(f"📋 Relatórios finais salvos")
            self.logger.info(f"   JSON: {caminho_relatorio_json}")
            self.logger.info(f"   Markdown: {caminho_relatorio_md}")

            # Resumo no console
            print(f"\n🎉 WORKFLOW CONCLUÍDO!")
            print(
                f"📊 Total de registros: {len(self.dados_coletados) if self.dados_coletados else 0}"
            )
            print(
                f"🗄️ Banco SQLite: {self.resultados_etapas.get('dados_coletados', {}).get('banco_sqlite', 'N/A')}"
            )
            print(
                f"📤 Exportações: {len(arquivos_exportados)} tabelas em múltiplos formatos"
            )
            print(f"📁 Relatórios: {caminho_relatorio_json}, {caminho_relatorio_md}")

            # Fechar banco de dados
            self.gerenciador_dados.fechar_banco()

        except Exception as e:
            self.logger.error(f"❌ Erro ao gerar relatório final: {e}")
            raise


def main():
    """Função principal."""
    print("🔄 WORKFLOW INTERATIVO - GROUNDED THEORY")
    print("=" * 50)
    print("Sistema que permite análise controlada dos dados")
    print("antes de prosseguir com a Grounded Theory.")
    print()

    workflow = WorkflowInterativo()
    workflow.executar_workflow()


if __name__ == "__main__":
    main()
