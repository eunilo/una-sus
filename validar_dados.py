#!/usr/bin/env python3
"""
Script para validar e limpar os dados coletados pelo scraper UNA-SUS.
"""

import os
from datetime import datetime
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def carregar_dados(csv_path: str) -> pd.DataFrame:
    """Carrega os dados do CSV."""
    if not os.path.exists(csv_path):
        print(f"❌ Arquivo {csv_path} não encontrado!")
        return pd.DataFrame()

    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        print(f"✅ Dados carregados: {len(df):,} registros")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame()


def analisar_estrutura(df: pd.DataFrame) -> Dict:
    """Analisa a estrutura dos dados."""
    print("\n📊 ANÁLISE DA ESTRUTURA DOS DADOS")
    print("=" * 50)

    info = {
        "total_registros": len(df),
        "colunas": list(df.columns),
        "colunas_vazias": [],
        "colunas_completas": [],
        "tipos_dados": {},
    }

    print(f"Total de registros: {len(df):,}")
    print(f"Total de colunas: {len(df.columns)}")
    print(f"Colunas: {', '.join(df.columns)}")

    # Analisar cada coluna
    for col in df.columns:
        na_count = df[col].isna().sum()
        empty_count = (df[col] == "").sum()
        total_empty = na_count + empty_count
        completeness = ((len(df) - total_empty) / len(df)) * 100

        info["tipos_dados"][col] = str(df[col].dtype)

        if completeness == 0:
            info["colunas_vazias"].append(col)
            print(f"❌ {col}: {completeness:.1f}% preenchida")
        elif completeness == 100:
            info["colunas_completas"].append(col)
            print(f"✅ {col}: {completeness:.1f}% preenchida")
        else:
            print(f"⚠️  {col}: {completeness:.1f}% preenchida")

    return info


def validar_cursos(df: pd.DataFrame) -> Dict:
    """Valida os dados dos cursos."""
    print("\n🎓 VALIDAÇÃO DOS CURSOS")
    print("=" * 50)

    validacao = {
        "cursos_unicos": 0,
        "cursos_sem_nome": 0,
        "cursos_sem_descricao": 0,
        "cursos_sem_id": 0,
        "cursos_duplicados": 0,
        "cursos_incompletos": 0,
    }

    # Contar cursos únicos
    for col in ["co_seq_curso", "id_curso", "co_curso"]:
        if col in df.columns:
            validacao["cursos_unicos"] = df[col].nunique()
            break

        # Verificar campos obrigatórios
    if "no_curso" in df.columns:
        validacao["cursos_sem_nome"] = df["no_curso"].isna().sum()

    if "ds_curso" in df.columns:
        validacao["cursos_sem_descricao"] = df["ds_curso"].isna().sum()

    # Verificar cursos incompletos
    if "curso_incompleto" in df.columns:
        validacao["cursos_incompletos"] = (df["curso_incompleto"] == "Sim").sum()

    # Verificar IDs
    for col in ["co_seq_curso", "id_curso", "co_curso"]:
        if col in df.columns:
            validacao["cursos_sem_id"] = df[col].isna().sum()
            break

    # Verificar duplicatas
    if "no_curso" in df.columns:
        validacao["cursos_duplicados"] = df["no_curso"].duplicated().sum()

    print(f"Cursos únicos: {validacao['cursos_unicos']:,}")
    print(f"Cursos sem nome: {validacao['cursos_sem_nome']:,}")
    print(f"Cursos sem descrição: {validacao['cursos_sem_descricao']:,}")
    print(f"Cursos sem ID: {validacao['cursos_sem_id']:,}")
    print(f"Cursos duplicados: {validacao['cursos_duplicados']:,}")
    print(f"Cursos incompletos: {validacao['cursos_incompletos']:,}")

    return validacao


def validar_ofertas(df: pd.DataFrame) -> Dict:
    """Valida os dados das ofertas."""
    print("\n📚 VALIDAÇÃO DAS OFERTAS")
    print("=" * 50)

    validacao = {
        "ofertas_unicas": 0,
        "ofertas_sem_id": 0,
        "ofertas_sem_vagas": 0,
        "ofertas_sem_publico": 0,
        "ofertas_com_erro": 0,
    }

    if "id_oferta" in df.columns:
        validacao["ofertas_unicas"] = df["id_oferta"].nunique()
        validacao["ofertas_sem_id"] = df["id_oferta"].isna().sum()

    if "vagas" in df.columns:
        validacao["ofertas_sem_vagas"] = df["vagas"].isna().sum()

    if "publico_alvo" in df.columns:
        validacao["ofertas_sem_publico"] = df["publico_alvo"].isna().sum()

    if "erro" in df.columns:
        validacao["ofertas_com_erro"] = df["erro"].notna().sum()

    print(f"Ofertas únicas: {validacao['ofertas_unicas']:,}")
    print(f"Ofertas sem ID: {validacao['ofertas_sem_id']:,}")
    print(f"Ofertas sem vagas: {validacao['ofertas_sem_vagas']:,}")
    print(f"Ofertas sem público-alvo: {validacao['ofertas_sem_publico']:,}")
    print(f"Ofertas com erro: {validacao['ofertas_com_erro']:,}")

    return validacao


def analisar_deia(df: pd.DataFrame) -> Dict:
    """Analisa os dados relacionados a DEIA."""
    print("\n🌈 ANÁLISE DEIA")
    print("=" * 50)

    analise = {
        "total_cursos": len(df),
        "cursos_com_deia": 0,
        "cursos_sem_deia": 0,
        "descritores_encontrados": [],
        "percentual_deia": 0,
    }

    if "tem_deia" in df.columns:
        deia_counts = df["tem_deia"].value_counts()
        analise["cursos_com_deia"] = deia_counts.get("Sim", 0)
        analise["cursos_sem_deia"] = deia_counts.get("Não", 0)
        analise["percentual_deia"] = (analise["cursos_com_deia"] / len(df)) * 100

    if "deia_encontrado" in df.columns:
        descritores = df["deia_encontrado"].dropna().unique()
        analise["descritores_encontrados"] = list(descritores)

    print(f"Total de cursos: {analise['total_cursos']:,}")
    print(f"Cursos com DEIA: {analise['cursos_com_deia']:,}")
    print(f"Cursos sem DEIA: {analise['cursos_sem_deia']:,}")
    print(f"Percentual DEIA: {analise['percentual_deia']:.2f}%")

    if analise["descritores_encontrados"]:
        print(
            f"Descritores encontrados: {', '.join(analise['descritores_encontrados'])}"
        )

    return analise


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa os dados removendo duplicatas e registros inválidos."""
    print("\n🧹 LIMPEZA DOS DADOS")
    print("=" * 50)

    df_original = df.copy()
    registros_originais = len(df)

    # Remover linhas completamente vazias
    df = df.dropna(how="all")
    print(f"Linhas completamente vazias removidas: {registros_originais - len(df)}")

    # Remover duplicatas baseadas no ID do curso
    for col in ["co_seq_curso", "id_curso", "co_curso"]:
        if col in df.columns:
            duplicatas = df[col].duplicated().sum()
            df = df.drop_duplicates(subset=[col], keep="first")
            print(f"Duplicatas removidas ({col}): {duplicatas}")
            break

    # Limpar strings vazias
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].replace("", np.nan)

    registros_finais = len(df)
    print(f"Registros removidos: {registros_originais - registros_finais}")
    print(f"Registros finais: {registros_finais}")

    return df


def salvar_dados_limpos(df: pd.DataFrame, csv_path: str):
    """Salva os dados limpos."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"unasus_dados_limpos_{timestamp}.csv"

    try:
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"\n✅ Dados limpos salvos em: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Erro ao salvar dados limpos: {e}")
        return None


def gerar_relatorio_completo(
    df: pd.DataFrame,
    info: Dict,
    validacao_cursos: Dict,
    validacao_ofertas: Dict,
    analise_deia: Dict,
) -> str:
    """Gera um relatório completo da validação."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    relatorio_path = f"relatorio_validacao_{timestamp}.txt"

    with open(relatorio_path, "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE VALIDAÇÃO - SCRAPER UNA-SUS\n")
        f.write("=" * 50 + "\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("ESTRUTURA DOS DADOS\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total de registros: {info['total_registros']:,}\n")
        f.write(f"Total de colunas: {len(info['colunas'])}\n")
        f.write(f"Colunas vazias: {len(info['colunas_vazias'])}\n")
        f.write(f"Colunas completas: {len(info['colunas_completas'])}\n\n")

        f.write("VALIDAÇÃO DOS CURSOS\n")
        f.write("-" * 20 + "\n")
        for key, value in validacao_cursos.items():
            f.write(f"{key}: {value:,}\n")
        f.write("\n")

        f.write("VALIDAÇÃO DAS OFERTAS\n")
        f.write("-" * 20 + "\n")
        for key, value in validacao_ofertas.items():
            f.write(f"{key}: {value:,}\n")
        f.write("\n")

        f.write("ANÁLISE DEIA\n")
        f.write("-" * 20 + "\n")
        for key, value in analise_deia.items():
            if isinstance(value, list):
                f.write(f"{key}: {', '.join(value)}\n")
            else:
                f.write(f"{key}: {value}\n")

    print(f"📋 Relatório salvo em: {relatorio_path}")
    return relatorio_path


def main():
    """Função principal."""
    print("🔍 VALIDADOR DE DADOS - SCRAPER UNA-SUS")
    print("=" * 60)

    # Carregar dados
    df = carregar_dados("unasus_ofertas_detalhadas.csv")
    if df.empty:
        return

    # Análises
    info = analisar_estrutura(df)
    validacao_cursos = validar_cursos(df)
    validacao_ofertas = validar_ofertas(df)
    analise_deia = analisar_deia(df)

    # Perguntar se quer limpar os dados
    print("\n" + "=" * 60)
    resposta = input("Deseja limpar os dados? (s/n): ").lower().strip()

    if resposta == "s":
        df_limpo = limpar_dados(df)
        if not df_limpo.empty:
            salvar_dados_limpos(df_limpo, "unasus_ofertas_detalhadas.csv")

    # Gerar relatório
    print("\n" + "=" * 60)
    resposta = input("Deseja gerar relatório completo? (s/n): ").lower().strip()

    if resposta == "s":
        gerar_relatorio_completo(
            df, info, validacao_cursos, validacao_ofertas, analise_deia
        )

    print("\n✅ Validação concluída!")


if __name__ == "__main__":
    main()
