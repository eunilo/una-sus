#!/usr/bin/env python3
"""
🔗 Módulo de Codificação Axial - Grounded Theory
================================================

Este módulo implementa a terceira etapa da Grounded Theory: Codificação Axial.
Responsável por relacionar categorias e subcategorias.

🎯 FUNCIONALIDADES:
- Relacionamento entre categorias
- Identificação de condições
- Análise de consequências
- Estratégias de ação
- Paradigma de codificação

🔬 METODOLOGIA:
- Paradigma de Strauss e Corbin
- Condições causais
- Fenômeno central
- Contexto
- Estratégias de intervenção
- Consequências
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Set


class CodificacaoAxial:
    """
    🔗 Codificação Axial para Grounded Theory

    Implementa relacionamento entre categorias e subcategorias.
    """

    def __init__(self, logger: logging.Logger):
        """
        Inicializa o codificador axial.

        Args:
            logger: Logger para acompanhamento
        """
        self.logger = logger
        self.paradigma_codificacao = {}
        self.relacionamentos = {}
        self.condicoes_causais = {}
        self.consequencias = {}
        self.estrategias = {}

    def codificar_axial(self, dados_codificacao_aberta: Dict) -> Dict:
        """
        🔗 Realiza codificação axial dos dados.

        Args:
            dados_codificacao_aberta: Resultados da codificação aberta

        Returns:
            Dicionário com resultados da codificação axial
        """
        self.logger.info("🔗 INICIANDO CODIFICAÇÃO AXIAL")

        resultados = {
            "paradigma_codificacao": {},
            "relacionamentos": {},
            "condicoes_causais": {},
            "consequencias": {},
            "estrategias": {},
            "memos_analiticos": [],
            "estatisticas": {},
        }

        # Extrair conceitos e categorias da codificação aberta
        conceitos = dados_codificacao_aberta.get("conceitos_identificados", {})
        categorias = dados_codificacao_aberta.get("categorias_iniciais", {})

        # Aplicar paradigma de codificação
        self._aplicar_paradigma_codificacao(conceitos, categorias)

        # Identificar relacionamentos
        self._identificar_relacionamentos(conceitos, categorias)

        # Analisar condições causais
        self._analisar_condicoes_causais(conceitos)

        # Identificar consequências
        self._identificar_consequencias(conceitos)

        # Desenvolver estratégias
        self._desenvolver_estrategias(conceitos, categorias)

        # Criar memos analíticos
        self._criar_memos_analiticos()

        # Calcular estatísticas
        resultados["estatisticas"] = self._calcular_estatisticas()

        self.logger.info("✅ CODIFICAÇÃO AXIAL CONCLUÍDA")
        return resultados

    def _aplicar_paradigma_codificacao(self, conceitos: Dict, categorias: Dict):
        """
        🎯 Aplica o paradigma de codificação de Strauss e Corbin.

        Args:
            conceitos: Conceitos identificados
            categorias: Categorias iniciais
        """
        self.logger.info("🎯 Aplicando paradigma de codificação...")

        paradigma = {
            "condicoes_causais": [],
            "fenomeno_central": [],
            "contexto": [],
            "condicoes_intervenientes": [],
            "estrategias_de_acao": [],
            "consequencias": [],
        }

        # Identificar fenômeno central (mais frequente)
        conceitos_frequentes = sorted(
            conceitos.items(), key=lambda x: x[1]["frequencia"], reverse=True
        )

        if conceitos_frequentes:
            fenomeno_central = conceitos_frequentes[0][0]
            paradigma["fenomeno_central"].append(fenomeno_central)
            self.logger.info(f"🎯 Fenômeno central identificado: {fenomeno_central}")

        # Classificar outros conceitos
        for conceito, info in conceitos.items():
            if conceito in paradigma["fenomeno_central"]:
                continue

            # Classificar baseado no conteúdo
            if any(termo in conceito.lower() for termo in ["causa", "origem", "fator"]):
                paradigma["condicoes_causais"].append(conceito)
            elif any(
                termo in conceito.lower()
                for termo in ["contexto", "ambiente", "situação"]
            ):
                paradigma["contexto"].append(conceito)
            elif any(
                termo in conceito.lower()
                for termo in ["intervenção", "ação", "programa"]
            ):
                paradigma["estrategias_de_acao"].append(conceito)
            elif any(
                termo in conceito.lower()
                for termo in ["resultado", "efeito", "impacto"]
            ):
                paradigma["consequencias"].append(conceito)
            else:
                paradigma["condicoes_intervenientes"].append(conceito)

        self.paradigma_codificacao = paradigma

        self.logger.info(f"🎯 Paradigma aplicado: {len(paradigma)} elementos")

    def _identificar_relacionamentos(self, conceitos: Dict, categorias: Dict):
        """
        🔗 Identifica relacionamentos entre conceitos.

        Args:
            conceitos: Conceitos identificados
            categorias: Categorias iniciais
        """
        self.logger.info("🔗 Identificando relacionamentos...")

        relacionamentos = {}

        # Relacionamentos por categoria
        for categoria, conceitos_categoria in categorias.items():
            if len(conceitos_categoria) > 1:
                relacionamentos[categoria] = {
                    "tipo": "intra_categoria",
                    "conceitos": conceitos_categoria,
                    "forca_relacionamento": "alta",
                }

        # Relacionamentos entre categorias
        categorias_lista = list(categorias.keys())
        for i, cat1 in enumerate(categorias_lista):
            for cat2 in categorias_lista[i + 1 :]:
                chave_relacionamento = f"{cat1}_x_{cat2}"
                relacionamentos[chave_relacionamento] = {
                    "tipo": "inter_categoria",
                    "categoria1": cat1,
                    "categoria2": cat2,
                    "forca_relacionamento": "media",
                }

        self.relacionamentos = relacionamentos

        self.logger.info(f"🔗 Relacionamentos identificados: {len(relacionamentos)}")

    def _analisar_condicoes_causais(self, conceitos: Dict):
        """
        🔍 Analisa condições causais dos fenômenos.

        Args:
            conceitos: Conceitos identificados
        """
        self.logger.info("🔍 Analisando condições causais...")

        condicoes = {}

        # Identificar condições causais baseadas em frequência
        conceitos_frequentes = [
            conceito
            for conceito, info in conceitos.items()
            if info["frequencia"] > 5  # Mais de 5 ocorrências
        ]

        for conceito in conceitos_frequentes:
            condicoes[conceito] = {
                "tipo": "condicao_causal",
                "frequencia": conceitos[conceito]["frequencia"],
                "contextos": conceitos[conceito]["contextos"],
                "intensidade": (
                    "alta" if conceitos[conceito]["frequencia"] > 10 else "media"
                ),
            }

        self.condicoes_causais = condicoes

        self.logger.info(f"🔍 Condições causais identificadas: {len(condicoes)}")

    def _identificar_consequencias(self, conceitos: Dict):
        """
        📊 Identifica consequências dos fenômenos.

        Args:
            conceitos: Conceitos identificados
        """
        self.logger.info("📊 Identificando consequências...")

        consequencias = {}

        # Identificar consequências baseadas em padrões
        for conceito, info in conceitos.items():
            if any(
                termo in conceito.lower()
                for termo in ["resultado", "efeito", "impacto", "mudança"]
            ):
                consequencias[conceito] = {
                    "tipo": "consequencia",
                    "frequencia": info["frequencia"],
                    "contextos": info["contextos"],
                    "natureza": (
                        "positiva" if "melhoria" in conceito.lower() else "neutra"
                    ),
                }

        self.consequencias = consequencias

        self.logger.info(f"📊 Consequências identificadas: {len(consequencias)}")

    def _desenvolver_estrategias(self, conceitos: Dict, categorias: Dict):
        """
        🎯 Desenvolve estratégias de ação/intervenção.

        Args:
            conceitos: Conceitos identificados
            categorias: Categorias iniciais
        """
        self.logger.info("🎯 Desenvolvendo estratégias...")

        estrategias = {}

        # Identificar estratégias baseadas em conceitos de ação
        for conceito, info in conceitos.items():
            if any(
                termo in conceito.lower()
                for termo in ["ação", "intervenção", "programa", "estratégia"]
            ):
                estrategias[conceito] = {
                    "tipo": "estrategia_acao",
                    "frequencia": info["frequencia"],
                    "contextos": info["contextos"],
                    "viabilidade": "alta" if info["frequencia"] > 3 else "media",
                }

        # Estratégias baseadas em categorias
        if "Ações" in categorias:
            for acao in categorias["Ações"]:
                if acao not in estrategias:
                    estrategias[acao] = {
                        "tipo": "estrategia_categoria",
                        "categoria_origem": "Ações",
                        "viabilidade": "media",
                    }

        self.estrategias = estrategias

        self.logger.info(f"🎯 Estratégias desenvolvidas: {len(estrategias)}")

    def _criar_memos_analiticos(self):
        """
        📝 Cria memos analíticos sobre a codificação axial.
        """
        self.logger.info("📝 Criando memos analíticos...")

        memos = []

        # Memo sobre paradigma
        if self.paradigma_codificacao:
            memo_paradigma = {
                "tipo": "paradigma_codificacao",
                "titulo": "Paradigma de Codificação Identificado",
                "conteudo": f"Fenômeno central: {self.paradigma_codificacao.get('fenomeno_central', [])}",
                "paradigma": self.paradigma_codificacao,
                "timestamp": datetime.now().isoformat(),
            }
            memos.append(memo_paradigma)

        # Memo sobre relacionamentos
        if self.relacionamentos:
            memo_relacionamentos = {
                "tipo": "relacionamentos",
                "titulo": "Relacionamentos Identificados",
                "conteudo": f"Total de relacionamentos: {len(self.relacionamentos)}",
                "relacionamentos": self.relacionamentos,
                "timestamp": datetime.now().isoformat(),
            }
            memos.append(memo_relacionamentos)

        # Memo sobre estratégias
        if self.estrategias:
            estrategias_viaveis = [
                nome
                for nome, info in self.estrategias.items()
                if info.get("viabilidade") == "alta"
            ]

            memo_estrategias = {
                "tipo": "estrategias_viaveis",
                "titulo": "Estratégias Mais Viáveis",
                "conteudo": f"Estratégias de alta viabilidade: {estrategias_viaveis}",
                "estrategias": estrategias_viaveis,
                "timestamp": datetime.now().isoformat(),
            }
            memos.append(memo_estrategias)

        self.memos_analiticos = memos

    def _calcular_estatisticas(self) -> Dict:
        """
        📊 Calcula estatísticas da codificação axial.

        Returns:
            Dicionário com estatísticas
        """
        estatisticas = {
            "total_relacionamentos": len(self.relacionamentos),
            "total_condicoes_causais": len(self.condicoes_causais),
            "total_consequencias": len(self.consequencias),
            "total_estrategias": len(self.estrategias),
            "memos_criados": len(self.memos_analiticos),
        }

        # Estatísticas do paradigma
        if self.paradigma_codificacao:
            for categoria, elementos in self.paradigma_codificacao.items():
                estatisticas[f"paradigma_{categoria}"] = len(elementos)

        return estatisticas

    def salvar_resultados(self, resultados: Dict, nome_arquivo: str = None):
        """
        💾 Salva resultados da codificação axial.

        Args:
            resultados: Resultados da codificação
            nome_arquivo: Nome do arquivo (opcional)
        """
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"codificacao_axial_{timestamp}.json"

        caminho = os.path.join("resultados", nome_arquivo)

        # Criar pasta se não existir
        os.makedirs("resultados", exist_ok=True)

        # Salvar resultados
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)

        self.logger.info(f"💾 Resultados salvos em: {caminho}")
