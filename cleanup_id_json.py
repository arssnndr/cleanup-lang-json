#!/usr/bin/env python3
import json
import os

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

def remove_keys_recursively(obj, keys_to_keep, current_path=""):
    """Remove keys from nested JSON object that are not in the reference keys"""
    if isinstance(obj, dict):
        keys_to_delete = []
        for key in obj.keys():
            path = f"{current_path}.{key}" if current_path else key
            if path not in keys_to_keep:
                keys_to_delete.append(key)
            else:
                # Recursively clean nested objects
                if isinstance(obj[key], (dict, list)):
                    remove_keys_recursively(obj[key], keys_to_keep, path)
        
        # Remove keys that are not in en.json
        for key in keys_to_delete:
            del obj[key]
            print(f"Removed key: {current_path}.{key}" if current_path else f"Removed key: {key}")
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                path = f"{current_path}[{i}]"
                remove_keys_recursively(item, keys_to_keep, path)

def main():
    # File paths
    en_json_path = "en.json"
    id_json_path = "id.json"
    backup_path = "id.json.backup"
    
    # Check if files exist
    if not os.path.exists(id_json_path):
        print(f"Error: {id_json_path} not found!")
        return
    
    if not os.path.exists(en_json_path):
        print(f"Error: {en_json_path} not found!")
        return
    
    # Load JSON files
    print("Loading JSON files...")
    en_data = load_json_file(en_json_path)
    id_data = load_json_file(id_json_path)
    
    if en_data is None or id_data is None:
        print("Failed to load JSON files!")
        return
    
    # Create backup of id.json
    print(f"Creating backup: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(id_data, f, indent=2, ensure_ascii=False)
    
    # Get all keys from en.json
    print("Analyzing keys in en.json...")
    en_keys = get_all_keys(en_data)
    print(f"Found {len(en_keys)} keys in en.json")
    
    # Get all keys from id.json (before cleanup)
    id_keys_before = get_all_keys(id_data)
    print(f"Found {len(id_keys_before)} keys in id.json")
    
    # Find keys that exist in id.json but not in en.json
    extra_keys = id_keys_before - en_keys
    print(f"Found {len(extra_keys)} extra keys in id.json that don't exist in en.json")
    
    if extra_keys:
        print("\nExtra keys to be removed:")
        for key in sorted(extra_keys):
            print(f"  - {key}")
    
    # Remove extra keys from id.json
    print("\nRemoving extra keys from id.json...")
    remove_keys_recursively(id_data, en_keys)
    
    # Get all keys from id.json (after cleanup)
    id_keys_after = get_all_keys(id_data)
    print(f"\nAfter cleanup: {len(id_keys_after)} keys remain in id.json")
    print(f"Removed {len(id_keys_before) - len(id_keys_after)} keys")
    
    # Save the cleaned id.json
    print(f"\nSaving cleaned id.json...")
    with open(id_json_path, 'w', encoding='utf-8') as f:
        json.dump(id_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Cleanup completed successfully!")
    print(f"📁 Original file backed up as: {backup_path}")
    print(f"🧹 Cleaned file saved as: {id_json_path}")

if __name__ == "__main__":
    main()
