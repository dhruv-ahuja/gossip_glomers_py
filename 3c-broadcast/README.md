# multi-node fault-tolerant broadcast

Sample implementation for a multi node broadcast system that gossips messages to other nodes. This challenge introduces network partitions between nodes, disabling communication for periods of time.

Broadcasting data to all neighbours every second ensures that we eventually reach a point of consistency, despite network partitions.

## execution

- `chmod +x 3c-broadcast/main.py`
- `maelstrom test -w broadcast --bin 3c-broadcast/main.py --node-count 5 --time-limit 20 --rate 10 --nemesis partition`
