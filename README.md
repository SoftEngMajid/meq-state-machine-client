# MEQ State Machine Client – Skeleton

This branch contains the **initial skeleton setup** for the MEQ client.  
It provides the basic environment and dependency configuration.  
The full solution is available in the `state_machine` branch.

---

## Setup (Ubuntu)

Install required system packages:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip graphviz graphviz-dev
```

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/<your-username>/meq-state-machine-client.git
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

## Environment Variables

The client requires server details to be provided via environment variables.  
Create a `.env` file in the project root with the following values:

```
SERVER_IP=4.197.189.229
SERVER_PORT=65432
```

`.env` is ignored by Git for security.  
Use `.env.example` in the `state_machine` branch as a template.

---

## Branches

- `main` → skeleton setup (this branch)  
- `state_machine` → full solution with client logic, visualization, and diagram  

---

This skeleton branch ensures reviewers can set up the environment, install dependencies, and understand the branch structure, while the full solution lives in `state_machine`.

---
