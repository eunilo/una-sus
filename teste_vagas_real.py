import re

import requests
from bs4 import BeautifulSoup


def testar_extracao_vagas_real():
    """Testa a extração de vagas com um ID real de oferta da UNA-SUS."""

    # IDs de ofertas reais da UNA-SUS (exemplos)
    ofertas_reais = ["123456", "789012", "345678"]  # Exemplo  # Exemplo  # Exemplo

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    print("=== TESTE DE EXTRAÇÃO DE VAGAS - OFERTAS REAIS ===\n")

    for id_oferta in ofertas_reais:
        url_oferta = f"https://www.unasus.gov.br/cursos/oferta/{id_oferta}"

        try:
            print(f"Testando oferta: {id_oferta}")
            print(f"URL: {url_oferta}")

            resp = requests.get(url_oferta, headers=headers, timeout=30)

            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")

                # Buscar o div principal com os dados da oferta
                oferta_quadro = soup.find("div", id="oferta_quadro")

                if oferta_quadro:
                    print("✅ Div 'oferta_quadro' encontrado!")
                    texto_completo = oferta_quadro.get_text()

                    if texto_completo.strip():
                        print(f"Texto encontrado ({len(texto_completo)} caracteres):")
                        print(f"Primeiros 300 chars: {texto_completo[:300]}...")

                        # Extrair vagas usando regex
                        vagas_match = re.search(r"Vagas:\s*(\d+)", texto_completo)
                        if vagas_match:
                            vagas = vagas_match.group(1)
                            print(f"✅ Vagas encontradas: {vagas}")
                        else:
                            print("❌ Vagas não encontradas no texto")
                            # Procurar por padrões similares
                            for linha in texto_completo.split("\n"):
                                if "Vagas" in linha or "vagas" in linha:
                                    print(f"  - Linha com 'vagas': {linha.strip()}")
                    else:
                        print("❌ Div encontrado mas texto vazio")
                else:
                    print("❌ Div 'oferta_quadro' não encontrado")
                    # Verificar outras estruturas possíveis
                    divs = soup.find_all("div")
                    print(f"Total de divs encontrados: {len(divs)}")
                    for div in divs[:3]:
                        if div.get("id"):
                            print(f"  - Div com ID: {div.get('id')}")
            else:
                print(f"❌ Erro HTTP: {resp.status_code}")

        except Exception as e:
            print(f"❌ Erro ao testar oferta {id_oferta}: {e}")

        print("-" * 60)


if __name__ == "__main__":
    testar_extracao_vagas_real()
