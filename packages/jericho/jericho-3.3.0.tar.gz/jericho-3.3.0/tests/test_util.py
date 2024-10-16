from jericho.util import chunk

def test_chunk():
    chunks = chunk("ABCDEF", n=3)
    assert chunks == ["AB", "CD", "EF"]