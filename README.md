# State Machine Client (MEQ challenge)

The​‍​‌‍​‍‌​‍​‌‍​‍‌ aim of this project is to have a Python TCP client that would be able to find and display a state machine with random states on the MEQ server. 
The concept states that the state machine has to be from A to Z, A is the initial state, Z is the terminal; every state except Z has actions "1","2","3". In order for the server to understand the requests of the client and to send the replies, every communication should end with ​‍​‌‍​‍‌​‍​‌‍​‍‌LF.
Note : LF is the Line Feed Character
## Features

-​‍​‌‍​‍‌​‍​‌‍​‍‌ A TCP client that issues commands "1","2","3" with LF to the server and reads LF-terminated responses

- Identifies the transitions to create a directed graph

- Renders the graph and stores `state_machine.png`

- The server IP and port are read from the environment ​‍​‌‍​‍‌​‍​‌‍​‍‌variables
## Ubuntu setup
```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
git clone https://github.com/SoftEngMajid/state-machine-client.git
cd state-machine-client
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

