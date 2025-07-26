import re

import requests
from bs4 import BeautifulSoup


def testar_extracao_vagas(id_oferta):
    """Testa a extração de vagas de uma oferta específica."""
    url_oferta = f"https://www.unasus.gov.br/cursos/oferta/{id_oferta}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        print(f"Testando oferta: {id_oferta}")
        print(f"URL: {url_oferta}")

        resp = requests.get(url_oferta, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Buscar o div principal com os dados da oferta
        oferta_quadro = soup.find("div", id="oferta_quadro")

        if oferta_quadro:
            print("✅ Div 'oferta_quadro' encontrado!")
            texto_completo = oferta_quadro.get_text()
            print(f"Texto completo:\n{texto_completo[:500]}...")

            # Extrair vagas usando regex
            vagas_match = re.search(r"Vagas:\s*(\d+)", texto_completo)
            if vagas_match:
                vagas = vagas_match.group(1)
                print(f"✅ Vagas encontradas: {vagas}")
            else:
                print("❌ Vagas não encontradas no texto")
                print("Padrões encontrados no texto:")
                for linha in texto_completo.split("\n"):
                    if "Vagas" in linha:
                        print(f"  - {linha.strip()}")
        else:
            print("❌ Div 'oferta_quadro' não encontrado")
            print("Estrutura HTML encontrada:")
            for div in soup.find_all("div")[:5]:
                print(f"  - {div.get('id', 'sem-id')}: " f"{div.get_text()[:100]}...")

        return True

    except Exception as e:
        print(f"❌ Erro ao testar oferta {id_oferta}: {e}")
        return False


# Testar com algumas ofertas conhecidas
ofertas_teste = ["12345", "67890", "11111"]  # IDs de exemplo

print("=== TESTE DE EXTRAÇÃO DE VAGAS ===\n")

for oferta in ofertas_teste:
    print(f"\n--- Testando Oferta {oferta} ---")
    testar_extracao_vagas(oferta)
    print("-" * 50)

print("\n=== FIM DOS TESTES ===")
