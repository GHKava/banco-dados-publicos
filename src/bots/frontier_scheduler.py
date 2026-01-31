"""
Frontier Scheduler - Processa frontier queue periodicamente

Implementa fetch-decode-execute loop para consumir URLs da frontier queue
com suporte a batch processing, retry logic e graceful shutdown.

Autor: Data Engineer
Data: 2026-01-31
Task: T-015
"""

import logging
import signal
import time
from dataclasses import dataclass
from typing import Callable, Optional

logger = logging.getLogger(__name__)


@dataclass
class SchedulerConfig:
    """Configuração do scheduler"""

    interval_seconds: int = 60  # Intervalo entre execuções
    batch_size: int = 10  # URLs por batch
    max_retries: int = 3  # Max tentativas por URL
    adaptive_interval: bool = True  # Aumenta interval se queue vazia


@dataclass
class WorkerStats:
    """Estatísticas de execução do worker"""

    urls_processed: int = 0
    urls_failed: int = 0
    duration_seconds: float = 0.0
    queue_size_before: int = 0
    queue_size_after: int = 0


class FrontierScheduler:
    """
    Scheduler que processa frontier queue periodicamente.

    Implementa fetch-decode-execute loop com:
    - Batch processing (N URLs por iteração)
    - Graceful shutdown (SIGINT/SIGTERM)
    - Adaptive interval (aumenta se queue vazia)
    - Metrics logging
    """

    def __init__(self, frontier, config: Optional[SchedulerConfig] = None):
        """
        Inicializa scheduler.

        Args:
            frontier: URLFrontier instance (T-011)
            config: SchedulerConfig (usa default se None)
        """
        self.frontier = frontier
        self.config = config or SchedulerConfig()
        self.running = False
        self.iteration_count = 0
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Registra signal handlers para graceful shutdown"""
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def _handle_shutdown(self, signum, frame):
        """Handler para SIGINT/SIGTERM"""
        logger.info(f"Recebido sinal {signum}, iniciando graceful shutdown...")
        self.stop()

    def start(self, worker_func: Optional[Callable] = None):
        """
        Inicia scheduler em loop contínuo.

        Args:
            worker_func: Função a executar em cada iteração (default: _default_worker)
                         Signature: worker_func(frontier, batch_size) -> dict
        """
        self.running = True
        worker_func = worker_func or self._default_worker

        logger.info(
            f"Frontier scheduler iniciado: "
            f"interval={self.config.interval_seconds}s, "
            f"batch={self.config.batch_size}"
        )

        while self.running:
            try:
                self.iteration_count += 1
                stats = self._run_iteration(worker_func)
                self._log_stats(stats)

                # Adaptive interval: aumenta para 5min se queue vazia
                sleep_duration = self.config.interval_seconds
                if self.config.adaptive_interval and stats.queue_size_before == 0:
                    sleep_duration = 300  # 5 minutos
                    logger.info("Queue vazia, aumentando interval para 5min")

                # Sleep interruptible (verifica running a cada 1s)
                for _ in range(sleep_duration):
                    if not self.running:
                        break
                    time.sleep(1)

            except Exception as e:
                logger.error(f"Erro em iteração {self.iteration_count}: {e}", exc_info=True)
                time.sleep(5)  # Backoff em caso de erro

        logger.info(f"Scheduler parado após {self.iteration_count} iterações")

    def stop(self):
        """Para scheduler (graceful shutdown)"""
        self.running = False

    def _run_iteration(self, worker_func: Callable) -> WorkerStats:
        """
        Executa uma iteração do worker.

        Args:
            worker_func: Função worker a executar

        Returns:
            WorkerStats com métricas da iteração
        """
        start_time = time.time()
        queue_size_before = self.frontier.get_queue_size()

        logger.debug(
            f"Iteração {self.iteration_count}: " f"queue_size={queue_size_before}, " f"batch={self.config.batch_size}"
        )

        # Executar worker
        result = worker_func(self.frontier, self.config.batch_size)

        # Coletar stats
        duration = time.time() - start_time
        queue_size_after = self.frontier.get_queue_size()

        return WorkerStats(
            urls_processed=result.get("processed", 0),
            urls_failed=result.get("failed", 0),
            duration_seconds=duration,
            queue_size_before=queue_size_before,
            queue_size_after=queue_size_after,
        )

    def _log_stats(self, stats: WorkerStats):
        """Log estatísticas da iteração"""
        logger.info(
            f"Iteração {self.iteration_count} concluída: "
            f"processed={stats.urls_processed}, "
            f"failed={stats.urls_failed}, "
            f"duration={stats.duration_seconds:.2f}s, "
            f"queue={stats.queue_size_before} → {stats.queue_size_after}"
        )

    def _default_worker(self, frontier, batch_size: int) -> dict:
        """
        Worker default (placeholder).

        Em produção, este worker seria substituído por função que:
        1. Chama HTTP fetcher (T-016)
        2. Valida response (T-017)
        3. Armazena raw content (T-018)

        Args:
            frontier: URLFrontier instance
            batch_size: Número de URLs a processar

        Returns:
            dict com {'processed': int, 'failed': int}
        """
        processed = 0
        failed = 0

        for _ in range(batch_size):
            url_data = frontier.get_next_url()
            if not url_data:
                break  # Queue vazia

            logger.debug(f"Processing URL: {url_data.url} (source={url_data.source_id})")

            # Placeholder: marca como processado
            # TODO: Integrar com T-016 (HTTP fetcher)
            processed += 1

        return {"processed": processed, "failed": failed}


def run_frontier_scheduler(frontier, config: Optional[SchedulerConfig] = None, worker_func: Optional[Callable] = None):
    """
    Função utilitária para executar scheduler.

    Args:
        frontier: URLFrontier instance
        config: SchedulerConfig (usa default se None)
        worker_func: Função worker customizada (usa default se None)

    Exemplo:
        >>> from src.bots.url_frontier import URLFrontier
        >>> frontier = URLFrontier(redis_client)
        >>> config = SchedulerConfig(interval_seconds=30, batch_size=5)
        >>> run_frontier_scheduler(frontier, config)
    """
    scheduler = FrontierScheduler(frontier, config)
    scheduler.start(worker_func)
