# The Benefit of Concurrency in Model Checking

This project implements a **concurrent model checking framework** for hardware verification on sequential circuits using [ABC](https://github.com/berkeley-abc/abc). It is based on the research paper:

**The Benefit of Concurrency in Model Checking**  
Baruch Sterin, Niklas Een, Alan Mishchenko, and Robert Brayton  
Berkeley Verification and Synthesis Research Center (BVSRC),  
University of California, Berkeley  
[Paper Link (IWLS 2011)](https://people.eecs.berkeley.edu/~alanmi/publications/2011/iwls11_par.pdf)

---

##  Project Context

This project was developed as part of the **Verification of Programs** course under the guidance of:

**Prof. Ansuman Banerjee**  
Professor, Indian Statistical Institute, Kolkata  
Verified email: ansuman@isical.ac.in

**Project Contributors**  
- Ranjan Kumar Choubey, M.Tech CS, ISI Kolkata  
- Mona Kumari, M.Tech CS, ISI Kolkata  

---

##  Installation

### Prerequisites

- Linux (Ubuntu recommended)
- Python 3.7+
- Git
- Build tools (`gcc`, `make`, etc.)

### Installing ABC

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake git bison flex
git clone https://github.com/berkeley-abc/abc.git
cd abc && make -j4 && cd ..
sudo cp abc/abc /usr/local/bin/
abc -c "help"
```

---

### Setting up Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

##  Dataset Setup

### HWMCC'10 Benchmarks

```bash
sudo apt-get install -y p7zip-full
mkdir -p dataset
wget https://fmv.jku.at/hwmcc/hwmcc10-except-intel-aiger1.7z -O hwmcc10.7z
7z x hwmcc10.7z -o dataset
```

### Custom AIG Files

Place your `.aig` files in the dataset folder:
```bash
cp /path/to/your/files/*.aig dataset/
```

---

##  Usage

Run the framework:
```bash
python main.py
```

This will:
1. Load selected AIG files from the dataset
2. Use multiple ABC engines in parallel
3. Stop when the first conclusive result (SAT/UNSAT) is found
4. Save results in `results.csv`

---

##  Configuration

Edit `main.py`:
- `ENGINE_LIST`: List of ABC engines (e.g., `["pdr", "bmc", "int"]`)
- `TIMEOUT`: Per-engine timeout in seconds
- `BENCHMARK_DIR` and `selected`: Specify dataset location and files

---

##  Available Verification Engines

| Engine   | Description                                                  |
|----------|--------------------------------------------------------------|
| `pdr`    | Property Directed Reachability (strong for safety)           |
| `bmc`    | Bounded Model Checking                                       |
| `int`    | Interpolation-based Model Checking                           |
| `sim`    | Random Simulation (lightweight)                              |
| `dprove` | Auto engine strategy selection                               |
| `smt`    | SMT-based checking (if compiled with SMT support)            |

---

##  Output

A `results.csv` is generated with:
- Benchmark name
- Circuit statistics (inputs, FFs, ANDs)
- Verification result (SAT/UNSAT/UNKNOWN)
- Engine that succeeded
- Time taken (sec)

---

## 🛠 Troubleshooting

### ABC Not Found

```bash
sudo ln -s $(pwd)/abc/abc /usr/local/bin/abc
```

### Temp Directory Permissions

```bash
chmod -R 755 temp
```

### Memory/Timeout

Increase `TIMEOUT` in `main.py` or run on a larger machine.

---

##  Reference

Sterin, Een, Mishchenko, Brayton.  
**"The Benefit of Concurrency in Model Checking"**,  
IWLS 2011 — [Link](https://people.eecs.berkeley.edu/~alanmi/publications/2011/iwls11_par.pdf)
