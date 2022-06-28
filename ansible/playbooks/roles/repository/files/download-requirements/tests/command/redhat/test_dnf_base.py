from src.command.redhat.dnf import DnfBase


def test_filter_non_critical_errors():
    STDERR = '\n'.join([
        '1st line',
        'Failed to set locale, defaulting to C.UTF-8',
        '3rd line'])

    base = DnfBase(1)
    output = base._filter_non_critical_errors(STDERR)
    assert output == "1st line\n3rd line"
