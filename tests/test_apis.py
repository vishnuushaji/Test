import pytest
import os

def test_upload_csv(client, temp_csv_file):
    with open(temp_csv_file, 'rb') as f:
        response = client.post(
            "/api/v1/upload", 
            files={"file": ("test.csv", f, "text/csv")}
        )
    
    assert response.status_code == 202
    assert "request_id" in response.json()

def test_status_api(client):
    # First, upload a CSV to get a request_id
    with open(temp_csv_file, 'rb') as f:
        upload_response = client.post(
            "/api/v1/upload", 
            files={"file": ("test.csv", f, "text/csv")}
        )
    
    request_id = upload_response.json()["request_id"]
    
    # Check status
    status_response = client.get(f"/api/v1/status/{request_id}")
    
    assert status_response.status_code == 200
    assert "status" in status_response.json()