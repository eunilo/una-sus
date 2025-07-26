import pandas as pd

try:
    df = pd.read_csv("unasus_ofertas_detalhadas.csv", encoding="utf-8-sig")

    if "id_oferta" in df.columns:
        ofertas = df["id_oferta"].dropna().unique()
        print(f"Total de ofertas únicas: {len(ofertas)}")
        print("Primeiros 5 IDs de ofertas:")
        for i, oferta in enumerate(ofertas[:5]):
            print(f"  {i+1}. {oferta}")
    else:
        print("Coluna 'id_oferta' não encontrada no CSV")
        print("Colunas disponíveis:", list(df.columns))

except Exception as e:
    print(f"Erro ao ler CSV: {e}")
