# -*- coding: utf-8 -*-
__author__ = 'stitch'
from scrapy import signals
from scrapy.exceptions import NotConfigured
import tarfile
import shutil
import os
from contextlib import closing

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
'''
class SendEmail(object):
    def __init__(self):
        self.frm = '467738357@qq.com'
        self.to = '467738357@qq.com'
'''

class ClearFile(object):
    def __init__(self):
        self.folder = 'pic/full'
        self.filename = 'complete.tar.gz'

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        ext = cls()
        crawler.signals.connect(ext.clear_file, signal=signals.spider_closed)
        return ext

    def clear_file(self, spider):
        shutil.rmtree(self.folder)
        os.remove(self.filename)