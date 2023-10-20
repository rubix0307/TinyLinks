import hashlib
from mongo_db import db


async def get_long_url(short_url: str):
    link = await db.link.find_one({"short_url": short_url})
    if link:
        answer = {'long_url': link.get('long_url')}
    else:
        answer = {"error": "Short url does`t exist"}
    return answer

async def create_short_url(long_url: str, custom_short_url=None, user_id=None):
    if custom_short_url:
        short_url = await db.link.find_one({"short_url": custom_short_url})
        if short_url:
            return {"error": "Short url already exists"}
        else:
            short_url = custom_short_url
    else:
        short_url = hashlib.sha256(long_url.encode()).hexdigest()[:10]

    data = {"short_url": short_url, "long_url": long_url}
    if user_id:
        data.update({'user_id': user_id})
    db.link.insert_one(data)
    return data

async def update_short_url(short_link: str, new_long_url: str):

    original_link = await db.link.find_one({"short_url": short_link})
    new_data = {'long_url': new_long_url, 'short_url': short_link}
    answer = await db.link.update_one({'_id': original_link['_id']}, {'$set': new_data})

    if answer.modified_count:
        return new_data
    else:
        return {'error': 'not updated'}

async def get_all_user_url(user_id):
    links = db.link.find({"user_id": user_id})
    data_as_list = await links.to_list(length=100)

    return data_as_list




