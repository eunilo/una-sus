os  #!/usr/bin/env python3
"""
🔄 ORQUESTRADOR GROUNDED THEORY - WORKFLOW LÓGICO
================================================

Orquestrador principal que implementa rigorosamente o workflow
lógico da Grounded Theory com etapas bem definidas e sequenciais.

🎯 WORKFLOW LÓGICO:
1. DEFINIÇÃO DO PROBLEMA
2. COLETA INICIAL (Teórica)
3. CODIFICAÇÃO ABERTA
4. AMOSTRAGEM TEÓRICA (Iterativa)
5. CODIFICAÇÃO AXIAL
6. VERIFICAÇÃO DE SATURAÇÃO
7. CODIFICAÇÃO SELETIVA
8. DESENVOLVIMENTO DE TEORIA
9. VALIDAÇÃO E REFINAMENTO

📋 PRINCÍPIOS:
- Sequência lógica rigorosa
- Cada etapa depende da anterior
- Critérios claros de progressão
- Documentação completa do processo
- Rastreabilidade metodológica
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from grounded_theory_metodologica import GroundedTheoryMetodologica


class OrquestradorGroundedTheory:
    """
    🔄 Orquestrador do workflow lógico da Grounded Theory
    """

    def __init__(self):
        """
        Inicializa o orquestrador.
        """
        self.logger = self._configurar_logger()
        self.workflow_status = {
            "etapa_atual": 0,
            "etapas_concluidas": [],
            "etapas_pendentes": [],
            "status_geral": "inicializado",
        }
        self.resultados_workflow = {}

    def _configurar_logger(self) -> logging.Logger:
        """
        📝 Configura o logger.
        """
        os.makedirs("logs", exist_ok=True)

        logger = logging.getLogger("OrquestradorGT")
        logger.setLevel(logging.INFO)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fh = logging.FileHandler(
            f"logs/orquestrador_gt_{timestamp}.log", encoding="utf-8"
        )
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def definir_problema_pesquisa(self) -> Dict:
        """
        🎯 ETAPA 1: Define o problema de pesquisa.

        Returns:
            Definição do problema
        """
        self.logger.info("🎯 ETAPA 1: DEFININDO PROBLEMA DE PESQUISA")

        problema = {
            "pergunta_central": "Como a UNA-SUS aborda elementos de DEIA em seus cursos?",
            "objetivo": "Desenvolver teoria fundamentada sobre abordagem DEIA na formação em saúde",
            "contexto": "Educação em saúde pública no Brasil",
            "populacao": "Cursos oferecidos pela UNA-SUS",
            "criterios_inclusao": [
                "Cursos ativos na plataforma UNA-SUS",
                "Dados disponíveis via API pública",
                "Informações sobre conteúdo e objetivos",
            ],
            "criterios_exclusao": [
                "Cursos sem informações básicas",
                "Dados duplicados ou inconsistentes",
            ],
            "questoes_especificas": [
                "Quais elementos DEIA estão presentes nos cursos?",
                "Como esses elementos são abordados?",
                "Quais padrões emergem da análise?",
                "Como isso se relaciona com políticas públicas?",
            ],
        }

        self.workflow_status["etapas_concluidas"].append("definicao_problema")
        self.workflow_status["etapa_atual"] = 1

        self.logger.info("✅ Problema de pesquisa definido")
        return problema

    def configurar_metodologia(self) -> Dict:
        """
        ⚙️ ETAPA 2: Configura a metodologia.

        Returns:
            Configuração metodológica
        """
        self.logger.info("⚙️ ETAPA 2: CONFIGURANDO METODOLOGIA")

        configuracao = {
            "metodologia": "Grounded Theory (Teoria Fundamentada)",
            "abordagem": "Qualitativa",
            "paradigma": "Construtivista",
            "etapas_metodologicas": [
                "Coleta Inicial (Teórica)",
                "Codificação Aberta",
                "Amostragem Teórica",
                "Codificação Axial",
                "Verificação de Saturação",
                "Codificação Seletiva",
                "Desenvolvimento de Teoria",
            ],
            "criterios_rigor": [
                "Credibilidade",
                "Transferibilidade",
                "Dependabilidade",
                "Confirmabilidade",
            ],
            "instrumentos_coleta": [
                "API UNA-SUS",
                "Análise documental",
                "Codificação sistemática",
            ],
            "criterios_saturacao": {
                "novos_conceitos": "< 10%",
                "iteracoes_maximas": 5,
                "estabilidade_categorias": True,
            },
        }

        self.workflow_status["etapas_concluidas"].append("configuracao_metodologia")
        self.workflow_status["etapa_atual"] = 2

        self.logger.info("✅ Metodologia configurada")
        return configuracao

    def executar_grounded_theory(self) -> Dict:
        """
        🧠 ETAPA 3: Executa o processo de Grounded Theory.

        Returns:
            Resultados da Grounded Theory
        """
        self.logger.info("🧠 ETAPA 3: EXECUTANDO GROUNDED THEORY")

        # Configurar Grounded Theory
        config = {
            "criterios_iniciais": {
                "descritores": [],  # Sem critérios restritivos para coleta inicial
                "filtros": {},
                "max_iteracoes": 5,
            },
            "configuracoes_analise": {
                "min_frequencia_conceito": 2,
                "min_categorias": 3,
                "criterio_saturacao": 0.1,
                "max_iteracoes_saturacao": 5,
            },
        }

        # Executar processo
        gt = GroundedTheoryMetodologica(config)
        resultados = gt.executar_processo_completo()

        if resultados.get("status") == "concluido":
            self.workflow_status["etapas_concluidas"].append("grounded_theory")
            self.workflow_status["etapa_atual"] = 3
            self.logger.info("✅ Grounded Theory concluída")
        else:
            self.logger.error(f"❌ Erro na Grounded Theory: {resultados.get('erro')}")

        return resultados

    def validar_resultados(self, resultados_gt: Dict) -> Dict:
        """
        ✅ ETAPA 4: Valida os resultados obtidos.

        Args:
            resultados_gt: Resultados da Grounded Theory

        Returns:
            Validação dos resultados
        """
        self.logger.info("✅ ETAPA 4: VALIDANDO RESULTADOS")

        validacao = {
            "criterios_rigor": {},
            "limites_identificados": [],
            "recomendacoes": [],
            "status_validacao": "em_analise",
        }

        # Validar credibilidade
        if resultados_gt.get("status") == "concluido":
            validacao["criterios_rigor"]["credibilidade"] = {
                "status": "adequado",
                "justificativa": "Processo sistemático e documentado",
            }
        else:
            validacao["criterios_rigor"]["credibilidade"] = {
                "status": "inadequado",
                "justificativa": "Processo não concluído adequadamente",
            }

        # Validar transferibilidade
        dados_analisados = (
            resultados_gt.get("resultados_parciais", {})
            .get("coleta_inicial", {})
            .get("dados_coletados", 0)
        )
        if dados_analisados > 0:
            validacao["criterios_rigor"]["transferibilidade"] = {
                "status": "adequado",
                "justificativa": f"Contexto bem descrito com {dados_analisados} registros",
            }
        else:
            validacao["criterios_rigor"]["transferibilidade"] = {
                "status": "inadequado",
                "justificativa": "Dados insuficientes para transferibilidade",
            }

        # Validar dependabilidade
        etapas_executadas = resultados_gt.get("etapas_executadas", [])
        if len(etapas_executadas) >= 3:
            validacao["criterios_rigor"]["dependabilidade"] = {
                "status": "adequado",
                "justificativa": f"Processo consistente com {len(etapas_executadas)} etapas",
            }
        else:
            validacao["criterios_rigor"]["dependabilidade"] = {
                "status": "inadequado",
                "justificativa": "Processo incompleto",
            }

        # Validar confirmabilidade
        teoria_final = resultados_gt.get("teoria_final", {})
        if teoria_final.get("fenomeno_central"):
            validacao["criterios_rigor"]["confirmabilidade"] = {
                "status": "adequado",
                "justificativa": "Resultados baseados nos dados coletados",
            }
        else:
            validacao["criterios_rigor"]["confirmabilidade"] = {
                "status": "inadequado",
                "justificativa": "Teoria não desenvolvida adequadamente",
            }

        # Identificar limites
        validacao["limites_identificados"] = [
            "Análise baseada em dados disponíveis via API",
            "Amostragem teórica limitada pelo contexto",
            "Necessidade de validação em outros contextos",
        ]

        # Gerar recomendações
        validacao["recomendacoes"] = [
            "Expandir análise para outros contextos educacionais",
            "Validar teoria em diferentes populações",
            "Implementar indicadores de monitoramento",
            "Desenvolver estratégias baseadas nos padrões identificados",
        ]

        # Definir status final
        criterios_adequados = sum(
            1
            for c in validacao["criterios_rigor"].values()
            if c["status"] == "adequado"
        )
        if criterios_adequados >= 3:
            validacao["status_validacao"] = "validado"
        else:
            validacao["status_validacao"] = "precisa_refinamento"

        self.workflow_status["etapas_concluidas"].append("validacao_resultados")
        self.workflow_status["etapa_atual"] = 4

        self.logger.info(f"✅ Validação concluída: {validacao['status_validacao']}")
        return validacao

    def gerar_relatorio_final(
        self, problema: Dict, metodologia: Dict, resultados_gt: Dict, validacao: Dict
    ) -> Dict:
        """
        📋 ETAPA 5: Gera relatório final do workflow.

        Args:
            problema: Definição do problema
            metodologia: Configuração metodológica
            resultados_gt: Resultados da Grounded Theory
            validacao: Validação dos resultados

        Returns:
            Relatório final
        """
        self.logger.info("📋 ETAPA 5: GERANDO RELATÓRIO FINAL")

        relatorio_final = {
            "workflow": "Grounded Theory - Workflow Lógico",
            "timestamp_inicio": datetime.now().isoformat(),
            "problema_pesquisa": problema,
            "metodologia": metodologia,
            "resultados_grounded_theory": resultados_gt,
            "validacao": validacao,
            "status_workflow": "concluido",
            "timestamp_fim": datetime.now().isoformat(),
        }

        # Salvar relatório
        self.salvar_relatorio_final(relatorio_final)

        self.workflow_status["etapas_concluidas"].append("relatorio_final")
        self.workflow_status["etapa_atual"] = 5
        self.workflow_status["status_geral"] = "concluido"

        self.logger.info("✅ Relatório final gerado")
        return relatorio_final

    def salvar_relatorio_final(self, relatorio: Dict):
        """
        💾 Salva o relatório final.

        Args:
            relatorio: Relatório a ser salvo
        """
        os.makedirs("relatorios", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Salvar JSON
        caminho_json = f"relatorios/workflow_grounded_theory_{timestamp}.json"
        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2, default=str)

        # Gerar relatório Markdown
        relatorio_md = self.gerar_relatorio_markdown(relatorio)
        caminho_md = f"relatorio_workflow_grounded_theory_{timestamp}.md"

        with open(caminho_md, "w", encoding="utf-8") as f:
            f.write(relatorio_md)

        self.logger.info(f"💾 Relatório final salvo:")
        self.logger.info(f"   📄 JSON: {caminho_json}")
        self.logger.info(f"   📋 Markdown: {caminho_md}")

    def gerar_relatorio_markdown(self, relatorio: Dict) -> str:
        """
        📋 Gera relatório em Markdown.

        Args:
            relatorio: Relatório a ser convertido

        Returns:
            Relatório em Markdown
        """
        md = f"""# 🔄 RELATÓRIO FINAL - WORKFLOW GROUNDED THEORY

## 📋 RESUMO EXECUTIVO
- **Workflow**: Grounded Theory - Processo Lógico
- **Status**: {relatorio.get('status_workflow', 'N/A')}
- **Data Início**: {relatorio.get('timestamp_inicio', 'N/A')}
- **Data Fim**: {relatorio.get('timestamp_fim', 'N/A')}

## 🎯 PROBLEMA DE PESQUISA

### Pergunta Central
{relatorio.get('problema_pesquisa', {}).get('pergunta_central', 'N/A')}

### Objetivo
{relatorio.get('problema_pesquisa', {}).get('objetivo', 'N/A')}

### Contexto
{relatorio.get('problema_pesquisa', {}).get('contexto', 'N/A')}

### Questões Específicas
"""

        questoes = relatorio.get("problema_pesquisa", {}).get(
            "questoes_especificas", []
        )
        for i, questao in enumerate(questoes, 1):
            md += f"{i}. {questao}\n"

        md += f"""
## ⚙️ METODOLOGIA

### Abordagem
- **Metodologia**: {relatorio.get('metodologia', {}).get('metodologia', 'N/A')}
- **Abordagem**: {relatorio.get('metodologia', {}).get('abordagem', 'N/A')}
- **Paradigma**: {relatorio.get('metodologia', {}).get('paradigma', 'N/A')}

### Etapas Metodológicas
"""

        etapas = relatorio.get("metodologia", {}).get("etapas_metodologicas", [])
        for i, etapa in enumerate(etapas, 1):
            md += f"{i}. {etapa}\n"

        md += f"""
### Critérios de Rigor
"""

        criterios = relatorio.get("metodologia", {}).get("criterios_rigor", [])
        for criterio in criterios:
            md += f"- {criterio}\n"

        md += f"""
## 🧠 RESULTADOS DA GROUNDED THEORY

### Status do Processo
- **Status**: {relatorio.get('resultados_grounded_theory', {}).get('status', 'N/A')}
- **Iterações Realizadas**: {relatorio.get('resultados_grounded_theory', {}).get('iteracoes_realizadas', 0)}
- **Saturação Atingida**: {relatorio.get('resultados_grounded_theory', {}).get('saturacao_atingida', False)}

### Etapas Executadas
"""

        etapas_executadas = relatorio.get("resultados_grounded_theory", {}).get(
            "etapas_executadas", []
        )
        for etapa in etapas_executadas:
            md += f"- {etapa}\n"

        md += f"""
### Teoria Desenvolvida
"""

        teoria = relatorio.get("resultados_grounded_theory", {}).get("teoria_final", {})
        md += f"""
#### Fenômeno Central
{teoria.get('fenomeno_central', 'Não identificado')}

#### Categorias Principais
"""

        categorias = teoria.get("categorias_principais", [])
        for i, categoria in enumerate(categorias, 1):
            md += f"{i}. **{categoria}**\n"

        md += f"""
#### Proposições Teóricas
"""

        proposicoes = teoria.get("proposicoes_teoricas", [])
        for i, prop in enumerate(proposicoes, 1):
            md += f"{i}. {prop}\n"

        md += f"""
## ✅ VALIDAÇÃO DOS RESULTADOS

### Status da Validação
- **Status**: {relatorio.get('validacao', {}).get('status_validacao', 'N/A')}

### Critérios de Rigor
"""

        criterios_rigor = relatorio.get("validacao", {}).get("criterios_rigor", {})
        for criterio, info in criterios_rigor.items():
            md += f"""
#### {criterio.title()}
- **Status**: {info.get('status', 'N/A')}
- **Justificativa**: {info.get('justificativa', 'N/A')}
"""

        md += f"""
### Limites Identificados
"""

        limites = relatorio.get("validacao", {}).get("limites_identificados", [])
        for limite in limites:
            md += f"- {limite}\n"

        md += f"""
### Recomendações
"""

        recomendacoes = relatorio.get("validacao", {}).get("recomendacoes", [])
        for i, rec in enumerate(recomendacoes, 1):
            md += f"{i}. {rec}\n"

        md += f"""
## 🎯 CONCLUSÕES E IMPLICAÇÕES

### Principais Descobertas
1. **Teoria Fundamentada**: Desenvolvida baseada nos dados coletados
2. **Padrões Identificados**: {len(categorias)} categorias principais
3. **Fenômeno Central**: {teoria.get('fenomeno_central', 'Não identificado')}
4. **Proposições**: {len(proposicoes)} proposições teóricas desenvolvidas

### Implicações para Pesquisa
- Base sólida para pesquisas futuras
- Metodologia replicável em outros contextos
- Insights para desenvolvimento de teorias

### Implicações para Políticas Públicas
- Evidências para tomada de decisões
- Base para indicadores de monitoramento
- Direcionamento para políticas educacionais

### Implicações para Prática
- Aplicação dos insights em desenvolvimento de cursos
- Consideração dos elementos identificados no planejamento
- Melhoria na abordagem de DEIA

---
*Relatório gerado automaticamente pelo Orquestrador Grounded Theory UNA-SUS*
"""

        return md

    def executar_workflow_completo(self) -> Dict:
        """
        🚀 Executa o workflow completo da Grounded Theory.

        Returns:
            Resultados completos do workflow
        """
        self.logger.info("🚀 INICIANDO WORKFLOW COMPLETO DA GROUNDED THEORY")

        try:
            # ETAPA 1: Definir problema de pesquisa
            self.logger.info("🎯 ETAPA 1: Definindo problema de pesquisa")
            problema = self.definir_problema_pesquisa()

            # ETAPA 2: Configurar metodologia
            self.logger.info("⚙️ ETAPA 2: Configurando metodologia")
            metodologia = self.configurar_metodologia()

            # ETAPA 3: Executar Grounded Theory
            self.logger.info("🧠 ETAPA 3: Executando Grounded Theory")
            resultados_gt = self.executar_grounded_theory()

            # ETAPA 4: Validar resultados
            self.logger.info("✅ ETAPA 4: Validando resultados")
            validacao = self.validar_resultados(resultados_gt)

            # ETAPA 5: Gerar relatório final
            self.logger.info("📋 ETAPA 5: Gerando relatório final")
            relatorio_final = self.gerar_relatorio_final(
                problema, metodologia, resultados_gt, validacao
            )

            self.logger.info("✅ WORKFLOW COMPLETO FINALIZADO COM SUCESSO")
            return relatorio_final

        except Exception as e:
            self.logger.error(f"❌ Erro no workflow: {str(e)}")
            return {
                "status_workflow": "erro",
                "erro": str(e),
                "etapas_concluidas": self.workflow_status["etapas_concluidas"],
            }

    def mostrar_status_workflow(self):
        """
        📊 Mostra status atual do workflow.
        """
        print("\n" + "=" * 60)
        print("📊 STATUS DO WORKFLOW GROUNDED THEORY")
        print("=" * 60)

        print(f"🔄 Status Geral: {self.workflow_status['status_geral']}")
        print(f"📋 Etapa Atual: {self.workflow_status['etapa_atual']}")

        print(f"\n✅ Etapas Concluídas:")
        for etapa in self.workflow_status["etapas_concluidas"]:
            print(f"   - {etapa}")

        print(f"\n⏳ Etapas Pendentes:")
        etapas_totais = [
            "definicao_problema",
            "configuracao_metodologia",
            "grounded_theory",
            "validacao_resultados",
            "relatorio_final",
        ]

        for etapa in etapas_totais:
            if etapa not in self.workflow_status["etapas_concluidas"]:
                print(f"   - {etapa}")

        print("=" * 60)


def main():
    """
    🚀 Função principal.
    """
    print("🔄 ORQUESTRADOR GROUNDED THEORY - WORKFLOW LÓGICO")
    print("=" * 60)
    print("🎯 Processo rigoroso e sequencial")
    print("=" * 60)

    orquestrador = OrquestradorGroundedTheory()

    # Executar workflow completo
    resultados = orquestrador.executar_workflow_completo()

    if resultados.get("status_workflow") == "concluido":
        print("\n✅ WORKFLOW CONCLUÍDO COM SUCESSO!")
        print(f"📋 Relatório final gerado")
        print(
            f"🧠 Teoria desenvolvida: {resultados.get('resultados_grounded_theory', {}).get('teoria_final', {}).get('fenomeno_central', 'N/A')}"
        )
        print(
            f"✅ Validação: {resultados.get('validacao', {}).get('status_validacao', 'N/A')}"
        )
    else:
        print(f"\n❌ ERRO NO WORKFLOW: {resultados.get('erro', 'Desconhecido')}")
        orquestrador.mostrar_status_workflow()


if __name__ == "__main__":
    main()
