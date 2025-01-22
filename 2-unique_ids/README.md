# unique-ids

`uuid_gen` uses string-converted UUID4 IDs to ensure uniqueness.

`timestamped` uses a string combining a cryptographically-secure random intenger and the POSIX timestamp at the time of request.
This yields almost neglibly better performance than the UUID4 generation method.

## output

`uuid_gen`:

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

`timestamped`:

```
{ ...
 :net {:all {:send-count 49810,
             :recv-count 49810,
             :msg-count 49810,
             :msgs-per-op 2.000241},
       :clients {:send-count 49810,
                 :recv-count 49810,
                 :msg-count 49810},
       :servers {:send-count 0,
                 :recv-count 0,
                 :msg-count 0,
                 :msgs-per-op 0.0},
       :valid? true},
 :workload {:valid? true,
            :attempted-count 24902,
            :acknowledged-count 24902,
            :duplicated-count 0,
            :duplicated {},
            :range ["10000307800144602181737274490"
                    "9995742327677228931737274495"]},
 :valid? true}
```

## execution

`uuid_gen`:

- `chmod +x 2-unique_ids/uuid_gen.py`
- `maelstrom test -w unique-ids --bin 2-unique_ids/uuid_gen.py --time-limit 30 --rate 1000 --node-count 3 --availability total --nemesis partition`

`timestamped`:

- `chmod +x 2-unique_ids/timestamped.py`
- `maelstrom test -w unique-ids --bin 2-unique_ids/timestamped.py --time-limit 30 --rate 1000 --node-count 3 --availability total --nemesis partition`
