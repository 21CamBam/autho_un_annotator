import re
import subprocess
import urllib.request
import wget

CR = 'reviewboard.west.isilon.com'
GITHUB = 'github.west.ision.com'
PR = 'pull'
COMMIT = 'commit'
CODE = 'blob'
GITDIR = 'tree'
TEST_RESULTS = 'qa/log/QA_test_results'

FREQUENCY = ['The following failures were matched to this bug.', 'Frequency +1']

def get_directory_listing(path, url):
    p = subprocess.Popen(['lftp', '{0}{1}'.format(url,path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, _ = p.communicate(b'ls')
    return out.decode('utf-8').split('\n')

def get_file(path, url):
    return urllib.request.urlopen(url + path).read().decode('utf-8')

def download_file(path, url, filename):
    if filename:
        filename = wget.download(url=url + path, out=filename)
    else:
        filename = wget.download(url=url + path)
    return filename


def get_frequency_count(comments):
    l = re.findall('{}|{}'.format(FREQUENCY[0], FREQUENCY[1]), comments[0])
    return len(l)

def get_test_urls(comments):
    l = re.findall('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', comments[0])
    d = {}
    d["CR"] = []
    d["PR"] = []
    d["COMMIT"] = []
    d["CODE"] = []
    d["GITDIR"] = []
    d["TEST_RESULTS"] = []
    for item in l:
        if CR in item:
            d["CR"].append(item)
        elif GITHUB in item:
            if PR in item:
                d["PR"].append(item)
            elif COMMIT in item:
                d["COMMIT"].append(item)
            elif CODE in item:
                d["CODE"].append(item)
            elif GITDIR in item:
                d["GITDIR"].append(item)
            else:
                d["GITHUB_OTHER"].append(item)
        elif TEST_RESULTS in item:
            d["TEST_RESULTS"].append(item)
    return d
