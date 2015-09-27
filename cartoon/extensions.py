# -*- coding: utf-8 -*-
__author__ = 'stitch'
from scrapy import signals
from scrapy.exceptions import NotConfigured
from contextlib import closing
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
import email
import tarfile
import shutil
import os
import logging

class TarFolder(object):
    def __init__(self):
        self.folder = 'pic/full'
        self.filename = 'complete.tar.gz'

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        ext = cls()
        crawler.signals.connect(ext.tar_folder, signal=signals.spider_closed)
        return ext

    def tar_folder(self, spider):
        with closing(tarfile.TarFile.gzopen(self.filename, 'w')) as out:
            out.add(self.folder)


class SendEmail(object):
    def __init__(self):
        self.filename = 'complete.tar.gz'

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        self.From = crawler.settings['MAIL_FROM']
        self.Host = crawler.settings['MAIL_HOST']
        self.Pass = crawler.settings['MAIL_PASS']
        self.Port = crawler.settings['MAIL_PORT']
        self.User = crawler.settings['MAIL_USER']
        ext = cls()
        crawler.signals.connect(ext.send_email, signal=signals.spider_closed)
        return ext

    def send_email(self, spider):
        msg = MIMEMultipart()

        ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        file_msg = MIMEBase(maintype, subtype)
        data = open(self.filename, 'rb')
        file_msg.set_payload(data.read())
        data.close()
        email.Encoders.encode_base64(file_msg)
        file_msg.add_header('Content-Disposition', 'attachment', filename = 'cartoon.tar.gz')
        msg.attach(file_msg)

        try:
            server = smtplib.SMTP(self.Host, self.Port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.User, self.Pass)
            server.sendmail(self.From, self.From, msg.as_string())
        except Exception,e:
            print str(e)
        finally:
            server.quit()


class ClearFile(object):
    def __init__(self):
        self.folder = 'pic/full/'
        self.filename = 'complete.tar.gz'

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        ext = cls()
        crawler.signals.connect(ext.clear_file, signal=signals.spider_closed)
        return ext

    def clear_file(self, spider):
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
        if os.path.exists(self.filename):
            os.remove(self.filename)
