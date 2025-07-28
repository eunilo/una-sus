#!/usr/bin/env python3
"""
🔍 Módulo de Codificação Aberta - Grounded Theory
=================================================

Este módulo implementa a segunda etapa da Grounded Theory: Codificação Aberta.
Responsável por identificar conceitos básicos nos dados coletados.

🎯 FUNCIONALIDADES:
- Identificação de conceitos
- Extração de propriedades
- Categorização inicial
- Análise de frequência
- Geração de memos

🔬 METODOLOGIA:
- Codificação linha por linha
- Identificação de conceitos
- Comparação constante
- Memos analíticos
"""

import json
import logging
import os
import re
from collections import Counter
from datetime import datetime
from typing import Dict, List, Set


class CodificacaoAberta:
    """
    🔍 Codificação Aberta para Grounded Theory

    Implementa identificação de conceitos básicos nos dados coletados.
    """

    def __init__(self, logger: logging.Logger):
        """
        Inicializa o codificador aberto.

        Args:
            logger: Logger para acompanhamento
        """
        self.logger = logger
        self.conceitos_identificados = {}
        self.categorias_iniciais = {}
        self.memos_analiticos = []

    def codificar_dados(self, dados: List[Dict]) -> Dict:
        """
        🔍 Realiza codificação aberta dos dados.

        Args:
            dados: Dados coletados para codificação

        Returns:
            Dicionário com resultados da codificação
        """
        self.logger.info("🔍 INICIANDO CODIFICAÇÃO ABERTA")
        self.logger.info(f"📊 Dados para codificar: {len(dados)} registros")

        resultados = {
            "conceitos_identificados": {},
            "categorias_iniciais": {},
            "memos_analiticos": [],
            "estatisticas": {},
        }

        # Processar cada registro
        for i, registro in enumerate(dados):
            self.logger.info(f"🔍 Codificando registro {i+1}/{len(dados)}")

            # Codificar texto do registro
            conceitos_registro = self._codificar_texto(registro)

            # Adicionar ao dicionário de conceitos
            for conceito, contexto in conceitos_registro.items():
                if conceito not in self.conceitos_identificados:
                    self.conceitos_identificados[conceito] = {
                        "frequencia": 0,
                        "contextos": [],
                        "primeira_ocorrencia": registro.get("id", f"reg_{i}"),
                        "propriedades": set(),
                    }

                self.conceitos_identificados[conceito]["frequencia"] += 1
                self.conceitos_identificados[conceito]["contextos"].append(contexto)

        # Gerar categorias iniciais
        self._gerar_categorias_iniciais()

        # Criar memos analíticos
        self._criar_memos_analiticos()

        # Calcular estatísticas
        resultados["estatisticas"] = self._calcular_estatisticas()

        self.logger.info("✅ CODIFICAÇÃO ABERTA CONCLUÍDA")
        return resultados

    def _codificar_texto(self, registro: Dict) -> Dict[str, str]:
        """
        🔍 Codifica o texto de um registro.

        Args:
            registro: Registro individual

        Returns:
            Dicionário de conceitos identificados
        """
        conceitos = {}

        # Extrair texto do registro
        texto_completo = self._extrair_texto_registro(registro)

        # Identificar conceitos usando diferentes estratégias
        conceitos.update(self._identificar_conceitos_por_palavras_chave(texto_completo))
        conceitos.update(self._identificar_conceitos_por_padroes(texto_completo))
        conceitos.update(self._identificar_conceitos_por_frases(texto_completo))

        return conceitos

    def _extrair_texto_registro(self, registro: Dict) -> str:
        """
        📝 Extrai texto completo do registro.

        Args:
            registro: Registro individual

        Returns:
            Texto completo para análise
        """
        campos_texto = ["titulo", "descricao", "palavras_chave", "publico_alvo"]
        texto_completo = ""

        for campo in campos_texto:
            if campo in registro and registro[campo]:
                texto_completo += f" {registro[campo]}"

        return texto_completo.lower().strip()

    def _identificar_conceitos_por_palavras_chave(self, texto: str) -> Dict[str, str]:
        """
        🎯 Identifica conceitos por palavras-chave.

        Args:
            texto: Texto para análise

        Returns:
            Dicionário de conceitos identificados
        """
        conceitos = {}

        # Palavras-chave relacionadas a DEIA
        palavras_chave_deia = [
            "diversidade",
            "equidade",
            "inclusão",
            "acessibilidade",
            "saúde mental",
            "população negra",
            "indígena",
            "lgbtqi+",
            "pessoa com deficiência",
            "vulnerabilidade",
            "discriminação",
        ]

        for palavra in palavras_chave_deia:
            if palavra in texto:
                conceitos[palavra] = f"Palavra-chave DEIA: {palavra}"

        return conceitos

    def _identificar_conceitos_por_padroes(self, texto: str) -> Dict[str, str]:
        """
        🔍 Identifica conceitos por padrões de texto.

        Args:
            texto: Texto para análise

        Returns:
            Dicionário de conceitos identificados
        """
        conceitos = {}

        # Padrões para identificar conceitos
        padroes = [
            (r"saúde da (\w+)", "Saúde específica"),
            (r"população (\w+)", "População específica"),
            (r"(\w+) vulnerável", "Vulnerabilidade"),
            (r"(\w+) inclusivo", "Inclusão"),
            (r"(\w+) acessível", "Acessibilidade"),
        ]

        for padrao, tipo in padroes:
            matches = re.findall(padrao, texto)
            for match in matches:
                conceito = f"{tipo}: {match}"
                conceitos[conceito] = f"Padrão identificado: {padrao}"

        return conceitos

    def _identificar_conceitos_por_frases(self, texto: str) -> Dict[str, str]:
        """
        📝 Identifica conceitos por frases completas.

        Args:
            texto: Texto para análise

        Returns:
            Dicionário de conceitos identificados
        """
        conceitos = {}

        # Frases que indicam conceitos
        frases_conceito = [
            "direitos humanos",
            "cidadania",
            "justiça social",
            "determinantes sociais",
            "promoção da saúde",
            "prevenção",
            "cuidado integral",
        ]

        for frase in frases_conceito:
            if frase in texto:
                conceitos[frase] = f"Frase conceito: {frase}"

        return conceitos

    def _gerar_categorias_iniciais(self):
        """
        📊 Gera categorias iniciais baseadas nos conceitos identificados.
        """
        self.logger.info("📊 Gerando categorias iniciais...")

        # Agrupar conceitos por similaridade
        categorias = {
            "Saúde Específica": [],
            "Populações": [],
            "Conceitos DEIA": [],
            "Ações": [],
            "Contextos": [],
        }

        for conceito, info in self.conceitos_identificados.items():
            if any(
                termo in conceito.lower() for termo in ["saúde", "mental", "física"]
            ):
                categorias["Saúde Específica"].append(conceito)
            elif any(
                termo in conceito.lower() for termo in ["população", "pessoa", "grupo"]
            ):
                categorias["Populações"].append(conceito)
            elif any(
                termo in conceito.lower()
                for termo in ["diversidade", "equidade", "inclusão"]
            ):
                categorias["Conceitos DEIA"].append(conceito)
            elif any(
                termo in conceito.lower()
                for termo in ["ação", "intervenção", "programa"]
            ):
                categorias["Ações"].append(conceito)
            else:
                categorias["Contextos"].append(conceito)

        self.categorias_iniciais = categorias

        self.logger.info(f"📊 Categorias geradas: {list(categorias.keys())}")

    def _criar_memos_analiticos(self):
        """
        📝 Cria memos analíticos sobre a codificação.
        """
        self.logger.info("📝 Criando memos analíticos...")

        # Memo sobre conceitos mais frequentes
        conceitos_frequentes = sorted(
            self.conceitos_identificados.items(),
            key=lambda x: x[1]["frequencia"],
            reverse=True,
        )[:5]

        memo_frequencia = {
            "tipo": "frequencia_conceitos",
            "titulo": "Conceitos Mais Frequentes",
            "conteudo": f"Os conceitos mais frequentes são: {[c[0] for c in conceitos_frequentes]}",
            "timestamp": datetime.now().isoformat(),
        }

        # Memo sobre categorias
        memo_categorias = {
            "tipo": "categorias_iniciais",
            "titulo": "Categorias Iniciais Identificadas",
            "conteudo": f"Foram identificadas {len(self.categorias_iniciais)} categorias principais",
            "categorias": self.categorias_iniciais,
            "timestamp": datetime.now().isoformat(),
        }

        self.memos_analiticos = [memo_frequencia, memo_categorias]

    def _calcular_estatisticas(self) -> Dict:
        """
        📊 Calcula estatísticas da codificação.

        Returns:
            Dicionário com estatísticas
        """
        total_conceitos = len(self.conceitos_identificados)
        total_categorias = len(self.categorias_iniciais)

        # Conceito mais frequente
        conceito_mais_frequente = (
            max(self.conceitos_identificados.items(), key=lambda x: x[1]["frequencia"])
            if self.conceitos_identificados
            else None
        )

        estatisticas = {
            "total_conceitos": total_conceitos,
            "total_categorias": total_categorias,
            "conceito_mais_frequente": (
                conceito_mais_frequente[0] if conceito_mais_frequente else None
            ),
            "frequencia_maxima": (
                conceito_mais_frequente[1]["frequencia"]
                if conceito_mais_frequente
                else 0
            ),
            "memos_criados": len(self.memos_analiticos),
        }

        return estatisticas

    def salvar_resultados(self, resultados: Dict, nome_arquivo: str = None):
        """
        💾 Salva resultados da codificação.

        Args:
            resultados: Resultados da codificação
            nome_arquivo: Nome do arquivo (opcional)
        """
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"codificacao_aberta_{timestamp}.json"

        caminho = os.path.join("resultados", nome_arquivo)

        # Criar pasta se não existir
        os.makedirs("resultados", exist_ok=True)

        # Salvar resultados
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)

        self.logger.info(f"💾 Resultados salvos em: {caminho}")
