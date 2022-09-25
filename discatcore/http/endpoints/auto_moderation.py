# SPDX-License-Identifier: MIT

# this file was auto-generated by scripts/generate_endpoints.py

from typing import Any, Optional, Union

import discord_typings
from discord_typings import Snowflake

from discatcore.file import BasicFile
from discatcore.http.endpoints.core import EndpointMixin
from discatcore.http.route import Route
from discatcore.types import Unset

__all__ = ("AutoModerationEndpoints",)


class AutoModerationEndpoints(EndpointMixin):
    def list_auto_moderation_rules(self, guild_id: Snowflake):
        return self.request(
            Route("GET", "/guilds/{guild_id}/auto-moderation/rules", guild_id=guild_id)
        )

    def get_auto_moderation_rule(self, guild_id: Snowflake, auto_moderation_rule_id: Snowflake):
        return self.request(
            Route(
                "GET",
                "/guilds/{guild_id}/auto-moderation/rules/{auto_moderation_rule_id}",
                guild_id=guild_id,
                auto_moderation_rule_id=auto_moderation_rule_id,
            )
        )

    def create_auto_moderation_rule(
        self,
        guild_id: Snowflake,
        *,
        name: str,
        event_type: int,
        trigger_type: int,
        trigger_metadata: dict[str, Any] = Unset,
        actions: list[discord_typings.AutoModerationActionData],
        enabled: bool = Unset,
        exempt_roles: list[Snowflake] = Unset,
        exempt_channels: list[Snowflake] = Unset,
        reason: Optional[str] = None,
    ):
        return self.request(
            Route("POST", "/guilds/{guild_id}/auto-moderation/rules", guild_id=guild_id),
            json_params={
                "name": name,
                "event_type": event_type,
                "trigger_type": trigger_type,
                "trigger_metadata": trigger_metadata,
                "actions": actions,
                "enabled": enabled,
                "exempt_roles": exempt_roles,
                "exempt_channels": exempt_channels,
            },
            reason=reason,
        )

    def modify_auto_moderation_rule(
        self,
        guild_id: Snowflake,
        auto_moderation_rule_id: Snowflake,
        *,
        name: str = Unset,
        event_type: int = Unset,
        trigger_type: int = Unset,
        trigger_metadata: dict[str, Any] = Unset,
        actions: list[discord_typings.AutoModerationActionData] = Unset,
        enabled: bool = Unset,
        exempt_roles: list[Snowflake] = Unset,
        exempt_channels: list[Snowflake] = Unset,
        reason: Optional[str] = None,
    ):
        return self.request(
            Route(
                "PATCH",
                "/guilds/{guild_id}/auto-moderation/rules/{auto_moderation_rule_id}",
                guild_id=guild_id,
                auto_moderation_rule_id=auto_moderation_rule_id,
            ),
            json_params={
                "name": name,
                "event_type": event_type,
                "trigger_type": trigger_type,
                "trigger_metadata": trigger_metadata,
                "actions": actions,
                "enabled": enabled,
                "exempt_roles": exempt_roles,
                "exempt_channels": exempt_channels,
            },
            reason=reason,
        )

    def delete_auto_moderation_rule(
        self, guild_id: Snowflake, auto_moderation_rule_id: Snowflake, reason: Optional[str] = None
    ):
        return self.request(
            Route(
                "DELETE",
                "/guilds/{guild_id}/auto-moderation/rules/{auto_moderation_rule_id}",
                guild_id=guild_id,
                auto_moderation_rule_id=auto_moderation_rule_id,
            ),
            reason=reason,
        )
