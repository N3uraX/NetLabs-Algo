import os
import sys
print("--- EXECUTING migrations/env.py ---")

from logging.config import fileConfig

# from sqlalchemy import engine_from_config # No longer needed
from sqlalchemy import pool
import asyncio # <--- Import asyncio
from sqlalchemy.ext.asyncio import create_async_engine # <--- Import create_async_engine

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Path setup:
# Assuming env.py is in backend/migrations/
# and the 'app' package is in backend/app/
# We need 'backend/' to be in sys.path for `from app...` imports to work.
# When alembic runs from `backend/`, `.` is already effectively `backend/` in sys.path usually.
# However, to be explicit and robust:
Alembic_Dir = os.path.dirname(__file__) # .../backend/migrations
Backend_Dir = os.path.abspath(os.path.join(Alembic_Dir, '..')) # .../backend
if Backend_Dir not in sys.path:
    sys.path.insert(0, Backend_Dir)

print(f"PYTHONPATH for Alembic: {sys.path}")
print(f"Attempting to import from 'app' using Backend_Dir: {Backend_Dir}")

# Import your app's Base model and settings
from app.core.database import Base
from app.models import * # Ensure all models are imported so Base registers them
from app.core.config import settings as app_settings

# Set the target metadata for Alembic
target_metadata = Base.metadata

print("--- DIAGNOSTIC PRINT (env.py) ---")
print("Detected tables in Base.metadata by Alembic env.py:")
if target_metadata:
    for table_name in target_metadata.tables:
        print(f"- {table_name}")
else:
    print("- No metadata tables found.")
print("--- END DIAGNOSTIC PRINT ---")

# Helper synchronous function for Alembic operations
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

# Function to run migrations in 'online' mode (async version)
async def run_migrations_online_async() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    db_url = app_settings.DATABASE_URL
    if not db_url:
        raise ValueError("DATABASE_URL is not set in the application settings (.env file).")

    # Create an async engine
    connectable = create_async_engine(
        str(db_url),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    # Offline mode is not typically used for modern web apps with live DBs
    # context.run_migrations_offline()
    print("Offline mode is not configured. Please run with a database connection.")
else:
    asyncio.run(run_migrations_online_async()) 