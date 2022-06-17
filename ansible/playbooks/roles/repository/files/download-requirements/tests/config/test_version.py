from src.config.version import Version


def test_version_1():
    assert Version('1.2.4') < Version('2.3.0dev')


def test_version_2():
    assert not (Version('1.2.4') < Version('1.1.0'))
