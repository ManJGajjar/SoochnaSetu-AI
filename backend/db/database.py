import json
import os
import boto3
from decimal import Decimal

def _convert_decimals(obj):
    if isinstance(obj, list):
        return [_convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: _convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

def get_dynamodb():
    region = os.getenv("AWS_REGION", "ap-south-1")
    return boto3.resource("dynamodb", region_name=region)

def get_table(table_name: str):
    return get_dynamodb().Table(table_name)

def init_db():
    pass

def seed_schemes(db):
    pass

def get_all_schemes():
    table = get_table('SoochnaSetu-Schemes')
    try:
        response = table.scan()
        items = response.get('Items', [])
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
            
        result = []
        for d in _convert_decimals(items):
            if not d.get("isActive", True):
                continue
            d["isActive"] = bool(d.get("isActive", 1))
            result.append(d)
        return result
    except Exception as e:
        print(f"Error fetching schemes from DynamoDB: {e}")
        return []

def get_scheme_by_id(scheme_id: str):
    table = get_table('SoochnaSetu-Schemes')
    try:
        response = table.get_item(Key={'schemeId': scheme_id})
        item = response.get('Item')
        if not item:
            return None
        d = _convert_decimals(item)
        d["isActive"] = bool(d.get("isActive", 1))
        return d
    except Exception as e:
        print(f"Error fetching scheme by ID: {e}")
        return None

def get_db():
    return None
