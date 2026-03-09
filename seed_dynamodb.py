import boto3
import json
from decimal import Decimal

# Helper to convert float to Decimal for DynamoDB
def parse_float(v):
    return Decimal(str(v))

def seed_dynamodb():
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('SoochnaSetu-Schemes')
    
    # Check if table exists
    table.load()
    
    with open('backend/data/schemes_seed.json', 'r', encoding='utf-8') as f:
        schemes = json.loads(f.read(), parse_float=parse_float)
        
    print(f"Loaded {len(schemes)} schemes. Seeding DynamoDB...")
    with table.batch_writer() as batch:
        for scheme in schemes:
            # Clean empty strings if any, DynamoDB doesn't like empty string sets or similar, but string values are fine.
            # Handle float conversions handled by parse_float
            batch.put_item(Item=scheme)
            
    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_dynamodb()
