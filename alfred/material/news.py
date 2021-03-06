#!/usr/bin/env python

import os

import pymongo
import requests
import untangle
from lxml import html


class News:

    def __init__(self, source, region, tags, title, teaser, link, image_link, created_at, highlights):
        self.read_by_users = []
        self.source = source
        self.region = region
        self.tags = tags
        self.title = title
        self.teaser = teaser
        self.link = link  # the link to the article
        self.image_link = image_link
        self.created_at = created_at
        self.highlights = highlights

    def __eq__(self, o):
        result = type(self) == type(o)
        result = result and self.source == o.source
        result = result and self.region == o.region
        result = result and self.tags == o.tags
        result = result and self.title == o.title
        result = result and self.teaser == o.teaser
        result = result and self.link == o.link
        result = result and self.image_link == o.image_link
        result = result and self.created_at == o.created_at
        result = result and self.highlights == o.highlights
        print(result)
        return result

    def __ne__(self, other):
        return not self == other

    def to_string(self):
        str = "*{}*\n_{}_\n\n{}\n\n{}".format(self.title,
                                                    self.created_at,
                                                    self.teaser,
                                                    self.highlights)
        # self.link.replace("_", "\_"))
        return str

    def to_json(self):
        print(self.__dict__)
        return self.__dict__


def fetch_xml(url):
    try:
        return untangle.parse(requests.get(url).content.decode('utf-8'))
    except ValueError:
        print("error retrieving", url)


def try_to_extract(source, extractor, alternative):
    try:
        return extractor(source)
    except AttributeError as e:
        # print('AttributeError:', e)
        return alternative
    except KeyError as e:
        # print('KeyError:', e)
        return alternative


def save_in_db(collection, news):
    client = pymongo.MongoClient(os.environ.get('MONGO_DB_URL'))
    db_news = client.alfred_db[collection]
    for n in news:
        # TODO drop if already in db, otherwise save it
        db_news.insert_one(n.to_json())
    print(db_news.count())
    client.close()


class NdrClient:

    def __init__(self):
        self.regions = [
            'niedersachsen',
            'schleswig-holstein',
            'mecklenburg-vorpommern',
            'hamburg'
        ]
        template = "https://www.ndr.de/nachrichten/{}/index-nimex.html"
        self.region_urls = {region: template.format(region) for region in
                            self.regions}

    def fetch_region_news(self, region):
        result = []
        if region not in self.regions:
            return result
        news_list = fetch_xml(self.region_urls[region])
        tag_extractor = lambda x: [t.cdata for t in x.meta.keywordset.keyword]
        link_extractor = lambda x: x.meta.rdf_RDF.rdf_Description.prism_isFormatOf.cdata
        for news_item in news_list.rdf_RDF.item:
            if "https://www.ndr.de/nachrichten" in news_item['rdf:about']:
                news_article = fetch_xml(news_item.link.cdata).exchange.story
                n = News(
                    source="ndr.de",
                    region=region,
                    tags=try_to_extract(news_article, tag_extractor, ""),
                    title=try_to_extract(news_item, lambda x: x.title.cdata, ""),
                    teaser=try_to_extract(news_item, lambda x: x.description.cdata, ""),
                    link=try_to_extract(news_article, link_extractor, ""),
                    image_link=try_to_extract(news_item, lambda x: x.mp_image.mp_data.cdata, ""),
                    created_at=self.crawl_updatet_at(
                        ndr_link=try_to_extract(news_article, link_extractor, "")),
                    highlights=self.crawl_highlights(
                        ndr_link=try_to_extract(news_article, link_extractor, ""))
                )
                result.append(n)
        return result

    def crawl_updatet_at(self, ndr_link):
        page = requests.get(ndr_link)
        tree = html.fromstring(page.content)
        reply = []
        for xs in tree.cssselect('div.lastchanged'):
            if xs.text:
                return xs.text.rstrip()

    def crawl_highlights(self, ndr_link):
        page = requests.get(ndr_link)
        tree = html.fromstring(page.text)
        reply = []
        for xs in tree.cssselect('article h3'):
            if xs.text:
                reply.append(xs.text.rstrip())

        return "\n- ".join(reply).join(["- ", "\n"])
