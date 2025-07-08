#!/usr/bin/env python3
import json

def load_json_file(file_path):
    """Load JSON file and return as dictionary"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def get_all_keys(obj, prefix=""):
    """Get all keys from nested JSON object as a set of dot-notation paths"""
    keys = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{prefix}.{key}" if prefix else key
            keys.add(current_path)
            if isinstance(value, (dict, list)):
                keys.update(get_all_keys(value, current_path))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            current_path = f"{prefix}[{i}]"
            if isinstance(item, (dict, list)):
                keys.update(get_all_keys(item, current_path))
    return keys

def main():
    # Load JSON files
    print("Loading JSON files...")
    id_data = load_json_file("id.json")
    en_data = load_json_file("en.json")
    
    if id_data is None or en_data is None:
        print("Failed to load JSON files!")
        return
    
    # Get all keys from both files
    id_keys = get_all_keys(id_data)
    en_keys = get_all_keys(en_data)
    
    print(f"Keys in id.json: {len(id_keys)}")
    print(f"Keys in en.json: {len(en_keys)}")
    
    # Check for extra keys in en.json
    extra_keys = en_keys - id_keys
    missing_keys = id_keys - en_keys
    
    if extra_keys:
        print(f"\n❌ Found {len(extra_keys)} extra keys in en.json:")
        for key in sorted(extra_keys):
            print(f"  - {key}")
    else:
        print("\n✅ No extra keys found in en.json - cleanup successful!")
    
    if missing_keys:
        print(f"\n⚠️  Found {len(missing_keys)} keys missing in en.json:")
        for key in sorted(list(missing_keys)[:10]):  # Show first 10 only
            print(f"  - {key}")
        if len(missing_keys) > 10:
            print(f"  ... and {len(missing_keys) - 10} more")
    else:
        print("\n✅ All keys from id.json are present in en.json!")
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"  - id.json: {len(id_keys)} keys")
    print(f"  - en.json: {len(en_keys)} keys")
    print(f"  - Extra keys in en.json: {len(extra_keys)}")
    print(f"  - Missing keys in en.json: {len(missing_keys)}")

if __name__ == "__main__":
    main()
