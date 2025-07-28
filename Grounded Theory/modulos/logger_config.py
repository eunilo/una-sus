"""
📝 Módulo de configuração de logging para o sistema Grounded Theory.

Este módulo fornece configurações padronizadas de logging para todos os componentes
do sistema, com diferentes níveis de detalhamento e formatação.
"""

import logging
import os
from datetime import datetime
from typing import Optional


class LoggerConfig:
    """Configurador centralizado de logging para o sistema."""

    # Cores para terminal (ANSI)
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    # Emojis para diferentes tipos de log
    EMOJIS = {
        "DEBUG": "🔍",
        "INFO": "ℹ️",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "CRITICAL": "🚨",
        "SUCCESS": "✅",
        "PROGRESS": "🔄",
        "COMPLETE": "🎉",
        "DATA": "📊",
        "ANALYSIS": "🧠",
        "COLLECTION": "📥",
        "PROCESSING": "⚙️",
        "SAVING": "💾",
        "LOADING": "📂",
    }

    @classmethod
    def setup_logger(
        cls,
        name: str,
        log_level: str = "INFO",
        log_to_file: bool = True,
        log_to_console: bool = True,
        detailed_format: bool = True,
    ) -> logging.Logger:
        """
        Configura um logger com formatação personalizada.

        Args:
            name: Nome do logger
            log_level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Se deve salvar logs em arquivo
            log_to_console: Se deve exibir logs no console
            detailed_format: Se deve usar formato detalhado

        Returns:
            Logger configurado
        """
        # Criar diretório de logs se não existir
        os.makedirs("logs", exist_ok=True)

        # Configurar logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level.upper()))

        # Limpar handlers existentes para evitar duplicação
        logger.handlers.clear()

        # Formato base
        if detailed_format:
            base_format = "%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s"
        else:
            base_format = "%(asctime)s | %(levelname)-8s | %(message)s"

        # Handler para arquivo
        if log_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/{name.lower()}_{timestamp}.log"

            file_handler = logging.FileHandler(filename, encoding="utf-8")
            file_handler.setLevel(getattr(logging, log_level.upper()))

            file_formatter = logging.Formatter(base_format)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        # Handler para console
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, log_level.upper()))

            # Formato colorido para console
            if detailed_format:
                console_format = (
                    "%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s"
                )
            else:
                console_format = "%(asctime)s | %(levelname)-8s | %(message)s"

            console_formatter = ColoredFormatter(console_format)
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

        return logger

    @classmethod
    def get_workflow_logger(cls) -> logging.Logger:
        """Retorna logger configurado para workflow interativo."""
        return cls.setup_logger(
            "WorkflowInterativo", log_level="INFO", detailed_format=True
        )

    @classmethod
    def get_gt_logger(cls) -> logging.Logger:
        """Retorna logger configurado para Grounded Theory."""
        return cls.setup_logger(
            "GroundedTheory", log_level="INFO", detailed_format=True
        )

    @classmethod
    def get_collection_logger(cls) -> logging.Logger:
        """Retorna logger configurado para coleta de dados."""
        return cls.setup_logger(
            "DataCollection", log_level="INFO", detailed_format=False
        )

    @classmethod
    def get_analysis_logger(cls) -> logging.Logger:
        """Retorna logger configurado para análise."""
        return cls.setup_logger("DataAnalysis", log_level="INFO", detailed_format=True)

    @classmethod
    def get_coding_logger(cls) -> logging.Logger:
        """Retorna logger configurado para codificação."""
        return cls.setup_logger(
            "CodingProcess", log_level="DEBUG", detailed_format=True
        )


class ColoredFormatter(logging.Formatter):
    """Formatter que adiciona cores e emojis aos logs do console."""

    def format(self, record):
        # Adicionar emoji baseado no nível
        emoji = LoggerConfig.EMOJIS.get(record.levelname, "")

        # Adicionar cor baseada no nível
        color = LoggerConfig.COLORS.get(record.levelname, "")
        reset = LoggerConfig.COLORS["RESET"]

        # Formatar a mensagem
        formatted = super().format(record)

        # Adicionar emoji e cor
        if emoji and color:
            formatted = f"{color}{emoji} {formatted}{reset}"
        elif emoji:
            formatted = f"{emoji} {formatted}"
        elif color:
            formatted = f"{color}{formatted}{reset}"

        return formatted


class ProgressLogger:
    """Logger especializado para acompanhar progresso de operações longas."""

    def __init__(self, logger: logging.Logger, operation_name: str):
        self.logger = logger
        self.operation_name = operation_name
        self.start_time = None
        self.total_items = 0
        self.current_item = 0

    def start(self, total_items: int = 0):
        """Inicia o acompanhamento de progresso."""
        self.start_time = datetime.now()
        self.total_items = total_items
        self.current_item = 0

        self.logger.info(
            f"🔄 Iniciando {self.operation_name}"
            + (f" - Total: {total_items} itens" if total_items > 0 else "")
        )

    def update(self, current: int = None, message: str = None):
        """Atualiza o progresso."""
        if current is not None:
            self.current_item = current

        if self.total_items > 0:
            percentage = (self.current_item / self.total_items) * 100
            progress_msg = f"📊 {self.operation_name}: {self.current_item}/{self.total_items} ({percentage:.1f}%)"
        else:
            progress_msg = (
                f"📊 {self.operation_name}: {self.current_item} itens processados"
            )

        if message:
            progress_msg += f" - {message}"

        self.logger.info(progress_msg)

    def complete(self, message: str = None):
        """Marca a conclusão da operação."""
        if self.start_time:
            duration = datetime.now() - self.start_time
            duration_str = str(duration).split(".")[0]  # Remove microssegundos

            complete_msg = f"✅ {self.operation_name} concluído em {duration_str}"
            if message:
                complete_msg += f" - {message}"

            self.logger.info(complete_msg)
        else:
            self.logger.info(f"✅ {self.operation_name} concluído")


class SectionLogger:
    """Logger para seções organizadas do processo."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.section_count = 0

    def start_section(self, title: str, description: str = None):
        """Inicia uma nova seção."""
        self.section_count += 1
        self.logger.info("")
        self.logger.info(f"🎯 SEÇÃO {self.section_count}: {title}")
        self.logger.info("=" * 60)

        if description:
            self.logger.info(f"📝 {description}")
            self.logger.info("-" * 40)

    def end_section(self, summary: str = None):
        """Finaliza a seção atual."""
        if summary:
            self.logger.info(f"📋 Resumo: {summary}")

        self.logger.info("=" * 60)
        self.logger.info("")

    def subsection(self, title: str):
        """Cria uma subseção."""
        self.logger.info(f"📌 {title}")
        self.logger.info("-" * 30)

    def step(self, step_number: int, description: str):
        """Registra um passo específico."""
        self.logger.info(f"  {step_number}. {description}")

    def result(self, result_type: str, value, details: str = None):
        """Registra um resultado."""
        result_msg = f"📊 {result_type}: {value}"
        if details:
            result_msg += f" ({details})"
        self.logger.info(result_msg)

    def error(self, error_msg: str, details: str = None):
        """Registra um erro."""
        error_log = f"❌ {error_msg}"
        if details:
            error_log += f" - Detalhes: {details}"
        self.logger.error(error_log)

    def success(self, message: str):
        """Registra um sucesso."""
        self.logger.info(f"✅ {message}")

    def warning(self, message: str):
        """Registra um aviso."""
        self.logger.warning(f"⚠️ {message}")
