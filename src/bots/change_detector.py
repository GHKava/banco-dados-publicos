"""
Change Detector Bot - Detecta mudanças em URLs já crawlados

Compara hashes SHA256 de conteúdo e verifica headers Last-Modified/ETag
para determinar se uma URL sofreu mudanças desde última coleta.

Autor: Data Engineer
Data: 2026-01-31
Task: T-014
"""

import hashlib
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ChangeResult:
    """Resultado da detecção de mudança"""

    has_changed: bool
    new_hash: str
    old_hash: Optional[str] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    size_diff: Optional[int] = None
    change_type: str = "unknown"  # 'content', 'metadata', 'none'


def compute_content_hash(content: bytes, algorithm: str = "sha256") -> str:
    """
    Calcula hash do conteúdo usando algoritmo especificado.

    Args:
        content: Conteúdo em bytes
        algorithm: Algoritmo de hash ('sha256', 'md5')

    Returns:
        Hash hexadecimal do conteúdo

    Raises:
        ValueError: Se algorithm não suportado
    """
    if algorithm not in ["sha256", "md5"]:
        raise ValueError(f"Algoritmo não suportado: {algorithm}")

    if algorithm == "sha256":
        hasher = hashlib.sha256()
    else:
        hasher = hashlib.md5()

    # Hash incremental para suportar arquivos grandes
    chunk_size = 8192
    if len(content) <= chunk_size:
        hasher.update(content)
    else:
        for i in range(0, len(content), chunk_size):
            hasher.update(content[i:i + chunk_size])

    return hasher.hexdigest()


def has_content_changed(old_hash: str, new_content: bytes) -> bool:
    """
    Verifica se conteúdo mudou comparando hashes.

    Args:
        old_hash: Hash SHA256 do conteúdo anterior
        new_content: Novo conteúdo em bytes

    Returns:
        True se conteúdo diferente, False caso contrário
    """
    new_hash = compute_content_hash(new_content)
    return old_hash != new_hash


def parse_last_modified(last_modified_str: Optional[str]) -> Optional[datetime]:
    """
    Parseia string Last-Modified header para datetime.

    Args:
        last_modified_str: Header Last-Modified (RFC 2822 format)

    Returns:
        datetime ou None se parsing falhar

    Exemplo:
        "Wed, 21 Oct 2015 07:28:00 GMT" -> datetime(2015, 10, 21, 7, 28)
    """
    if not last_modified_str:
        return None

    # Formatos comuns: RFC 2822 e ISO 8601
    formats = [
        "%a, %d %b %Y %H:%M:%S GMT",  # RFC 2822
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(last_modified_str.strip(), fmt)
        except ValueError:
            continue

    logger.warning(f"Não foi possível parsear Last-Modified: {last_modified_str}")
    return None


def check_last_modified(
    last_modified_header: Optional[str], last_known_date: Optional[datetime]
) -> bool:
    """
    Verifica se Last-Modified indica mudança.

    Args:
        last_modified_header: Header Last-Modified da resposta atual
        last_known_date: Data da última coleta conhecida

    Returns:
        True se houve mudança (ou se impossível determinar), False caso contrário
    """
    if not last_modified_header or not last_known_date:
        return True  # Conservador: assume mudança se dados insuficientes

    parsed_date = parse_last_modified(last_modified_header)
    if not parsed_date:
        return True  # Não conseguiu parsear, assume mudança

    # Remove timezone para comparação (simplificação)
    if parsed_date.tzinfo:
        parsed_date = parsed_date.replace(tzinfo=None)
    if last_known_date.tzinfo:
        last_known_date = last_known_date.replace(tzinfo=None)

    return parsed_date > last_known_date


def detect_change(
    url: str,
    old_hash: Optional[str],
    new_content: bytes,
    headers: dict,
    last_known_date: Optional[datetime] = None,
) -> ChangeResult:
    """
    Detecta mudanças em URL comparando hash e headers.

    Args:
        url: URL verificada
        old_hash: Hash SHA256 anterior (None se primeira coleta)
        new_content: Novo conteúdo fetched
        headers: Headers HTTP da resposta (deve conter Last-Modified, ETag se disponíveis)
        last_known_date: Data da última coleta (para comparação Last-Modified)

    Returns:
        ChangeResult com informações sobre mudança detectada

    Exemplo:
        >>> result = detect_change(
        ...     "https://dados.gov.br/dataset/teste",
        ...     "abc123",
        ...     b"novo conteudo",
        ...     {"Last-Modified": "Wed, 21 Oct 2015 07:28:00 GMT"},
        ...     datetime(2015, 10, 20)
        ... )
        >>> result.has_changed
        True
    """
    new_hash = compute_content_hash(new_content)

    # Extração de headers (sempre, independente de old_hash)
    last_modified_header = headers.get("Last-Modified") or headers.get("last-modified")
    etag = headers.get("ETag") or headers.get("etag")

    # Primeira coleta (sem hash anterior)
    if old_hash is None:
        # Parse Last-Modified mesmo em primeira coleta
        parsed_last_modified = None
        if last_modified_header:
            parsed_last_modified = parse_last_modified(last_modified_header)

        logger.info(f"Primeira coleta de {url}, hash: {new_hash[:8]}...")
        return ChangeResult(
            has_changed=True,
            new_hash=new_hash,
            old_hash=None,
            last_modified=parsed_last_modified,
            etag=etag,
            change_type="initial",
        )

    # Comparação de hash
    content_changed = old_hash != new_hash

    # Verificação Last-Modified
    metadata_changed = False
    if last_modified_header and last_known_date:
        metadata_changed = check_last_modified(last_modified_header, last_known_date)

    # Decisão final
    has_changed = content_changed or metadata_changed

    # Size diff (se mudou)
    size_diff = None
    if content_changed and old_hash:
        size_diff = len(new_content)  # Simplificação (sem old_size armazenado)

    # Change type
    change_type = "none"
    if content_changed:
        change_type = "content"
    elif metadata_changed:
        change_type = "metadata"

    # Parse Last-Modified
    parsed_last_modified = None
    if last_modified_header:
        parsed_last_modified = parse_last_modified(last_modified_header)

    logger.info(
        f"Change detection para {url}: "
        f"changed={has_changed}, type={change_type}, "
        f"hash_match={not content_changed}"
    )

    return ChangeResult(
        has_changed=has_changed,
        new_hash=new_hash,
        old_hash=old_hash,
        last_modified=parsed_last_modified,
        etag=etag,
        size_diff=size_diff,
        change_type=change_type,
    )
