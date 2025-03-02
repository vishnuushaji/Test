import pytest
import os
from src.services.csv_validator import CSVValidator
from tests.utils.generate_test_csv import generate_test_csv

@pytest.fixture
def test_csv_path(tmp_path):
    """Create a temporary test CSV file."""
    csv_path = os.path.join(tmp_path, "test.csv")
    generate_test_csv(csv_path)
    return csv_path

def test_csv_validation(test_csv_path):
    """Test CSV validation with the test file."""
    result = CSVValidator.validate_csv(test_csv_path)
    assert result["valid"] == True

def test_csv_content(test_csv_path):
    """Test CSV content structure."""
    import pandas as pd
    
    df = pd.read_csv(test_csv_path)
    
    # Check columns
    required_columns = ["Serial Number", "Product Name", "Input Image Urls"]
    assert all(col in df.columns for col in required_columns)
    
    # Check data types
    assert df["Serial Number"].dtype in ['int64', 'int32']
    assert df["Product Name"].dtype == 'object'
    assert df["Input Image Urls"].dtype == 'object'
    
    # Check for non-empty values
    assert not df["Input Image Urls"].isna().any()