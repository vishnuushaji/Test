import pytest
from fastapi.testclient import TestClient
from main import app
import tempfile
import os

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def temp_csv_file():
    # Create a temporary CSV file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        temp_file.write("""Serial Number,Product Name,Input Image Urls
1,Test Product,https://example.com/image1.jpg,https://example.com/image2.jpg
2,Another Product,https://example.com/image3.jpg,https://example.com/image4.jpg""")
        temp_file.close()
    
    yield temp_file.name
    
    # Cleanup
    os.unlink(temp_file.name)