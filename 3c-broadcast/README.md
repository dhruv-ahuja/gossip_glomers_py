# multi-node fault-tolerant broadcast

Sample implementation for a multi node broadcast system that gossips messages to other nodes. This challenge introduces network partitions between nodes, disabling communication for periods of time.

## execution

- `chmod +x 3c-broadcast/main.py`
- `maelstrom test -w broadcast --bin 3c-broadcast/main.py --node-count 5 --time-limit 20 --rate 10 --nemesis partition`
