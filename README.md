# sched

List scheduler for a directed acyclic graph of arithmetic operations.

## Machine

- One multiplier, latency 3
- One adder, latency 1

An operation uses its unit on the cycle it issues. The result is ready `latency` cycles later. A consumer may start at `producer start + producer latency`. Length is the maximum of `start + latency`. If two ready operations have the same slack, the alphabetically earlier name goes first.

## Graphs

1. Adds `a -> b -> c`. Starts: a 0, b 1, c 2. Length 3.
2. Independent multiplies `m0`, `m1`. Starts: m0 0, m1 1. Length 4.
3. Multiply `m` feeds add `a`. Starts: m 0, a 3. Length 4.
4. Multiply `mc` feeds add `a1`, which feeds add `a2`. Independent multiply `mf` has no successor. Starts: mc 0, mf 1, a1 3, a2 4. Length 5. Issuing `mf` first stretches the length to 6.
5. `a` depends on `b` and `b` depends on `a`. Rejected.

Slack is `ALAP start - ASAP start`, with no resource limit. It is not the start cycle. A slack of 0 means the operation is on the critical path: its earliest start and its latest start are the same.

Graph 4, critical-path length 5:

| op | depends on | ASAP start | ALAP start | slack |
| --- | --- | --- | --- | --- |
| `mc` | | 0 | 0 | 0 |
| `a1` | `mc` | 3 | 3 | 0 |
| `a2` | `a1` | 4 | 4 | 0 |
| `mf` | | 0 | 2 | 2 |

`a1` cannot start at 0. It starts at 3, after `mc`'s latency. It also cannot start later than 3, or `a2` finishes after cycle 5, so its slack is 0. `mf` may start at 0, 1, or 2 and still finish by 5, so its slack is 2.