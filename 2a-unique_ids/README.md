# unique-ids

Uses string-converted UUID4 IDs to ensure uniqueness.

## output

```
{ ...
 :net {:all {:send-count 49682,
             :recv-count 49682,
             :msg-count 49682,
             :msgs-per-op 2.0002415},
       :clients {:send-count 49682,
                 :recv-count 49682,
                 :msg-count 49682},
       :servers {:send-count 0,
                 :recv-count 0,
                 :msg-count 0,
                 :msgs-per-op 0.0},
       :valid? true},
 :workload {:valid? true,
            :attempted-count 24838,
            :acknowledged-count 24838,
            :duplicated-count 0,
            :duplicated {},
            :range ["00065ffe-01fb-429a-a131-3a94b0b1451f"
                    "fffdf123-f68e-4ac2-b174-56c171f85fa8"]},
 :valid? true}
```

## execution

- `chmod +x 2a-unique_ids/id_gen.py`
- `maelstrom test -w unique-ids --bin 2a-unique_ids/id_gen.py --time-limit 30 --rate 1000 --node-count 3 --availability total --nemesis partition`
