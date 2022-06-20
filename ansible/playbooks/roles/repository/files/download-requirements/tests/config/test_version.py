from src.config.version import Version


def test_version_major():
    assert Version('1.2.4') < Version('2.3.0dev')


def test_version_minor():
    assert Version('1.2.4') < Version('1.3.0dev')


def test_version_patch():
    assert Version('1.2.4') < Version('1.2.5dev')


def test_version_not():
    assert not (Version('1.2.4') < Version('1.1.0'))
