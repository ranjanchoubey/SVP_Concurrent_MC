import os
import pandas as pd
from IPython.display import display
import shutil

# Import from our modules
from utils import extract_stats
from verification import run_concurrent_engines
from transformation import c_prove

def setup_temp_dir():
    """
    Create a temporary directory for intermediate files.
    Clean up any existing temporary directory.
    
    Returns:
        str: Path to the temporary directory
    """
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
    
    # Clean up existing temp directory if it exists
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    # Create a new temp directory
    os.makedirs(temp_dir)
    
    return temp_dir

def batch_run(aig_files, engines, timeout, temp_dir):
    """
    Run verification on a batch of AIG files and collect results.
    
    Args:
        aig_files (list): List of paths to AIG files
        engines (list): List of verification engines to use
        timeout (int): Maximum time (in seconds) to allow each verification engine to run
        temp_dir (str): Directory to store temporary files
        
    Returns:
        DataFrame: Results of verification in a pandas DataFrame
    """
    results = []
    for aig_file in aig_files:
        print(f"\n Running dataset: {aig_file}")
        
        # Extract circuit statistics
        pi, ff, ands = extract_stats(aig_file)
        
        try:
            # Run verification with transformations
            res_type, engine, t = c_prove(aig_file, engines, timeout, temp_dir)
            
            # Store results
            results.append({
                "dataset": aig_file,
                "Inputs": pi,
                "FFs": ff,
                "ANDs": ands,
                "Result": res_type,
                "Engine": engine,
                "Time (sec)": round(t, 2) if t else "-"
            })
        except Exception as e:
            # Handle exceptions and record errors
            results.append({
                "dataset": aig_file,
                "Inputs": pi,
                "FFs": ff,
                "ANDs": ands,
                "Result": "ERROR",
                "Engine": "-",
                "Time (sec)": "-"
            })
    
    # Convert results to DataFrame
    return pd.DataFrame(results)


def main():
    """
    Main entry point for the verification framework.
    
    Configures verification parameters, runs the verification process,
    and saves results to a CSV file.
    """
    # Configuration
    engines = ["pdr", "bmc", "int", "dprove", "sim"]
    timeout = 120
    
    dataset_files = [
        "dataset/139442p0.aig",
        "dataset/bc57sensorsp0.aig",
        "dataset/bj08amba3g3.aig",
        "dataset/bob1u05cu.aig",
    ]

    # Setup temporary directory
    temp_dir = setup_temp_dir()
    
    try:
        # Run verification on datasets
        df = batch_run(dataset_files, engines, timeout, temp_dir)
        
        # Display and save results
        display(df)
        df.to_csv("dataset_results.csv", index=False)
    finally:
        # Clean up ABC history file
        abc_history = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abc.history")
        if os.path.exists(abc_history):
            os.remove(abc_history)

if __name__ == "__main__":
    main()




