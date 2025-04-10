#!/usr/bin/env python3
"""
Extract reproducibility rates from reproducibility-experiment.json
"""

import json
import numpy as np
import sys
import os
from pathlib import Path

def process_reproducibility_data(json_file):
    """
    Extract reproducibility rates from the given JSON file and compute statistics.
    """
    # Check if file exists
    if not os.path.isfile(json_file):
        print(f"Error: File {json_file} does not exist.")
        return

    # Load JSON data
    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {json_file} is not a valid JSON file.")
            return

    # Extract reproducibility rates
    reproducibility_rates = []
    pattern_data = []

    # Handle both the new format (with reproducibility_experiments array)
    # and the old format (with a single experiment)
    if 'reproducibility_experiments' in data:
        experiments = data['reproducibility_experiments']
        for exp in experiments:
            pattern_id = exp['pattern_id']
            mapping_id = exp['mapping_id']
            repro_rate = exp['reproducibility_rate']
            reproducibility_rates.append(repro_rate)
            pattern_data.append({
                'pattern_id': pattern_id[:8],  # Just show first 8 chars for brevity
                'mapping_id': mapping_id[:8], 
                'reproducibility_rate': repro_rate
            })
    elif 'reproducibility' in data:
        # Old format with single experiment
        exp = data['reproducibility']
        pattern_id = exp['pattern_id']
        mapping_id = exp['mapping_id']
        repro_rate = exp['reproducibility_rate']
        reproducibility_rates.append(repro_rate)
        pattern_data.append({
            'pattern_id': pattern_id[:8],
            'mapping_id': mapping_id[:8],
            'reproducibility_rate': repro_rate
        })
    else:
        print("Error: Could not find reproducibility data in JSON.")
        return

    # Sort pattern data by reproducibility rate (highest first)
    pattern_data.sort(key=lambda x: x['reproducibility_rate'], reverse=True)
    
    # Calculate statistics
    if reproducibility_rates:
        repro_array = np.array(reproducibility_rates)
        stats = {
            'count': len(reproducibility_rates),
            'min': np.min(repro_array),
            'max': np.max(repro_array),
            'mean': np.mean(repro_array),
            'median': np.median(repro_array),
            'std_dev': np.std(repro_array)
        }
    else:
        stats = {
            'count': 0,
            'min': 0,
            'max': 0,
            'mean': 0,
            'median': 0,
            'std_dev': 0
        }
    
    return pattern_data, stats

def main():
    # Use provided filename or default
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = "reproducibility-experiment.json"
    
    result = process_reproducibility_data(json_file)
    if not result:
        return
    
    pattern_data, stats = result
    
    # Print summary statistics
    print("\n=== REPRODUCIBILITY SUMMARY ===")
    print(f"Number of patterns: {stats['count']}")
    print(f"Overall reproducibility rate: {stats['mean']:.4f} ({stats['mean']*100:.2f}%)")
    print(f"Median reproducibility rate: {stats['median']:.4f} ({stats['median']*100:.2f}%)")
    print(f"Minimum reproducibility rate: {stats['min']:.4f} ({stats['min']*100:.2f}%)")
    print(f"Maximum reproducibility rate: {stats['max']:.4f} ({stats['max']*100:.2f}%)")
    print(f"Standard deviation: {stats['std_dev']:.4f}")
    
    # Print individual pattern rates
    print("\n=== PATTERN REPRODUCIBILITY RATES ===")
    print(f"{'Pattern ID':10} {'Mapping ID':10} {'Repro Rate':10}")
    print(f"{'-'*10} {'-'*10} {'-'*10}")
    for p in pattern_data:
        print(f"{p['pattern_id']:10} {p['mapping_id']:10} {p['reproducibility_rate']:.4f}")
    
    # Save results to CSV
    csv_file = Path(json_file).stem + "_reproducibility.csv"
    with open(csv_file, "w") as f:
        f.write("pattern_id,mapping_id,reproducibility_rate\n")
        for p in pattern_data:
            f.write(f"{p['pattern_id']},{p['mapping_id']},{p['reproducibility_rate']}\n")
    
    print(f"\nData saved to {csv_file}")

if __name__ == "__main__":
    main()