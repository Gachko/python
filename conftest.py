import shutil
import pytest
from django.conf import settings
import os
from pathlib import Path

@pytest.fixture(scope='session', autouse=True)
def setup_test_db():
    main_db_path = settings.DATABASES['default']['NAME']
    test_db_path = settings.DATABASES['default']['TEST']['NAME']

    print(f"Main DB: {main_db_path}")
    print(f"Test DB: {test_db_path}")
    print(f"Full path to test DB: {os.path.abspath(test_db_path)}")

    if not os.path.exists(main_db_path):
        raise FileNotFoundError(f"Main database not found: {main_db_path}")

    if os.path.exists(test_db_path):
        print(f"Removing existing test DB: {test_db_path}")
        os.remove(test_db_path)

    shutil.copy2(main_db_path, test_db_path)

    if not os.path.exists(test_db_path):
        raise FileNotFoundError(f"Failed to create test database: {test_db_path}")

    print(f"Test database created at: {test_db_path}")

    yield

#     if os.path.exists(test_db_path):
#         os.remove(test_db_path)