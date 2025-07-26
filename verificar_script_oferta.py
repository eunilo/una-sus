import re

import requests
from bs4 import BeautifulSoup


def verificar_script_oferta():
    """Verifica se há JavaScript que carrega o conteúdo da oferta."""

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
        resp = requests.get(url_oferta, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Verificar scripts que podem carregar conteúdo
        scripts = soup.find_all("script")
        print(f"Total de scripts encontrados: {len(scripts)}")

        for i, script in enumerate(scripts):
            if script.string:
                script_content = script.string.lower()

                # Verificar se o script contém referências à oferta
                if any(
                    termo in script_content
                    for termo in ["oferta", "oferta_quadro", "ajax", "load"]
                ):
                    print(f"\n📋 Script {i+1} relevante encontrado:")
                    print(f"  Tipo: {script.get('type', 'sem-tipo')}")
                    print(f"  Src: {script.get('src', 'inline')}")
                    print(f"  Tamanho: {len(script.string)} caracteres")

                    # Mostrar partes relevantes do script
                    linhas_relevantes = []
                    for linha in script.string.split("\n"):
                        if any(
                            termo in linha.lower()
                            for termo in ["oferta", "ajax", "load", "get", "post"]
                        ):
                            linhas_relevantes.append(linha.strip())

                    if linhas_relevantes:
                        print("  Linhas relevantes:")
                        for linha in linhas_relevantes[:5]:
                            print(f"    {linha}")

        # Verificar se há chamadas AJAX ou endpoints de API
        print(f"\n🔍 Verificando possíveis endpoints de API...")

        # Procurar por URLs de API no HTML
        urls_api = re.findall(
            r'["\']([^"\']*api[^"\']*)["\']', resp.text, re.IGNORECASE
        )
        if urls_api:
            print("URLs de API encontradas:")
            for url in set(urls_api):
                print(f"  - {url}")

        # Procurar por endpoints de oferta
        endpoints_oferta = re.findall(
            r'["\']([^"\']*oferta[^"\']*)["\']', resp.text, re.IGNORECASE
        )
        if endpoints_oferta:
            print("Endpoints de oferta encontrados:")
            for endpoint in set(endpoints_oferta):
                print(f"  - {endpoint}")

        # Verificar se há dados JSON embutidos
        scripts_json = re.findall(
            r"<script[^>]*>([^<]*)</script>", resp.text, re.IGNORECASE
        )
        for script_content in scripts_json:
            if "oferta" in script_content.lower() and "{" in script_content:
                print(f"\n📋 Script com JSON encontrado:")
                print(f"  Conteúdo: {script_content[:200]}...")

    except Exception as e:
        print(f"Erro ao verificar scripts: {e}")


if __name__ == "__main__":
    verificar_script_oferta()
