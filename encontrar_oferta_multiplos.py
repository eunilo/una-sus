import requests
from bs4 import BeautifulSoup


def encontrar_oferta_multiplos():
    """Testa múltiplos cursos até encontrar um com ofertas."""

    url = "https://www.unasus.gov.br/cursos/rest/busca"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
    }
    payload = {"busca": "", "ordenacao": "Por nome", "status": "Todos", "proximo": 0}

    try:
        print("Consultando API da UNA-SUS...")
        resp = requests.post(url, json=payload, headers=headers, timeout=30)

        if resp.status_code == 200:
            data = resp.json()
            itens = data.get("results", {}).get("itens", [])

            if itens:
                print(f"✅ Encontrados {len(itens)} cursos!")
                print("Testando cursos para encontrar ofertas...\n")

                for i, curso in enumerate(itens[:10]):  # Testa os primeiros 10 cursos
                    id_curso = curso.get("co_seq_curso") or curso.get("id_curso")
                    nome_curso = curso.get("no_curso", "N/A")

                    if id_curso:
                        print(
                            f"Testando curso {i+1}: {nome_curso[:50]}... (ID: {id_curso})"
                        )

                        ofertas = extrair_ofertas_do_curso(id_curso)

                        if ofertas:
                            print(f"✅ Encontradas {len(ofertas)} ofertas!")
                            print("IDs de ofertas para teste:")
                            for j, oferta in enumerate(ofertas[:3]):
                                print(f"  {j+1}. {oferta}")
                            return ofertas[:3]
                        else:
                            print("❌ Nenhuma oferta encontrada")
                    else:
                        print("❌ Curso sem ID válido")

                    print("-" * 40)

                print("❌ Nenhum curso com ofertas encontrado nos primeiros 10")
                return []
            else:
                print("❌ Nenhum curso encontrado na API")
                return []
        else:
            print(f"❌ Erro HTTP: {resp.status_code}")
            return []

    except Exception as e:
        print(f"❌ Erro ao consultar API: {e}")
        return []


def extrair_ofertas_do_curso(id_curso):
    """Extrai ofertas de um curso específico."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        resp = requests.get(url_curso, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")

        ofertas = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "/cursos/oferta/" in href:
                id_oferta = href.split("/")[-1]
                if id_oferta.isdigit():
                    ofertas.append(id_oferta)

        return list(set(ofertas))  # Remove duplicados

    except Exception as e:
        print(f"Erro ao extrair ofertas do curso {id_curso}: {e}")
        return []


if __name__ == "__main__":
    ofertas = encontrar_oferta_multiplos()
    if ofertas:
        print(f"\nIDs de ofertas para teste: {ofertas}")
    else:
        print("\nNenhum ID de oferta encontrado para teste.")
