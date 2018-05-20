# -*- coding: utf-8 -*-
import scrapy
from JobboleArticle.items import JobboleArticleItem
import re
import datetime


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        nodes = response.css('#archive .post.floated-thumb')
        for node in nodes:
            image_url = node.css('.post-thumb img::attr(src)').extract_first('')
            detail_url = node.css('.post-meta .archive-title::attr(href)').extract_first('')
            yield scrapy.Request(url=response.urljoin(detail_url),meta={'front_image_url':image_url}, callback=self.parse_detail)
        next_page = response.css('#archive .navigation.margin-20 .next.page-numbers::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_detail(self, response):
        front_image_url = response.meta.get('front_image_url', '')
        title = response.css('.grid-8 .entry-header h1::text').extract_first()
        create_date =  response.css('.entry-meta .entry-meta-hide-on-mobile::text').extract_first().strip().replace('·', '').strip()
        tags_list = response.css('.entry-meta .entry-meta-hide-on-mobile a::text').extract()
        tags_pure = [element for element in tags_list if not element.strip().endswith('评论')]
        tags = '.'.join(tags_pure)
        praise = response.css('.post-adds span[class*="vote-post-up"] h10::text')
        praise_re = praise.re_first('.*?(\d+)')
        praise_nums = int(praise_re) if praise_re else 0
        fav = response.css('.post-adds span[class*="bookmark-btn"]::text')
        fav_re = fav.re_first('.*?(\d+)')
        fav_nums = int(fav_re) if fav_re else 0
        comment = response.css('.post-adds a[href="#article-comment"] span::text')
        comment_re = comment.re_first('.*?(\d+)')
        comment_nums = int(comment_re) if comment_re else 0

        article_item = JobboleArticleItem()
        article_item['front_image_url'] = [front_image_url]  # 注意是数组的形式
        article_item['title'] = title
        article_item['url'] = response.url
        try:
            create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item['create_date'] = create_date
        article_item['tags'] = tags
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['praise_nums'] = praise_nums
        yield article_item
















