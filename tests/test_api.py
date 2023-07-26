from click.testing import CliRunner

from api import cli
from .settings import DATA_PATH


def test_blend_two_lists_with_weights_cli():
    runner = CliRunner()
    result = runner.invoke(
        cli.blend_two_lists_with_weights,
        [f"{DATA_PATH}/list1.txt", f"{DATA_PATH}/list2.txt", "0.42", "0.34", "--random-seed", "1"])

    assert result.exit_code == 0
    assert result.output
