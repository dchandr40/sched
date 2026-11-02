def test_graph1_length():
    starts = {"a": 0, "b": 1, "c": 2}
    latency = 1
    length = max(start + latency for start in starts.values())
    assert length == 3