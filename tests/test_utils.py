# SPDX-License-Identifier: MIT

import pytest

from discatcore import utils


class TestSnowflake:
    @pytest.mark.parametrize(
        ["expected", "snowflake"],
        [
            ((utils.DISCORD_EPOCH / 1000), 0),
            (1553400385.989, 559226493553737740),
            (1600376556.284, 756258832526868541),
            (1517155232.186, 407203299977068544),
        ],
    )
    def test_snowflake_timestamp(self, expected: float, snowflake: int):
        assert utils.Snowflake(snowflake).raw_timestamp == expected

    @pytest.mark.parametrize(
        ["expected", "snowflake"],
        [
            (0, 0),
            (5, utils.DISCORD_EPOCH),
            (1, 559226493553737740),
            (2, 756258832526868541),
            (0, 407203299977068544),
        ],
    )
    def test_snowflake_iwid(self, expected: int, snowflake: int):
        assert utils.Snowflake(snowflake).iwid == expected

    @pytest.mark.parametrize(
        ["expected", "snowflake"],
        [
            (0, 0),
            (11, utils.DISCORD_EPOCH),
            (0, 559226493553737740),
            (0, 756258832526868541),
            (0, 407203299977068544),
        ],
    )
    def test_snowflake_ipid(self, expected: int, snowflake: int):
        assert utils.Snowflake(snowflake).ipid == expected

    @pytest.mark.parametrize(
        ["expected", "snowflake"],
        [
            (0, 0),
            (0, utils.DISCORD_EPOCH),
            (12, 559226493553737740),
            (61, 756258832526868541),
            (0, 407203299977068544),
        ],
    )
    def test_snowflake_increment(self, expected: int, snowflake: int):
        assert utils.Snowflake(snowflake).increment == expected


def test_dumps():
    test_dict = {"hello": "there", "I contain data": 96}
    test_dict_dumped = utils.dumps(test_dict)

    if utils.has_orjson:
        assert test_dict_dumped == '{"hello":"there","I contain data":96}'
    else:
        assert test_dict_dumped == '{"hello": "there", "I contain data": 96}'


def test_loads():
    test_json = '{"hello":"there","I contain data":96}'
    assert utils.loads(test_json) == {"hello": "there", "I contain data": 96}
