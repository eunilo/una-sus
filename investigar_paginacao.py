#!/usr/bin/env python3
"""
Script para investigar a paginação da API da UNA-SUS.
"""

import json
import time

import requests

URL = "https://www.unasus.gov.br/cursos/rest/busca"
HEADERS = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}


def investigar_paginacao():
    """Investiga como funciona a paginação."""
    print("🔍 INVESTIGANDO PAGINAÇÃO DA API UNA-SUS")
    print("=" * 60)

    # Teste 1: Primeira página
    print("\n📄 TESTE 1: Primeira página")
    payload1 = {"busca": "", "ordenacao": "Por nome", "status": "Todos", "proximo": 0}

    resp1 = requests.post(URL, json=payload1, headers=HEADERS, timeout=30)
    data1 = resp1.json()

    print(f"Status: {resp1.status_code}")
    print(f"Payload: {payload1}")
    print(f"Resposta completa: {json.dumps(data1, indent=2)}")

    # Teste 2: Segunda página (se houver token)
    if "results" in data1 and "proximo" in data1["results"]:
        proximo = data1["results"]["proximo"]
        print(f"\n📄 TESTE 2: Segunda página (token: {proximo})")

        payload2 = {
            "busca": "",
            "ordenacao": "Por nome",
            "status": "Todos",
            "proximo": proximo,
        }

        resp2 = requests.post(URL, json=payload2, headers=HEADERS, timeout=30)
        data2 = resp2.json()

        print(f"Status: {resp2.status_code}")
        print(f"Payload: {payload2}")
        print(f"Resposta completa: {json.dumps(data2, indent=2)}")

        # Comparar resultados
        itens1 = data1.get("results", {}).get("itens", [])
        itens2 = data2.get("results", {}).get("itens", [])

        print(f"\n📊 COMPARAÇÃO:")
        print(f"Página 1: {len(itens1)} itens")
        print(f"Página 2: {len(itens2)} itens")

        # Verificar se são diferentes
        ids1 = [item.get("co_seq_curso") for item in itens1]
        ids2 = [item.get("co_seq_curso") for item in itens2]

        print(f"IDs página 1: {ids1[:5]}...")
        print(f"IDs página 2: {ids2[:5]}...")

        if set(ids1) == set(ids2):
            print("❌ PROBLEMA: As duas páginas têm os mesmos cursos!")
        else:
            print("✅ SUCESSO: As páginas têm cursos diferentes!")

    # Teste 3: Diferentes valores de "proximo"
    print(f"\n📄 TESTE 3: Testando diferentes valores de 'proximo'")
    for proximo_teste in [1, 10, 20, 50]:
        payload_teste = {
            "busca": "",
            "ordenacao": "Por nome",
            "status": "Todos",
            "proximo": proximo_teste,
        }

        try:
            resp_teste = requests.post(
                URL, json=payload_teste, headers=HEADERS, timeout=30
            )
            data_teste = resp_teste.json()
            itens_teste = data_teste.get("results", {}).get("itens", [])

            print(f"Token {proximo_teste}: {len(itens_teste)} itens")

            if itens_teste:
                primeiro_id = itens_teste[0].get("co_seq_curso")
                print(f"  Primeiro ID: {primeiro_id}")

        except Exception as e:
            print(f"Token {proximo_teste}: Erro - {e}")

        time.sleep(1)

    # Salvar investigação
    investigacao = {"teste_1": {"payload": payload1, "resposta": data1}}

    if "results" in data1 and "proximo" in data1["results"]:
        investigacao["teste_2"] = {"payload": payload2, "resposta": data2}

    with open("investigacao_paginacao.json", "w", encoding="utf-8") as f:
        json.dump(investigacao, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Investigação salva em: investigacao_paginacao.json")


if __name__ == "__main__":
    investigar_paginacao()
