# test_hello.py
import pytest
from src.main import hello_world # <--- THIS IMPORT IS CRUCIAL AND MUST BE CORRECT

def test_true_is_true():
    """A basic test to confirm pytest is working."""
    assert True is True

def test_hello_world_output():
    """Tests if the hello_world function returns the expected string."""
    assert hello_world() == "Hello World"