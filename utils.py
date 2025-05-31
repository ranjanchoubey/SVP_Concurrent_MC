import re
import subprocess
import os

def extract_stats(aig_file):
    """
    Extract circuit statistics from an AIG file using ABC.
    
    Args:
        aig_file (str): Path to the AIG file
        
    Returns:
        tuple: (number of inputs, number of flip-flops, number of AND gates)
               Returns (None, None, None) if extraction fails
    """
    try:
        # Run ABC command to get statistics
        result = subprocess.run(
            ["abc", "-c", f"read {aig_file}; print_stats"],
            capture_output=True,
            text=True
        )
        output = result.stdout + result.stderr
        
        # Parse the output to extract the required statistics
        for line in output.strip().splitlines():
            if "i/o =" in line and "lat =" in line and "and =" in line:
                match = re.search(r"i/o\s*=\s*(\d+)\s*/\s*\d+\s+lat\s*=\s*(\d+)\s+and\s*=\s*(\d+)", line)
                if match:
                    return int(match.group(1)), int(match.group(2)), int(match.group(3))
    except Exception as e:
        print(f"extract_stats error on {aig_file}: {e}")
    
    # Return None values if extraction fails
    return None, None, None
