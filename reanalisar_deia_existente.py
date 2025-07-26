import pandas as pd
import logging
from scraper_unasus_melhorado import encontrar_descritor_deia_melhorado, DESCRITORES_DEIA

def setup_logging():
    """Configura o sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('reanalise_deia.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def reanalisar_deia_existente(arquivo_entrada: str, arquivo_saida: str):
    """Reanalisa os dados existentes com a busca DEIA melhorada."""
    logger = setup_logging()
    logger.info("=== INICIANDO REANÁLISE DEIA ===")
    
    try:
        # Carrega os dados existentes
        df = pd.read_csv(arquivo_entrada, encoding="utf-8-sig")
        logger.info(f"Carregados {len(df)} registros do arquivo {arquivo_entrada}")
        
        # Conta registros originais
        if "tem_deia" in df.columns:
            deia_original = df["tem_deia"].value_counts()
            logger.info(f"DEIA original - Sim: {deia_original.get('Sim', 0)}, Não: {deia_original.get('Não', 0)}")
        
        # Coleta todos os textos para análise
        textos_para_analise = []
        
        for idx, row in df.iterrows():
            if idx % 100 == 0:
                logger.info(f"Processando registro {idx + 1}/{len(df)}")
            
            # Coleta todos os campos de texto
            campos_texto = []
            
            # Campos básicos
            if pd.notna(row.get("no_curso")):
                campos_texto.append(f"Título: {row['no_curso']}")
            
            if pd.notna(row.get("ds_curso")):
                campos_texto.append(f"Descrição do curso: {row['ds_curso']}")
            
            if pd.notna(row.get("descricao_oferta")):
                campos_texto.append(f"Descrição da oferta: {row['descricao_oferta']}")
            
            if pd.notna(row.get("palavras_chave")):
                campos_texto.append(f"Palavras-chave: {row['palavras_chave']}")
            
            if pd.notna(row.get("publico_alvo")):
                campos_texto.append(f"Público-alvo: {row['publico_alvo']}")
            
            if pd.notna(row.get("temas")):
                campos_texto.append(f"Temas: {row['temas']}")
            
            if pd.notna(row.get("decs")):
                campos_texto.append(f"DeCs: {row['decs']}")
            
            if pd.notna(row.get("programas_governo")):
                campos_texto.append(f"Programas de governo: {row['programas_governo']}")
            
            # Combina todos os textos
            texto_completo = " ".join(campos_texto)
            
            # Busca descritores DEIA
            descritor_encontrado = encontrar_descritor_deia_melhorado(texto_completo)
            
            # Atualiza o DataFrame
            df.at[idx, "tem_deia"] = "Sim" if descritor_encontrado else "Não"
            df.at[idx, "deia_encontrado"] = descritor_encontrado
            df.at[idx, "texto_analisado_deia"] = texto_completo[:1000]  # Primeiros 1000 caracteres
            
            if descritor_encontrado:
                logger.info(f"DEIA encontrado no registro {idx + 1}: {descritor_encontrado}")
                logger.info(f"  Curso: {row.get('no_curso', 'N/A')}")
        
        # Salva os resultados
        df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")
        logger.info(f"Resultados salvos em {arquivo_saida}")
        
        # Gera estatísticas finais
        if "tem_deia" in df.columns:
            deia_final = df["tem_deia"].value_counts()
            logger.info("=== ESTATÍSTICAS FINAIS ===")
            logger.info(f"Cursos com DEIA: {deia_final.get('Sim', 0)}")
            logger.info(f"Cursos sem DEIA: {deia_final.get('Não', 0)}")
            
            # Mostra exemplos de cursos com DEIA
            if deia_final.get('Sim', 0) > 0:
                cursos_deia = df[df["tem_deia"] == "Sim"]
                logger.info("Exemplos de cursos com DEIA encontrados:")
                for _, curso in cursos_deia.head(10).iterrows():
                    logger.info(f"  - {curso.get('no_curso', 'N/A')}")
                    logger.info(f"    Descritor: {curso.get('deia_encontrado', 'N/A')}")
                    logger.info(f"    ID: {curso.get('co_seq_curso', 'N/A')}")
                    logger.info("")
        
        logger.info("=== REANÁLISE FINALIZADA ===")
        
    except Exception as e:
        logger.error(f"Erro durante a reanálise: {e}")

if __name__ == "__main__":
    # Reanalisa o arquivo existente
    reanalisar_deia_existente(
        "unasus_ofertas_detalhadas.csv",
        "unasus_ofertas_reanalisadas_deia.csv"
    ) 