import pandas as pd
from scraper_unasus_melhorado import encontrar_descritor_deia_melhorado, DESCRITORES_DEIA

def testar_busca_deia():
    """Testa a busca DEIA com exemplos."""
    print("=== TESTE DE BUSCA DEIA MELHORADA ===")
    print(f"Total de descritores DEIA: {len(DESCRITORES_DEIA)}")
    print()
    
    # Exemplos de texto para teste
    exemplos = [
        {
            "titulo": "Saúde Mental e Diversidade na Atenção Primária",
            "descricao": "Curso sobre abordagem inclusiva e equitativa para populações vulneráveis",
            "palavras_chave": "saúde mental, diversidade, inclusão, equidade"
        },
        {
            "titulo": "Atenção à Saúde da População Negra",
            "descricao": "Formação para profissionais de saúde sobre equidade racial",
            "palavras_chave": "população negra, equidade, saúde"
        },
        {
            "titulo": "Saúde da Pessoa com Deficiência",
            "descricao": "Curso sobre acessibilidade e inclusão na atenção à saúde",
            "palavras_chave": "deficiência, acessibilidade, inclusão"
        },
        {
            "titulo": "Saúde LGBTQI+ na Atenção Básica",
            "descricao": "Formação sobre diversidade sexual e de gênero",
            "palavras_chave": "LGBTQI+, diversidade, saúde"
        },
        {
            "titulo": "Atenção à Saúde do Idoso",
            "descricao": "Curso sobre cuidados geriátricos",
            "palavras_chave": "idoso, geriatria, cuidados"
        },
        {
            "titulo": "Saúde da População Indígena",
            "descricao": "Atenção diferenciada à saúde indígena",
            "palavras_chave": "indígena, saúde, atenção diferenciada"
        },
        {
            "titulo": "Atenção à População em Situação de Rua",
            "descricao": "Cuidados de saúde para pessoas em vulnerabilidade social",
            "palavras_chave": "população de rua, vulnerabilidade, saúde"
        },
        {
            "titulo": "Saúde da Mulher",
            "descricao": "Atenção integral à saúde feminina",
            "palavras_chave": "mulher, saúde feminina, atenção integral"
        },
        {
            "titulo": "Curso Básico de Enfermagem",
            "descricao": "Formação técnica em enfermagem",
            "palavras_chave": "enfermagem, formação técnica"
        },
        {
            "titulo": "Atenção Primária à Saúde",
            "descricao": "Fundamentos da APS",
            "palavras_chave": "atenção primária, saúde"
        }
    ]
    
    resultados = []
    
    for i, exemplo in enumerate(exemplos, 1):
        print(f"Exemplo {i}: {exemplo['titulo']}")
        
        # Combina todos os textos
        texto_completo = f"{exemplo['titulo']} {exemplo['descricao']} {exemplo['palavras_chave']}"
        
        # Busca descritores DEIA
        descritor_encontrado = encontrar_descritor_deia_melhorado(texto_completo)
        
        resultado = {
            "exemplo": i,
            "titulo": exemplo["titulo"],
            "tem_deia": "Sim" if descritor_encontrado else "Não",
            "descritor_encontrado": descritor_encontrado
        }
        resultados.append(resultado)
        
        print(f"  Tem DEIA: {resultado['tem_deia']}")
        if descritor_encontrado:
            print(f"  Descritor: {descritor_encontrado}")
        print()
    
    # Cria DataFrame com resultados
    df_resultados = pd.DataFrame(resultados)
    
    # Estatísticas
    total_exemplos = len(resultados)
    com_deia = len(df_resultados[df_resultados["tem_deia"] == "Sim"])
    sem_deia = len(df_resultados[df_resultados["tem_deia"] == "Não"])
    
    print("=== ESTATÍSTICAS DOS TESTES ===")
    print(f"Total de exemplos: {total_exemplos}")
    print(f"Com DEIA: {com_deia}")
    print(f"Sem DEIA: {sem_deia}")
    print(f"Taxa de detecção: {(com_deia/total_exemplos)*100:.1f}%")
    print()
    
    # Mostra exemplos com DEIA encontrado
    if com_deia > 0:
        print("Exemplos com DEIA detectado:")
        for _, row in df_resultados[df_resultados["tem_deia"] == "Sim"].iterrows():
            print(f"  - {row['titulo']}: {row['descritor_encontrado']}")
        print()
    
    # Mostra exemplos sem DEIA
    if sem_deia > 0:
        print("Exemplos sem DEIA detectado:")
        for _, row in df_resultados[df_resultados["tem_deia"] == "Não"].iterrows():
            print(f"  - {row['titulo']}")
        print()
    
    # Salva resultados
    df_resultados.to_csv("teste_busca_deia_resultados.csv", index=False, encoding="utf-8-sig")
    print("Resultados salvos em 'teste_busca_deia_resultados.csv'")

if __name__ == "__main__":
    testar_busca_deia() 