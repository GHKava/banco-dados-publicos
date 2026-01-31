"""
Testes para Change Detector Bot

Autor: Data Engineer
Data: 2026-01-31
Task: T-014
"""

import hashlib
from datetime import datetime

import pytest

from src.bots.change_detector import (
    ChangeResult,
    check_last_modified,
    compute_content_hash,
    detect_change,
    has_content_changed,
    parse_last_modified,
)


class TestComputeContentHash:
    """Testes para compute_content_hash()"""

    def test_compute_sha256_simple(self):
        """Hash SHA256 de conteúdo simples"""
        content = b"hello world"
        expected = hashlib.sha256(content).hexdigest()
        assert compute_content_hash(content) == expected

    def test_compute_sha256_large(self):
        """Hash SHA256 de conteúdo grande (>8KB)"""
        content = b"x" * 10000
        expected = hashlib.sha256(content).hexdigest()
        assert compute_content_hash(content) == expected

    def test_compute_md5(self):
        """Hash MD5 quando especificado"""
        content = b"hello world"
        expected = hashlib.md5(content).hexdigest()
        assert compute_content_hash(content, algorithm="md5") == expected

    def test_invalid_algorithm(self):
        """Erro para algoritmo inválido"""
        with pytest.raises(ValueError, match="Algoritmo não suportado"):
            compute_content_hash(b"test", algorithm="sha512")

    def test_empty_content(self):
        """Hash de conteúdo vazio"""
        content = b""
        expected = hashlib.sha256(content).hexdigest()
        assert compute_content_hash(content) == expected


class TestHasContentChanged:
    """Testes para has_content_changed()"""

    def test_content_unchanged(self):
        """Conteúdo não mudou (hash igual)"""
        content = b"same content"
        old_hash = compute_content_hash(content)
        assert has_content_changed(old_hash, content) is False

    def test_content_changed(self):
        """Conteúdo mudou (hash diferente)"""
        old_content = b"old content"
        new_content = b"new content"
        old_hash = compute_content_hash(old_content)
        assert has_content_changed(old_hash, new_content) is True

    def test_whitespace_matters(self):
        """Mudança de espaços é detectada"""
        old_content = b"hello world"
        new_content = b"hello  world"  # Espaço extra
        old_hash = compute_content_hash(old_content)
        assert has_content_changed(old_hash, new_content) is True


class TestParseLastModified:
    """Testes para parse_last_modified()"""

    def test_parse_rfc2822(self):
        """Parsing de RFC 2822 format"""
        header = "Wed, 21 Oct 2015 07:28:00 GMT"
        result = parse_last_modified(header)
        assert result == datetime(2015, 10, 21, 7, 28, 0)

    def test_parse_rfc2822_with_timezone(self):
        """Parsing de RFC 2822 com timezone"""
        header = "Wed, 21 Oct 2015 07:28:00 +0000"
        result = parse_last_modified(header)
        assert result.year == 2015
        assert result.month == 10
        assert result.day == 21

    def test_parse_iso8601(self):
        """Parsing de ISO 8601 format"""
        header = "2015-10-21 07:28:00"
        result = parse_last_modified(header)
        assert result == datetime(2015, 10, 21, 7, 28, 0)

    def test_parse_invalid_format(self):
        """Retorna None para formato inválido"""
        header = "invalid date string"
        result = parse_last_modified(header)
        assert result is None

    def test_parse_none(self):
        """Retorna None para entrada None"""
        result = parse_last_modified(None)
        assert result is None

    def test_parse_empty_string(self):
        """Retorna None para string vazia"""
        result = parse_last_modified("")
        assert result is None


class TestCheckLastModified:
    """Testes para check_last_modified()"""

    def test_no_change_detected(self):
        """Sem mudança quando Last-Modified é anterior"""
        header = "Wed, 21 Oct 2015 07:28:00 GMT"
        last_known = datetime(2015, 10, 22, 0, 0, 0)  # Depois do header
        result = check_last_modified(header, last_known)
        assert result is False

    def test_change_detected(self):
        """Mudança detectada quando Last-Modified é posterior"""
        header = "Wed, 21 Oct 2015 07:28:00 GMT"
        last_known = datetime(2015, 10, 20, 0, 0, 0)  # Antes do header
        result = check_last_modified(header, last_known)
        assert result is True

    def test_missing_header(self):
        """Assume mudança quando header ausente"""
        result = check_last_modified(None, datetime(2015, 10, 20))
        assert result is True

    def test_missing_last_known(self):
        """Assume mudança quando last_known ausente"""
        header = "Wed, 21 Oct 2015 07:28:00 GMT"
        result = check_last_modified(header, None)
        assert result is True

    def test_invalid_header_format(self):
        """Assume mudança quando parsing falha"""
        header = "invalid date"
        last_known = datetime(2015, 10, 20)
        result = check_last_modified(header, last_known)
        assert result is True


class TestDetectChange:
    """Testes para detect_change()"""

    def test_initial_collection(self):
        """Primeira coleta (sem hash anterior)"""
        url = "https://dados.gov.br/dataset/teste"
        content = b"initial content"
        headers = {}

        result = detect_change(url, None, content, headers)

        assert result.has_changed is True
        assert result.change_type == "initial"
        assert result.old_hash is None
        assert len(result.new_hash) == 64  # SHA256

    def test_content_changed_hash_diff(self):
        """Mudança detectada por diferença de hash"""
        url = "https://dados.gov.br/dataset/teste"
        old_content = b"old content"
        new_content = b"new content"
        old_hash = compute_content_hash(old_content)
        headers = {}

        result = detect_change(url, old_hash, new_content, headers)

        assert result.has_changed is True
        assert result.change_type == "content"
        assert result.old_hash == old_hash
        assert result.new_hash != old_hash

    def test_content_unchanged(self):
        """Sem mudança quando hash igual"""
        url = "https://dados.gov.br/dataset/teste"
        content = b"same content"
        old_hash = compute_content_hash(content)
        headers = {}

        result = detect_change(url, old_hash, content, headers)

        assert result.has_changed is False
        assert result.change_type == "none"
        assert result.new_hash == old_hash

    def test_metadata_change_only(self):
        """Mudança detectada apenas por Last-Modified"""
        url = "https://dados.gov.br/dataset/teste"
        content = b"same content"
        old_hash = compute_content_hash(content)
        headers = {"Last-Modified": "Wed, 21 Oct 2015 07:28:00 GMT"}
        last_known = datetime(2015, 10, 20)

        result = detect_change(url, old_hash, content, headers, last_known)

        assert result.has_changed is True
        assert result.change_type == "metadata"
        assert result.last_modified == datetime(2015, 10, 21, 7, 28, 0)

    def test_etag_extraction(self):
        """ETag é extraído dos headers"""
        url = "https://dados.gov.br/dataset/teste"
        content = b"test content"
        headers = {"ETag": '"abc123"'}

        result = detect_change(url, None, content, headers)

        assert result.etag == '"abc123"'

    def test_case_insensitive_headers(self):
        """Headers case-insensitive (last-modified, etag)"""
        url = "https://dados.gov.br/dataset/teste"
        content = b"test content"
        headers = {"last-modified": "Wed, 21 Oct 2015 07:28:00 GMT", "etag": '"xyz"'}

        result = detect_change(url, None, content, headers)

        assert result.last_modified == datetime(2015, 10, 21, 7, 28, 0)
        assert result.etag == '"xyz"'

    def test_size_diff_computed(self):
        """Size diff é computado quando há mudança"""
        url = "https://dados.gov.br/dataset/teste"
        old_content = b"old"
        new_content = b"new content is longer"
        old_hash = compute_content_hash(old_content)
        headers = {}

        result = detect_change(url, old_hash, new_content, headers)

        assert result.size_diff == len(new_content)
