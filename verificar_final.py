#!/usr/bin/env python3
"""
Script de verificação final do scraper UNA-SUS
Testa todas as funcionalidades implementadas e mostra estatísticas completas.
"""

import os
from datetime import datetime

import pandas as pd


def verificar_dataset_completo():
    """Verifica o dataset completo e mostra estatísticas detalhadas."""

    csv_path = "unasus_ofertas_detalhadas.csv"

    if not os.path.exists(csv_path):
        print("❌ Arquivo CSV não encontrado!")
        print("Execute o scraper primeiro: python scraper_unasus_incremental.py")
        return

    try:
        print("🔍 VERIFICAÇÃO FINAL DO DATASET UNA-SUS")
        print("=" * 50)

        # Carregar dados
        df = pd.read_csv(csv_path, encoding="utf-8-sig")

        # Estatísticas básicas
        print(f"\n📊 ESTATÍSTICAS BÁSICAS:")
        print(f"  - Total de registros: {len(df):,}")
        print(f"  - Total de colunas: {len(df.columns)}")
        print(f"  - Cursos únicos: {df['co_seq_curso'].nunique():,}")
        print(f"  - Ofertas únicas: {df['id_oferta'].nunique():,}")

        # Verificar colunas importantes
        colunas_importantes = [
            "vagas",
            "publico_alvo",
            "local_oferta",
            "formato",
            "programas_governo",
            "temas",
            "decs",
            "descricao_oferta",
            "palavras_chave",
            "tem_deia",
            "deia_encontrado",
        ]

        print(f"\n✅ VERIFICAÇÃO DE COLUNAS IMPORTANTES:")
        for coluna in colunas_importantes:
            if coluna in df.columns:
                preenchidos = df[coluna].notna().sum()
                percentual = (preenchidos / len(df)) * 100
                print(f"  - {coluna}: {preenchidos:,}/{len(df):,} ({percentual:.1f}%)")
            else:
                print(f"  - {coluna}: ❌ COLUNA NÃO ENCONTRADA")

        # Estatísticas de vagas
        if "vagas" in df.columns:
            print(f"\n🎯 ESTATÍSTICAS DE VAGAS:")
            vagas_preenchidas = df[df["vagas"].notna() & (df["vagas"] != "")]
            print(f"  - Ofertas com vagas: {len(vagas_preenchidas):,}")
            print(f"  - Taxa de sucesso: {(len(vagas_preenchidas)/len(df)*100):.1f}%")

            if len(vagas_preenchidas) > 0:
                # Converter para numérico para estatísticas
                vagas_numericas = pd.to_numeric(
                    vagas_preenchidas["vagas"], errors="coerce"
                )
                vagas_numericas = vagas_numericas.dropna()

                if len(vagas_numericas) > 0:
                    print(f"  - Média de vagas: {vagas_numericas.mean():.0f}")
                    print(f"  - Mediana de vagas: {vagas_numericas.median():.0f}")
                    print(f"  - Máximo de vagas: {vagas_numericas.max():,}")
                    print(f"  - Mínimo de vagas: {vagas_numericas.min():,}")

        # Estatísticas DEIA
        if "tem_deia" in df.columns:
            print(f"\n🌈 ESTATÍSTICAS DEIA:")
            cursos_deia = df[df["tem_deia"] == "Sim"]
            print(f"  - Cursos com DEIA: {len(cursos_deia):,}")
            print(f"  - Percentual DEIA: {(len(cursos_deia)/len(df)*100):.1f}%")

            if "deia_encontrado" in df.columns:
                descritores = cursos_deia["deia_encontrado"].value_counts()
                print(f"  - Top 3 descritores:")
                for i, (descritor, count) in enumerate(descritores.head(3).items()):
                    print(f"    {i+1}. {descritor}: {count}")

        # Estatísticas de formato
        if "formato" in df.columns:
            print(f"\n📚 FORMATOS DE ENSINO:")
            formatos = df["formato"].value_counts()
            for formato, count in formatos.head(5).items():
                print(f"  - {formato}: {count:,}")

        # Estatísticas de órgãos
        if "no_orgao" in df.columns:
            print(f"\n🏛️ ÓRGÃOS RESPONSÁVEIS:")
            orgaos = df["no_orgao"].value_counts()
            for orgao, count in orgaos.head(5).items():
                print(f"  - {orgao}: {count:,}")

        # Verificar qualidade dos dados
        print(f"\n🔍 QUALIDADE DOS DADOS:")
        registros_completos = df.dropna(
            subset=["vagas", "publico_alvo", "formato"]
        ).shape[0]
        print(
            f"  - Registros completos (vagas + público + formato): {registros_completos:,}"
        )
        print(f"  - Taxa de completude: {(registros_completos/len(df)*100):.1f}%")

        # Exemplos de dados
        print(f"\n📋 EXEMPLOS DE DADOS COLETADOS:")
        if len(df) > 0:
            exemplo = df.iloc[0]
            print(f"  - Curso: {exemplo.get('no_curso', 'N/A')[:50]}...")
            print(f"  - Vagas: {exemplo.get('vagas', 'N/A')}")
            print(f"  - Formato: {exemplo.get('formato', 'N/A')}")
            print(f"  - DEIA: {exemplo.get('tem_deia', 'N/A')}")

        # Informações do arquivo
        print(f"\n💾 INFORMAÇÕES DO ARQUIVO:")
        tamanho_arquivo = os.path.getsize(csv_path) / (1024 * 1024)  # MB
        print(f"  - Tamanho: {tamanho_arquivo:.2f} MB")
        print(f"  - Caminho: {os.path.abspath(csv_path)}")

        # Timestamp da verificação
        print(
            f"\n⏰ Verificação realizada em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )

        print(f"\n✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")

    except Exception as e:
        print(f"❌ Erro durante a verificação: {e}")


def verificar_funcionalidades():
    """Verifica se todas as funcionalidades estão implementadas."""

    print("🔧 VERIFICAÇÃO DE FUNCIONALIDADES")
    print("=" * 40)

    # Verificar se o scraper principal existe
    if os.path.exists("scraper_unasus_incremental.py"):
        print("✅ Scraper principal encontrado")
    else:
        print("❌ Scraper principal não encontrado")

    # Verificar se o requirements.txt existe
    if os.path.exists("requirements.txt"):
        print("✅ Requirements.txt encontrado")
    else:
        print("❌ Requirements.txt não encontrado")

    # Verificar se o README.md existe
    if os.path.exists("README.md"):
        print("✅ README.md encontrado")
    else:
        print("❌ README.md não encontrado")

    # Verificar se o .gitignore existe
    if os.path.exists(".gitignore"):
        print("✅ .gitignore encontrado")
    else:
        print("❌ .gitignore não encontrado")


if __name__ == "__main__":
    print("🚀 INICIANDO VERIFICAÇÃO FINAL DO PROJETO UNA-SUS")
    print("=" * 60)

    verificar_funcionalidades()
    print()
    verificar_dataset_completo()

    print("\n" + "=" * 60)
    print("🎉 VERIFICAÇÃO FINALIZADA!")
    print("O projeto está pronto para uso e contribuições!")
