#!/usr/bin/env python3
"""
File Writer Helper for Robot Framework
Handles JSON and CSV file writing without syntax issues
"""

import json
import csv
import sys

def write_json_file(filename, data):
    """Write data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"JSON file written successfully: {filename}")
        return True
    except Exception as e:
        print(f"Error writing JSON file: {str(e)}")
        return False

def write_csv_file(filename, products, category_name, timestamp):
    """Write products to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ranking', 'title', 'price', 'rating', 'category', 'extracted_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for product in products:
                product['category'] = category_name
                product['extracted_at'] = timestamp
                writer.writerow(product)
        print(f"CSV file written successfully: {filename}")
        return True
    except Exception as e:
        print(f"Error writing CSV file: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python file_writer.py <command> <args...>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "json":
        if len(sys.argv) < 3:
            print("Usage: python file_writer.py json <filename> <json_data>")
            sys.exit(1)
        filename = sys.argv[2]
        json_data = sys.argv[3]
        data = json.loads(json_data)
        write_json_file(filename, data)
    
    elif command == "csv":
        if len(sys.argv) < 6:
            print("Usage: python file_writer.py csv <filename> <products_json> <category> <timestamp>")
            sys.exit(1)
        filename = sys.argv[2]
        products_json = sys.argv[3]
        category = sys.argv[4]
        timestamp = sys.argv[5]
        products = json.loads(products_json)
        write_csv_file(filename, products, category, timestamp)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
