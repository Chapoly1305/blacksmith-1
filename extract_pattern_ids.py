#!/usr/bin/env python3
import json
import argparse
import sys

def extract_pattern_ids(json_file):
    """Extract all pattern IDs from a Blacksmith JSON summary file."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {json_file} is not a valid JSON file.")
        return []
    except FileNotFoundError:
        print(f"Error: File {json_file} not found.")
        return []
    
    pattern_ids = []
    
    # Check if this is the new format with a "hammering_patterns" key
    if "hammering_patterns" in data:
        patterns = data["hammering_patterns"]
    # Or the old format where patterns are directly in the root array
    elif isinstance(data, list):
        patterns = data
    else:
        print("Warning: No patterns found in the JSON file. Unexpected format.")
        return []
    
    # Extract pattern IDs
    for pattern in patterns:
        if "id" in pattern:
            pattern_ids.append(pattern["id"])
        # Some older files might use "instance_id" instead
        elif "instance_id" in pattern:
            pattern_ids.append(pattern["instance_id"])
    
    return pattern_ids

def main():
    parser = argparse.ArgumentParser(description='Extract pattern IDs from Blacksmith JSON summary file.')
    parser.add_argument('json_file', help='Path to the Blacksmith JSON summary file')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    parser.add_argument('--count', '-c', action='store_true', help='Only print the count of patterns')
    
    args = parser.parse_args()
    
    pattern_ids = extract_pattern_ids(args.json_file)
    
    if args.count:
        print(f"Found {len(pattern_ids)} patterns in {args.json_file}")
        return
    
    # Prepare output
    output = "\n".join(pattern_ids)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Extracted {len(pattern_ids)} pattern IDs to {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()