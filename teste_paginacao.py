#!/usr/bin/env python3
"""
Script para testar a paginação da API da UNA-SUS.
"""

import json
import time

import requests

URL = "https://www.unasus.gov.br/cursos/rest/busca"
HEADERS = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}


def testar_paginacao():
    """Testa a paginação da API."""
    print("🔍 TESTANDO PAGINAÇÃO DA API UNA-SUS")
    print("=" * 50)

    # Primeira página
    payload = {"busca": "", "ordenacao": "Por nome", "status": "Todos", "proximo": 0}

    pagina = 1
    cursos_unicos = set()

    while pagina <= 5:  # Testar apenas 5 páginas
        print(f"\n📄 PÁGINA {pagina}")
        print("-" * 30)
        print(f"Payload: {payload}")

        try:
            resp = requests.post(URL, json=payload, headers=HEADERS, timeout=30)
            data = resp.json()

            print(f"Status: {resp.status_code}")
            print(f"Total de resultados: {data.get('results', {}).get('total', 'N/A')}")

            itens = data.get("results", {}).get("itens", [])
            print(f"Cursos nesta página: {len(itens)}")

            # Verificar se são cursos únicos
            novos_cursos = 0
            for curso in itens:
                id_curso = (
                    curso.get("co_seq_curso")
                    or curso.get("id_curso")
                    or curso.get("co_curso")
                    or curso.get("id")
                )
                if id_curso and str(id_curso) not in cursos_unicos:
                    cursos_unicos.add(str(id_curso))
                    novos_cursos += 1

            print(f"Novos cursos únicos: {novos_cursos}")
            print(f"Total de cursos únicos até agora: {len(cursos_unicos)}")

            # Mostrar alguns cursos como exemplo
            if itens:
                print("\nExemplos de cursos:")
                for i, curso in enumerate(itens[:3], 1):
                    print(
                        f"  {i}. {curso.get('no_curso', 'N/A')} (ID: {curso.get('co_seq_curso', 'N/A')})"
                    )

            # Obter token da próxima página
            proximo = data.get("results", {}).get("proximo")
            print(f"\nToken atual: {payload.get('proximo', 0)}")
            print(f"Token próximo: {proximo}")

            if not proximo:
                print("❌ Não há mais páginas!")
                break

            # Atualizar payload para próxima página
            payload["proximo"] = proximo

            pagina += 1
            time.sleep(1)  # Pausa entre requisições

        except Exception as e:
            print(f"❌ Erro na página {pagina}: {e}")
            break

    print(f"\n📊 RESUMO:")
    print(f"Páginas processadas: {pagina - 1}")
    print(f"Total de cursos únicos: {len(cursos_unicos)}")

    # Salvar resultado para análise
    resultado = {
        "paginas_processadas": pagina - 1,
        "cursos_unicos": len(cursos_unicos),
        "payload_final": payload,
    }

    with open("teste_paginacao_resultado.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Resultado salvo em: teste_paginacao_resultado.json")


if __name__ == "__main__":
    testar_paginacao()
