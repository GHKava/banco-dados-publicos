"""
Test database connection and basic CRUD operations.

This script validates:
- Database connectivity
- SQLAlchemy ORM setup
- Table creation via Alembic migrations
- Basic INSERT/SELECT operations
"""

import sys

from sqlalchemy import select

from src.storage.database import get_engine, get_session
from src.storage.models import Source


def test_connection():
    """Test database connection."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            _ = conn.execute(select(1))
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_insert_source():
    """Test INSERT operation on sources table."""
    try:
        session = next(get_session())

        # Create test source
        test_source = Source(
            name="TEST-DOU",
            base_url="https://in.gov.br",
            source_type="government",
            license_info={"type": "public_domain", "verified": False},
            robots_policy="METADATA_ONLY",
            tos_compliance=False,
            status="PENDING_REVIEW",
        )

        session.add(test_source)
        session.commit()

        print(f"✅ INSERT successful: {test_source}")
        print(f"   ID: {test_source.id}")
        print(f"   Created at: {test_source.created_at}")

        # Query back
        sources = session.query(Source).all()
        print(f"✅ SELECT successful: {len(sources)} sources found")

        # Cleanup
        session.delete(test_source)
        session.commit()
        print("✅ DELETE successful (cleanup)")

        return True
    except Exception as e:
        print(f"❌ CRUD operations failed: {e}")
        return False
    finally:
        session.close()


def main():
    """Run all tests."""
    print("=" * 60)
    print("Database Connection & CRUD Test")
    print("=" * 60)
    print()

    tests_passed = 0
    tests_total = 2

    if test_connection():
        tests_passed += 1

    if test_insert_source():
        tests_passed += 1

    print()
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{tests_total}")
    print("=" * 60)

    if tests_passed == tests_total:
        print("✅ All tests PASSED")
        return 0
    else:
        print("❌ Some tests FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
