from dh_workspace import greet


def test_greet_default():
    assert greet() == "Hello, World!"
