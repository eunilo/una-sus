import re

import requests
from bs4 import BeautifulSoup


def teste_oferta_detalhado():
    """Teste detalhado de uma oferta específica."""

    # ID da oferta que sabemos que existe
    id_oferta = "416264"
    url_oferta = f"https://www.unasus.gov.br/cursos/oferta/{id_oferta}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        print(f"Testando oferta: {id_oferta}")
        print(f"URL: {url_oferta}")

        resp = requests.get(url_oferta, headers=headers, timeout=30)

        print(f"Status da resposta: {resp.status_code}")
        print(f"Tamanho da página: {len(resp.text)} caracteres")

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")

            # Verificar se há redirecionamento
            if "redirect" in resp.text.lower() or "location" in resp.text.lower():
                print("⚠️ Possível redirecionamento detectado")

            # Buscar o div principal com os dados da oferta
            oferta_quadro = soup.find("div", id="oferta_quadro")

            if oferta_quadro:
                print("✅ Div 'oferta_quadro' encontrado!")
                texto_completo = oferta_quadro.get_text()

                print(f"Tamanho do texto do div: {len(texto_completo)} caracteres")
                print(f"Texto do div (primeiros 200 chars): '{texto_completo[:200]}'")

                if texto_completo.strip():
                    print("✅ Div tem conteúdo!")

                    # Extrair vagas usando regex
                    vagas_match = re.search(r"Vagas:\s*(\d+)", texto_completo)
                    if vagas_match:
                        vagas = vagas_match.group(1)
                        print(f"✅ VAGAS ENCONTRADAS: {vagas}")
                    else:
                        print("❌ Vagas não encontradas no texto")

                        # Procurar por padrões similares
                        for linha in texto_completo.split("\n"):
                            if "Vagas" in linha or "vagas" in linha:
                                print(f"  - Linha com 'vagas': {linha.strip()}")
                else:
                    print("❌ Div encontrado mas texto vazio")

                    # Verificar se há JavaScript que carrega o conteúdo
                    scripts = soup.find_all("script")
                    scripts_com_oferta = [
                        s for s in scripts if s.string and "oferta" in s.string.lower()
                    ]
                    print(f"Scripts com 'oferta': {len(scripts_com_oferta)}")

                    # Verificar se há iframe ou conteúdo carregado dinamicamente
                    iframes = soup.find_all("iframe")
                    print(f"Iframes encontrados: {len(iframes)}")

                    # Verificar se há divs com conteúdo
                    divs_com_conteudo = [
                        d for d in soup.find_all("div") if d.get_text().strip()
                    ]
                    print(f"Divs com conteúdo: {len(divs_com_conteudo)}")

                    # Mostrar alguns divs com conteúdo
                    for i, div in enumerate(divs_com_conteudo[:3]):
                        print(
                            f"  Div {i+1} (ID: {div.get('id', 'sem-id')}): {div.get_text()[:100]}..."
                        )
            else:
                print("❌ Div 'oferta_quadro' não encontrado")

                # Verificar outras estruturas possíveis
                divs = soup.find_all("div")
                divs_com_id = [d for d in divs if d.get("id")]
                print(f"Total de divs: {len(divs)}")
                print(f"Divs com ID: {len(divs_com_id)}")

                for div in divs_com_id[:5]:
                    print(f"  - Div com ID: {div.get('id')}")

        else:
            print(f"❌ Erro HTTP: {resp.status_code}")

    except Exception as e:
        print(f"❌ Erro ao testar oferta {id_oferta}: {e}")


if __name__ == "__main__":
    teste_oferta_detalhado()
