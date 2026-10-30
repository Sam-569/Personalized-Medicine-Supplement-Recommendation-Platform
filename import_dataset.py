#!/usr/bin/env python3
"""Convenience CLI script to import knowledge base dataset into the configured database."""
import os
import sys

# Add backend directory to sys.path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

os.environ.setdefault("JWT_SECRET", "temporary-cli-key-for-dataset-import-32chars")
from app.data_importer import main

if __name__ == "__main__":
    main()

