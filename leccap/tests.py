from __future__ import absolute_import
from .config import ConfigParser

def test_config():
    c = ConfigParser()
    c.set("logins.username", "test1")
    assert c.get("logins.username") == "test1"
    c.set("concurrency", 10)
    assert c.get("concurrency") == 10

def test_all():
    test_config()

if __name__ == "__main__":
    test_all()
