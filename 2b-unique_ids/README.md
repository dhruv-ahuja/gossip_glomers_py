# unique-ids

This instance uses string combining a random integer from 0 to system-maximum limit (9223372036854775807 in my case) and the request's POSIX timestamp.
This yields almost neglibly better performance than the UUID4 generation method.

## output

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

- `chmod +x 2b-unique_ids/id_gen.py`
- `maelstrom test -w unique-ids --bin 2b-unique_ids/id_gen.py --time-limit 30 --rate 1000 --node-count 3 --availability total --nemesis partition`
