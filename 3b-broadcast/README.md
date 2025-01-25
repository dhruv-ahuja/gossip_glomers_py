# multi-node broadcast

Sample implementation for a multi node broadcast system that gossips messages to other nodes. There is no network partition in this challenge.

## execution

- `chmod +x 3b-broadcast/main.py`
- `maelstrom test -w broadcast --bin 3b-broadcast/main.py --node-count 2 --time-limit 20 --rate 10`
