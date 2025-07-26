import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import os

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

descritores = [
    "Diversidade, Equidade e Integração",
    "Diversidade, Equidade, Inclusão e Pertencimento",
    "Diversidade, Equidade, Inclusão, Acessibilidade",
    "Diversidade, Equidade, Inclusão, Pertencimento",
    "Diversidade, Igualdade e Inclusão",
    "Diversidade, Igualdade, Inclusão e Acessibilidade",
    "Diversidade, Igualdade, Inclusão, Pertencimento",
    "Equidade, Diversidade e Inclusão",
    "Inclusão, Diversidade, Equidade e Acessibilidade",
    "Inclusão, Diversidade, Equidade, Acessibilidade"
]

def encontrar_descritor(titulo, descricao, descritores):
    texto = (titulo or "") + " " + (descricao or "")
    for descritor in descritores:
        if descritor.lower() in texto.lower():
            return descritor
    return ""

def extrair_ofertas_do_curso(id_curso):
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"
    try:
        resp = requests.get(url_curso, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")
        ofertas = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            # Verifica tanto links absolutos quanto relativos
            if "/cursos/oferta/" in href or "../oferta/" in href:
                # Extrai o ID da oferta do final da URL
                if "/cursos/oferta/" in href:
                    id_oferta = href.split("/")[-1]
                elif "../oferta/" in href:
                    id_oferta = href.split("/")[-1]
                
                if id_oferta.isdigit():
                    ofertas.append(id_oferta)
        return list(set(ofertas))  # Remove duplicados
    except Exception as e:
        print(f"Erro ao buscar ofertas do curso {id_curso}: {e}")
        return []

def extrair_dados_oferta(id_oferta):
    url_oferta = f"https://www.unasus.gov.br/cursos/oferta/{id_oferta}"
    try:
        resp = requests.get(url_oferta, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")
        dados = {"id_oferta": id_oferta, "url_oferta": url_oferta}
        # Exemplo de extração (ajuste conforme o HTML real):
        # Código da oferta
        dados["codigo_oferta"] = id_oferta
        # Número de vagas
        vagas = soup.find(string=lambda t: t and "Vagas" in t)
        if vagas:
            try:
                dados["vagas"] = vagas.parent.find_next("td").text.strip()
            except:
                dados["vagas"] = ""
        else:
            dados["vagas"] = ""
        # Público-alvo
        publico = soup.find(string=lambda t: t and "Público-alvo" in t)
        if publico:
            try:
                dados["publico_alvo"] = publico.parent.find_next("td").text.strip()
            except:
                dados["publico_alvo"] = ""
        else:
            dados["publico_alvo"] = ""
        # Local da oferta
        local = soup.find(string=lambda t: t and "Local" in t)
        if local:
            try:
                dados["local_oferta"] = local.parent.find_next("td").text.strip()
            except:
                dados["local_oferta"] = ""
        else:
            dados["local_oferta"] = ""
        # Formato
        formato = soup.find(string=lambda t: t and "Formato" in t)
        if formato:
            try:
                dados["formato"] = formato.parent.find_next("td").text.strip()
            except:
                dados["formato"] = ""
        else:
            dados["formato"] = ""
        # Programas de governo
        programas = soup.find(string=lambda t: t and "Programas de governo" in t)
        if programas:
            try:
                dados["programas_governo"] = programas.parent.find_next("td").text.strip()
            except:
                dados["programas_governo"] = ""
        else:
            dados["programas_governo"] = ""
        # Temas
        temas = soup.find(string=lambda t: t and "Temas" in t)
        if temas:
            try:
                dados["temas"] = temas.parent.find_next("td").text.strip()
            except:
                dados["temas"] = ""
        else:
            dados["temas"] = ""
        # DeCs
        decs = soup.find(string=lambda t: t and "DeCs" in t)
        if decs:
            try:
                dados["decs"] = decs.parent.find_next("td").text.strip()
            except:
                dados["decs"] = ""
        else:
            dados["decs"] = ""
        # Descrição da oferta
        descricao = soup.find(string=lambda t: t and "Descrição da oferta" in t)
        if descricao:
            try:
                dados["descricao_oferta"] = descricao.parent.find_next("td").text.strip()
            except:
                dados["descricao_oferta"] = ""
        else:
            dados["descricao_oferta"] = ""
        # Palavras-chave
        palavras = soup.find(string=lambda t: t and "Palavras-chave" in t)
        if palavras:
            try:
                dados["palavras_chave"] = palavras.parent.find_next("td").text.strip()
            except:
                dados["palavras_chave"] = ""
        else:
            dados["palavras_chave"] = ""
        return dados
    except Exception as e:
        print(f"Erro ao buscar dados da oferta {id_oferta}: {e}")
        return {"id_oferta": id_oferta, "erro": str(e)}

def carregar_ids_processados(csv_path):
    if not os.path.exists(csv_path):
        return set()
    try:
        df_existente = pd.read_csv(csv_path, encoding="utf-8-sig")
        # Verifica qual coluna de ID existe
        if "co_seq_curso" in df_existente.columns:
            return set(df_existente["co_seq_curso"].astype(str).unique())
        elif "id_curso" in df_existente.columns:
            return set(df_existente["id_curso"].astype(str).unique())
        elif "co_curso" in df_existente.columns:
            return set(df_existente["co_curso"].astype(str).unique())
        else:
            print("Nenhuma coluna de ID de curso encontrada no CSV existente")
            return set()
    except Exception as e:
        print(f"Erro ao carregar CSV existente: {e}")
        return set()

todos_detalhes = []
pagina = 0
csv_path = "unasus_ofertas_detalhadas.csv"
lote = 10  # Salva a cada 10 cursos
cursos_processados = carregar_ids_processados(csv_path)
print(f"Cursos já processados: {len(cursos_processados)}")
print(f"Arquivo de saída: {csv_path}")

while True:
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        data = resp.json()
        itens = data.get("results", {}).get("itens", [])
        if not itens:
            break
        for curso in itens:
            id_curso = curso.get("co_seq_curso") or curso.get("id_curso") or curso.get("co_curso") or curso.get("id")
            if not id_curso:
                continue
            id_curso_str = str(id_curso)
            if id_curso_str in cursos_processados:
                continue  # Pula cursos já processados
            titulo = curso.get("no_curso", "")
            descricao = curso.get("ds_curso", "")
            encontrado = encontrar_descritor(titulo, descricao, descritores)
            curso["tem_deia"] = "Sim" if encontrado else "Não"
            curso["deia_encontrado"] = encontrado
            ofertas = extrair_ofertas_do_curso(id_curso)
            if not ofertas:
                todos_detalhes.append({**curso, "id_oferta": "", "erro": "Sem ofertas encontradas"})
            for id_oferta in ofertas:
                dados_oferta = extrair_dados_oferta(id_oferta)
                linha = {**curso, **dados_oferta}
                todos_detalhes.append(linha)
                time.sleep(1)
            cursos_processados.add(id_curso_str)
            # Salvamento incremental
            if len(todos_detalhes) >= lote:
                if os.path.exists(csv_path):
                    df_existente = pd.read_csv(csv_path, encoding="utf-8-sig")
                    df_novo = pd.DataFrame(todos_detalhes)
                    df_final = pd.concat([df_existente, df_novo], ignore_index=True)
                else:
                    df_final = pd.DataFrame(todos_detalhes)
                df_final.to_csv(csv_path, index=False, encoding="utf-8-sig")
                print(f"Progresso salvo após {len(cursos_processados)} cursos em {csv_path}")
                todos_detalhes = []
        pagina += 1
        print(f"Página {pagina} processada.")
        proximo = data.get("results", {}).get("proximo")
        if not proximo:
            break
        payload["proximo"] = proximo
        time.sleep(1)
    except Exception as e:
        print(f"Erro de conexão: {e}. Tentando novamente em 30 segundos...")
        time.sleep(30)
        continue

# Salva o restante
if todos_detalhes:
    if os.path.exists(csv_path):
        df_existente = pd.read_csv(csv_path, encoding="utf-8-sig")
        df_novo = pd.DataFrame(todos_detalhes)
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
    else:
        df_final = pd.DataFrame(todos_detalhes)
    df_final.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Finalizado! Todos os dados salvos em {csv_path}")
else:
    print("Nenhum dado detalhado coletado.")

import pandas as pd

csv_path = "unasus_ofertas_detalhadas.csv"
try:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    print(df.head())  # Mostra as 5 primeiras linhas
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")