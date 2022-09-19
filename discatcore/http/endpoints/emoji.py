"""
The MIT License (MIT)

Copyright (c) 2022-present EmreTech

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

# this file was auto-generated by scripts/generate_endpoints.py

from typing import Any, Optional, Union

import discord_typings
from discord_typings import Snowflake

from discatcore.file import BasicFile
from discatcore.http.endpoints.core import EndpointMixin
from discatcore.http.route import Route
from discatcore.types import Unset

__all__ = ("EmojiEndpoints",)


class EmojiEndpoints(EndpointMixin):
    async def list_guild_emojis(self, guild_id: Snowflake):
        return await self.request(Route("GET", "/guilds/{guild_id}/emojis", guild_id=guild_id))

    async def get_guild_emoji(self, guild_id: Snowflake, emoji_id: Snowflake):
        return await self.request(
            Route(
                "GET", "/guilds/{guild_id}/emojis/{emoji_id}", guild_id=guild_id, emoji_id=emoji_id
            )
        )

    async def create_guild_emoji(
        self,
        guild_id: Snowflake,
        *,
        name: str,
        image: str,
        roles: list[Snowflake],
        reason: Optional[str] = None,
    ):
        return await self.request(
            Route("POST", "/guilds/{guild_id}/emojis", guild_id=guild_id),
            json_params={"name": name, "image": image, "roles": roles},
            reason=reason,
        )

    async def modify_guild_emoji(
        self,
        guild_id: Snowflake,
        emoji_id: Snowflake,
        *,
        name: str = Unset,
        roles: list[Snowflake] = Unset,
        reason: Optional[str] = None,
    ):
        return await self.request(
            Route(
                "PATCH",
                "/guilds/{guild_id}/emojis/{emoji_id}",
                guild_id=guild_id,
                emoji_id=emoji_id,
            ),
            json_params={"name": name, "roles": roles},
            reason=reason,
        )

    async def delete_guild_emoji(
        self, guild_id: Snowflake, emoji_id: Snowflake, reason: Optional[str] = None
    ):
        return await self.request(
            Route(
                "DELETE",
                "/guilds/{guild_id}/emojis/{emoji_id}",
                guild_id=guild_id,
                emoji_id=emoji_id,
            ),
            reason=reason,
        )