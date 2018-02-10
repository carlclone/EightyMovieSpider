# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re

from ArticleSpider.items import EightysMovieItem


class EightysMovieSpider(scrapy.Spider):
    name = '80s'
    allowed_domains = ['www.80s.tw']
    start_urls = ['https://www.80s.tw/movie/list']

    def parse(self, response):
        movie_urls = response.css(".me1.clearfix li h3 a::attr(href)").extract()
        for movie_url in movie_urls:
            yield Request(url=parse.urljoin(response.url, movie_url), callback=self.parse_detail)

        #提取下一页的url 交给scrapy下载
        page_nodes = response.xpath('//*[@id="block3"]/div[3]/div/a')
        for page_node in page_nodes:
            page_a_tag = page_node.extract()
            match_re = re.match(".*?(下一页).*", page_a_tag)
            if match_re:
                #next_url = page_node.css('a::attr(href)').extract_first()
                snippet_url = re.match('.*href="(.*)".*',page_a_tag).group(1)
                next_url = parse.urljoin(response.url,snippet_url)
                print('当前url'+next_url)
                break

        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        # 忘记记录movie_id 和页面url了
        # 已爬取的数据出现的问题:1.有的url在第二条,第一条可能是字幕和其他东西  2.日期有其他文字 3.发行日期和时长调换了位置 4.有的没有时长
        # 接下来就是数据清洗的过程了
        movie_item = EightysMovieItem()
        name = response.xpath('//*[@id="minfo"]/div[2]/h1/text()').extract_first()
        description = response.xpath('//*[@id="minfo"]/div[2]/span[1]/text()').extract_first().strip()
        english_name_list = response.xpath('//*[@id="minfo"]/div[2]/span[2]/text()').extract()
        english_name = ''
        for english_name_cell in english_name_list:
            if english_name_cell.strip() != '':
                english_name = english_name_cell.strip()
                break
        type = response.xpath('//*[@id="minfo"]/div[2]/div[1]/span[1]/a/text()').extract_first()
        language = response.xpath('//*[@id="minfo"]/div[2]/div[1]/span[3]/a/text()').extract_first()
        area = response.xpath('//*[@id="minfo"]/div[2]/div[1]/span[2]/a/text()').extract_first()
        release_date = response.xpath('//*[@id="minfo"]/div[2]/div[1]/span[5]/text()').extract_first()
        movie_length = response.xpath('//*[@id="minfo"]/div[2]/div[1]/span[6]/text()').extract_first()

        douban_rank=''
        douban_rank_list = response.xpath('//*[@id="minfo"]/div[2]/div[2]/span[1]/text()').extract()
        for douban_rank_cell in douban_rank_list:
            if douban_rank_cell.strip() != '':
                douban_rank = douban_rank_cell.strip()
                break
        tv_download_link = response.xpath('//*[@id="myform"]/ul/li[2]/span[1]/span/a/@href').extract_first()
        cover = response.xpath('//*[@id="minfo"]/div[1]/img/@src').extract_first()

        movie_item["name"] = name
        movie_item["description"] = description
        movie_item["english_name"] = english_name
        movie_item["type"] = type
        movie_item["language"] = language
        movie_item["area"] = area
        movie_item["release_date"] = release_date
        movie_item["movie_length"] = movie_length
        movie_item["douban_rank"] = douban_rank
        movie_item["tv_download_link"] = tv_download_link
        movie_item["cover"] = cover

        yield movie_item  # yield后传递到pipeline中
