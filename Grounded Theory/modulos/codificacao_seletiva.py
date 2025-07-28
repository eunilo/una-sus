#!/usr/bin/env python3
"""
🎯 Módulo de Codificação Seletiva - Grounded Theory
===================================================

Este módulo implementa a quarta etapa da Grounded Theory: Codificação Seletiva.
Responsável por integrar categorias em uma teoria unificada.

🎯 FUNCIONALIDADES:
- Integração de categorias
- Desenvolvimento da teoria
- Identificação do fenômeno central
- Construção do modelo teórico
- Validação da teoria

🔬 METODOLOGIA:
- Integração teórica
- Fenômeno central
- Modelo teórico
- Validação
- Saturação teórica
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Set


class CodificacaoSeletiva:
    """
    🎯 Codificação Seletiva para Grounded Theory

    Implementa integração de categorias em uma teoria unificada.
    """

    def __init__(self, logger: logging.Logger):
        """
        Inicializa o codificador seletivo.

        Args:
            logger: Logger para acompanhamento
        """
        self.logger = logger
        self.fenomeno_central = None
        self.modelo_teorico = {}
        self.categorias_integradas = {}
        self.relacoes_principais = {}
        self.teoria_final = {}

    def codificar_seletiva(self, dados_aberta: Dict, dados_axial: Dict) -> Dict:
        """
        🎯 Realiza codificação seletiva dos dados.

        Args:
            dados_aberta: Resultados da codificação aberta
            dados_axial: Resultados da codificação axial

        Returns:
            Dicionário com resultados da codificação seletiva
        """
        self.logger.info("🎯 INICIANDO CODIFICAÇÃO SELETIVA")

        resultados = {
            "fenomeno_central": None,
            "modelo_teorico": {},
            "categorias_integradas": {},
            "relacoes_principais": {},
            "teoria_final": {},
            "memos_analiticos": [],
            "estatisticas": {},
        }

        # Identificar fenômeno central
        self._identificar_fenomeno_central(dados_aberta, dados_axial)

        # Integrar categorias
        self._integrar_categorias(dados_aberta, dados_axial)

        # Desenvolver modelo teórico
        self._desenvolver_modelo_teorico()

        # Estabelecer relações principais
        self._estabelecer_relacoes_principais()

        # Construir teoria final
        self._construir_teoria_final()

        # Criar memos analíticos
        self._criar_memos_analiticos()

        # Calcular estatísticas
        resultados["estatisticas"] = self._calcular_estatisticas()

        self.logger.info("✅ CODIFICAÇÃO SELETIVA CONCLUÍDA")
        return resultados

    def _identificar_fenomeno_central(self, dados_aberta: Dict, dados_axial: Dict):
        """
        🎯 Identifica o fenômeno central da teoria.

        Args:
            dados_aberta: Resultados da codificação aberta
            dados_axial: Resultados da codificação axial
        """
        self.logger.info("🎯 Identificando fenômeno central...")

        # Extrair fenômeno central da codificação axial
        paradigma = dados_axial.get("paradigma_codificacao", {})
        fenomenos_centrais = paradigma.get("fenomeno_central", [])

        if fenomenos_centrais:
            self.fenomeno_central = fenomenos_centrais[0]
            self.logger.info(
                f"🎯 Fenômeno central identificado: {self.fenomeno_central}"
            )
        else:
            # Identificar baseado na frequência de conceitos
            conceitos = dados_aberta.get("conceitos_identificados", {})
            if conceitos:
                conceito_mais_frequente = max(
                    conceitos.items(), key=lambda x: x[1]["frequencia"]
                )[0]
                self.fenomeno_central = conceito_mais_frequente
                self.logger.info(
                    f"🎯 Fenômeno central por frequência: {self.fenomeno_central}"
                )

    def _integrar_categorias(self, dados_aberta: Dict, dados_axial: Dict):
        """
        🔗 Integra categorias em torno do fenômeno central.

        Args:
            dados_aberta: Resultados da codificação aberta
            dados_axial: Resultados da codificação axial
        """
        self.logger.info("🔗 Integrando categorias...")

        categorias_integradas = {
            "fenomeno_central": self.fenomeno_central,
            "categorias_principais": {},
            "subcategorias": {},
            "propriedades": {},
        }

        # Integrar categorias da codificação aberta
        categorias_aberta = dados_aberta.get("categorias_iniciais", {})
        for categoria, conceitos in categorias_aberta.items():
            if self._categoria_relevante_para_fenomeno(categoria, conceitos):
                categorias_integradas["categorias_principais"][categoria] = {
                    "conceitos": conceitos,
                    "relevancia": "alta",
                    "relacao_com_fenomeno": "direta",
                }

        # Integrar elementos da codificação axial
        paradigma = dados_axial.get("paradigma_codificacao", {})
        for elemento, conceitos in paradigma.items():
            if elemento != "fenomeno_central" and conceitos:
                categorias_integradas["subcategorias"][elemento] = {
                    "conceitos": conceitos,
                    "tipo": elemento,
                    "relacao_com_fenomeno": self._determinar_relacao(elemento),
                }

        self.categorias_integradas = categorias_integradas

        self.logger.info(
            f"🔗 Categorias integradas: {len(categorias_integradas['categorias_principais'])} principais"
        )

    def _categoria_relevante_para_fenomeno(
        self, categoria: str, conceitos: List[str]
    ) -> bool:
        """
        🔍 Verifica se categoria é relevante para o fenômeno central.

        Args:
            categoria: Nome da categoria
            conceitos: Lista de conceitos da categoria

        Returns:
            True se relevante, False caso contrário
        """
        if not self.fenomeno_central:
            return True

        # Verificar se há conceitos relacionados ao fenômeno central
        for conceito in conceitos:
            if self.fenomeno_central.lower() in conceito.lower():
                return True

        # Verificar se a categoria tem alta frequência
        return len(conceitos) > 2

    def _determinar_relacao(self, elemento: str) -> str:
        """
        🔗 Determina relação do elemento com o fenômeno central.

        Args:
            elemento: Elemento do paradigma

        Returns:
            Tipo de relação
        """
        relacoes = {
            "condicoes_causais": "causal",
            "contexto": "contextual",
            "condicoes_intervenientes": "interveniente",
            "estrategias_de_acao": "intervencao",
            "consequencias": "consequencial",
        }

        return relacoes.get(elemento, "indireta")

    def _desenvolver_modelo_teorico(self):
        """
        🏗️ Desenvolve o modelo teórico integrado.
        """
        self.logger.info("🏗️ Desenvolvendo modelo teórico...")

        modelo = {
            "fenomeno_central": self.fenomeno_central,
            "estrutura": {
                "condicoes_causais": [],
                "contexto": [],
                "estrategias": [],
                "consequencias": [],
            },
            "relacoes": {},
            "propriedades": {},
        }

        # Estruturar modelo baseado nas categorias integradas
        if "subcategorias" in self.categorias_integradas:
            for elemento, info in self.categorias_integradas["subcategorias"].items():
                if elemento in modelo["estrutura"]:
                    modelo["estrutura"][elemento] = info["conceitos"]

        # Adicionar categorias principais
        if "categorias_principais" in self.categorias_integradas:
            for categoria, info in self.categorias_integradas[
                "categorias_principais"
            ].items():
                modelo["propriedades"][categoria] = info

        self.modelo_teorico = modelo

        self.logger.info("🏗️ Modelo teórico desenvolvido")

    def _estabelecer_relacoes_principais(self):
        """
        🔗 Estabelece relações principais entre elementos.
        """
        self.logger.info("🔗 Estabelecendo relações principais...")

        relacoes = {}

        # Relações baseadas no paradigma
        estrutura = self.modelo_teorico.get("estrutura", {})

        # Condições causais → Fenômeno central
        if estrutura.get("condicoes_causais"):
            relacoes["causa_efeito"] = {
                "tipo": "causal",
                "origem": "condicoes_causais",
                "destino": "fenomeno_central",
                "forca": "forte",
            }

        # Fenômeno central → Estratégias
        if estrutura.get("estrategias"):
            relacoes["fenomeno_estrategia"] = {
                "tipo": "intervencao",
                "origem": "fenomeno_central",
                "destino": "estrategias",
                "forca": "media",
            }

        # Estratégias → Consequências
        if estrutura.get("estrategias") and estrutura.get("consequencias"):
            relacoes["estrategia_consequencia"] = {
                "tipo": "resultado",
                "origem": "estrategias",
                "destino": "consequencias",
                "forca": "forte",
            }

        # Contexto → Fenômeno central
        if estrutura.get("contexto"):
            relacoes["contexto_fenomeno"] = {
                "tipo": "contextual",
                "origem": "contexto",
                "destino": "fenomeno_central",
                "forca": "media",
            }

        self.relacoes_principais = relacoes

        self.logger.info(f"🔗 Relações estabelecidas: {len(relacoes)}")

    def _construir_teoria_final(self):
        """
        🎯 Constrói a teoria final integrada.
        """
        self.logger.info("🎯 Construindo teoria final...")

        teoria = {
            "titulo": f"Teoria sobre {self.fenomeno_central}",
            "fenomeno_central": self.fenomeno_central,
            "modelo_teorico": self.modelo_teorico,
            "relacoes_principais": self.relacoes_principais,
            "categorias_integradas": self.categorias_integradas,
            "resumo_teorico": self._gerar_resumo_teorico(),
            "implicacoes": self._gerar_implicacoes(),
            "limitacoes": self._identificar_limitacoes(),
            "timestamp": datetime.now().isoformat(),
        }

        self.teoria_final = teoria

        self.logger.info("🎯 Teoria final construída")

    def _gerar_resumo_teorico(self) -> str:
        """
        📝 Gera resumo da teoria desenvolvida.

        Returns:
            Resumo da teoria
        """
        resumo = (
            f"A teoria desenvolvida centra-se no fenômeno '{self.fenomeno_central}'. "
        )

        estrutura = self.modelo_teorico.get("estrutura", {})

        if estrutura.get("condicoes_causais"):
            resumo += f"Este fenômeno é influenciado por condições causais como {', '.join(estrutura['condicoes_causais'][:3])}. "

        if estrutura.get("estrategias"):
            resumo += f"Estratégias de intervenção incluem {', '.join(estrutura['estrategias'][:3])}. "

        if estrutura.get("consequencias"):
            resumo += f"As consequências observadas são {', '.join(estrutura['consequencias'][:3])}. "

        return resumo

    def _gerar_implicacoes(self) -> List[str]:
        """
        💡 Gera implicações da teoria.

        Returns:
            Lista de implicações
        """
        implicacoes = []

        # Implicações práticas
        estrutura = self.modelo_teorico.get("estrutura", {})
        if estrutura.get("estrategias"):
            implicacoes.append(
                "Desenvolvimento de intervenções baseadas nas estratégias identificadas"
            )

        # Implicações teóricas
        if self.fenomeno_central:
            implicacoes.append(
                f"Contribuição para compreensão do fenômeno {self.fenomeno_central}"
            )

        # Implicações metodológicas
        implicacoes.append(
            "Validação da metodologia Grounded Theory para pesquisa em saúde"
        )

        return implicacoes

    def _identificar_limitacoes(self) -> List[str]:
        """
        ⚠️ Identifica limitações da teoria.

        Returns:
            Lista de limitações
        """
        limitacoes = []

        # Limitações baseadas nos dados
        if not self.fenomeno_central:
            limitacoes.append("Fenômeno central não claramente identificado")

        estrutura = self.modelo_teorico.get("estrutura", {})
        if not estrutura.get("consequencias"):
            limitacoes.append("Consequências não suficientemente exploradas")

        # Limitações metodológicas
        limitacoes.append("Necessidade de validação com dados adicionais")
        limitacoes.append("Possível influência do contexto específico dos dados")

        return limitacoes

    def _criar_memos_analiticos(self):
        """
        📝 Cria memos analíticos sobre a codificação seletiva.
        """
        self.logger.info("📝 Criando memos analíticos...")

        memos = []

        # Memo sobre fenômeno central
        if self.fenomeno_central:
            memo_fenomeno = {
                "tipo": "fenomeno_central",
                "titulo": "Fenômeno Central Identificado",
                "conteudo": f"Fenômeno central: {self.fenomeno_central}",
                "fenomeno": self.fenomeno_central,
                "timestamp": datetime.now().isoformat(),
            }
            memos.append(memo_fenomeno)

        # Memo sobre modelo teórico
        if self.modelo_teorico:
            memo_modelo = {
                "tipo": "modelo_teorico",
                "titulo": "Modelo Teórico Desenvolvido",
                "conteudo": f"Modelo com {len(self.modelo_teorico.get('estrutura', {}))} elementos estruturais",
                "modelo": self.modelo_teorico,
                "timestamp": datetime.now().isoformat(),
            }
            memos.append(memo_modelo)

        # Memo sobre teoria final
        if self.teoria_final:
            memo_teoria = {
                "tipo": "teoria_final",
                "titulo": "Teoria Final Construída",
                "conteudo": self.teoria_final.get("resumo_teorico", ""),
                "implicacoes": self.teoria_final.get("implicacoes", []),
                "timestamp": datetime.now().isoformat(),
            }
            memos.append(memo_teoria)

        self.memos_analiticos = memos

    def _calcular_estatisticas(self) -> Dict:
        """
        📊 Calcula estatísticas da codificação seletiva.

        Returns:
            Dicionário com estatísticas
        """
        estatisticas = {
            "fenomeno_central_identificado": self.fenomeno_central is not None,
            "categorias_principais": len(
                self.categorias_integradas.get("categorias_principais", {})
            ),
            "subcategorias": len(self.categorias_integradas.get("subcategorias", {})),
            "relacoes_estabelecidas": len(self.relacoes_principais),
            "memos_criados": len(self.memos_analiticos),
            "teoria_construida": bool(self.teoria_final),
        }

        return estatisticas

    def salvar_resultados(self, resultados: Dict, nome_arquivo: str = None):
        """
        💾 Salva resultados da codificação seletiva.

        Args:
            resultados: Resultados da codificação
            nome_arquivo: Nome do arquivo (opcional)
        """
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"codificacao_seletiva_{timestamp}.json"

        caminho = os.path.join("resultados", nome_arquivo)

        # Criar pasta se não existir
        os.makedirs("resultados", exist_ok=True)

        # Salvar resultados
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)

        self.logger.info(f"💾 Resultados salvos em: {caminho}")
