from bs4 import BeautifulSoup as BS
from bs4 import NavigableString, Tag
import requests

# url = "https://www.goodreads.com/quotes/"
# request = requests.get(url)
# soup = BS(request.content, "html.parser")
# print(soup.title)
#
# for listing in soup.find_all('div', {"class": "quote"}):
#     author = listing.find('span', class_="authorOrTitle").extract()
#     tags = listing.find('div', class_="greyText smallText left")
#
#     title = listing.find('a', class_="authorOrTitle")
#     if title is not None:
#         title.extract()
#
#     quote = listing.find('div', class_="quoteText")
#     #################################Print quotes
#     for string in quote.stripped_strings:
#         print(string)
#     #################################print author
#     author_string = author.string.replace(",", "")
#     print(author_string)
#     #################################print tags
#     for tag in tags or []:
#         if isinstance(tag, NavigableString):
#             continue
#         if isinstance(tag, Tag):
#             print(tag.get_text())
#
#     print('\n' * 2)

url = "https://www.goodreads.com/quotes/"
page = requests.get(url)
soup = BS(page.content, "html.parser")
all_soup = soup.find_all('div', {"class": "quote"})
scraper_output = []
print(soup.title)
# all_soup.append(soup.title)

for listing in all_soup:
    quote_string = []
    author_string = []
    author = listing.find('span', class_="authorOrTitle").extract()
    tags = listing.find('div', class_="greyText smallText left")

    title = listing.find('a', class_="authorOrTitle")
    if title is not None:
        title.extract()

    [s.extract() for s in soup('script')]

    quote = listing.find('div', class_="quoteText")

    #################################Print quotes
    for stripped_quote in quote.stripped_strings:
        # print(quote_string)
        if stripped_quote == '―':
            pass
        else:
            quote_string.append(stripped_quote)

    #################################print author

    # no_comma_author = author.string.replace(",", "")
    for stripped_author in author.stripped_strings:
        author_string.append(stripped_author)
    # author_string = author.string.replace(",", "")
    # print(author_string)



    #################################print tags
    tag_string = []
    for tag in tags or []:
        if isinstance(tag, NavigableString):
            continue
        if isinstance(tag, Tag):
            # print(tag.get_text())
            tag_string.append(tag.get_text())

    soup_bowl = {
        'quote_string': quote_string,
        'tag_string': tag_string,
        'author_string': author_string
    }
    scraper_output.append(soup_bowl)

    # print('\n' * 2)

print(scraper_output)