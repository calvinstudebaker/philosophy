"""
File: philosophy.py
Description: Given a url for a wikipedia article,
fetches the page for the given article, follows the first link
in the main text, and repeats the process until the page for
Philosophy is reached. Prints out the url's visited along the way.

Usage: python philosophy.py STARTING_WIKIPEDIA_LINK

"""

import urllib2						#to pull data from arbitrary url's
import sys							#to access command line arguments
from bs4 import BeautifulSoup		#to parse HTML
import constants					
import philosophy_exceptions		

"""
Function: relative_wikilink_to_absolute_url
Arguments: (string) relative_wikilink. A relative url
of the wikipedia website (i.e.: "/wiki/Ant")

Returns: (string) an absolute url that links to the same location as
the relative url. (i.e.: "https://en.wikipedia.org/wiki/Ant")
"""
def relative_wikilink_to_absolute_url(relative_wikilink):
	return constants.BASE_WIKI_URL + relative_wikilink

"""
Function: is_valid_wiki_article_url
Arguments: (string) url (i.e.: "https://en.wikipedia.org/wiki/Knowledge")

Returns: (boolean) a boolean value indicating whether the given url is of the
proper format to link to a wikipedia article. The url must begin with
"https://en.wikipedia.org/wiki/"
"""
def is_valid_wiki_article_url(url):
	return url.startswith(constants.BASE_WIKI_URL + constants.WIKI_DIRECTORY)

"""
Function: is_current_page
Arguments: 	(string) relative_wikilink. A relative wikipedia url.
			(string) current_wiki_url. The url of the wikipedia page currently being parsed.
Returns: (boolean) a boolean value indicating whether the given relative url
links to the current wikipedia page being parsed
"""
def is_current_page(relative_wikilink, current_wiki_url):
	return relative_wikilink_to_absolute_url(relative_wikilink) == current_wiki_url

"""
Function: is_end_state
Arguments: (string) url. Url to be checked against the target url (the url for the 
wikipedia page for philosophy)

Returns: (boolean) a boolean value indicating whether the given url is the wikipedia
page for philosophy
"""
def is_end_state(url):
	return url == constants.PHILOSOPHY_WIKI_URL

"""
Function: print_path
Arguments: (list) path_to_philosophy. A list of url's starting with
an arbitrary start url and ending with the url for the wikipedia philosophy page, each
url is the first link from the previous url.

Prints the list of urls one per line, and prints the number of hops required to go from
the starting url to Philosophy
"""
def print_path(path_to_philosophy):
	for url in path_to_philosophy:
		print url
	print str(len(path_to_philosophy)-1) + " hops"

"""
Function: is_valid_wikilink_a_href_tag
Arguments: (BeautifulSoup Tag Object) tag. The tag to be examined.
Returns: (boolean) A boolean value indicating whether a given tag is a
valid <a> tag that can be used as a link in the path to philosophy. In order
for a link to be valid, it must be an <a> tag, it must be a standard link (no
special classes like a redirecting link or a citation link), it must have an
href that links to an article, it cannot link to a special wikipedia page such
as the "citations needed" description, user page, file page, etc.
It must be a standard wikipedia article.

"""
def is_valid_wikilink_a_href_tag(tag):

	special_identifiers = [
		constants.INTERNAL_PAGE_IDENTIFIER,
		constants.USER_IDENTIFIER,
		constants.HELP_IDENTIFIER,
		constants.FILE_IDENTIFIER
	]

	is_a_tag = tag.name == "a"
	has_no_special_classes = not tag.has_attr('class')
	has_href = tag.has_attr('href')
	is_article = has_href and tag['href'].startswith(constants.WIKI_DIRECTORY)
	is_a_special_wikipedia_page = has_href and \
		any(identifier in tag['href'] for identifier in special_identifiers)
	
	return is_a_tag and has_no_special_classes and is_article \
		and not is_a_special_wikipedia_page

"""
Function: get_parsed_html
Arguments: (string) wiki_url. Url for a wikipedia article
Returns: (BeautifulSoup Object) A BeautifulSoup Object that represents the
parsed html data fetched from the given url.

"""
def get_parsed_html(wiki_url):
	#try to open the link given. If it is invalid, raise an exception
	try:
		response = urllib2.urlopen(wiki_url)
	except urllib2.HTTPError as e:
		if e.code == constants.HTTP_NOT_FOUND_CODE:
			raise philosophy_exceptions.NonexistantArticleError(wiki_url)
		else:
			raise e

	#parse the html from the given url using BeautifulSoup
	html = response.read()
	parsed_html = BeautifulSoup(html, "html.parser")

	return parsed_html

"""
Function: check_nonexistant_page
Arguments: (BeautifulSoup Object) wiki_main_text. BeautifulSoup Object
that represents parsed html data for the main text of a wikipedia page.
Description: Wikipedia will render pages for articles that do not exist,
and will display a standard message describing how there exists no page
for the requested topic. This function checks to make sure the given text
is not this "does not exist" text, and raises a NonexistantArticleError
if it is.
"""
def check_nonexistant_page(wiki_main_text):
	nonexistant_article_tag = wiki_main_text.find('div', class_ = constants.NONEXISTANT_ARTICLE_IDENTIFIER)
	if nonexistant_article_tag:
		raise philosophy_exceptions.NonexistantArticleError(wiki_url)

"""
Function: get_first_wikilink_from_paragraph
Arguments: (BeautifulSoup Object) paragraph. The paragraph that
the link will be pulled from.
			(String) wiki_url. The url of the wikipedia page currently
being parsed.
Returns: (String) The first valid wikipedia link in the given paragraph.
In the form of a relative wikipedia url. Returns None if no valid links are found.

"""
def get_first_wikilink_from_paragraph(paragraph, wiki_url):
	#find the first valid a tag in the paragraph
	a_href_tag = paragraph.find(is_valid_wikilink_a_href_tag)

	#as long as we have an a tag and it links to the current page, we
	#need to grab the next a tag.
	while a_href_tag and is_current_page(a_href_tag['href'], wiki_url):
		a_href_tag = a_href_tag.find_next_sibling(is_valid_wikilink_a_href_tag)

	#grab the relative url text from the href attr of the a tag
	first_wikilink = None
	if a_href_tag:
		first_wikilink = a_href_tag['href']

	return first_wikilink

"""
Function: get_first_wikilink_url_on_page
Arguments: (string) wiki_url. The url of the current wikipedia page
from which we should follow the first wikipedia article link.
Returns: (string) url of the first wikipedia link in the main text of the page.
If no links exist in the main text, a NoLinkArticleError exception is raised.
"""
def get_first_wikilink_url_on_page(wiki_url):
	#initialize variable for the first wikipedia link on the page
	first_wikilink = None

	#get a BeautifulSoup Object representing the parsed html of the given
	#wikipedia page
	parsed_html = get_parsed_html(wiki_url)

	#grab the main text of the wikipedia page
	main_text = parsed_html.body.find('div', id = constants.MAIN_TEXT_IDENTIFIER)

	#make sure the text doesn't indicate that no article exists
	check_nonexistant_page(main_text)

	#grab the first paragraph of the main text
	paragraph = main_text.find('p', recursive=False)

	while paragraph:
		#get the first wikipedia link in this paragraph
		first_wikilink = get_first_wikilink_from_paragraph(paragraph, wiki_url)

		#if there was no link, advance to the next paragraph. Otherwise, break.
		if not first_wikilink:
			paragraph = paragraph.find_next_sibling('p', recursive=False)
		else:
			break

	#if no links to other wikipedia articles were found, raise a
	#NoLinkArticleError exception
	if not first_wikilink:
		raise philosophy_exceptions.NoLinkArticleError(wiki_url)

	#return an absolute url of the linked wikipedia page
	return relative_wikilink_to_absolute_url(first_wikilink)


"""
Function: create_path_to_philosophy
Arguments: (string) url. The wikipedia url to begin the search from.
Returns: (list) a list of urls starting with given url and ending with
the url for the wikipedia page for Philosophy. Each url in the list is
the first link in the page from the previous url.
Prints the path as it goes, and the resulting number of hops.
If a cycle is found in the path, a CycleError exception is raised. 
If the search goes on for too long and the limit of hops is reached, 
a HopLimitError exception is raised.
"""
def create_path_to_philosophy(url):
	path_to_philosophy = []
	hops = 0

	#start with the given url
	path_to_philosophy.append(url)
	print url

	#as long as we haven't made it to philosophy and we are
	#still under the hop limit, continue to follow links
	while not is_end_state(url) and hops < constants.MAX_HOPS:
		#hop to the next url
		url = get_first_wikilink_url_on_page(url)

		#if we have seen this url then a cycle exists, raise a CycleError
		if url in path_to_philosophy:
			raise philosophy_exceptions.CycleError(url)

		#add the url to the path
		print url
		path_to_philosophy.append(url)
		hops += 1

	#if the loop ended and we are not yet at Philosophy, we hit the hop limit
	#raise a HopLimitError exception
	if not is_end_state(url):
		raise philosophy_exceptions.HopLimitError(hops)

	print str(hops) + " hops"

	return path_to_philosophy

"""
Function: main
Arguments: none
Description: Entry point of the program. Creates a path to philosophy
from a given url and prints the result
"""
def main():
	#if incorrect input was provided, give the user an example of proper usage and end
	if len(sys.argv) != 2:
		print "Example Usage: python philosophy.py STARTING_WIKIPEDIA_LINK"
		return

	#get the provided url and check that it is a valid wikipedia url
	url = sys.argv[1]
	if not is_valid_wiki_article_url(url):
		raise philosophy_exceptions.InputError(url)

	#create the path to philosophy
	path_to_philosophy = create_path_to_philosophy(url)

	#EDIT: decided it was nicer to watch the path created as it goes rather
	#than having it all printed at the end. create_path_to_philosophy now does
	#the printing

	#print the result
	#print_path(path_to_philosophy)
	
if __name__ == "__main__":
	main()
