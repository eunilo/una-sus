#!/usr/bin/env python3
"""
🧠 Grounded Theory Runner - Orquestrador Principal
==================================================

Este módulo orquestra todo o processo de Grounded Theory, coordenando
os diferentes módulos de codificação e análise.

🎯 FUNCIONALIDADES:
- Orquestração completa do processo
- Gerenciamento de iterações
- Controle de saturação teórica
- Geração de relatórios
- Integração de módulos

🔬 METODOLOGIA:
- Processo iterativo completo
- Integração de todas as etapas
- Controle de qualidade
- Documentação automática
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List

from modulos.codificacao_aberta import CodificacaoAberta
from modulos.codificacao_axial import CodificacaoAxial
from modulos.codificacao_seletiva import CodificacaoSeletiva

# Importar módulos da Grounded Theory
from modulos.coleta_dados import ColetorDadosGroundedTheory


class GroundedTheoryRunner:
    """
    🧠 Orquestrador principal da Grounded Theory

    Coordena todo o processo de pesquisa qualitativa.
    """

    def __init__(self, config: Dict = None):
        """
        Inicializa o runner da Grounded Theory.

        Args:
            config: Configurações do processo
        """
        self.config = config or self._config_padrao()
        self.logger = self._configurar_logger()
        self.iteracao_atual = 0
        self.dados_acumulados = []
        self.resultados_parciais = []
        self.saturacao_atingida = False

        # Inicializar módulos
        self.coletor = ColetorDadosGroundedTheory(self.config, self.logger)
        self.codificador_aberta = CodificacaoAberta(self.logger)
        self.codificador_axial = CodificacaoAxial(self.logger)
        self.codificador_seletiva = CodificacaoSeletiva(self.logger)

    def _config_padrao(self) -> Dict:
        """
        📋 Retorna configuração padrão.

        Returns:
            Configuração padrão
        """
        return {
            "criterios_iniciais": {
                "descritores": [
                    "diversidade",
                    "equidade",
                    "inclusão",
                    "acessibilidade",
                ],
                "filtros": {},
                "max_iteracoes": 5,
            },
            "configuracoes_analise": {
                "min_frequencia_conceito": 3,
                "min_categorias": 3,
                "criterio_saturacao": 0.1,  # 10% de novos conceitos
            },
        }

    def _configurar_logger(self) -> logging.Logger:
        """
        📝 Configura o logger para o processo.

        Returns:
            Logger configurado
        """
        # Criar pasta de logs se não existir
        os.makedirs("logs", exist_ok=True)

        # Configurar logger
        logger = logging.getLogger("GroundedTheory")
        logger.setLevel(logging.INFO)

        # Handler para arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fh = logging.FileHandler(
            f"logs/grounded_theory_{timestamp}.log", encoding="utf-8"
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

    def executar_processo_completo(self) -> Dict:
        """
        🚀 Executa o processo completo de Grounded Theory.

        Returns:
            Resultados finais do processo
        """
        self.logger.info("🚀 INICIANDO PROCESSO COMPLETO DE GROUNDED THEORY")

        resultados_finais = {
            "processo": "Grounded Theory Completa",
            "iteracoes_realizadas": 0,
            "dados_coletados": [],
            "resultados_parciais": [],
            "teoria_final": {},
            "estatisticas_gerais": {},
            "timestamp_inicio": datetime.now().isoformat(),
            "timestamp_fim": None,
        }

        try:
            # Coleta inicial
            self.logger.info("📊 ETAPA 1: COLETA INICIAL")
            dados_iniciais = self.coletor.coleta_inicial()
            self.dados_acumulados.extend(dados_iniciais)

            # Processar iterações até saturação
            while (
                not self.saturacao_atingida
                and self.iteracao_atual
                < self.config["criterios_iniciais"]["max_iteracoes"]
            ):
                self.iteracao_atual += 1
                self.logger.info(f"🔄 INICIANDO ITERAÇÃO {self.iteracao_atual}")

                # Executar iteração
                resultado_iteracao = self._executar_iteracao()
                self.resultados_parciais.append(resultado_iteracao)

                # Verificar saturação
                self._verificar_saturacao()

            # Codificação seletiva final
            self.logger.info("🎯 ETAPA FINAL: CODIFICAÇÃO SELETIVA")
            teoria_final = self._executar_codificacao_seletiva_final()

            # Gerar resultados finais
            resultados_finais.update(
                {
                    "iteracoes_realizadas": self.iteracao_atual,
                    "dados_coletados": self.dados_acumulados,
                    "resultados_parciais": self.resultados_parciais,
                    "teoria_final": teoria_final,
                    "estatisticas_gerais": self._calcular_estatisticas_gerais(),
                    "timestamp_fim": datetime.now().isoformat(),
                }
            )

            # Salvar resultados
            self._salvar_resultados_finais(resultados_finais)

            self.logger.info("✅ PROCESSO COMPLETO FINALIZADO COM SUCESSO")

        except Exception as e:
            self.logger.error(f"❌ ERRO NO PROCESSO: {str(e)}")
            resultados_finais["erro"] = str(e)

        return resultados_finais

    def _executar_iteracao(self) -> Dict:
        """
        🔄 Executa uma iteração completa.

        Returns:
            Resultados da iteração
        """
        resultado_iteracao = {
            "iteracao": self.iteracao_atual,
            "timestamp_inicio": datetime.now().isoformat(),
            "dados_coletados": [],
            "codificacao_aberta": {},
            "codificacao_axial": {},
            "insights_gerados": [],
        }

        # Coleta iterativa
        if self.iteracao_atual > 1:
            insights_anteriores = self._extrair_insights_anteriores()
            dados_novos = self.coletor.coleta_iterativa(insights_anteriores)
            self.dados_acumulados.extend(dados_novos)
            resultado_iteracao["dados_coletados"] = dados_novos

        # Codificação aberta
        self.logger.info(f"🔍 ITERAÇÃO {self.iteracao_atual}: Codificação Aberta")
        codificacao_aberta = self.codificador_aberta.codificar_dados(
            self.dados_acumulados
        )
        resultado_iteracao["codificacao_aberta"] = codificacao_aberta

        # Codificação axial
        self.logger.info(f"🔗 ITERAÇÃO {self.iteracao_atual}: Codificação Axial")
        codificacao_axial = self.codificador_axial.codificar_axial(codificacao_aberta)
        resultado_iteracao["codificacao_axial"] = codificacao_axial

        # Gerar insights
        insights = self._gerar_insights(codificacao_aberta, codificacao_axial)
        resultado_iteracao["insights_gerados"] = insights

        resultado_iteracao["timestamp_fim"] = datetime.now().isoformat()

        return resultado_iteracao

    def _extrair_insights_anteriores(self) -> List[Dict]:
        """
        🔍 Extrai insights das iterações anteriores.

        Returns:
            Lista de insights
        """
        insights = []

        for resultado in self.resultados_parciais:
            # Insights da codificação aberta
            cod_aberta = resultado.get("codificacao_aberta", {})
            conceitos_frequentes = cod_aberta.get("estatisticas", {}).get(
                "conceito_mais_frequente"
            )
            if conceitos_frequentes:
                insights.append(
                    {
                        "tipo": "conceito_frequente",
                        "conceito": conceitos_frequentes,
                        "iteracao": resultado["iteracao"],
                    }
                )

            # Insights da codificação axial
            cod_axial = resultado.get("codificacao_axial", {})
            fenomeno_central = cod_axial.get("paradigma_codificacao", {}).get(
                "fenomeno_central", []
            )
            if fenomeno_central:
                insights.append(
                    {
                        "tipo": "fenomeno_central",
                        "fenomeno": fenomeno_central[0],
                        "iteracao": resultado["iteracao"],
                    }
                )

        return insights

    def _gerar_insights(self, cod_aberta: Dict, cod_axial: Dict) -> List[Dict]:
        """
        💡 Gera insights baseados nas codificações.

        Args:
            cod_aberta: Resultados da codificação aberta
            cod_axial: Resultados da codificação axial

        Returns:
            Lista de insights
        """
        insights = []

        # Insight sobre conceitos emergentes
        conceitos = cod_aberta.get("conceitos_identificados", {})
        conceitos_novos = [
            conceito
            for conceito, info in conceitos.items()
            if info["frequencia"] == 1  # Conceitos que apareceram apenas uma vez
        ]

        if conceitos_novos:
            insights.append(
                {
                    "tipo": "categoria_emergente",
                    "conceitos": conceitos_novos,
                    "descritores_sugeridos": conceitos_novos[:3],
                }
            )

        # Insight sobre padrões
        categorias = cod_aberta.get("categorias_iniciais", {})
        if len(categorias) > 3:
            insights.append(
                {
                    "tipo": "padrao_identificado",
                    "padrao": "muitas_categorias",
                    "filtro_sugerido": {"max_categorias": 3},
                }
            )

        return insights

    def _verificar_saturacao(self):
        """
        🎯 Verifica se atingiu saturação teórica.
        """
        if self.iteracao_atual < 2:
            return  # Precisa de pelo menos 2 iterações

        # Verificar com o coletor
        dados_anteriores = self.dados_acumulados[
            : -len(self.resultados_parciais[-1]["dados_coletados"])
        ]
        dados_novos = self.resultados_parciais[-1]["dados_coletados"]

        self.saturacao_atingida = self.coletor.verificar_saturacao(
            dados_novos, dados_anteriores
        )

        if self.saturacao_atingida:
            self.logger.info("🎯 SATURAÇÃO TEÓRICA ATINGIDA")

    def _executar_codificacao_seletiva_final(self) -> Dict:
        """
        🎯 Executa codificação seletiva final com todos os dados.

        Returns:
            Resultados da codificação seletiva
        """
        # Usar dados da última iteração
        ultima_iteracao = self.resultados_parciais[-1]
        cod_aberta = ultima_iteracao["codificacao_aberta"]
        cod_axial = ultima_iteracao["codificacao_axial"]

        # Executar codificação seletiva
        cod_seletiva = self.codificador_seletiva.codificar_seletiva(
            cod_aberta, cod_axial
        )

        return cod_seletiva

    def _calcular_estatisticas_gerais(self) -> Dict:
        """
        📊 Calcula estatísticas gerais do processo.

        Returns:
            Estatísticas gerais
        """
        estatisticas = {
            "total_iteracoes": self.iteracao_atual,
            "total_dados_coletados": len(self.dados_acumulados),
            "saturacao_atingida": self.saturacao_atingida,
            "duracao_processo": self._calcular_duracao(),
            "conceitos_identificados": 0,
            "categorias_finais": 0,
        }

        # Estatísticas dos dados
        if self.resultados_parciais:
            ultima_iteracao = self.resultados_parciais[-1]
            cod_aberta = ultima_iteracao.get("codificacao_aberta", {})
            estatisticas["conceitos_identificados"] = cod_aberta.get(
                "estatisticas", {}
            ).get("total_conceitos", 0)
            estatisticas["categorias_finais"] = cod_aberta.get("estatisticas", {}).get(
                "total_categorias", 0
            )

        return estatisticas

    def _calcular_duracao(self) -> str:
        """
        ⏱️ Calcula duração do processo.

        Returns:
            Duração formatada
        """
        # Implementar cálculo de duração
        return "Processo em andamento"

    def _salvar_resultados_finais(self, resultados: Dict):
        """
        💾 Salva resultados finais do processo.

        Args:
            resultados: Resultados finais
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"resultados_grounded_theory_{timestamp}.json"

        caminho = os.path.join("resultados", nome_arquivo)

        # Criar pasta se não existir
        os.makedirs("resultados", exist_ok=True)

        # Salvar resultados
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)

        self.logger.info(f"💾 Resultados finais salvos em: {caminho}")

    def gerar_relatorio_final(self, resultados: Dict) -> str:
        """
        📊 Gera relatório final do processo.

        Args:
            resultados: Resultados do processo

        Returns:
            Relatório em formato texto
        """
        relatorio = f"""
# 🧠 RELATÓRIO FINAL - GROUNDED THEORY

## 📋 RESUMO EXECUTIVO
- **Processo**: {resultados.get('processo', 'N/A')}
- **Iterações Realizadas**: {resultados.get('iteracoes_realizadas', 0)}
- **Dados Coletados**: {len(resultados.get('dados_coletados', []))}
- **Saturação Atingida**: {'Sim' if resultados.get('saturacao_atingida', False) else 'Não'}

## 🎯 TEORIA FINAL
"""

        teoria_final = resultados.get("teoria_final", {})
        if teoria_final:
            relatorio += f"""
### Fenômeno Central
{teoria_final.get('fenomeno_central', 'Não identificado')}

### Resumo Teórico
{teoria_final.get('resumo_teorico', 'Não disponível')}

### Implicações
"""
            for i, implicacao in enumerate(teoria_final.get("implicacoes", []), 1):
                relatorio += f"{i}. {implicacao}\n"

        relatorio += f"""
## 📊 ESTATÍSTICAS GERAIS
"""

        estatisticas = resultados.get("estatisticas_gerais", {})
        for chave, valor in estatisticas.items():
            relatorio += f"- **{chave.replace('_', ' ').title()}**: {valor}\n"

        return relatorio


def main():
    """
    🚀 Função principal para executar Grounded Theory.
    """
    print("🧠 INICIANDO GROUNDED THEORY RUNNER")

    # Configuração personalizada (opcional)
    config = {
        "criterios_iniciais": {
            "descritores": [
                "diversidade",
                "equidade",
                "inclusão",
                "acessibilidade",
                "saúde mental",
            ],
            "filtros": {},
            "max_iteracoes": 3,
        }
    }

    # Criar e executar runner
    runner = GroundedTheoryRunner(config)
    resultados = runner.executar_processo_completo()

    # Gerar e salvar relatório
    relatorio = runner.gerar_relatorio_final(resultados)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"relatorio_grounded_theory_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(relatorio)

    print("✅ PROCESSO CONCLUÍDO!")
    print(f"📊 Relatório salvo: relatorio_grounded_theory_{timestamp}.md")


if __name__ == "__main__":
    main()
