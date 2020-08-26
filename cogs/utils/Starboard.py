from .Database import Database
from create_database import StarBoardMessages, StarBoardSettings, StarboardAllowedRoles, StarBoardIgnoredChannels
from loguru import logger


class StarBoard(Database):
    def __init__(self):
        super().__init__()

    async def post_starboard_settings(self, server_id: int, enabled: bool, channel_id: int, emoji: str, threshold: int):
        settings = StarBoardSettings(server_id=server_id,
                                     enabled=enabled,
                                     channel_id=channel_id,
                                     emoji=emoji,
                                     threshold=threshold)
        self.session.add(settings)
        await self.commit()



    async def clear_starboard(self, id: int):
        try:
            stmt = StarBoardMessages.__table__.delete().where(StarBoardMessages.server_id == id)
            self.session.execute(stmt)
            await self.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    async def get_ignored_starboard_channels(self, server_id: int):
        list_of_channels = []
        channels = self.session.query(StarBoardIgnoredChannels).filter_by(server_id=server_id).all()
        for channel in channels:
            list_of_channels.append(channel.channel_id)
        return list_of_channels


    async def delete_starboard_ignored_channel(self, server_id, channel_id):
        res = self.session.query(StarBoardIgnoredChannels) \
            .filter_by(server_id=server_id) \
            .filter_by(channel_id=channel_id).delete()
        if res == 1:
            return True
        return False

    async def add_starboard_ignored_channel(self, server_id, channel_id):
        channel = StarBoardIgnoredChannels(server_id=server_id,
                                           channel_id=channel_id)
        self.session.add(channel)
        await self.commit()
        return True

    async def get_starboard_settings(self, server_id):
        settings = self.session.query(StarBoardSettings).filter_by(server_id=server_id).one_or_none()
        return settings

    async def update_starboard_settings(self, server_id, emoji=None, channel_id=None, threshold=None, enabled=None):
        updated = False
        settings = self.session.query(StarBoardSettings).filter_by(server_id=server_id).one_or_none()
        if settings is not None and emoji is not None:
            settings.emoji = emoji
            updated = True
        if settings is not None and channel_id is not None:
            settings.channel_id = channel_id
            updated = True
        if settings is not None and threshold is not None:
            settings.threshold = threshold
            updated = True
        if settings is not None and enabled is not None:
            settings.enabled = enabled
            updated = True
        if updated:
            await self.commit()
        return updated

    async def get_starboard_roles(self, server_id):
        list_of_roles = []
        roles = self.session.query(StarboardAllowedRoles).filter_by(server_id=server_id).all()
        for role in roles:
            list_of_roles.append(role.role_id)
        return list_of_roles

    async def delete_starboard_role(self, server_id, role_id):
        role = self.session.query(StarboardAllowedRoles).filter_by(server_id=server_id).filter_by(
            role_id=role_id).one_or_none()
        if role is not None:
            role.delete()
            await self.commit()
            return True
        return False

    async def post_starboard_role(self, server_id, role_id):
        role = StarboardAllowedRoles(server_id=server_id,
                                     role_id=role_id)
        self.session.add(role)
        await self.commit()

    async def get_starboard_messages(self, guild_id):
        messages = self.session.query(StarBoardMessages).filter_by(server_id=guild_id).all()
        return messages

    async def get_one_starboard_message(self, guild_id, original_message_id):
        message = self.session.query(StarBoardMessages) \
            .filter_by(server_id=guild_id) \
            .filter_by(original_message_id=original_message_id).one_or_none()
        return message

    async def update_starboard_message(self, original_message_id, starboard_message_id=None, count=None):
        """
        Updates the message data based on the origional_message_id
        :param original_message_id: The ID used to fetch the message that will be updated
        :param starboard_message_id: The message ID found on the starboard if it is preset
        :param count: Number of votes
        :return:
        """
        was_updated = False
        message = self.session.query(StarBoardMessages).filter_by(original_message_id=original_message_id).one_or_none()
        if starboard_message_id is not None:
            message.starboard_message_id = starboard_message_id
            await self.commit()
            was_updated = True
        if count is not None:
            message.count = count
            await self.commit()
            was_updated = True
        if was_updated:
            return message
        else:
            return False

    async def post_starboard_message(self, guild_id, original_message_id, starboard_message_id=None, count=0):
        if await self.get_one_starboard_message(guild_id, original_message_id) is None:
            message = StarBoardMessages(server_id=guild_id,
                                        starboard_message_id=starboard_message_id,
                                        original_message_id=original_message_id,
                                        count=count)
            self.session.add(message)
            await self.commit()
            return message
        else:
            return await self.update_starboard_message(original_message_id, starboard_message_id, count)
