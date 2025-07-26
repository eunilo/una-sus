import json

import requests

from scraper_unasus_melhorado import COOKIES, HEADERS, PAYLOAD_INICIAL, URL


def verificar_configuracoes():
    """Verifica se as configurações de cookies e headers estão funcionando."""
    print("=== VERIFICAÇÃO DE CONFIGURAÇÕES ===")
    print()

    # Verificar headers
    print("1. VERIFICANDO HEADERS:")
    for key, value in HEADERS.items():
        print(f"   {key}: {value}")
    print()

    # Verificar cookies
    print("2. VERIFICANDO COOKIES:")
    for key, value in COOKIES.items():
        print(f"   {key}: {value}")
    print()

    # Verificar payload
    print("3. VERIFICANDO PAYLOAD:")
    for key, value in PAYLOAD_INICIAL.items():
        print(f"   {key}: {value}")
    print()

    # Testar conexão com a API
    print("4. TESTANDO CONEXÃO COM A API:")
    try:
        response = requests.post(
            URL,
            data=PAYLOAD_INICIAL,
            headers=HEADERS,
            cookies=COOKIES,
            timeout=30,
        )

        print(f"   Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            itens = data.get("results", {}).get("itens", [])
            print("   ✅ Conexão bem-sucedida!")
            print(f"   Itens encontrados: {len(itens)}")

            if itens:
                print("   Primeiro item:")
                primeiro_item = itens[0]
                for key, value in primeiro_item.items():
                    print(f"     {key}: {value}")
        else:
            print(f"   ❌ Erro na conexão: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}...")

    except Exception as e:
        print(f"   ❌ Erro na conexão: {e}")

    print()

    # Comparar com arquivo original
    print("5. COMPARAÇÃO COM ARQUIVO ORIGINAL:")

    # Headers originais (do arquivo original)
    headers_originais = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.unasus.gov.br",
        "Referer": (
            "https://www.unasus.gov.br/cursos/busca?status=todos&busca="
            "&ordenacao=Relev%C3%A2ncia%20na%20busca"
        ),
    }

    # Cookies originais
    cookies_originais = {
        "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
        "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
        "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272": (
            "_329a72cffc11d2904ae393c82d0cfb72"
        ),
    }

    # Payload original
    payload_original = {
        "busca": "",
        "ordenacao": "Por nome",
        "status": "Todos",
        "proximo": 0,
    }

    # Verificar diferenças
    print("   Headers:")
    for key in headers_originais:
        if key in HEADERS:
            if headers_originais[key] == HEADERS[key]:
                print(f"     ✅ {key}: OK")
            else:
                print(f"     ❌ {key}: DIFERENTE")
                print(f"        Original: {headers_originais[key]}")
                print(f"        Atual: {HEADERS[key]}")
        else:
            print(f"     ❌ {key}: AUSENTE")

    print("   Cookies:")
    for key in cookies_originais:
        if key in COOKIES:
            if cookies_originais[key] == COOKIES[key]:
                print(f"     ✅ {key}: OK")
            else:
                print(f"     ❌ {key}: DIFERENTE")
                print(f"        Original: {cookies_originais[key]}")
                print(f"        Atual: {COOKIES[key]}")
        else:
            print(f"     ❌ {key}: AUSENTE")

    print("   Payload:")
    for key in payload_original:
        if key in PAYLOAD_INICIAL:
            if payload_original[key] == PAYLOAD_INICIAL[key]:
                print(f"     ✅ {key}: OK")
            else:
                print(f"     ❌ {key}: DIFERENTE")
                print(f"        Original: {payload_original[key]}")
                print(f"        Atual: {PAYLOAD_INICIAL[key]}")
        else:
            print(f"     ❌ {key}: AUSENTE")

    print()
    print("=== VERIFICAÇÃO CONCLUÍDA ===")


if __name__ == "__main__":
    verificar_configuracoes()
