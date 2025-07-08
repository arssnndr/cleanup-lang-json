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
    print("🔍 Verifying final cleanup results...")
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
    
    # Check for differences
    extra_keys_in_en = en_keys - id_keys
    extra_keys_in_id = id_keys - en_keys
    
    print("\n📊 Analysis Results:")
    print(f"  - Keys only in en.json: {len(extra_keys_in_en)}")
    print(f"  - Keys only in id.json: {len(extra_keys_in_id)}")
    
    if extra_keys_in_en:
        print(f"\n❌ Keys only in en.json:")
        for key in sorted(extra_keys_in_en):
            print(f"  - {key}")
    
    if extra_keys_in_id:
        print(f"\n❌ Keys only in id.json:")
        for key in sorted(extra_keys_in_id):
            print(f"  - {key}")
    
    # Final verification
    if extra_keys_in_en == set() and extra_keys_in_id == set():
        print("\n✅ PERFECT! Both files have identical key structures!")
        print("🎉 Cleanup completed successfully - both files are now synchronized!")
    else:
        print(f"\n⚠️  Files still have differences:")
        print(f"   - Total unique keys in en.json: {len(extra_keys_in_en)}")
        print(f"   - Total unique keys in id.json: {len(extra_keys_in_id)}")
    
    # Summary
    print(f"\n📋 Final Summary:")
    print(f"  - id.json: {len(id_keys)} keys")
    print(f"  - en.json: {len(en_keys)} keys")
    print(f"  - Key structure match: {'✅ YES' if len(extra_keys_in_en) == 0 and len(extra_keys_in_id) == 0 else '❌ NO'}")

if __name__ == "__main__":
    main()
