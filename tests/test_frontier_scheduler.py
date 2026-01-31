"""
Testes para Frontier Scheduler

Autor: Data Engineer
Data: 2026-01-31
Task: T-015
"""

import signal
import time
from unittest.mock import Mock, patch

from src.bots.frontier_scheduler import FrontierScheduler, SchedulerConfig, WorkerStats, run_frontier_scheduler


class TestSchedulerConfig:
    """Testes para SchedulerConfig"""

    def test_default_config(self):
        """Config default tem valores razoáveis"""
        config = SchedulerConfig()
        assert config.interval_seconds == 60
        assert config.batch_size == 10
        assert config.max_retries == 3
        assert config.adaptive_interval is True

    def test_custom_config(self):
        """Config customizado funciona"""
        config = SchedulerConfig(interval_seconds=30, batch_size=5, adaptive_interval=False)
        assert config.interval_seconds == 30
        assert config.batch_size == 5
        assert config.adaptive_interval is False


class TestWorkerStats:
    """Testes para WorkerStats"""

    def test_default_stats(self):
        """Stats default zeradas"""
        stats = WorkerStats()
        assert stats.urls_processed == 0
        assert stats.urls_failed == 0
        assert stats.duration_seconds == 0.0

    def test_custom_stats(self):
        """Stats customizadas"""
        stats = WorkerStats(
            urls_processed=5,
            urls_failed=2,
            duration_seconds=1.5,
            queue_size_before=100,
            queue_size_after=95,
        )
        assert stats.urls_processed == 5
        assert stats.urls_failed == 2
        assert stats.duration_seconds == 1.5
        assert stats.queue_size_before == 100
        assert stats.queue_size_after == 95


class TestFrontierScheduler:
    """Testes para FrontierScheduler"""

    def test_init_default_config(self):
        """Scheduler inicializa com config default"""
        frontier = Mock()
        scheduler = FrontierScheduler(frontier)
        assert scheduler.config.interval_seconds == 60
        assert scheduler.config.batch_size == 10
        assert scheduler.running is False
        assert scheduler.iteration_count == 0

    def test_init_custom_config(self):
        """Scheduler inicializa com config customizada"""
        frontier = Mock()
        config = SchedulerConfig(interval_seconds=30, batch_size=5)
        scheduler = FrontierScheduler(frontier, config)
        assert scheduler.config.interval_seconds == 30
        assert scheduler.config.batch_size == 5

    @patch("signal.signal")
    def test_signal_handlers_registered(self, mock_signal):
        """Signal handlers são registrados no __init__"""
        frontier = Mock()
        FrontierScheduler(frontier)

        # Verifica se signal.signal foi chamado para SIGINT e SIGTERM
        assert mock_signal.call_count >= 2
        calls = [call[0] for call in mock_signal.call_args_list]
        assert any(signal.SIGINT in call for call in calls)
        assert any(signal.SIGTERM in call for call in calls)

    def test_stop_sets_running_false(self):
        """stop() seta running=False"""
        frontier = Mock()
        scheduler = FrontierScheduler(frontier)
        scheduler.running = True
        scheduler.stop()
        assert scheduler.running is False

    def test_handle_shutdown_calls_stop(self):
        """_handle_shutdown() chama stop()"""
        frontier = Mock()
        scheduler = FrontierScheduler(frontier)
        scheduler.running = True
        scheduler._handle_shutdown(signal.SIGINT, None)
        assert scheduler.running is False

    @patch("time.sleep")
    def test_start_executes_worker(self, mock_sleep):
        """start() executa worker e incrementa iteration_count"""
        frontier = Mock()
        frontier.get_queue_size.return_value = 10
        scheduler = FrontierScheduler(frontier)

        # Worker que para após 1 iteração
        def worker_func(frontier, batch_size):
            scheduler.stop()
            return {"processed": 5, "failed": 0}

        scheduler.start(worker_func)

        assert scheduler.iteration_count == 1
        frontier.get_queue_size.assert_called()

    @patch("time.sleep")
    def test_adaptive_interval_on_empty_queue(self, mock_sleep):
        """Adaptive interval aumenta para 5min se queue vazia"""
        frontier = Mock()
        frontier.get_queue_size.return_value = 0  # Queue vazia
        config = SchedulerConfig(interval_seconds=60, adaptive_interval=True)
        scheduler = FrontierScheduler(frontier, config)

        # Worker que para após 1 iteração
        iteration_count = 0

        def worker_func(frontier, batch_size):
            nonlocal iteration_count
            iteration_count += 1
            if iteration_count >= 1:
                scheduler.stop()
            return {"processed": 0, "failed": 0}

        scheduler.start(worker_func)

        # Sleep deve ter sido chamado 300 vezes (5min * 1s cada)
        assert mock_sleep.call_count == 300

    @patch("time.sleep")
    def test_no_adaptive_interval_if_disabled(self, mock_sleep):
        """Adaptive interval não aumenta se disabled"""
        frontier = Mock()
        frontier.get_queue_size.return_value = 0  # Queue vazia
        config = SchedulerConfig(interval_seconds=60, adaptive_interval=False)
        scheduler = FrontierScheduler(frontier, config)

        iteration_count = 0

        def worker_func(frontier, batch_size):
            nonlocal iteration_count
            iteration_count += 1
            if iteration_count >= 1:
                scheduler.stop()
            return {"processed": 0, "failed": 0}

        scheduler.start(worker_func)

        # Sleep deve ter sido chamado 60 vezes (60s * 1s cada)
        assert mock_sleep.call_count == 60

    def test_run_iteration_calls_worker(self):
        """_run_iteration() chama worker_func"""
        frontier = Mock()
        frontier.get_queue_size.return_value = 10
        scheduler = FrontierScheduler(frontier)

        worker_func = Mock(return_value={"processed": 5, "failed": 2})
        stats = scheduler._run_iteration(worker_func)

        worker_func.assert_called_once_with(frontier, scheduler.config.batch_size)
        assert stats.urls_processed == 5
        assert stats.urls_failed == 2
        assert stats.duration_seconds > 0

    def test_default_worker_processes_urls(self):
        """_default_worker() processa URLs da frontier"""
        frontier = Mock()
        frontier.get_next_url.side_effect = [
            Mock(url="http://example.com/1", source_id="src1"),
            Mock(url="http://example.com/2", source_id="src1"),
            None,  # Queue vazia
        ]

        scheduler = FrontierScheduler(frontier)
        result = scheduler._default_worker(frontier, batch_size=3)

        assert result["processed"] == 2
        assert result["failed"] == 0
        assert frontier.get_next_url.call_count == 3

    def test_default_worker_empty_queue(self):
        """_default_worker() retorna 0 se queue vazia"""
        frontier = Mock()
        frontier.get_next_url.return_value = None

        scheduler = FrontierScheduler(frontier)
        result = scheduler._default_worker(frontier, batch_size=10)

        assert result["processed"] == 0
        assert result["failed"] == 0


class TestRunFrontierScheduler:
    """Testes para run_frontier_scheduler()"""

    @patch("time.sleep")
    def test_run_with_default_config(self, mock_sleep):
        """run_frontier_scheduler() executa com config default"""
        frontier = Mock()
        frontier.get_queue_size.return_value = 0

        # Usar thread para parar após 100ms
        import threading

        scheduler_ref = []

        def stop_after_delay():
            time.sleep(0.1)
            if scheduler_ref:
                scheduler_ref[0].stop()

        thread = threading.Thread(target=stop_after_delay)
        thread.start()

        # Capturar scheduler para parar
        original_init = FrontierScheduler.__init__

        def patched_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            scheduler_ref.append(self)

        with patch.object(FrontierScheduler, "__init__", patched_init):
            run_frontier_scheduler(frontier)

        thread.join()
        assert len(scheduler_ref) > 0

    @patch("time.sleep")
    def test_run_with_custom_config(self, mock_sleep):
        """run_frontier_scheduler() aceita config customizada"""
        frontier = Mock()
        frontier.get_queue_size.return_value = 5
        config = SchedulerConfig(interval_seconds=30, batch_size=5)

        # Usar thread para parar após 100ms
        import threading

        scheduler_ref = []

        def stop_after_delay():
            time.sleep(0.1)
            if scheduler_ref:
                scheduler_ref[0].stop()

        thread = threading.Thread(target=stop_after_delay)
        thread.start()

        # Capturar scheduler
        original_init = FrontierScheduler.__init__

        def patched_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            scheduler_ref.append(self)

        with patch.object(FrontierScheduler, "__init__", patched_init):
            run_frontier_scheduler(frontier, config)

        thread.join()
        assert scheduler_ref[0].config.interval_seconds == 30
