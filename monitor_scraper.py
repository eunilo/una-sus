#!/usr/bin/env python3
"""
Script de monitoramento para o scraper UNA-SUS.
Permite acompanhar o progresso em tempo real e gerar relatórios.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, Optional

import pandas as pd


def carregar_checkpoint() -> Optional[Dict]:
    """Carrega o checkpoint atual do scraper."""
    checkpoint_file = "checkpoint.json"
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar checkpoint: {e}")
    return None


def analisar_csv(csv_path: str) -> Dict:
    """Analisa o arquivo CSV e retorna estatísticas."""
    if not os.path.exists(csv_path):
        return {"erro": "Arquivo CSV não encontrado"}

    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        stats = {
            "total_registros": len(df),
            "colunas": list(df.columns),
            "cursos_unicos": 0,
            "ofertas_unicas": 0,
            "cursos_com_deia": 0,
            "cursos_sem_deia": 0,
            "ultima_atualizacao": datetime.fromtimestamp(
                os.path.getmtime(csv_path)
            ).strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Contar cursos únicos
        for col in ["co_seq_curso", "id_curso", "co_curso"]:
            if col in df.columns:
                stats["cursos_unicos"] = df[col].nunique()
                break

        # Contar ofertas únicas
        if "id_oferta" in df.columns:
            stats["ofertas_unicas"] = df["id_oferta"].nunique()

        # Estatísticas DEIA
        if "tem_deia" in df.columns:
            deia_counts = df["tem_deia"].value_counts()
            stats["cursos_com_deia"] = deia_counts.get("Sim", 0)
            stats["cursos_sem_deia"] = deia_counts.get("Não", 0)

        return stats
    except Exception as e:
        return {"erro": f"Erro ao analisar CSV: {e}"}


def mostrar_progresso():
    """Mostra o progresso atual do scraper."""
    print("=" * 60)
    print("MONITORAMENTO DO SCRAPER UNA-SUS")
    print("=" * 60)

    # Carregar checkpoint
    checkpoint = carregar_checkpoint()
    if checkpoint:
        print(f"📊 CHECKPOINT ATUAL:")
        print(f"   Página: {checkpoint.get('pagina_atual', 0)}")
        print(f"   Cursos processados: {checkpoint.get('cursos_processados', 0)}")
        print(f"   Ofertas processadas: {checkpoint.get('ofertas_processadas', 0)}")
        print(f"   Última atualização: {checkpoint.get('ultima_atualizacao', 'N/A')}")
        print()

    # Analisar CSV
    csv_stats = analisar_csv("unasus_ofertas_detalhadas.csv")
    if "erro" not in csv_stats:
        print(f"📁 ARQUIVO CSV:")
        print(f"   Total de registros: {csv_stats['total_registros']:,}")
        print(f"   Cursos únicos: {csv_stats['cursos_unicos']:,}")
        print(f"   Ofertas únicas: {csv_stats['ofertas_unicas']:,}")
        print(f"   Cursos com DEIA: {csv_stats['cursos_com_deia']:,}")
        print(f"   Cursos sem DEIA: {csv_stats['cursos_sem_deia']:,}")
        print(f"   Última atualização: {csv_stats['ultima_atualizacao']}")
        print()

        # Calcular progresso estimado
        if checkpoint and csv_stats["cursos_unicos"] > 0:
            progresso = (
                csv_stats["cursos_unicos"] / (csv_stats["cursos_unicos"] + 1000)
            ) * 100  # Estimativa
            print(f"📈 PROGRESSO ESTIMADO: {progresso:.1f}%")
    else:
        print(f"❌ ERRO: {csv_stats['erro']}")

    print("=" * 60)


def mostrar_logs_recentes():
    """Mostra os logs mais recentes."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        print("📝 Nenhum log encontrado.")
        return

    # Encontrar o log mais recente
    log_files = [f for f in os.listdir(log_dir) if f.endswith(".log")]
    if not log_files:
        print("📝 Nenhum arquivo de log encontrado.")
        return

    log_files.sort(reverse=True)
    log_file = os.path.join(log_dir, log_files[0])

    print(f"📝 ÚLTIMAS LINHAS DO LOG ({log_files[0]}):")
    print("-" * 60)

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Mostrar as últimas 10 linhas
            for line in lines[-10:]:
                print(line.strip())
    except Exception as e:
        print(f"Erro ao ler log: {e}")


def gerar_relatorio():
    """Gera um relatório detalhado."""
    print("📋 GERANDO RELATÓRIO DETALHADO...")
    print("=" * 60)

    csv_stats = analisar_csv("unasus_ofertas_detalhadas.csv")
    if "erro" in csv_stats:
        print(f"❌ {csv_stats['erro']}")
        return

    checkpoint = carregar_checkpoint()

    # Relatório
    relatorio = {
        "timestamp": datetime.now().isoformat(),
        "checkpoint": checkpoint,
        "csv_stats": csv_stats,
    }

    # Salvar relatório
    relatorio_file = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(relatorio_file, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    print(f"✅ Relatório salvo em: {relatorio_file}")

    # Mostrar resumo
    print(f"\n📊 RESUMO:")
    print(f"   Total de registros: {csv_stats['total_registros']:,}")
    print(f"   Cursos únicos: {csv_stats['cursos_unicos']:,}")
    print(f"   Ofertas únicas: {csv_stats['ofertas_unicas']:,}")
    if checkpoint:
        print(f"   Página atual: {checkpoint.get('pagina_atual', 0)}")


def main():
    """Função principal do monitor."""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        mostrar_progresso()
        mostrar_logs_recentes()

        print("\n🔄 Atualizando em 30 segundos... (Ctrl+C para sair)")
        print("Opções:")
        print("  r - Gerar relatório")
        print("  q - Sair")

        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n👋 Monitoramento finalizado.")
            break


if __name__ == "__main__":
    main()
