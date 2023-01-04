# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from dataclasses import dataclass

import discord_typings as dt

from ..utils.event import Event

__all__ = (
    "GatewayEvent",
    "UnknownEvent",
    "ApplicationCommandPermissionsUpdateEvent",
    "AutoModerationRuleCreateEvent",
    "AutoModerationRuleDeleteEvent",
    "AutoModerationRuleUpdateEvent",
    "ChannelCreateEvent",
    "ChannelDeleteEvent",
    "ChannelPinsUpdateEvent",
    "ChannelUpdateEvent",
    "GuildBanAddEvent",
    "GuildBanRemoveEvent",
    "GuildCreateEvent",
    "GuildDeleteEvent",
    "GuildEmojisUpdateEvent",
    "GuildIntegrationsUpdateEvent",
    "GuildMemberAddEvent",
    "GuildMemberRemoveEvent",
    "GuildMemberUpdateEvent",
    "GuildMembersChunkEvent",
    "GuildRoleCreateEvent",
    "GuildRoleDeleteEvent",
    "GuildRoleUpdateEvent",
    "GuildScheduledEventCreateEvent",
    "GuildScheduledEventDeleteEvent",
    "GuildScheduledEventUpdateEvent",
    "GuildScheduledEventUserAddEvent",
    "GuildScheduledEventUserRemoveEvent",
    "GuildStickersUpdateEvent",
    "GuildUpdateEvent",
    "IntegrationCreateEvent",
    "IntegrationDeleteEvent",
    "IntegrationUpdateEvent",
    "InteractionCreateEvent",
    "InvalidSessionEvent",
    "InviteCreateEvent",
    "InviteDeleteEvent",
    "MessageCreateEvent",
    "MessageDeleteEvent",
    "MessageDeleteBulkEvent",
    "MessageReactionAddEvent",
    "MessageReactionRemoveEvent",
    "MessageReactionRemoveAllEvent",
    "MessageReactionRemoveEmojiEvent",
    "MessageUpdateEvent",
    "PresenceUpdateEvent",
    "ReadyEvent",
    "ReconnectEvent",
    "ResumedEvent",
    "StageInstanceCreateEvent",
    "StageInstanceDeleteEvent",
    "StageInstanceUpdateEvent",
    "ThreadCreateEvent",
    "ThreadDeleteEvent",
    "ThreadListSyncEvent",
    "ThreadMemberUpdateEvent",
    "ThreadMembersUpdateEvent",
    "ThreadUpdateEvent",
    "TypingStartEvent",
    "UserUpdateEvent",
    "VoiceServerUpdateEvent",
    "VoiceStateUpdateEvent",
    "WebhooksUpdateEvent",
)


@dataclass
class GatewayEvent(Event):
    pass


@dataclass
class UnknownEvent(GatewayEvent):
    data: dt.DispatchEvent


@dataclass
class ReadyEvent(GatewayEvent):
    data: dt.ReadyData


@dataclass
class ResumedEvent(GatewayEvent):
    pass


@dataclass
class ReconnectEvent(GatewayEvent):
    pass


@dataclass
class InvalidSessionEvent(GatewayEvent):
    resumable: bool


@dataclass
class ApplicationCommandPermissionsUpdateEvent(GatewayEvent):
    data: dt.ApplicationCommandPermissionsUpdateData


@dataclass
class AutoModerationRuleCreateEvent(GatewayEvent):
    data: dt.AutoModerationRuleData


@dataclass
class AutoModerationRuleDeleteEvent(GatewayEvent):
    data: dt.AutoModerationRuleData


@dataclass
class AutoModerationRuleUpdateEvent(GatewayEvent):
    data: dt.AutoModerationRuleData


@dataclass
class ChannelCreateEvent(GatewayEvent):
    data: dt.ChannelCreateData


@dataclass
class ChannelDeleteEvent(GatewayEvent):
    data: dt.ChannelDeleteData


@dataclass
class ChannelPinsUpdateEvent(GatewayEvent):
    data: dt.ChannelPinsUpdateData


@dataclass
class ChannelUpdateEvent(GatewayEvent):
    data: dt.ChannelUpdateData


@dataclass
class GuildBanAddEvent(GatewayEvent):
    data: dt.GuildBanAddData


@dataclass
class GuildBanRemoveEvent(GatewayEvent):
    data: dt.GuildBanRemoveData


@dataclass
class GuildCreateEvent(GatewayEvent):
    data: dt.GuildCreateData


@dataclass
class GuildDeleteEvent(GatewayEvent):
    data: dt.GuildDeleteData


@dataclass
class GuildEmojisUpdateEvent(GatewayEvent):
    data: dt.GuildEmojisUpdateData


@dataclass
class GuildIntegrationsUpdateEvent(GatewayEvent):
    data: dt.GuildIntergrationsUpdateData


@dataclass
class GuildMemberAddEvent(GatewayEvent):
    data: dt.GuildMemberAddData


@dataclass
class GuildMemberRemoveEvent(GatewayEvent):
    data: dt.GuildMemberRemoveData


@dataclass
class GuildMemberUpdateEvent(GatewayEvent):
    data: dt.GuildMemberUpdateData


@dataclass
class GuildMembersChunkEvent(GatewayEvent):
    data: dt.GuildMembersChunkData


@dataclass
class GuildRoleCreateEvent(GatewayEvent):
    data: dt.GuildRoleCreateData


@dataclass
class GuildRoleDeleteEvent(GatewayEvent):
    data: dt.GuildRoleDeleteData


@dataclass
class GuildRoleUpdateEvent(GatewayEvent):
    data: dt.GuildRoleUpdateData


@dataclass
class GuildScheduledEventCreateEvent(GatewayEvent):
    data: dt.GuildScheduledEventCreateData


@dataclass
class GuildScheduledEventDeleteEvent(GatewayEvent):
    data: dt.GuildScheduledEventDeleteData


@dataclass
class GuildScheduledEventUpdateEvent(GatewayEvent):
    data: dt.GuildScheduledEventUpdateData


@dataclass
class GuildScheduledEventUserAddEvent(GatewayEvent):
    data: dt.GuildScheduledEventUserAddData


@dataclass
class GuildScheduledEventUserRemoveEvent(GatewayEvent):
    data: dt.GuildScheduledEventUserRemoveData


@dataclass
class GuildStickersUpdateEvent(GatewayEvent):
    data: dt.GuildStickersUpdateData


@dataclass
class GuildUpdateEvent(GatewayEvent):
    data: dt.GuildUpdateData


@dataclass
class IntegrationCreateEvent(GatewayEvent):
    data: dt.IntegrationCreateData


@dataclass
class IntegrationDeleteEvent(GatewayEvent):
    data: dt.IntegrationDeleteData


@dataclass
class IntegrationUpdateEvent(GatewayEvent):
    data: dt.IntegrationUpdateData


@dataclass
class InteractionCreateEvent(GatewayEvent):
    data: dt.InteractionCreateData


@dataclass
class InviteCreateEvent(GatewayEvent):
    data: dt.InviteCreateData


@dataclass
class InviteDeleteEvent(GatewayEvent):
    data: dt.InviteDeleteData


@dataclass
class MessageCreateEvent(GatewayEvent):
    data: dt.MessageCreateData


@dataclass
class MessageDeleteEvent(GatewayEvent):
    data: dt.MessageDeleteData


@dataclass
class MessageDeleteBulkEvent(GatewayEvent):
    data: dt.MessageDeleteBulkData


@dataclass
class MessageReactionAddEvent(GatewayEvent):
    data: dt.MessageReactionAddData


@dataclass
class MessageReactionRemoveEvent(GatewayEvent):
    data: dt.MessageReactionRemoveData


@dataclass
class MessageReactionRemoveAllEvent(GatewayEvent):
    data: dt.MessageReactionRemoveAllData


@dataclass
class MessageReactionRemoveEmojiEvent(GatewayEvent):
    data: dt.MessageReactionRemoveEmojiData


@dataclass
class MessageUpdateEvent(GatewayEvent):
    data: dt.MessageUpdateData


@dataclass
class PresenceUpdateEvent(GatewayEvent):
    data: dt.PresenceUpdateData


@dataclass
class StageInstanceCreateEvent(GatewayEvent):
    data: dt.StageInstanceCreateData


@dataclass
class StageInstanceDeleteEvent(GatewayEvent):
    data: dt.StageInstanceDeleteData


@dataclass
class StageInstanceUpdateEvent(GatewayEvent):
    data: dt.StageInstanceUpdateData


@dataclass
class ThreadCreateEvent(GatewayEvent):
    data: dt.ThreadCreateData


@dataclass
class ThreadDeleteEvent(GatewayEvent):
    data: dt.ThreadDeleteData


@dataclass
class ThreadListSyncEvent(GatewayEvent):
    data: dt.ThreadListSyncData


@dataclass
class ThreadMemberUpdateEvent(GatewayEvent):
    data: dt.ThreadMemberUpdateData


@dataclass
class ThreadMembersUpdateEvent(GatewayEvent):
    data: dt.ThreadMembersUpdateData


@dataclass
class ThreadUpdateEvent(GatewayEvent):
    data: dt.ThreadUpdateData


@dataclass
class TypingStartEvent(GatewayEvent):
    data: dt.TypingStartData


@dataclass
class UserUpdateEvent(GatewayEvent):
    data: dt.UserUpdateData


@dataclass
class VoiceServerUpdateEvent(GatewayEvent):
    data: dt.VoiceServerUpdateData


@dataclass
class VoiceStateUpdateEvent(GatewayEvent):
    data: dt.VoiceStateData


@dataclass
class WebhooksUpdateEvent(GatewayEvent):
    data: dt.WebhooksUpdateData


name_to_class: dict[str, t.Any] = {
    "application_command_permissions_update": ApplicationCommandPermissionsUpdateEvent,
    "auto_moderation_rule_create": AutoModerationRuleCreateEvent,
    "auto_moderation_rule_delete": AutoModerationRuleDeleteEvent,
    "auto_moderation_rule_update": AutoModerationRuleUpdateEvent,
    "channel_create": ChannelCreateEvent,
    "channel_delete": ChannelDeleteEvent,
    "channel_pins_update": ChannelPinsUpdateEvent,
    "channel_update": ChannelUpdateEvent,
    "guild_ban_add": GuildBanAddEvent,
    "guild_ban_remove": GuildBanRemoveEvent,
    "guild_create": GuildCreateEvent,
    "guild_delete": GuildDeleteEvent,
    "guild_emojis_update": GuildEmojisUpdateEvent,
    "guild_integrations_update": GuildIntegrationsUpdateEvent,
    "guild_member_add": GuildMemberAddEvent,
    "guild_member_remove": GuildMemberRemoveEvent,
    "guild_member_update": GuildMemberUpdateEvent,
    "guild_members_chunk": GuildMembersChunkEvent,
    "guild_role_create": GuildRoleCreateEvent,
    "guild_role_delete": GuildRoleDeleteEvent,
    "guild_role_update": GuildRoleUpdateEvent,
    "guild_scheduled_event_create": GuildScheduledEventCreateEvent,
    "guild_scheduled_event_delete": GuildScheduledEventDeleteEvent,
    "guild_scheduled_event_update": GuildScheduledEventUpdateEvent,
    "guild_scheduled_event_user_add": GuildScheduledEventUserAddEvent,
    "guild_scheduled_event_user_remove": GuildScheduledEventUserRemoveEvent,
    "guild_stickers_update": GuildStickersUpdateEvent,
    "guild_update": GuildUpdateEvent,
    "integration_create": IntegrationCreateEvent,
    "integration_delete": IntegrationDeleteEvent,
    "integration_update": IntegrationUpdateEvent,
    "interaction_create": InteractionCreateEvent,
    "invite_create": InviteCreateEvent,
    "invite_delete": InviteDeleteEvent,
    "message_create": MessageCreateEvent,
    "message_delete": MessageDeleteEvent,
    "message_delete_bulk": MessageDeleteBulkEvent,
    "message_reaction_add": MessageReactionAddEvent,
    "message_reaction_remove": MessageReactionRemoveEvent,
    "message_reaction_remove_all": MessageReactionRemoveAllEvent,
    "message_reaction_remove_emoji": MessageReactionRemoveEmojiEvent,
    "message_update": MessageUpdateEvent,
    "presence_update": PresenceUpdateEvent,
    "ready": ReadyEvent,
    "stage_instance_create": StageInstanceCreateEvent,
    "stage_instance_delete": StageInstanceDeleteEvent,
    "stage_instance_update": StageInstanceUpdateEvent,
    "thread_create": ThreadCreateEvent,
    "thread_delete": ThreadDeleteEvent,
    "thread_list_sync": ThreadListSyncEvent,
    "thread_member_update": ThreadMemberUpdateEvent,
    "thread_members_update": ThreadMembersUpdateEvent,
    "thread_update": ThreadUpdateEvent,
    "typing_start": TypingStartEvent,
    "user_update": UserUpdateEvent,
    "voice_server_update": VoiceServerUpdateEvent,
    "voice_state_update": VoiceStateUpdateEvent,
    "webhooks_update": WebhooksUpdateEvent,
}
