import csv
import os

def generate_test_csv(output_path: str):
    """Generate a test CSV file with sample data."""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Sample data with real image URLs
    data = [
        {
            "Serial Number": 1,
            "Product Name": "SKU1",
            "Input Image Urls": "https://picsum.photos/200/300,https://picsum.photos/200/301"
        },
        {
            "Serial Number": 2,
            "Product Name": "SKU2",
            "Input Image Urls": "https://picsum.photos/200/302,https://picsum.photos/200/303"
        }
    ]
    
    # Write CSV file
    with open(output_path, 'w', newline='') as file:
        writer = csv.DictWriter(
            file, 
            fieldnames=["Serial Number", "Product Name", "Input Image Urls"]
        )
        
        writer.writeheader()
        writer.writerows(data)

    print(f"Test CSV generated at: {output_path}")

if __name__ == "__main__":
    # Generate test CSV in tests/data directory
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'data', 
        'test.csv'
    )
    generate_test_csv(csv_path)