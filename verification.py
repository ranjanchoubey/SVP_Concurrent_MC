import sys
sys.dont_write_bytecode = True

import time
import multiprocessing as mp
import subprocess
import sys

def abc_worker(aig_file, engine, timeout, result_queue):
    """
    Worker function to run a verification engine on an AIG file.
    
    Args:
        aig_file (str): Path to the AIG file
        engine (str): ABC verification engine to use (e.g., 'pdr', 'bmc')
        timeout (int): Maximum time (in seconds) to allow engine to run
        result_queue (Queue): Queue to store the results
    """
    # Construct ABC command
    cmd = f'read {aig_file}; {engine}; print_stats'
    start = time.time()
    
    try:
        # Run ABC verification command
        result = subprocess.run(["abc", "-c", cmd], capture_output=True, text=True, timeout=timeout)
        end = time.time()
        output = result.stdout + result.stderr
        print(f"\n--- Output from {engine} ---\n{output}\n------------------------")

        # Parse results to determine verification outcome
        output_lower = output.lower()
        if "unsat" in output_lower or "property proved" in output_lower:
            result_queue.put(("UNSAT", engine, end - start))
        elif "sat" in output_lower or "counterexample" in output_lower:
            result_queue.put(("SAT", engine, end - start))
        else:
            result_queue.put(("UNKNOWN", engine, end - start))
    except subprocess.TimeoutExpired:
        result_queue.put(("TIMEOUT", engine, timeout))

def run_concurrent_engines(aig_file, engines, timeout):
    """
    Run multiple verification engines in parallel and return the first conclusive result.
    
    Args:
        aig_file (str): Path to the AIG file
        engines (list): List of ABC verification engines to use
        timeout (int): Maximum time (in seconds) to allow each engine to run
        
    Returns:
        tuple: (result_type, engine_name, execution_time)
               result_type can be "SAT", "UNSAT", "UNKNOWN"
    """
    # Create a manager to handle communication between processes
    manager = mp.Manager()
    result_queue = manager.Queue()
    
    # Start a process for each verification engine
    processes = [mp.Process(target=abc_worker, args=(aig_file, engine, timeout, result_queue)) 
                for engine in engines]
    
    for p in processes: 
        p.start()

    # Wait for a definitive result (SAT or UNSAT)
    result = None
    for _ in range(len(engines)):
        res_type, res_engine, res_time = result_queue.get()
        if res_type in ["SAT", "UNSAT"]:
            result = (res_type, res_engine, res_time)
            break

    # Terminate all processes once we have a result
    for p in processes:
        p.terminate()
        p.join()
        
    return result if result else ("UNKNOWN", None, None)
