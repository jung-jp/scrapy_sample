
import scrapy
from scrapy.item import Item, Field

class WebItem(Item):
    site = Field()
    rank = Field()
    title = Field()
    req_url = Field()
    res_url = Field()
    doctype = Field()
    css = Field()
    js = Field()
    layout = Field()
    sidebar = Field()
    emulate = Field()
    embed_style_cnt = Field()
    embed_script_cnt = Field()
    etc = Field()
    reg_dt = Field()
