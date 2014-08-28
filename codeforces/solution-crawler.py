#!/usr/bin/env python

# Use this script to lookup Accepted solution at codeforce.com
#
# Requires
# ========
#
# - System packages: libxml2-dev, libxslt-dev
# - Python packages: mechanize, lxml, cssselect

import os.path
from os import makedirs
from sys import argv, exc_info
import shelve
import json
import re

import mechanize
import lxml.html

DEBUG_ERROR = 1
DEBUG_INFO = 2
DEBUG_DEBUG = 3
DEBUG_LEVEL = DEBUG_INFO
SOLUTIONS_DIR = "solutions/"

class Crawler:
    LIST_URL = 'http://codeforces.com/problemset/status/page/'
    SUBMISSION_URL = 'http://codeforces.com/data/submitSource'
    CACHE_PATH = '.cache'
    ACCEPTED = 'Accepted'
    def __init__(self, search_term):
        self.list_url = self.LIST_URL
        self.submission_url = self.SUBMISSION_URL
        self.cache_path = self.CACHE_PATH
        self.search_term = search_term
        self.initialize()

    def initialize(self):
        self.a = mechanize.Browser()
        self.a.set_handle_robots(False)
        self.a.set_handle_refresh(False)
        self.cache = shelve.open(self.cache_path);

    def crawl_range(self, range):
        for i in range:
            info("Page %d:" % i);
            found = self.crawl_listing(i)
            if found != None:
                for f in found:
                    yield f

    def crawl_listing(self, page):
        url = self.LIST_URL + str(page)
        content = self.fetch_listing(url)
        doc = lxml.html.document_fromstring(content)#.getroottree().getroot()
        solutions = doc.cssselect('.status-frame-datatable')
        matches = []
        for sol in solutions:
            solution_names = sol.xpath('//tr[td[position()=3]]');
            for solrow in solution_names:
                if self.check_tr(solrow):
                    solution = self.create_solution(solrow.getchildren())
                    solution['source'] = self.get_source(solution)
                    yield solution

    def check_tr(self, tr):
        tds = tr.getchildren()
        td_name = tds[3].text_content()
        td_status = tds[5].text_content()
        return td_name.find(self.search_term) >= 0 \
            and td_status.find(self.ACCEPTED) >= 0

    @staticmethod
    def create_solution(tds):
        return {
            'id': str(tds[0].text_content()).strip(),
            'timestamp': tds[1].text_content().strip(),
            'author': tds[2].text_content().strip(),
            'problem': tds[3].text_content().strip(),
            'lang': tds[4].text_content().strip(),
            'status': tds[5].text_content().strip(),
            'time': tds[6].text_content().strip(),
            'memory': tds[7].text_content().strip(),
        }

    def get_source(self, solution):
        content = self.fetch_submission(self.submission_url, solution['id'])
        data = json.loads(content)
        source = str(data.get('source'))
        return re.sub(r"(\r)?\n", "\n", source)

    def fetch_listing(self, url):
        debug("Server hit: {0}".format(url))
        resp = self.a.open(url)
        src = resp.get_data()
        return src
        
    def fetch_submission(self, url, submission_id):
        # TODO yin: use hashkeys
        key = url+'#'+str(submission_id)
        if self.cache.has_key(key):
            debug("Cache hit: {0}".format(key))
            return self.cache[key]
        else:
            debug("Server hit: {0}@submissionId={1}".format(url, submission_id))
            resp = self.a.open(url, "submissionId=%s" % str(submission_id))
            src = resp.get_data()
            self.cache[key] = src
            self.cache.sync()
        return src

def info(str):
    if DEBUG_LEVEL >= DEBUG_INFO:
        print str

def debug(str):
    if DEBUG_LEVEL >= DEBUG_DEBUG:
        print str

def print_solution(solution, filename=None):
    if filename == None:
        print sol['problem'], sol['id'], sol['lang'], sol['time'], sol['memory']
    else:
        print filename

def save_solution(solution):
    prob = solution['problem'].replace(' ', '')
    sid = solution['id']
    auth = solution['author'].replace(' ', '')
    time = solution['time'].replace(' ', '')
    mem = solution['memory'].replace(' ', '').lower()
    lang = solution['lang'].replace(' ', '').lower()
    filename = '{0}-{1}-{2}x{3}-{4}.{5}' \
        .format(prob, sid, time, mem, auth, lang)
    path = SOLUTIONS_DIR + filename
    if not os.path.exists(SOLUTIONS_DIR):
        makedirs(SOLUTIONS_DIR)
    with open(path, 'w') as f:
        f.write(sol['source'])
    return filename

if __name__ == '__main__':
    if len(argv) < 4:
        print "solution-crawlet.py <problem> <start> <end>"
        print "<problem is in the format XXXY, X = [0-9], Y = [A-E]"
        exit(1)
    start = int(argv[2])
    end = int(argv[3]) + 1
    solutions = Crawler(argv[1]).crawl_range(range(start, end))
    if solutions != None:
        for sol in solutions:
            filename = save_solution(sol)
            print_solution(sol, filename)
