import requests
import pandas as pd
import time

url = "https://www.unasus.gov.br/cursos/rest/busca"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

payload = {
    "busca": "",
    "ordenacao": "Por nome",
    "status": "Todos",
    "proximo": 0
}

print("Testando conexão com a API da UNA-SUS...")

try:
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    data = resp.json()
    itens = data.get("results", {}).get("itens", [])
    
    print(f"Conectado com sucesso!")
    print(f"Total de itens na primeira página: {len(itens)}")
    
    if itens:
        primeiro_curso = itens[0]
        print(f"Primeiro curso: {primeiro_curso.get('no_curso', 'N/A')}")
        print(f"ID do curso: {primeiro_curso.get('id_curso', primeiro_curso.get('co_curso', 'N/A'))}")
        
        # Testa salvar um arquivo simples
        df_teste = pd.DataFrame(itens[:5])  # Primeiros 5 cursos
        df_teste.to_csv("teste_unasus.csv", index=False, encoding="utf-8-sig")
        print("Arquivo de teste criado: teste_unasus.csv")
        
except Exception as e:
    print(f"Erro na conexão: {e}") 