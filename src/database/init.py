"""
Database initialization utilities.

Provides functions to create schema and validate PostgreSQL + pgvector setup.
"""

import os
from pathlib import Path
from typing import Optional

import psycopg
from psycopg import sql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def get_database_url(env_file: Optional[str] = None) -> str:
    """
    Get PostgreSQL connection URL from environment or .env file.

    Args:
        env_file: Path to .env file (optional)

    Returns:
        Database URL string

    Raises:
        ValueError: If DATABASE_URL not found in environment
    """
    if env_file:
        from dotenv import load_dotenv

        load_dotenv(env_file)

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Fallback to component-based URL
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "postgres")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        database = os.getenv("DB_NAME", "banco_dados_publicos")

        db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    return db_url


def create_database_if_not_exists(
    admin_url: str = "postgresql://postgres:postgres@localhost:5432/postgres",
    db_name: str = "banco_dados_publicos",
) -> None:
    """
    Create database if it doesn't exist.

    Args:
        admin_url: PostgreSQL admin connection URL
        db_name: Name of database to create
    """
    with psycopg.connect(admin_url, autocommit=True) as conn:
        with conn.cursor() as cur:
            # Check if database exists
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (db_name,),
            )
            exists = cur.fetchone()

            if not exists:
                print(f"Creating database: {db_name}")
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print(f"✅ Database '{db_name}' created successfully")
            else:
                print(f"✅ Database '{db_name}' already exists")


def install_extensions(db_url: str) -> None:
    """
    Install required PostgreSQL extensions.

    Args:
        db_url: Database connection URL
    """
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            print("Installing extensions...")

            # uuid-ossp
            cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            print("✅ uuid-ossp extension installed")

            # pgvector
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                print("✅ pgvector extension installed")
            except psycopg.Error as e:
                print(f"⚠️  Warning: Could not install pgvector: {e}")
                print("    pgvector may need to be installed manually or via Docker image")

        conn.commit()


def execute_schema_file(db_url: str, schema_file: Path) -> None:
    """
    Execute SQL schema file.

    Args:
        db_url: Database connection URL
        schema_file: Path to schema.sql file
    """
    if not schema_file.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_file}")

    print(f"Executing schema: {schema_file}")

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            schema_sql = schema_file.read_text(encoding="utf-8")
            cur.execute(schema_sql)
        conn.commit()

    print("✅ Schema created successfully")


def init_database(
    db_url: Optional[str] = None,
    admin_url: str = "postgresql://postgres:postgres@localhost:5432/postgres",
    schema_file: Optional[Path] = None,
    create_db: bool = True,
) -> None:
    """
    Initialize database with schema and extensions.

    Args:
        db_url: Target database URL (reads from env if None)
        admin_url: Admin connection for creating database
        schema_file: Path to schema.sql (defaults to src/database/schema.sql)
        create_db: Whether to create database if not exists
    """
    # Get database URL
    if not db_url:
        db_url = get_database_url()

    print(f"Initializing database: {db_url}")

    # Extract database name from URL
    db_name = db_url.split("/")[-1].split("?")[0]

    # Create database if requested
    if create_db:
        create_database_if_not_exists(admin_url, db_name)

    # Install extensions
    install_extensions(db_url)

    # Execute schema file
    if not schema_file:
        # Default to src/database/schema.sql
        schema_file = Path(__file__).parent / "schema.sql"

    execute_schema_file(db_url, schema_file)

    print("✅ Database initialization complete")


def verify_setup(db_url: Optional[str] = None) -> dict:
    """
    Verify database setup and return status.

    Args:
        db_url: Database connection URL (reads from env if None)

    Returns:
        Dictionary with verification results
    """
    if not db_url:
        db_url = get_database_url()

    results = {
        "connection": False,
        "extensions": {"uuid-ossp": False, "pgvector": False},
        "tables": {},
    }

    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            results["connection"] = True  # type: ignore[index]

            # Check extensions
            ext_result = conn.execute(text("SELECT extname FROM pg_extension"))
            extensions = [row[0] for row in ext_result]
            results["extensions"]["uuid-ossp"] = "uuid-ossp" in extensions  # type: ignore[index]
            results["extensions"]["pgvector"] = "vector" in extensions  # type: ignore[index]

            # Check tables
            table_result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
            tables = [row[0] for row in table_result]

            expected_tables = ["sources", "documents", "chunks", "embeddings", "audit_log"]
            for table in expected_tables:
                results["tables"][table] = table in tables  # type: ignore[index]

        engine.dispose()

    except Exception as e:
        results["error"] = str(e)  # type: ignore[index]

    return results


def get_session(db_url: Optional[str] = None):
    """
    Create SQLAlchemy session.

    Args:
        db_url: Database connection URL (reads from env if None)

    Returns:
        SQLAlchemy Session
    """
    if not db_url:
        db_url = get_database_url()

    engine = create_engine(db_url, echo=False)
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    """CLI for database initialization."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        # Verify setup
        results = verify_setup()
        print("\n=== Database Verification ===")
        print(f"Connection: {'✅' if results['connection'] else '❌'}")
        print("Extensions:")
        for ext, status in results["extensions"].items():
            print(f"  {ext}: {'✅' if status else '❌'}")
        print("Tables:")
        for table, exists in results["tables"].items():
            print(f"  {table}: {'✅' if exists else '❌'}")

        if "error" in results:
            print(f"\n❌ Error: {results['error']}")
            sys.exit(1)

        # Check if all essential components exist
        all_ok = results["connection"] and results["extensions"]["uuid-ossp"] and all(results["tables"].values())

        if all_ok:
            print("\n✅ Database setup is complete and valid")
            sys.exit(0)
        else:
            print("\n⚠️  Database setup incomplete")
            sys.exit(1)

    else:
        # Initialize database
        init_database()
