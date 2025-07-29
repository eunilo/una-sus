#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATABASE COMPLETO UNA-SUS
========================

Sistema de database que mantém TODOS os dados originais em uma estrutura completa,
sem separação em tabelas, preservando a visão geral dos dados.
"""

import json
import logging
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd


class DatabaseCompleto:
    """
    Sistema de database completo para dados UNA-SUS.

    Mantém todos os dados originais em uma estrutura única,
    preservando a visão geral e facilitando análises.
    """

    def __init__(self, db_path: str = "database_completo.db"):
        """
        Inicializa o database completo.

        Args:
            db_path: Caminho para o arquivo SQLite
        """
        self.db_path = db_path
        self.logger = self._configurar_logger()

        # Criar diretório se não existir
        os.makedirs(
            os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True
        )

        # Inicializar database
        self._criar_tabela_completa()

    def _configurar_logger(self) -> logging.Logger:
        """Configura o logger."""
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        return logging.getLogger(__name__)

    def _criar_tabela_completa(self):
        """Cria uma tabela única com todos os dados."""
        self.logger.info("🔧 Criando tabela completa...")

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Tabela única com todos os campos originais
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS dados_completos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    co_seq_curso INTEGER,
                    no_curso TEXT,
                    qt_carga_horaria_total INTEGER,
                    co_seq_orgao INTEGER,
                    sg_orgao TEXT,
                    no_orgao TEXT,
                    no_formato TEXT,
                    no_nivel TEXT,
                    no_modalidade TEXT,
                    ds_imagem TEXT,
                    status TEXT,
                    status_ordem INTEGER,
                    rank INTEGER,
                    tem_deia TEXT,
                    deia_encontrado TEXT,
                    id_oferta INTEGER,
                    url_oferta TEXT,
                    codigo_oferta TEXT,
                    vagas INTEGER,
                    publico_alvo TEXT,
                    local_oferta TEXT,
                    formato TEXT,
                    programas_governo TEXT,
                    temas TEXT,
                    decs TEXT,
                    descricao_oferta TEXT,
                    palavras_chave TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Tabela de logs
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS logs_coleta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    mensagem TEXT,
                    registros_processados INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Índices para melhor performance
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_curso ON dados_completos(co_seq_curso)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_orgao ON dados_completos(co_seq_orgao)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_status ON dados_completos(status)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_modalidade ON dados_completos(no_modalidade)"
            )

            conn.commit()
            self.logger.info("✅ Tabela completa criada com sucesso!")

    def carregar_dados_completos(
        self, arquivo_csv: str = "unasus_ofertas_detalhadas.csv"
    ):
        """
        Carrega todos os dados originais para o database.

        Args:
            arquivo_csv: Caminho para o arquivo CSV
        """
        if not os.path.exists(arquivo_csv):
            self.logger.error(f"❌ Arquivo {arquivo_csv} não encontrado!")
            return False

        self.logger.info(f"📁 Carregando dados completos de: {arquivo_csv}")

        try:
            # Carregar CSV original
            df = pd.read_csv(arquivo_csv)
            self.logger.info(f"📊 {len(df)} registros carregados")

            with sqlite3.connect(self.db_path) as conn:
                # Limpar tabela existente
                cursor = conn.cursor()
                cursor.execute("DELETE FROM dados_completos")

                # Inserir todos os dados
                df.to_sql("dados_completos", conn, if_exists="append", index=False)

                # Registrar log
                self._registrar_log(
                    "CARGA_COMPLETA",
                    f"Dados completos carregados: {len(df)} registros",
                    len(df),
                    conn,
                )

            self.logger.info("✅ Dados completos carregados com sucesso!")
            return True

        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar dados: {e}")
            return False

    def _registrar_log(
        self, tipo: str, mensagem: str, registros: int, conn: sqlite3.Connection
    ):
        """Registra log de operação."""
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO logs_coleta (tipo, mensagem, registros_processados)
            VALUES (?, ?, ?)
        """,
            (tipo, mensagem, registros),
        )
        conn.commit()

    def obter_estatisticas_completas(self) -> Dict:
        """Obtém estatísticas completas do database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            stats = {}

            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM dados_completos")
            stats["total_registros"] = cursor.fetchone()[0]

            # Estatísticas por status
            cursor.execute(
                "SELECT status, COUNT(*) FROM dados_completos GROUP BY status"
            )
            stats["ofertas_por_status"] = dict(cursor.fetchall())

            # Estatísticas por instituição
            cursor.execute(
                """
                SELECT no_orgao, COUNT(*) as total_ofertas, COUNT(DISTINCT co_seq_curso) as total_cursos
                FROM dados_completos 
                GROUP BY no_orgao 
                ORDER BY total_cursos DESC 
                LIMIT 10
            """
            )
            stats["top_instituicoes"] = [
                dict(zip(["instituicao", "ofertas", "cursos"], row))
                for row in cursor.fetchall()
            ]

            # Estatísticas por modalidade
            cursor.execute(
                "SELECT no_modalidade, COUNT(*) FROM dados_completos GROUP BY no_modalidade"
            )
            stats["ofertas_por_modalidade"] = dict(cursor.fetchall())

            # Estatísticas de carga horária
            cursor.execute(
                """
                SELECT 
                    AVG(qt_carga_horaria_total) as media,
                    MIN(qt_carga_horaria_total) as minima,
                    MAX(qt_carga_horaria_total) as maxima
                FROM dados_completos 
                WHERE qt_carga_horaria_total IS NOT NULL
            """
            )
            row = cursor.fetchone()
            stats["carga_horaria"] = {
                "media": row[0],
                "minima": row[1],
                "maxima": row[2],
            }

            # Estatísticas DEIA
            cursor.execute(
                "SELECT tem_deia, COUNT(*) FROM dados_completos GROUP BY tem_deia"
            )
            stats["deia"] = dict(cursor.fetchall())

            return stats

    def exportar_dados_completos(
        self, formato: str = "csv", diretorio: str = "exports"
    ):
        """
        Exporta todos os dados completos.

        Args:
            formato: Formato de exportação (csv, json)
            diretorio: Diretório de destino
        """
        os.makedirs(diretorio, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        with sqlite3.connect(self.db_path) as conn:
            # Carregar todos os dados
            df = pd.read_sql_query("SELECT * FROM dados_completos", conn)

            if formato == "csv":
                arquivo = f"{diretorio}/database_completo_{timestamp}.csv"
                df.to_csv(arquivo, index=False, encoding="utf-8-sig")
            elif formato == "json":
                arquivo = f"{diretorio}/database_completo_{timestamp}.json"
                df.to_json(arquivo, orient="records", force_ascii=False, indent=2)

            self.logger.info(f"📤 Database completo exportado: {arquivo}")

            # Criar resumo estruturado
            self._criar_resumo_completo(df, diretorio, timestamp)

    def _criar_resumo_completo(self, df: pd.DataFrame, diretorio: str, timestamp: str):
        """
        Cria um resumo completo dos dados.

        Args:
            df: DataFrame com dados completos
            diretorio: Diretório de destino
            timestamp: Timestamp para nome do arquivo
        """
        self.logger.info("📋 Criando resumo completo...")

        resumo = {
            "metadata": {
                "timestamp": timestamp,
                "total_registros": len(df),
                "total_cursos": df["co_seq_curso"].nunique(),
                "total_instituicoes": df["co_seq_orgao"].nunique(),
                "total_ofertas": (
                    df["id_oferta"].nunique() if "id_oferta" in df.columns else 0
                ),
                "campos_disponiveis": list(df.columns),
            },
            "estatisticas_gerais": {
                "ofertas_por_status": df["status"].value_counts().to_dict(),
                "cursos_por_instituicao": df.groupby("no_orgao")["co_seq_curso"]
                .nunique()
                .to_dict(),
                "modalidades": df["no_modalidade"].value_counts().to_dict(),
                "niveis": (
                    df["no_nivel"].value_counts().to_dict()
                    if "no_nivel" in df.columns
                    else {}
                ),
                "formatos": (
                    df["no_formato"].value_counts().to_dict()
                    if "no_formato" in df.columns
                    else {}
                ),
            },
            "carga_horaria": {
                "media": df["qt_carga_horaria_total"].mean(),
                "minima": df["qt_carga_horaria_total"].min(),
                "maxima": df["qt_carga_horaria_total"].max(),
                "distribuicao": df["qt_carga_horaria_total"]
                .value_counts()
                .head(10)
                .to_dict(),
            },
            "deia": {
                "total_com_deia": (
                    df[df["tem_deia"] == "Sim"].shape[0]
                    if "tem_deia" in df.columns
                    else 0
                ),
                "percentual_deia": (
                    (df[df["tem_deia"] == "Sim"].shape[0] / len(df) * 100)
                    if "tem_deia" in df.columns
                    else 0
                ),
            },
            "top_instituicoes": df.groupby("no_orgao")
            .agg({"co_seq_curso": "nunique", "id_oferta": "count"})
            .sort_values("co_seq_curso", ascending=False)
            .head(10)
            .to_dict("index"),
            "top_cursos": df.groupby("no_curso")
            .agg({"id_oferta": "count"})
            .sort_values("id_oferta", ascending=False)
            .head(10)
            .to_dict("index"),
        }

        # Salvar resumo em JSON
        arquivo_resumo = f"{diretorio}/resumo_completo_{timestamp}.json"
        with open(arquivo_resumo, "w", encoding="utf-8") as f:
            json.dump(resumo, f, indent=2, ensure_ascii=False, default=str)

        self.logger.info(f"📤 Resumo completo salvo: {arquivo_resumo}")

        # Criar arquivos de análise específicos
        self._criar_analises_especificas(df, diretorio, timestamp)

    def _criar_analises_especificas(
        self, df: pd.DataFrame, diretorio: str, timestamp: str
    ):
        """
        Cria análises específicas dos dados.

        Args:
            df: DataFrame com dados completos
            diretorio: Diretório de destino
            timestamp: Timestamp para nome do arquivo
        """
        self.logger.info("📊 Criando análises específicas...")

        # Análise por instituição
        analise_instituicoes = (
            df.groupby("no_orgao")
            .agg(
                {
                    "co_seq_curso": "nunique",
                    "id_oferta": "count",
                    "qt_carga_horaria_total": "mean",
                    "status": lambda x: (x == "com oferta aberta").sum(),
                    "tem_deia": lambda x: (x == "Sim").sum(),
                }
            )
            .rename(
                columns={
                    "co_seq_curso": "total_cursos",
                    "id_oferta": "total_ofertas",
                    "qt_carga_horaria_total": "carga_horaria_media",
                    "status": "ofertas_abertas",
                    "tem_deia": "cursos_com_deia",
                }
            )
            .reset_index()
        )

        arquivo_instituicoes = f"{diretorio}/analise_instituicoes_{timestamp}.csv"
        analise_instituicoes.to_csv(
            arquivo_instituicoes, index=False, encoding="utf-8-sig"
        )

        # Análise por curso
        analise_cursos = (
            df.groupby(["no_curso", "no_orgao"])
            .agg(
                {
                    "id_oferta": "count",
                    "qt_carga_horaria_total": "first",
                    "tem_deia": "first",
                    "no_modalidade": "first",
                    "status": lambda x: (x == "com oferta aberta").sum(),
                }
            )
            .rename(
                columns={
                    "id_oferta": "total_ofertas",
                    "qt_carga_horaria_total": "carga_horaria",
                    "tem_deia": "tem_deia",
                    "no_modalidade": "modalidade",
                    "status": "ofertas_abertas",
                }
            )
            .reset_index()
        )

        arquivo_cursos = f"{diretorio}/analise_cursos_{timestamp}.csv"
        analise_cursos.to_csv(arquivo_cursos, index=False, encoding="utf-8-sig")

        # Análise temporal (se houver datas)
        if "dt_inicio_inscricao" in df.columns:
            df_temporal = df.copy()
            df_temporal["ano"] = pd.to_datetime(
                df_temporal["dt_inicio_inscricao"], errors="coerce"
            ).dt.year

            analise_temporal = (
                df_temporal.groupby("ano")
                .agg(
                    {
                        "id_oferta": "count",
                        "co_seq_curso": "nunique",
                        "no_orgao": "nunique",
                    }
                )
                .rename(
                    columns={
                        "id_oferta": "total_ofertas",
                        "co_seq_curso": "total_cursos",
                        "no_orgao": "total_instituicoes",
                    }
                )
                .reset_index()
            )

            arquivo_temporal = f"{diretorio}/analise_temporal_{timestamp}.csv"
            analise_temporal.to_csv(arquivo_temporal, index=False, encoding="utf-8-sig")

        self.logger.info(f"📤 Análises específicas criadas:")
        self.logger.info(f"   • {arquivo_instituicoes}")
        self.logger.info(f"   • {arquivo_cursos}")
        if "dt_inicio_inscricao" in df.columns:
            self.logger.info(f"   • {arquivo_temporal}")


def main():
    """Função principal."""
    print("🚀 INICIALIZANDO DATABASE COMPLETO UNA-SUS")
    print("=" * 50)

    # Criar database completo
    db = DatabaseCompleto()

    # Carregar dados completos
    if db.carregar_dados_completos():
        # Obter estatísticas
        stats = db.obter_estatisticas_completas()

        print(f"\n📊 ESTATÍSTICAS DO DATABASE COMPLETO:")
        print(f"   • Total de registros: {stats['total_registros']:,}")

        print(f"\n🎯 OFERTAS POR STATUS:")
        for status, count in stats["ofertas_por_status"].items():
            print(f"   • {status}: {count:,}")

        print(f"\n🏢 TOP INSTITUIÇÕES:")
        for inst in stats["top_instituicoes"][:5]:
            print(
                f"   • {inst['instituicao']}: {inst['cursos']} cursos, {inst['ofertas']} ofertas"
            )

        print(f"\n📈 CARGA HORÁRIA:")
        carga = stats["carga_horaria"]
        print(f"   • Média: {carga['media']:.0f} horas")
        print(f"   • Mínima: {carga['minima']:.0f} horas")
        print(f"   • Máxima: {carga['maxima']:.0f} horas")

        # Exportar dados completos
        print(f"\n📤 Exportando dados completos...")
        db.exportar_dados_completos("csv")

        print(f"\n✅ DATABASE COMPLETO CRIADO COM SUCESSO!")
        print(f"   • Arquivo: database_completo.db")
        print(f"   • Dados exportados em: exports/")
        print(f"   • Mantém TODOS os campos originais")
        print(f"   • Visão geral preservada")
    else:
        print("❌ Erro ao criar database completo!")


if __name__ == "__main__":
    main()
