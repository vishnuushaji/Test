# tests/test_upload_api.py
import pytest
from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

@pytest.fixture
def test_csv_file(tmp_path):
    """Create a test CSV file for upload testing."""
    from tests.utils.generate_test_csv import generate_test_csv
    
    csv_path = os.path.join(tmp_path, "test.csv")
    generate_test_csv(csv_path)
    return csv_path

def test_upload_csv(test_csv_file):
    """Test CSV file upload endpoint."""
    with open(test_csv_file, 'rb') as f:
        response = client.post(
            "/upload",
            files={"file": ("test.csv", f, "text/csv")}
        )
    
    assert response.status_code == 202
    assert "request_id" in response.json()