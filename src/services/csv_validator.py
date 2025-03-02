import pandas as pd
import validators
from typing import List, Dict

class CSVValidator:
    @staticmethod
    def validate_csv(file_path: str) -> Dict[str, bool]:
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Check required columns
            required_columns = ['Serial Number', 'Product Name', 'Input Image Urls']
            if not all(col in df.columns for col in required_columns):
                return {"valid": False, "error": "Missing required columns"}
            
            # Validate image URLs
            def validate_urls(url_string):
                urls = url_string.split(',')
                return all(validators.url(url.strip()) for url in urls)
            
            invalid_rows = df[~df['Input Image Urls'].apply(validate_urls)]
            
            if not invalid_rows.empty:
                return {
                    "valid": False, 
                    "error": "Invalid URLs in rows",
                    "invalid_rows": invalid_rows.to_dict('records')
                }
            
            return {"valid": True}
        
        except Exception as e:
            return {"valid": False, "error": str(e)}