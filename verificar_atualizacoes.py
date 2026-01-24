#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Verificador de Atualizações - Sistema UNA-SUS
================================================

Script para verificar se há novas ofertas e atualizar o sistema.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List

import pandas as pd
import requests

# Garantir execução a partir da raiz do projeto e usar venv, se existir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
    venv_python = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        os.execv(venv_python, [venv_python, *sys.argv])


def verificar_dados_atuais() -> Dict:
    """Verifica os dados atuais coletados."""
    print("[*] Verificando dados atuais...")

    # Procurar arquivo CSV mais recente
    data_dir = "data"
    if not os.path.exists(data_dir):
        return {"existe": False}

    csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    if not csv_files:
        return {"existe": False}

    # Pegar o mais recente
    csv_files.sort(
        key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), reverse=True
    )
    arquivo_mais_recente = os.path.join(data_dir, csv_files[0])

    try:
        df = pd.read_csv(arquivo_mais_recente)
        data_modificacao = datetime.fromtimestamp(
            os.path.getmtime(arquivo_mais_recente)
        )

        return {
            "existe": True,
            "arquivo": arquivo_mais_recente,
            "total_registros": len(df),
            "data_coleta": data_modificacao.strftime("%d/%m/%Y %H:%M:%S"),
            "cursos_unicos": (
                df.get("no_curso", pd.Series()).nunique()
                if "no_curso" in df.columns
                else 0
            ),
            "ofertas_unicas": (
                df.get("id_oferta", pd.Series()).nunique()
                if "id_oferta" in df.columns
                else 0
            ),
        }
    except Exception as e:
        print(f"[!] Erro ao ler arquivo: {e}")
        return {"existe": False, "erro": str(e)}


def verificar_api_unasus() -> Dict:
    """Verifica a API UNA-SUS para ver se há novas ofertas."""
    print("[*] Verificando API UNA-SUS...")

    url_base = "https://www.unasus.gov.br/cursos/rest/busca"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.unasus.gov.br",
        "Referer": (
            "https://www.unasus.gov.br/cursos/busca?"
            "status=todos&busca=&ordenacao=Relev%C3%A2ncia%20na%20busca"
        ),
    }

    cookies = {
        "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
        "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
    }

    payload = {
        "busca": "",
        "ordenacao": "Por nome",
        "status": "Todos",
        "proximo": 0,
    }

    try:
        response = requests.post(
            url_base,
            data=payload,
            headers=headers,
            cookies=cookies,
            timeout=30,
        )

        if response.status_code != 200:
            return {
                "sucesso": False,
                "erro": f"Status HTTP {response.status_code}",
            }

        data = response.json()
        results = data.get("results", {})
        itens = results.get("itens", [])

        # Contar total de páginas (estimativa)
        total_itens = results.get("total", 0)
        itens_por_pagina = len(itens) if itens else 20

        return {
            "sucesso": True,
            "total_estimado": total_itens,
            "itens_primeira_pagina": len(itens),
            "itens_por_pagina": itens_por_pagina,
            "paginas_estimadas": (
                (total_itens // itens_por_pagina) + 1 if itens_por_pagina > 0 else 0
            ),
        }

    except Exception as e:
        return {
            "sucesso": False,
            "erro": str(e),
        }


def comparar_dados(dados_atuais: Dict, dados_api: Dict) -> Dict:
    """Compara dados atuais com dados da API."""
    print("[*] Comparando dados...")

    if not dados_atuais.get("existe"):
        return {
            "atualizacao_necesaria": True,
            "motivo": "Nenhum dado coletado anteriormente",
        }

    if not dados_api.get("sucesso"):
        return {
            "atualizacao_necesaria": False,
            "motivo": f"Erro ao verificar API: {dados_api.get('erro')}",
        }

    total_atual = dados_atuais.get("total_registros", 0)
    total_api = dados_api.get("total_estimado", 0)

    diferenca = total_api - total_atual

    return {
        "atualizacao_necesaria": diferenca > 0,
        "total_atual": total_atual,
        "total_api": total_api,
        "diferenca": diferenca,
        "percentual_diferenca": (
            (diferenca / total_atual * 100) if total_atual > 0 else 0
        ),
        "motivo": (
            f"API tem {diferenca} registros a mais"
            if diferenca > 0
            else "Dados estão atualizados"
        ),
    }


def executar_coleta():
    """Executa a coleta completa de dados."""
    print("[*] Executando coleta completa...")
    print("[*] Isso pode levar varios minutos...")

    try:
        from coletor_database_geral import ColetorDatabaseGeral

        coletor = ColetorDatabaseGeral()
        dados = coletor.coletar_dados_completos()

        return {
            "sucesso": True,
            "total_coletado": len(dados),
        }
    except Exception as e:
        return {
            "sucesso": False,
            "erro": str(e),
        }


def executar_analise():
    """Executa análise completa dos dados."""
    print("[*] Executando analise completa...")

    try:
        from analise.analisador_geral import AnalisadorGeral
        from analise.relatorios import (
            gerar_relatorios_visuais,
            salvar_relatorio_json,
            salvar_relatorio_texto,
        )

        analisador = AnalisadorGeral()

        if not analisador.carregar_dados():
            return {"sucesso": False, "erro": "Não foi possível carregar dados"}

        relatorio = analisador.gerar_relatorio_completo()

        # Salvar relatórios
        arquivo_json = salvar_relatorio_json(relatorio)
        arquivo_txt = salvar_relatorio_texto(relatorio)

        # Gerar relatórios visuais
        arquivos_visuais = gerar_relatorios_visuais(relatorio, analisador.dados)

        return {
            "sucesso": True,
            "relatorio_json": arquivo_json,
            "relatorio_txt": arquivo_txt,
            "relatorios_visuais": len(arquivos_visuais),
        }
    except Exception as e:
        return {
            "sucesso": False,
            "erro": str(e),
        }


def main():
    """Função principal."""
    import io

    # Configurar encoding UTF-8 para Windows
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace"
        )

    print("=" * 70)
    print("VERIFICADOR DE ATUALIZACOES - SISTEMA UNA-SUS")
    print("=" * 70)
    print()

    # 1. Verificar dados atuais
    dados_atuais = verificar_dados_atuais()

    if dados_atuais.get("existe"):
        print(f"[OK] Dados atuais encontrados:")
        print(f"     Arquivo: {dados_atuais['arquivo']}")
        print(f"     Total de registros: {dados_atuais['total_registros']:,}")
        print(f"     Cursos unicos: {dados_atuais['cursos_unicos']}")
        print(f"     Ofertas unicas: {dados_atuais['ofertas_unicas']}")
        print(f"     Data da coleta: {dados_atuais['data_coleta']}")
    else:
        print("[!] Nenhum dado coletado anteriormente")

    print()

    # 2. Verificar API
    dados_api = verificar_api_unasus()

    if dados_api.get("sucesso"):
        print(f"[OK] API UNA-SUS acessivel:")
        print(f"     Total estimado: {dados_api['total_estimado']:,}")
        print(f"     Itens na primeira pagina: {dados_api['itens_primeira_pagina']}")
        print(f"     Paginas estimadas: {dados_api['paginas_estimadas']}")
    else:
        print(f"[ERRO] Erro ao verificar API: {dados_api.get('erro')}")
        return

    print()

    # 3. Comparar dados
    comparacao = comparar_dados(dados_atuais, dados_api)

    print("[*] Comparacao:")
    print(f"     Total atual: {comparacao['total_atual']:,}")
    print(f"     Total na API: {comparacao['total_api']:,}")
    print(f"     Diferenca: {comparacao['diferenca']:,}")

    if comparacao.get("percentual_diferenca", 0) > 0:
        print(
            f"     Percentual de diferenca: {comparacao['percentual_diferenca']:.2f}%"
        )

    print(f"     Motivo: {comparacao['motivo']}")
    print()

    # 4. Decidir se precisa atualizar
    if comparacao["atualizacao_necesaria"]:
        print("[!] ATUALIZACAO NECESSARIA!")
        print()

        resposta = (
            input("Deseja executar a coleta completa agora? (s/n): ").strip().lower()
        )

        if resposta == "s":
            # Executar coleta
            resultado_coleta = executar_coleta()

            if resultado_coleta.get("sucesso"):
                print(
                    f"[OK] Coleta concluida: {resultado_coleta['total_coletado']:,} registros"
                )
                print()

                # Executar análise
                resultado_analise = executar_analise()

                if resultado_analise.get("sucesso"):
                    print("[OK] Analise concluida!")
                    print(f"     Relatorio JSON: {resultado_analise['relatorio_json']}")
                    print(f"     Relatorio TXT: {resultado_analise['relatorio_txt']}")
                    print(
                        f"     Relatorios visuais: {resultado_analise['relatorios_visuais']}"
                    )
                else:
                    print(f"[ERRO] Erro na analise: {resultado_analise.get('erro')}")
            else:
                print(f"[ERRO] Erro na coleta: {resultado_coleta.get('erro')}")
        else:
            print("[*] Coleta cancelada pelo usuario")
    else:
        print("[OK] Dados estao atualizados!")
        print()

        resposta = input("Deseja executar analise mesmo assim? (s/n): ").strip().lower()

        if resposta == "s":
            resultado_analise = executar_analise()

            if resultado_analise.get("sucesso"):
                print("[OK] Analise concluida!")
                print(f"     Relatorio JSON: {resultado_analise['relatorio_json']}")
                print(f"     Relatorio TXT: {resultado_analise['relatorio_txt']}")
                print(
                    f"     Relatorios visuais: {resultado_analise['relatorios_visuais']}"
                )
            else:
                print(f"[ERRO] Erro na analise: {resultado_analise.get('erro')}")


if __name__ == "__main__":
    main()
