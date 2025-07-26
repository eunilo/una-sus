import json

import requests
from bs4 import BeautifulSoup


def encontrar_oferta_real():
    """Encontra um ID de oferta real acessando a página de busca da UNA-SUS."""

    url_busca = "https://www.unasus.gov.br/cursos/busca"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        print("Acessando página de busca da UNA-SUS...")
        resp = requests.get(url_busca, headers=headers, timeout=30)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")

            # Procurar por links de ofertas
            links_oferta = soup.find_all("a", href=True)
            ofertas_encontradas = []

            for link in links_oferta:
                href = link["href"]
                if "/cursos/oferta/" in href:
                    id_oferta = href.split("/")[-1]
                    if id_oferta.isdigit():
                        ofertas_encontradas.append(id_oferta)

            if ofertas_encontradas:
                print(f"✅ Encontradas {len(ofertas_encontradas)} ofertas!")
                print("Primeiros 5 IDs de ofertas:")
                for i, oferta in enumerate(ofertas_encontradas[:5]):
                    print(f"  {i+1}. {oferta}")
                return ofertas_encontradas[:3]  # Retorna os 3 primeiros
            else:
                print("❌ Nenhuma oferta encontrada na página de busca")
                return []
        else:
            print(f"❌ Erro HTTP: {resp.status_code}")
            return []

    except Exception as e:
        print(f"❌ Erro ao acessar página de busca: {e}")
        return []


if __name__ == "__main__":
    ofertas = encontrar_oferta_real()
    if ofertas:
        print(f"\nIDs de ofertas para teste: {ofertas}")
    else:
        print("\nNenhum ID de oferta encontrado para teste.")
