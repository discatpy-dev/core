# SPDX-License-Identifier: MIT

import discord_typings as dt
import pytest

from discatcore.errors import _shorten_error_dict  # pyright: ignore[reportPrivateUsage]


@pytest.mark.parametrize(
    ["expected", "raw_error"],
    [
        (
            {
                "activities.0.platform": "Value must be one of ('desktop', 'android', 'ios').",
                "activities.0.type": "Value must be one of (0, 1, 2, 3, 4, 5).",
            },
            {
                "activities": {
                    "0": {
                        "platform": {
                            "_errors": [
                                {
                                    "code": "BASE_TYPE_CHOICES",
                                    "message": "Value must be one of ('desktop', 'android', 'ios').",
                                }
                            ]
                        },
                        "type": {
                            "_errors": [
                                {
                                    "code": "BASE_TYPE_CHOICES",
                                    "message": "Value must be one of (0, 1, 2, 3, 4, 5).",
                                }
                            ]
                        },
                    }
                }
            },
        ),
        (
            {"access_token": "This field is required"},
            {
                "access_token": {
                    "_errors": [{"code": "BASE_TYPE_REQUIRED", "message": "This field is required"}]
                }
            },
        ),
        (
            {"": "Command exceeds maximum size (4000)"},
            {
                "_errors": [
                    {
                        "code": "APPLICATION_COMMAND_TOO_LARGE",
                        "message": "Command exceeds maximum size (4000)",
                    }
                ]
            },
        ),
    ],
)
def test_shorten_error_dict(expected: dict[str, str], raw_error: dt.NestedHTTPErrorsData):
    assert _shorten_error_dict(raw_error) == expected
