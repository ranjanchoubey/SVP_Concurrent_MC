import os
import subprocess
from verification import run_concurrent_engines

def transform_and_verify(aig_filename, transform_cmds, stage_name, engines, timeout, temp_dir):
    """
    Transform an AIG file using ABC commands and verify the transformed file.
    
    Args:
        aig_filename (str): Path to the input AIG file
        transform_cmds (str): ABC commands to transform the AIG
        stage_name (str): Name of the transformation stage for logging
        engines (list): List of verification engines to use
        timeout (int): Maximum time (in seconds) to allow each verification engine to run
        temp_dir (str): Directory to store temporary files
        
    Returns:
        tuple: Verification result (result_type, engine_name, execution_time)
    """
    print(f"\n Running {stage_name} phase...")

    # Create a temporary file for the transformed AIG in the temp directory
    transformed_aig = os.path.join(temp_dir, f"{stage_name}_{os.path.basename(aig_filename)}")
    abc_script = f"read {aig_filename}; {transform_cmds}; write {transformed_aig}"
    
    # Run ABC to transform the circuit
    print("abc_script:", abc_script)
    result = subprocess.run(["abc", "-c", abc_script], capture_output=True, text=True)

    # Show transform log for debugging
    output = result.stdout + result.stderr
    print(f"\n--- Transform Output ({stage_name}) ---\n{output}\n------------------------")

    # Check if transformation was successful
    if not os.path.exists(transformed_aig) or os.path.getsize(transformed_aig) == 0:
        print(f"ABC transform failed for {aig_filename} during {stage_name}")
        return ("FAIL", None, None)

    # Verify the transformed AIG
    return run_concurrent_engines(transformed_aig, engines, timeout)

def c_prove(aig_file, engines, timeout, temp_dir):
    """
    Perform a common proof sequence on an AIG file.
    
    This function applies a sequence of simplification transforms
    before attempting verification.
    
    Args:
        aig_file (str): Path to the AIG file
        engines (list): List of verification engines to use
        timeout (int): Maximum time (in seconds) to allow each verification engine to run
        temp_dir (str): Directory to store temporary files
        
    Returns:
        tuple: Verification result (result_type, engine_name, execution_time)
    """
    # Apply simplification transforms and verify
    return transform_and_verify(
        aig_file, 
        "dc2; rewrite; retime -o; strash", 
        "simplify", 
        engines, 
        timeout,
        temp_dir
    )
