import io
import os
import tempfile
import unittest
import unittest.mock

import pytest

import joft.utils


def test_load_valid_yaml() -> None:
    """Quick test to check the loading of yaml files."""

    yaml_obj = joft.utils.load_and_parse_yaml_file("./tests/mock_data/valid.yaml")
    assert type(yaml_obj) is dict
    assert "kind" in yaml_obj.keys()
    assert "metadata" in yaml_obj.keys()
    assert "triggers" in yaml_obj.keys()
    assert "apiVersion" in yaml_obj.keys()


def test_load_invalid_yaml_raise() -> None:
    """The function should raise if the yaml file is invalid."""

    with pytest.raises(Exception):
        joft.utils.load_and_parse_yaml_file("./tests/mock_data/invalid.yaml")


@unittest.mock.patch("joft.utils.pathlib.Path.cwd")
@unittest.mock.patch("joft.utils.platformdirs")
def test_load_toml_app_config(mock_platformdirs, mock_cwd) -> None:
    """Test if we can find the app config file in one of the platform dirs

    Assert that user_config_dir is preferred over site_config_dir."""
    config_file_contents = """[jira.server]
    hostname = "{name}"
    pat_token = "__pat_token__"
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        mock_cwd.return_value = tmpdir
        dir_names = ["etc", ".config"]
        for name in dir_names:
            config_dir = os.path.join(tmpdir, name)
            os.makedirs(config_dir)

            with open(os.path.join(config_dir, "joft.config.toml"), "w") as fp:
                fp.write(config_file_contents.format(name=name))

        mock_platformdirs.user_config_dir.return_value = os.path.join(tmpdir, ".config")
        mock_platformdirs.site_config_dir.return_value = os.path.join(tmpdir, "etc")

        config = joft.utils.load_toml_app_config()

    assert config["jira"]["server"]["hostname"] == ".config"
    assert config["jira"]["server"]["pat_token"] == "__pat_token__"


@unittest.mock.patch("joft.utils.pathlib.Path.cwd")
@unittest.mock.patch("joft.utils.platformdirs")
def test_load_toml_app_config_no_config_found(mock_platformdirs, mock_cwd) -> None:
    """
    Test that we will end with a non-zero error code when there is no config present and
    printing a message on the stdout.
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        mock_cwd.return_value = tmpdir

        for name in "etc", ".config":
            config_dir = tmpdir + "/" + name
            os.makedirs(config_dir)

        mock_platformdirs.user_config_dir.return_value = tmpdir + "/" + ".config"
        mock_platformdirs.site_config_dir.return_value = ""

        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            with pytest.raises(SystemExit) as sys_exit:
                joft.utils.load_toml_app_config()

    assert "Cannot find configuration file" in mock_stdout.getvalue()
    assert sys_exit.value.args[0] == 1


@unittest.mock.patch("joft.utils.pathlib.Path.cwd")
def test_load_toml_app_config_invalid_config_found(mock_cwd) -> None:
    """
    Test that we will end with a non-zero error code when there is an invalid
    config present and printing a message on the stdout.
    """

    invalid_config_file_contents = """[jira.server]
    pat_token = "__pat_token__"
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        mock_cwd.return_value = tmpdir

        config_file_path = os.path.join(tmpdir, "joft.config.toml")
        with open(config_file_path, "w") as fp:
            fp.write(invalid_config_file_contents)

        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            with pytest.raises(SystemExit) as sys_exit:
                joft.utils.load_toml_app_config()

    assert f"Configuration file {config_file_path} is invalid" in mock_stdout.getvalue()
    assert "KeyError - 'hostname'" in mock_stdout.getvalue()
    assert sys_exit.value.args[0] == 1


@pytest.mark.parametrize(
    "config_file_content, raises",
    [
        ("[jira.server]\nhostname = 'foo'\npat_token = 'bar'", None),
        ("", KeyError),
        ("[jira.server]\nhostname = 'foo'", KeyError),
        ("[jira.server]\npat_token = 'bar'", KeyError),
        ("hostname = 'foo'\npat_token = 'bar'", KeyError),
    ],
)
def test_read_and_validate_config(config_file_content, raises, tmp_path) -> None:
    config_file_path = tmp_path / "joft.config.toml"
    config_file_path.write_text(config_file_content)

    if raises is None:
        config = joft.utils.read_and_validate_config(config_file_path)
        assert config["jira"]["server"]["hostname"] == "foo"
        assert config["jira"]["server"]["pat_token"] == "bar"
    else:
        with pytest.raises(raises):
            config = joft.utils.read_and_validate_config(config_file_path)
