import csv
import os

def generate_test_csv(output_path: str = None):
    """Generate test CSV files with sample data."""
    
    if output_path is None:
        # Default path in tests/data directory
        output_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'data'
        )
        os.makedirs(output_path, exist_ok=True)
        
        input_csv_path = os.path.join(output_path, 'input_test.csv')
        output_csv_path = os.path.join(output_path, 'output_test.csv')
    
    # Sample data for input CSV
    input_data = [
        {
            "Serial Number": "1.",
            "Product Name": "SKU1",
            "Input Image Urls": "https://www.public-image-url1.jpg,https://www.public-image-url2.jpg,https://www.public-image-url3.jpg"
        },
        {
            "Serial Number": "2.",
            "Product Name": "SKU2",
            "Input Image Urls": "https://www.public-image-url1.jpg,https://www.public-image-url2.jpg,https://www.public-image-url3.jpg"
        }
    ]
    
    # Sample data for output CSV
    output_data = [
        {
            "Serial Number": "1.",
            "Product Name": "SKU1",
            "Input Image Urls": "https://www.public-image-url1.jpg,https://www.public-image-url2.jpg,https://www.public-image-url3.jpg",
            "Output Image Urls": "https://www.public-image-output-url1.jpg,https://www.public-image-output-url2.jpg,https://www.public-image-output-url3.jpg"
        },
        {
            "Serial Number": "2.",
            "Product Name": "SKU2",
            "Input Image Urls": "https://www.public-image-url1.jpg,https://www.public-image-url2.jpg,https://www.public-image-url3.jpg",
            "Output Image Urls": "https://www.public-image-output-url1.jpg,https://www.public-image-output-url2.jpg,https://www.public-image-output-url3.jpg"
        }
    ]
    
    # Write input CSV file
    with open(input_csv_path, 'w', newline='') as file:
        writer = csv.DictWriter(
            file, 
            fieldnames=["Serial Number", "Product Name", "Input Image Urls"]
        )
        writer.writeheader()
        writer.writerows(input_data)
    
    print(f"Input CSV generated at: {input_csv_path}")
    
    # Write output CSV file
    with open(output_csv_path, 'w', newline='') as file:
        writer = csv.DictWriter(
            file, 
            fieldnames=["Serial Number", "Product Name", "Input Image Urls", "Output Image Urls"]
        )
        writer.writeheader()
        writer.writerows(output_data)
    
    print(f"Output CSV generated at: {output_csv_path}")
    
    return input_csv_path, output_csv_path

if __name__ == "__main__":
    input_path, output_path = generate_test_csv()
    
    # Display the contents of both files
    print("\nInput CSV Contents:")
    with open(input_path, 'r') as f:
        print(f.read())
    
    print("\nOutput CSV Contents:")
    with open(output_path, 'r') as f:
        print(f.read())