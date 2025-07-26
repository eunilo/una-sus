import pandas as pd


def verificar_vagas():
    """Verifica se as vagas estão sendo extraídas corretamente."""

    try:
        df = pd.read_csv("unasus_ofertas_detalhadas.csv", encoding="utf-8-sig")

        print(f"Total de registros: {len(df)}")
        print(f"Total de ofertas únicas: {df['id_oferta'].nunique()}")

        # Verificar se a coluna vagas existe
        if "vagas" in df.columns:
            print(f"\n📊 Estatísticas da coluna 'vagas':")
            print(f"  - Total de registros com vagas: {df['vagas'].notna().sum()}")
            print(f"  - Total de registros sem vagas: {df['vagas'].isna().sum()}")
            print(f"  - Registros com vagas preenchidas: {(df['vagas'] != '').sum()}")

            # Mostrar algumas ofertas com vagas
            ofertas_com_vagas = df[df["vagas"].notna() & (df["vagas"] != "")]
            if len(ofertas_com_vagas) > 0:
                print(f"\n✅ Ofertas com vagas encontradas: {len(ofertas_com_vagas)}")
                print("\nPrimeiras 5 ofertas com vagas:")
                for i, (_, row) in enumerate(ofertas_com_vagas.head().iterrows()):
                    print(f"  {i+1}. Oferta {row['id_oferta']}: {row['vagas']} vagas")
                    if "no_curso" in row:
                        print(f"     Curso: {row['no_curso'][:50]}...")
            else:
                print("\n❌ Nenhuma oferta com vagas encontrada")

            # Mostrar algumas ofertas sem vagas
            ofertas_sem_vagas = df[df["vagas"].isna() | (df["vagas"] == "")]
            if len(ofertas_sem_vagas) > 0:
                print(f"\n⚠️ Ofertas sem vagas: {len(ofertas_sem_vagas)}")
                print("\nPrimeiras 3 ofertas sem vagas:")
                for i, (_, row) in enumerate(ofertas_sem_vagas.head(3).iterrows()):
                    print(f"  {i+1}. Oferta {row['id_oferta']}")
                    if "no_curso" in row:
                        print(f"     Curso: {row['no_curso'][:50]}...")
        else:
            print("❌ Coluna 'vagas' não encontrada no CSV")

        # Verificar outras colunas importantes
        colunas_importantes = [
            "publico_alvo",
            "local_oferta",
            "formato",
            "programas_governo",
        ]
        print(f"\n📋 Verificação de outras colunas:")
        for coluna in colunas_importantes:
            if coluna in df.columns:
                preenchidas = (df[coluna].notna() & (df[coluna] != "")).sum()
                print(f"  {coluna}: {preenchidas}/{len(df)} preenchidas")
            else:
                print(f"  {coluna}: coluna não encontrada")

    except Exception as e:
        print(f"Erro ao verificar vagas: {e}")


if __name__ == "__main__":
    verificar_vagas()
