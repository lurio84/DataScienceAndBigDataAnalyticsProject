import pandas as pd
from pymongo import MongoClient
import os
import sys

def check_csv_file(filename):
    """Check if CSV file exists"""
    if not os.path.exists(filename):
        print(f"Error: {filename} not found in current directory")
        print("Please make sure 'clean_sample.csv' is in the same directory as this script")
        return False
    return True

def connect_to_mongodb():
    """Connect to MongoDB with error handling"""
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print("Please make sure MongoDB is running on localhost:27017")
        return None

def setup_database_and_collection(client, db_name, collection_name):
    """Create database and collection if they don't exist"""
    try:
        # Get database (creates if doesn't exist)
        db = client[db_name]
        
        # Check if collection exists
        if collection_name in db.list_collection_names():
            print(f"Collection '{collection_name}' already exists in database '{db_name}'")
            response = input("Do you want to clear existing data? (y/n): ").lower()
            if response == 'y':
                db[collection_name].delete_many({})
                print(f"Cleared existing data from '{collection_name}'")
        else:
            print(f"Creating new collection '{collection_name}' in database '{db_name}'")
        
        collection = db[collection_name]
        return db, collection
        
    except Exception as e:
        print(f"Error setting up database/collection: {e}")
        return None, None

def main():
    """Main function to import CSV data to MongoDB"""
    csv_filename = "clean_sample.csv"
    db_name = "game_reviews_db"
    collection_name = "clean_sample_reviews"
    
    print("Starting CSV to MongoDB import process...")
    
    # Check if CSV file exists
    if not check_csv_file(csv_filename):
        sys.exit(1)
    
    # Connect to MongoDB
    client = connect_to_mongodb()
    if not client:
        sys.exit(1)
    
    # Setup database and collection
    db, collection = setup_database_and_collection(client, db_name, collection_name)
    if not db or not collection:
        sys.exit(1)
    
    try:
        # Read CSV
        print(f"Reading {csv_filename}...")
        df = pd.read_csv(csv_filename)
        print(f"Found {len(df)} rows in CSV file")
        
        # Replace NaN with None for MongoDB compatibility
        df = df.where(pd.notnull(df), None)
        
        # Convert DataFrame to dictionary records
        records = df.to_dict(orient="records")
        
        # Insert data into MongoDB
        print(f"Inserting {len(records)} records into MongoDB...")
        result = collection.insert_many(records)
        
        print(f"Data inserted successfully!")
        print(f"Inserted {len(result.inserted_ids)} documents")
        print(f"Database: {db_name}")
        print(f"Collection: {collection_name}")
        
        # Show sample data
        print("\nSample document from collection:")
        sample = collection.find_one()
        if sample:
            for key, value in list(sample.items())[:5]:  # Show first 5 fields
                print(f"  {key}: {value}")
        
        print(f"\nTotal documents in collection: {collection.count_documents({})}")
        
    except FileNotFoundError:
        print(f"Error: {csv_filename} not found")
    except pd.errors.EmptyDataError:
        print(f"Error: {csv_filename} is empty")
    except Exception as e:
        print(f"Error during import: {e}")
    finally:
        client.close()
        print("MongoDB connection closed")

if __name__ == "__main__":
    main()


