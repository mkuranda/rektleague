from riot_request import *
from .models import Item, Champion

class ObjectNotFound(Exception) :
    """Raised when we can't find an object in db or from riot API"""
    pass

def get_item(riot_id):
    try:
        item = Item.objects.get(id=riot_id)
    except Item.DoesNotExist:
        requester = RiotRequester('/lol/static-data/v3/items/')
        try:
            item_data = requester.request(str(riot_id))
        except RiotNotFound:
            raise ObjectNotFound("Item " + str(riot_id))
        item = Item.objects.create(riot_id)
        item.name = item_data["name"]
        item.description = item_data["description"]
        item.save()
    return item

def get_champion(riot_id):
    try:
        champion = Champion.objects.get(id=riot_id)
    except Champion.DoesNotExist:
        requester = RiotRequester('/lol/static-data/v3/champions/')
        try:
            champion_data = requester.request(str(riot_id))
        except RiotNotFound:
            raise ObjectNotFound("Champion " + str(riot_id))
        champion = Champion.objects.create(id=riot_id)
        champion.name = champion_data["name"]
        champion.title = champion_data["title"]
        champion.save()
    return champion
