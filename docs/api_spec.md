# Image Processing System API Documentation

## Overview
This API allows users to upload CSV files for image processing and track the processing status.

## Endpoints

### 1. Upload CSV
- **URL:** `/api/v1/upload`
- **Method:** `POST`
- **Request Body:** Multipart form-data with CSV file
- **Success Response:**
  - Code: 202
  - Content: 
    ```json
    {
      "request_id": "unique-uuid",
      "message": "CSV uploaded and processing started"
    }
    ```

### 2. Check Status
- **URL:** `/api/v1/status/{request_id}`
- **Method:** `GET`
- **Success Response:**
  - Code: 200
  - Content:
    ```json
    {
      "request_id": "unique-uuid",
      "status": "PENDING/PROCESSING/COMPLETED/FAILED",
      "created_at": "timestamp",
      "output_csv_path": "path/to/output/csv"
    }
    ```

## Error Handling
- Detailed error responses with specific error messages
- HTTP status codes for different error scenarios