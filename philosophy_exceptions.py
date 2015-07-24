"""
File: philosophy_exceptions.py
Description: Defines classes for various exceptions that may be
encountered during a search for a wikipedia path to philosophy.
Got the idea from http://docs.python-guide.org/en/latest/writing/style/
that raising exceptions during the search might be better than returning
from the search at various places with unique return values and unique
error messages. The downside is the error messages could be more descriptive.
Would fix that next by adding more Attributes to each exception.
"""


"""
Class: InputError
Description: Exception raised for errors in the input.

Attributes:
    expr -- input expression in which the error occurred
    msg -- explanation of the error
"""
class InputError(Exception):
    def __init__(self, expr):
        self.expr = expr
        self.msg = "Invalid input: " + expr + ". Must provide a legitimate english wikipedia url."

    def __str__(self):
        return self.msg


"""
Class: HopLimitError
Description: Exception raised when the upper limit on hops is reached during philosophy search.

Attributes:
    hops -- number of hops reached
    msg -- explanation of the error
"""
class HopLimitError(Exception):
    def __init__(self, hops):
        self.hops = hops
        self.msg = "Hop Limit Reached. Philosophy was not found after " + str(hops) + " hops."

    def __str__(self):
        return self.msg


"""
Class: NonexistantArticleError
Description: Exception raised when a nonexistant wikipedia article is encountered.

Attributes:
    url -- url of the nonexistant wikipedia article
    msg -- explanation of the error
"""
class NonexistantArticleError(Exception):
    def __init__(self, url):
        self.url = url
        self.msg = "Encountered a nonexistant wikipedia article: " + url

    def __str__(self):
        return self.msg


"""
Class: NoLinkArticleError
Description: Exception raised when a wikipedia article with no links to other wikipedia
articles in the main text is encountered.

Attributes:
    url -- url of the wikipedia article with no wikipedia article links
    msg -- explanation of the error
"""
class NoLinkArticleError(Exception):
    def __init__(self, url):
        self.url = url
        self.msg = "Encountered a wikipedia article with no links to other wikipedia articles: " + url

    def __str__(self):
        return self.msg

"""
Class: CycleError
Description: Exception raised when a cycle is found in the path to philosophy.

Attributes:
    url -- repeated url
    msg -- explanation of the error
"""
class CycleError(Exception):
    def __init__(self, url):
        self.url = url
        self.msg = "Cycle exists in path to philosophy. Repeated url: " + url

    def __str__(self):
        return self.msg