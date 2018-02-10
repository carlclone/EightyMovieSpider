# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader


class EightysMovieItem(scrapy.Item):
    name =scrapy.Field()
    english_name =scrapy.Field()
    description =scrapy.Field()
    type =scrapy.Field()
    language =scrapy.Field()
    area =scrapy.Field()
    release_date =scrapy.Field()
    movie_length =scrapy.Field()
    douban_rank =scrapy.Field()
    tv_download_link =scrapy.Field()
    cover =scrapy.Field()


#class MovieItemLoader(ItemLoader):
    #自定义itemloader
    #default_output_processor = TakeFirst()

