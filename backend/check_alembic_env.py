import os
import sys

print("--- Starting check_alembic_env.py ---")

# Mimic path setup from migrations/env.py
# Assuming this script is in backend/ and app is in backend/app/
Backend_Dir = os.path.dirname(__file__) # .../backend
if Backend_Dir not in sys.path:
    sys.path.insert(0, Backend_Dir)

print(f"PYTHONPATH for check_alembic_env.py: {sys.path}")
print(f"Attempting to import from 'app' using Backend_Dir: {Backend_Dir}")

try:
    print("Importing Base and settings...")
    from app.core.database import Base
    from app.models import * # noqa: F403, F401 - Import all to register models
    from app.core.config import settings as app_settings
    print("Imports successful.")

    print(f"DATABASE_URL from settings: {app_settings.DATABASE_URL}")

    target_metadata = Base.metadata
    print("Detected tables in Base.metadata:")
    if target_metadata and target_metadata.tables:
        for table_name in target_metadata.tables:
            print(f"- {table_name}")
    else:
        print("- No metadata tables found or metadata is None.")

except ImportError as e:
    print(f"ImportError: {e}")
    print("This likely means a problem with sys.path or the project structure.")
except AttributeError as e:
    print(f"AttributeError: {e}")
    print("This could mean DATABASE_URL is not set in your .env file or not loaded by Pydantic settings.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("--- Finished check_alembic_env.py ---") 