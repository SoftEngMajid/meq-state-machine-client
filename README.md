# MEQ State Machine Client – Full Solution

This branch contains the **complete solution** for the MEQ challenge. 
It implements a TCP client that communicates with the MEQ server using LF‑terminated commands, explores all reachable states, and produces a clear summary of transitions along with a rendered diagram.

---

## Features
- LF‑terminated TCP client (`client.py`) 
- Environment‑based server configuration (`.env`) 
- Directed graph visualization (`visualize.py`) 
- Deduplicated edges for clean diagrams 
- Diagram output (`images/state_machine.png`) 
- Clear branching strategy: 
  - `main` → skeleton setup 
  - `state_machine` → full solution 

---

## Setup (Ubuntu)

Install required system packages:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip graphviz graphviz-dev
```

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/SoftEngMajid/meq-state-machine-client.git
cd meq-state-machine-client
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Requirements

The project depends on:

```
python-dotenv
networkx
pygraphviz
```

These are listed in `requirements.txt`.

---

## Environment Configuration

Create a `.env` file in the project root:

```
SERVER_IP=4.197.189.229
SERVER_PORT=65432
```

`.env` is ignored by Git for security. 
Use `.env.example` as a safe template for reviewers.

---

## Running the Client

Run the client to explore the state machine:

```bash
python3 client.py
```

The program will:
- Connect to the server 
- Explore all possible transitions 
- Print each transition in the format: 
  ```
  [Transition] A --(1)--> N
  ```
- At the end, print a structured summary of each state, including: 
  - Actions tried 
  - Shortest entry path 
  - Shortest exit path 

---

## Visualizing the State Machine

After running the client, a diagram is generated automatically:

- Output file: `images/state_machine.png`

The diagram shows:
- States as rounded boxes 
- Transitions labeled with action numbers 
- Left‑to‑right layout for readability 
- Deduplicated edges for clarity 

---

## Files in This Branch
- `client.py` → TCP client logic, exploration, and summary 
- `visualize.py` → Graphviz rendering with deduplication 
- `README.md` → Full documentation 
- `requirements.txt` → Python dependencies (`networkx`, `python-dotenv`, `pygraphviz`) 
- `.gitignore` → excludes `.env`, caches, IDE files 
- `.env.example` → safe template for server IP/Port 
- `images/state_machine.png` → rendered diagram 

---
