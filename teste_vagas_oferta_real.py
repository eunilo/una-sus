import re

import requests
from bs4 import BeautifulSoup


def testar_vagas_oferta_real():
    """Testa a extração de vagas de uma oferta real."""

    # ID da oferta que encontramos
    id_oferta = "416264"
    url_oferta = f"https://www.unasus.gov.br/cursos/oferta/{id_oferta}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        print(f"Testando extração de vagas da oferta: {id_oferta}")
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
                    print(f"Primeiros 500 chars:\n{texto_completo[:500]}...")

                    # Extrair vagas usando regex
                    vagas_match = re.search(r"Vagas:\s*(\d+)", texto_completo)
                    if vagas_match:
                        vagas = vagas_match.group(1)
                        print(f"\n✅ VAGAS ENCONTRADAS: {vagas}")

                        # Testar extração de outros campos
                        campos = {
                            "Público-alvo": r"Público-alvo:\s*(.*?)(?=\n\n|\nLocal|\nFormato|\nNível|\nModalidade|\nProgramas|\nTemas|\nDeCs|\nDescrição|\nPalavras-chave|$)",
                            "Local da Oferta": r"Local da Oferta:\s*(.*?)(?=\n\n|\nFormato|\nNível|\nModalidade|\nProgramas|\nTemas|\nDeCs|\nDescrição|\nPalavras-chave|$)",
                            "Formato": r"Formato:\s*(.*?)(?=\n\n|\nNível|\nModalidade|\nProgramas|\nTemas|\nDeCs|\nDescrição|\nPalavras-chave|$)",
                            "Programas de governo": r"Programas de governo:\s*(.*?)(?=\n\n|\nTemas|\nDeCs|\nDescrição|\nPalavras-chave|$)",
                            "Temas": r"Temas:\s*(.*?)(?=\n\n|\nDeCs|\nDescrição|\nPalavras-chave|$)",
                            "DeCs": r"DeCs:\s*(.*?)(?=\n\n|\nDescrição|\nPalavras-chave|$)",
                            "Descrição da oferta": r"Descrição da oferta:\s*(.*?)(?=\n\n|\nPalavras-chave|$)",
                            "Palavras-chave": r"Palavras-chave:\s*(.*?)(?=\n\n|$)",
                        }

                        print("\n📋 Outros campos extraídos:")
                        for campo, regex in campos.items():
                            match = re.search(regex, texto_completo, re.DOTALL)
                            if match:
                                valor = match.group(1).strip()
                                print(
                                    f"  {campo}: {valor[:100]}{'...' if len(valor) > 100 else ''}"
                                )
                            else:
                                print(f"  {campo}: Não encontrado")

                    else:
                        print("❌ Vagas não encontradas no texto")
                        print("Padrões encontrados no texto:")
                        for linha in texto_completo.split("\n"):
                            if "Vagas" in linha or "vagas" in linha:
                                print(f"  - {linha.strip()}")
                else:
                    print("❌ Div encontrado mas texto vazio")
            else:
                print("❌ Div 'oferta_quadro' não encontrado")
                # Verificar outras estruturas possíveis
                divs = soup.find_all("div")
                print(f"Total de divs encontrados: {len(divs)}")
                for div in divs[:5]:
                    if div.get("id"):
                        print(f"  - Div com ID: {div.get('id')}")
        else:
            print(f"❌ Erro HTTP: {resp.status_code}")

    except Exception as e:
        print(f"❌ Erro ao testar oferta {id_oferta}: {e}")


if __name__ == "__main__":
    testar_vagas_oferta_real()
