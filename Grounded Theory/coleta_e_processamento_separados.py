#!/usr/bin/env python3
"""
🔄 Coleta e Processamento Separados - UNA-SUS
============================================

Este script implementa a separação completa entre coleta de dados
e processamento DEIA, garantindo integridade do database original.

🎯 ARQUITETURA:
1. 📊 COLETA COMPLETA - Todos os dados UNA-SUS
2. 💾 DATABASE FIEL - Preservação dos dados originais
3. 🔍 PROCESSAMENTO DEIA - Análise não-destrutiva
4. 📈 RELATÓRIOS - Resultados separados

🔬 METODOLOGIA:
- Separação clara de responsabilidades
- Database intacto e atualizado
- Processamento não-destrutivo
- Logs detalhados de cada etapa
"""

import logging
import os
import sys
from datetime import datetime
from typing import Dict, List

from modulos.analisador_geral import AnalisadorGeral

# Importar módulos
from modulos.coletor_unasus_completo import ColetorUnasusCompleto
from modulos.processador_deia import ProcessadorDEIA


class OrquestradorColetaProcessamento:
    """
    🔄 Orquestrador de Coleta e Processamento Separados

    Coordena coleta completa e processamento DEIA mantendo integridade.
    """

    def __init__(self):
        """
        Inicializa o orquestrador.
        """
        self.logger = self._configurar_logger()
        self.coletor = ColetorUnasusCompleto(self.logger)
        self.processador = ProcessadorDEIA(self.logger)
        self.analisador = AnalisadorGeral(self.logger)
        self.dados_coletados = []
        self.resultados_processamento = {}
        self.resultados_analise_geral = {}

    def _configurar_logger(self) -> logging.Logger:
        """
        📝 Configura o logger principal.

        Returns:
            Logger configurado
        """
        # Criar pasta de logs se não existir
        os.makedirs("logs", exist_ok=True)

        # Configurar logger
        logger = logging.getLogger("OrquestradorColetaProcessamento")
        logger.setLevel(logging.INFO)

        # Handler para arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fh = logging.FileHandler(f"logs/orquestrador_{timestamp}.log", encoding="utf-8")
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

    def executar_coleta_completa(self) -> bool:
        """
        📊 Executa coleta completa de dados UNA-SUS.

        Returns:
            True se bem-sucedida, False caso contrário
        """
        self.logger.info("🚀 INICIANDO COLETA COMPLETA")
        self.logger.info("📋 PRINCÍPIO: Coletar TODOS os dados sem filtros")

        try:
            # Executar coleta completa
            self.dados_coletados = self.coletor.coletar_dados_completos()

            self.logger.info(
                f"✅ COLETA COMPLETA FINALIZADA: {len(self.dados_coletados)} cursos"
            )
            return True

        except Exception as e:
            self.logger.error(f"❌ ERRO NA COLETA: {str(e)}")
            return False

    def carregar_dados_existentes(self, caminho_arquivo: str) -> bool:
        """
        📂 Carrega dados existentes para processamento.

        Args:
            caminho_arquivo: Caminho para o arquivo de dados

        Returns:
            True se carregado com sucesso, False caso contrário
        """
        self.logger.info(f"📂 Carregando dados existentes: {caminho_arquivo}")

        try:
            # Carregar dados no coletor
            self.dados_coletados = self.coletor.carregar_dados_existentes(
                caminho_arquivo
            )

            if self.dados_coletados:
                self.logger.info(
                    f"✅ Dados carregados: {len(self.dados_coletados)} registros"
                )
                return True
            else:
                self.logger.error("❌ Nenhum dado carregado")
                return False

        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar dados: {str(e)}")
            return False

    def executar_processamento_deia(self) -> bool:
        """
        🔍 Executa processamento DEIA nos dados coletados.

        Returns:
            True se bem-sucedido, False caso contrário
        """
        self.logger.info("🔍 INICIANDO PROCESSAMENTO DEIA")
        self.logger.info("📋 PRINCÍPIO: Análise não-destrutiva dos dados")

        if not self.dados_coletados:
            self.logger.error("❌ Nenhum dado disponível para processamento")
            return False

        try:
            # Carregar dados no processador
            self.processador.dados_originais = self.dados_coletados

            # Executar análise DEIA
            self.resultados_processamento = self.processador.processar_analise_deia()

            self.logger.info("✅ PROCESSAMENTO DEIA FINALIZADO")
            return True

        except Exception as e:
            self.logger.error(f"❌ ERRO NO PROCESSAMENTO: {str(e)}")
            return False

    def executar_analise_geral(
        self, tipo_analise: str = "estatistica", parametros: Dict = None
    ) -> bool:
        """
        📊 Executa análise geral dos dados coletados.

        Args:
            tipo_analise: Tipo de análise ('estatistica', 'categoria', etc.)
            parametros: Parâmetros específicos da análise

        Returns:
            True se bem-sucedido, False caso contrário
        """
        self.logger.info(f"📊 INICIANDO ANÁLISE GERAL: {tipo_analise}")
        self.logger.info("📋 PRINCÍPIO: Análise flexível sem comprometer dados")

        if not self.dados_coletados:
            self.logger.error("❌ Nenhum dado disponível para análise")
            return False

        try:
            # Carregar dados no analisador
            self.analisador.dados_originais = self.dados_coletados

            # Configurar análise
            self.analisador.configurar_analise(tipo_analise, parametros)

            # Executar análise
            self.resultados_analise_geral = self.analisador.executar_analise()

            # Salvar resultados
            self.analisador.salvar_resultados()

            self.logger.info("✅ ANÁLISE GERAL CONCLUÍDA")
            return True

        except Exception as e:
            self.logger.error(f"❌ Erro na análise geral: {str(e)}")
            return False

    def executar_workflow_completo(
        self, executar_coleta: bool = True, caminho_dados: str = None
    ) -> Dict:
        """
        🔄 Executa workflow completo de coleta e processamento.

        Args:
            executar_coleta: Se deve executar coleta ou usar dados existentes
            caminho_dados: Caminho para dados existentes (se não executar coleta)

        Returns:
            Resultados do workflow
        """
        self.logger.info("🔄 INICIANDO WORKFLOW COMPLETO")

        resultados_workflow = {
            "workflow": "Coleta e Processamento Separados",
            "timestamp_inicio": datetime.now().isoformat(),
            "etapas_executadas": [],
            "resultados": {},
            "status": "em_andamento",
        }

        try:
            # ETAPA 1: Coleta ou Carregamento
            if executar_coleta:
                self.logger.info("📊 ETAPA 1: Coleta Completa de Dados")
                if self.executar_coleta_completa():
                    resultados_workflow["etapas_executadas"].append("coleta_completa")
                else:
                    raise Exception("Falha na coleta de dados")
            else:
                self.logger.info("📂 ETAPA 1: Carregamento de Dados Existentes")
                if caminho_dados and self.carregar_dados_existentes(caminho_dados):
                    resultados_workflow["etapas_executadas"].append(
                        "carregamento_dados"
                    )
                else:
                    raise Exception("Falha no carregamento de dados")

            # ETAPA 2: Processamento DEIA
            self.logger.info("🔍 ETAPA 2: Processamento DEIA")
            if self.executar_processamento_deia():
                resultados_workflow["etapas_executadas"].append("processamento_deia")
                resultados_workflow["resultados_deia"] = self.resultados_processamento
            else:
                raise Exception("Falha no processamento DEIA")

            # ETAPA 3: Análise Geral
            self.logger.info("📊 ETAPA 3: Análise Geral")
            if self.executar_analise_geral("estatistica"):
                resultados_workflow["etapas_executadas"].append("analise_geral")
                resultados_workflow["resultados_analise_geral"] = (
                    self.resultados_analise_geral
                )
            else:
                raise Exception("Falha na análise geral")

            # Workflow concluído com sucesso
            resultados_workflow["status"] = "concluido"
            resultados_workflow["timestamp_fim"] = datetime.now().isoformat()

            # Gerar relatório final
            self._gerar_relatorio_workflow(resultados_workflow)

            self.logger.info("✅ WORKFLOW COMPLETO FINALIZADO COM SUCESSO")

        except Exception as e:
            self.logger.error(f"❌ ERRO NO WORKFLOW: {str(e)}")
            resultados_workflow["status"] = "erro"
            resultados_workflow["erro"] = str(e)
            resultados_workflow["timestamp_fim"] = datetime.now().isoformat()

        return resultados_workflow

    def _gerar_relatorio_workflow(self, resultados: Dict):
        """
        📊 Gera relatório final do workflow.

        Args:
            resultados: Resultados do workflow
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_relatorio = f"relatorios/relatorio_workflow_{timestamp}.json"

        # Criar pasta se não existir
        os.makedirs("relatorios", exist_ok=True)

        # Salvar relatório
        import json

        with open(caminho_relatorio, "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)

        self.logger.info(f"📊 Relatório do workflow salvo: {caminho_relatorio}")

    def mostrar_estatisticas(self):
        """
        📈 Mostra estatísticas do processo.
        """
        print("\n" + "=" * 60)
        print("📊 ESTATÍSTICAS DO PROCESSO")
        print("=" * 60)

        print(f"📊 Dados Coletados: {len(self.dados_coletados)} cursos")

        if self.resultados_processamento:
            resumo = self.resultados_processamento.get("resumo_geral", {})
            print(f"🔍 Cursos com DEIA: {resumo.get('cursos_com_elementos_deia', 0)}")
            print(f"📈 Percentual DEIA: {resumo.get('percentual_deia', 0):.2f}%")

        if self.resultados_analise_geral:
            resumo_geral = self.resultados_analise_geral.get("resumo_geral", {})
            print(f"📈 Total de Cursos: {resumo_geral.get('total_cursos', 0)}")
            print(
                f"📂 Campos Disponíveis: {len(resumo_geral.get('campos_disponiveis', []))}"
            )

        print("=" * 60)


def main():
    """
    🚀 Função principal do script.
    """
    print("🔄 INICIANDO COLETA E PROCESSAMENTO SEPARADOS")
    print("📋 Arquitetura: Coleta Completa + Processamento DEIA")

    # Criar orquestrador
    orquestrador = OrquestradorColetaProcessamento()

    # Configurar opções
    print("\n🎯 OPÇÕES DISPONÍVEIS:")
    print("1. Executar coleta completa + processamento DEIA + análise geral")
    print("2. Usar dados existentes + processamento DEIA + análise geral")
    print("3. Apenas coleta completa")
    print("4. Apenas processamento DEIA")
    print("5. Apenas análise geral")
    print("6. Análise geral customizada")

    try:
        opcao = input("\nEscolha uma opção (1-6): ").strip()

        if opcao == "1":
            print("\n🚀 Executando workflow completo...")
            resultados = orquestrador.executar_workflow_completo(executar_coleta=True)

        elif opcao == "2":
            caminho = input("Caminho para arquivo de dados: ").strip()
            print(f"\n🚀 Executando processamento com dados existentes...")
            resultados = orquestrador.executar_workflow_completo(
                executar_coleta=False, caminho_dados=caminho
            )

        elif opcao == "3":
            print("\n📊 Executando apenas coleta completa...")
            sucesso = orquestrador.executar_coleta_completa()
            resultados = {"status": "coleta_concluida" if sucesso else "erro"}

        elif opcao == "4":
            caminho = input("Caminho para arquivo de dados: ").strip()
            print(f"\n🔍 Executando apenas processamento DEIA...")
            if orquestrador.carregar_dados_existentes(caminho):
                sucesso = orquestrador.executar_processamento_deia()
                resultados = {
                    "status": "processamento_concluido" if sucesso else "erro"
                }
            else:
                resultados = {"status": "erro_carregamento"}

        elif opcao == "5":
            caminho = input("Caminho para arquivo de dados: ").strip()
            print(f"\n📊 Executando apenas análise geral...")
            if orquestrador.carregar_dados_existentes(caminho):
                sucesso = orquestrador.executar_analise_geral("estatistica")
                resultados = {"status": "analise_concluida" if sucesso else "erro"}
            else:
                resultados = {"status": "erro_carregamento"}

        elif opcao == "6":
            caminho = input("Caminho para arquivo de dados: ").strip()
            print(f"\n🔧 Análise geral customizada...")
            print(
                "Tipos disponíveis: estatistica, categoria, temporal, geografica, conteudo, comparativa"
            )
            tipo = input("Tipo de análise: ").strip()
            if orquestrador.carregar_dados_existentes(caminho):
                sucesso = orquestrador.executar_analise_geral(tipo)
                resultados = {
                    "status": "analise_customizada_concluida" if sucesso else "erro"
                }
            else:
                resultados = {"status": "erro_carregamento"}

        else:
            print("❌ Opção inválida")
            return

        # Mostrar estatísticas
        orquestrador.mostrar_estatisticas()

        # Mostrar resultado
        print(f"\n📋 Status Final: {resultados.get('status', 'desconhecido')}")

        if resultados.get("status") == "concluido":
            print("✅ Processo concluído com sucesso!")
            print("📁 Verifique as pastas 'dados/', 'resultados/' e 'relatorios/'")

    except KeyboardInterrupt:
        print("\n⚠️ Processo interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")


if __name__ == "__main__":
    main()
