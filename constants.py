"""
File: constants.py
Description: Defines constants necessary for the path
to philosophy algorithm
"""

#base of all (english) wikipedia url's
BASE_WIKI_URL = "https://en.wikipedia.org"

#url for the wikipedia article for philosophy
PHILOSOPHY_WIKI_URL = "https://en.wikipedia.org/wiki/Philosophy"

#top level directory that all wikipedia article relative url's begin with
WIKI_DIRECTORY = "/wiki/"

#href identifier for internal wikipedia pages like "citation needed"
INTERNAL_PAGE_IDENTIFIER = "Wikipedia:"

#href identifier for wikipedia user pages
USER_IDENTIFIER = "User:"

#class identifier for the main text on a wikipedia page
MAIN_TEXT_IDENTIFIER = "mw-content-text"

#div class that exists in nonexistant wikipedia articles
NONEXISTANT_ARTICLE_IDENTIFIER = "noarticletext"

#maximum number of hops allowed before reaching the wikipedia article for philosophy
MAX_HOPS = 100

#HTTP status code for resource not found as defined by RFC 2616
HTTP_NOT_FOUND_CODE = 404