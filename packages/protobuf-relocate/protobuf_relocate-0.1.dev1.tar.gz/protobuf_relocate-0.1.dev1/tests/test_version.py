from subprocess import check_output

from packaging.version import Version

from protobuf_relocate import __version__


def test_version():
    assert Version(__version__) > Version("0.0.0")


def test_cli():
    output = check_output(["python-protobuf-relocate", "--version"])
    output_text = output.decode('ascii')
    assert output_text == f"python-protobuf-relocate, version {__version__}\n"
