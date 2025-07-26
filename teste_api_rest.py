import json

import requests


def teste_api_rest():
    """Testa a API REST da oferta."""

    id_oferta = "416264"
    url_api = f"https://www.unasus.gov.br/cursos/rest/oferta/{id_oferta}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"https://www.unasus.gov.br/cursos/oferta/{id_oferta}",
    }

    try:
        print(f"Testando API REST da oferta {id_oferta}")
        print(f"URL: {url_api}")

        resp = requests.get(url_api, headers=headers, timeout=30)

        print(f"Status: {resp.status_code}")

        if resp.status_code == 200:
            data = resp.json()
            print("✅ API REST funcionando!")
            print(f"Dados recebidos: {len(data)} campos")

            # Mostrar campos importantes
            campos_importantes = [
                "qt_vagas",
                "ds_publico_alvo",
                "no_local_oferta",
                "no_formato",
                "ds_programas_governo",
                "ds_temas",
                "ds_decs",
                "ds_oferta",
                "ds_palavras_chave",
            ]

            print("\n📋 Campos importantes:")
            for campo in campos_importantes:
                valor = data.get(campo, "N/A")
                print(f"  {campo}: {valor}")

            # Mostrar todos os campos disponíveis
            print(f"\n📋 Todos os campos disponíveis ({len(data)}):")
            for campo, valor in data.items():
                print(f"  {campo}: {valor}")

        else:
            print(f"❌ Erro HTTP: {resp.status_code}")
            print(f"Resposta: {resp.text[:200]}...")

    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    teste_api_rest()
