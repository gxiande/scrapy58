from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    address = Field()
    url = Field()
    province = Field()
    city = Field()
    district = Field()
    primurl = Field()