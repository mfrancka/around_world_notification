#!/usr/bin/env python3

import requests
from lxml import html
import json
from envelopes import Envelope, SMTP
import configparser
from datetime import datetime
import email.utils

class linksstorage:
    def __init__(self, path):
        self.path = path
        self.read_links()

    def add_links(self, new_links):
        self.links += new_links
        self.save_links()

    def read_links(self):
        try:
            f = open(self.path, 'r')
            self.links = json.loads(f.read())
            f.close()
        except FileNotFoundError as error:
            self.links = []

    def save_links(self):
        f = open(self.path, 'w')
        f.write(json.dumps(self.links))
        f.close()


class linksfinder:
    address = 'http://polacydookolaswiata.pl/aktualnosci/'

    def __init__(self, storage_path='./links-db/links.db'):
        self.storage = linksstorage(storage_path)
        page = requests.get(self.address)
        tree = html.fromstring(page.content)
        self.last_links = tree.xpath('//a[@class="blog-post-title"]/@href')

    def get_new_links(self):
        self.not_known_links = []
        for link in self.last_links:
            if (not link in self.storage.links):
                self.not_known_links.append(link)
        self.storage.add_links(self.not_known_links)


class notification:
    def __init__(self,config_path='./config.ini'):
        self.get_config(config_path)

    def get_config(self, config_path='./config.ini'):
        config = configparser.ConfigParser()
        config.read(config_path)
        self.login = config['email']['login']
        self.password = config['email']['password']
        self.host = config['email']['host']
        self.port = config['email']['port']
        self.tls = config['email']['tls']
        self.subject = config['notification']['subject']
        self.recipient = config['notification']['recipient']
        self.sender = config['notification']['sender']

    def send(self, links):
        self.connection = SMTP(port=self.port,host=self.host,tls=self.tls,
                               login=self.login,password=self.password)
        envelope = Envelope(
            from_addr=(self.sender, u'Notification'),
            to_addr=(self.recipient),
            subject=self.subject,
            text_body=u"Nowy link:\n {}".format("\n".join(links))
            )
        envelope.add_header('Date', email.utils.formatdate(localtime=True))
        envelope.add_header('In-Reply-To', 'notification@francka.pl')
        try:
            self.connection.send(envelope)
            print('Email sent.')
        except Exception as e:
            print('Could not send email with links: {}'.format(','.join(links)),
                  e)


def main():
    links = linksfinder()
    links.get_new_links()
    if (links.not_known_links):
        print('{}: Send notification with {}'.format(datetime.now().isoformat(),
                                                     links.not_known_links))
        notification_system = notification()
        notification_system.send(links.not_known_links)
    else:
        print('{}: Not found new links'.format(datetime.now().isoformat()))

if __name__ == '__main__':
    main()
