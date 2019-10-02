"""
 Bing (Web)

 @website     https://www.bing.com
 @provide-api yes (http://datamarket.azure.com/dataset/bing/search),
              max. 5000 query/month

 @using-api   no (because of query limit)
 @results     HTML (using search portal)
 @stable      no (HTML can change)
 @parse       url, title, content

 @todo        publishedDate
"""

import re
from lxml import html
from searx import logger, utils
from searx.engines.xpath import extract_text
from searx.url_utils import urlencode
from searx.utils import match_language, gen_useragent

<<<<<<< HEAD
logger = logger.getChild('bing engine')
=======
>>>>>>> 2d4a7f7a04705ba62ef8e91c5f73ba17ee3fed45

# engine dependent config
categories = ['general']
paging = True
language_support = True
supported_languages_url = 'https://www.bing.com/account/general'
language_aliases = {'zh-CN': 'zh-CHS', 'zh-TW': 'zh-CHT', 'zh-HK': 'zh-CHT'}

# search-url
base_url = 'https://www.bing.com/'
search_string = 'search?{query}&first={offset}'


def _get_offset_from_pageno(pageno):
    return (pageno - 1) * 10 + 1


# do search-request
def request(query, params):
    offset = _get_offset_from_pageno(params.get('pageno', 0))

    if params['language'] == 'all':
        lang = 'EN'
    else:
        lang = match_language(params['language'], supported_languages, language_aliases)

    query = query.decode('utf-8').encode('utf-8')

    search_path = search_string.format(
        query=urlencode({'q': query}),
        offset=offset)

    params['url'] = base_url + search_path

<<<<<<< HEAD
=======
    params['headers']['User-Agent'] = gen_useragent('Macintosh; Intel Mac OS X 10_12_6')

>>>>>>> 2d4a7f7a04705ba62ef8e91c5f73ba17ee3fed45
    return params


# get response from search-request
def response(resp):
    from searx.webapp import sentry
    results = []
    result_len = 0

    dom = html.fromstring(resp.text)
<<<<<<< HEAD
=======

    try:
        results.append({'number_of_results': int(dom.xpath('//span[@class="sb_count"]/text()')[0]
                                                 .split()[0].replace(',', ''))})
    except:
        sentry.captureException()

>>>>>>> 2d4a7f7a04705ba62ef8e91c5f73ba17ee3fed45
    # parse results
    for result in dom.xpath('//div[@class="sa_cc"]'):
        try:
            link = result.xpath('.//h3/a')[0]
            url = link.attrib.get('href')
            title = extract_text(link)
            content = extract_text(result.xpath('.//p'))

            # append result
            results.append({'url': url,
                            'title': title,
                            'content': content})
        except:
            sentry.captureException()

    # parse results again if nothing is found yet
    for result in dom.xpath('//li[@class="b_algo"]'):
        try:
            link = result.xpath('.//h2/a')[0]
            url = link.attrib.get('href')
            title = extract_text(link)
            content = extract_text(result.xpath('.//p'))

            # append result
            results.append({'url': url,
                            'title': title,
                            'content': content})
        except:
            sentry.captureException()

    try:
        result_len_container = "".join(dom.xpath('//span[@class="sb_count"]/text()'))
        result_len_container = utils.to_string(result_len_container)
        if "-" in result_len_container:
            # Remove the part "from-to" for paginated request ...
            result_len_container = result_len_container[result_len_container.find("-") * 2 + 2:]

        result_len_container = re.sub('[^0-9]', '', result_len_container)
        if len(result_len_container) > 0:
            result_len = int(result_len_container)
    except Exception as e:
        logger.debug('result error :\n%s', e)
        pass

    if _get_offset_from_pageno(resp.search_params.get("pageno", 0)) > result_len:
        return []

    results.append({'number_of_results': result_len})
    return results


# get supported languages from their site
def _fetch_supported_languages(resp):
    supported_languages = []
    dom = html.fromstring(resp.text)
    options = dom.xpath('//div[@id="limit-languages"]//input')
    for option in options:
        code = option.xpath('./@id')[0].replace('_', '-')
        if code == 'nb':
            code = 'no'
        supported_languages.append(code)

    return supported_languages
