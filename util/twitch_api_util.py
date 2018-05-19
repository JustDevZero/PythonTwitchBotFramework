import asyncio
from typing import Tuple

from aiohttp import ClientSession
from async_timeout import timeout

from dataclasses import dataclass

USER_API_URL = 'https://api.twitch.tv/helix/users?login={}'
STREAM_API_URL = 'https://api.twitch.tv/helix/streams?user_login={}'
CHANNEL_CHATTERS_URL = 'https://tmi.twitch.tv/group/user/{}/chatters'


async def get_url(url, headers=None):
    async with ClientSession(headers=headers) as session:
        async with timeout(10):
            async with session.get(url) as resp:
                return await resp.json()


async def get_user_data(user, headers=None):
    json = await get_url(USER_API_URL.format(user), headers)

    if not json['data']:
        return None

    return json['data'][0]


async def get_user_id(user, headers=None):
    data = await get_user_data(user, headers)

    if data is None:
        return -1

    return data['id']


async def get_stream_data(user_id, headers=None):
    json = await get_url(STREAM_API_URL.format(user_id), headers)

    if not json['data']:
        return {}

    return json['data'][0]


async def get_channel_chatters(channel: str):
    return await get_url(CHANNEL_CHATTERS_URL.format(channel))
