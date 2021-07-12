import json
from pprint import pprint
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from .forms import QuotesForm, TagsForm, QuotesForm_Tags, QuestionsForm
from .models import Quotes, Tags
from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import UpdateView
from bs4 import BeautifulSoup as BS
from bs4 import NavigableString, Tag
import requests
from django.http import Http404

from rest_framework import generics
from .models import Question
from GifsQuestionMark.serializers import QuestionSerializer
from rest_framework import filters

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



def home(request):
    return render(request, 'GifsQuestionMark/GifsQuestionMark_home.html')


def api_search(request):
    search = Question.objects.all()
    question_form = QuestionsForm()
    # for search_term in search:
    #     print(search_term.question_text)

    if request.method == "POST" and 'search' in request.POST:
        question_form = QuestionsForm(request.POST)

        # quote_form.add()
        # question_form.save()
        question_text = question_form['question_text'].value()
        # print(question_form['question_text'].value())
        print(question_text)
        author_text = question_form['author_text'].value()
        print(author_text)
        if question_text and author_text:
            lookup_string = "https://api.crossref.org/works?query={}+{}&rows=1&mailto=jmvanw@gmail.com".format(
                question_text, author_text)
        if not question_text:
            lookup_string = "https://api.crossref.org/works?query={}&rows=1&mailto=jmvanw@gmail.com".format(
                author_text)
        if not author_text:
            lookup_string = "https://api.crossref.org/works?query={}&rows=1&mailto=jmvanw@gmail.com".format(
                question_text)


        print(lookup_string)
        # lookup_string = "https://api.crossref.org/works?query={}+{}&filter=has-full-text:true&rows=1&mailto=jmvanw@gmail.com".format(
        #     author_text, question_text)
        response = requests.get(lookup_string)
        rando_data = response.json()
        pprint(rando_data)
        items_data = rando_data['message']['items']
        # ISSN_data = items_data[0]['ISSN']
        # if not ISSN_data:
        #     ISSN_data = ['no ISSN']
        title_data = items_data[0]['title']

        author_data = items_data[0].get('author')
        editor_data = items_data[0].get('editor')
        publisher_data = items_data[0].get('publisher')
        url_data = items_data[0].get('URL')
        print(author_data)
        # author_data = items_data[0]['author']
        if author_data:
            pass
        elif editor_data:
            author_data = editor_data
        else:
            author_data = publisher_data

        # try:
        #     author_data = items_data[0]['author']
        # except KeyError:
        #     print("Error message: No Author, returning random")




        # context = {'title_data': title_data, 'ISSN_data': ISSN_data, 'author_data': author_data}
        context = {'title_data': title_data, 'author_data': author_data, 'url_data': url_data, "question_form": question_form}

        return render(request, "GifsQuestionMark/GifsQuestionMark_api_search.html", context)

    context = {"search": search, "question_form": question_form}
    return render(request, 'GifsQuestionMark/GifsQuestionMark_api_search.html', context)

###Temp###This is such a beautiful view I might vomit
def api(request):
    # response = requests.get('https://jsonplaceholder.typicode.com/todos/')
    # response = requests.get('https://api.open-notify.org/astros.json')
    response = requests.get(
        'https://api.crossref.org/works?filter=is-update:true,&sample=1&mailto=jmvanw@gmail.com')
    # response = requests.get('https://api.crossref.org/works?filter=is-update:true,from-pub-date:2014-03-03&rows=1&mailto=jmvanw@gmail.com')
    # https://api.crossref.org/works?filter=has-full-text:true&mailto=jmvanw@gmail.com
    # transfor the response to json objects
    rando_data = response.json()
    message_results_data = rando_data['message']['total-results']
    status_data = rando_data["status"]
    # message_results_data = rando_data['message']['total-results']
    items_data = rando_data['message']['items']
    ISSN_data = items_data[0]['ISSN']

    title_data = items_data[0]['title']
    author_data = items_data[0].get('author')
    editor_data = items_data[0].get('editor')
    publisher_data = items_data[0].get('publisher')
    url_data = items_data[0].get('URL')

    if author_data:
        pass
    elif editor_data:
        author_data = editor_data
    else:
        author_data = publisher_data

    # test_response = requests.get("https://api.lyrics.ovh/v1/madonna/like_a_virgin")
    # print(test_response.status_code)

    # message_data2 = message_data['facets']
    # print(title_data)
    # print(message_results_data)
    # print(status_data)
    # print(rando_data)
    # print(json.dumps(rando_data, indent=4))
    pprint(rando_data)
    context = {'title_data': title_data, 'ISSN_data': ISSN_data, 'author_data': author_data}

    # return render(request, "GifsQuestionMark/GifsQuestionMark_API.html",
    #               {'message_data': message_data, 'title_data': title_data})
    return render(request, "GifsQuestionMark/GifsQuestionMark_API.html", context)
    # return render(request, "GifsQuestionMark/GifsQuestionMark_API.html", {'message_data': message_data})
    # return render(request, 'GifsQuestionMark/GifsQuestionMark_API.html')
###End Temp###

def goodreads_quote_scraper(request):
    url = "https://www.goodreads.com/quotes/"
    page = requests.get(url)
    soup = BS(page.content, "html.parser")
    all_soup = soup.find_all('div', {"class": "quote"})
    scraper_output = []
    print(soup.title)
    # all_soup.append(soup.title)

    # for listing in range(len(all_soup)):
    for listing in all_soup:
        stripped_quote = []
        author_string = []
        author = listing.find('span', class_="authorOrTitle").extract()
        tags = listing.find('div', class_="greyText smallText left")

        title = listing.find('a', class_="authorOrTitle")
        if title is not None:
            title.extract()

        [s.extract() for s in soup('script')]

        quote = listing.find('div', class_="quoteText")

        #################################Print quotes
        for quote_string in quote.stripped_strings:
            #print(quote_string)
            # if quote_string != '―':   ## does the same as if quote_string != chr(8213):    #8213 discovered using ord('―')
            if quote_string != chr(8213):
                stripped_quote.append(quote_string)


        #################################print author
        author_string = author.string.replace(",", "")
        # print(author_string)

        #################################print tags
        for tag in tags or []:
            if isinstance(tag, NavigableString):
                continue
            if isinstance(tag, Tag):
                # print(tag.get_text())
                tag_string = tag.get_text()

        soup_bowl = {
            'stripped_quote': stripped_quote,
            'tag_string': tag_string,
            'author_string': author_string
        }
        scraper_output.append(soup_bowl)

        # print('\n' * 2)


        print(scraper_output)

    context = {'scraper_output': scraper_output}
    return render(request, 'GifsQuestionMark/GifsQuestionMark_scraper.html', context)

def create_quote(request):
    quotes = Quotes.objects.all()
    quote_form = QuotesForm()
    for quote in quotes:
        print(quote.tags)
    if request.method == "POST" and 'quote' in request.POST:
        quote_form = QuotesForm(request.POST)
        if quote_form.is_valid():
            # quote_form.add()
            quote_form.save()
            return redirect('success')
        quote_form = QuotesForm()
    tags = Tags.objects.all()
    tag_form = TagsForm()
    if request.method == "POST" and 'tag' in request.POST:
        tag_form = TagsForm(request.POST)
        if tag_form.is_valid():

            tag_form.save()
            tag_form.save_m2m()
    tag_list = QuotesForm_Tags()

    context = {"quotes": quotes, "tags": tags, "quoteform": quote_form, "tag_form": tag_form, "taglist": tag_list}
    return render(request, 'GifsQuestionMark/GifsQuestionMark_create.html', context)

def success(request):
    tags=Tags.objects.all()
    if request.method == "POST":
        form = TagsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes') ##nonsense
    form = TagsForm()

    context = {"tags": tags, "form": form}
    return render(request, 'GifsQuestionMark/GifsQuestionMark_add_success.html', context)

def view_quotes(request):
    quotes = Quotes.objects.all()
    form = QuotesForm()
    paginator = Paginator(quotes, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"quotes": quotes, "form": form, 'page_obj': page_obj}
    return render(request, 'GifsQuestionMark/GifsQuestionMark_view_quotes.html', context) ##

def post_tag(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = TagsForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new tag object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)

def view_tag(request):
    tags = Tags.objects.all()

    form = TagsForm()

    context = {"tags": tags, "form": form}
    return render(request, 'GifsQuestionMark/GifsQuestionMark_view_tags.html', context) ##

def quote_content(request, id):
    id = int(id)
    quote = get_object_or_404(Quotes, id=id)
    tags = Tags.objects.all()
    # form = QuotesForm()

    context = {"quote": quote, "tags": tags}
    return render(request, 'GifsQuestionMark/GifsQuestionMark_quote_content.html', context)

def removeTag(request, id):
    tag = Tags.objects.get(id=id)
    tag.delete()
    messages.info(request, "tag removed.")
    return redirect('GifsQuestionMark_view_tags')

def removeQuote(request, id):
    quote = Quotes.objects.get(id=id)
    quote.delete()
    messages.info(request, "tag removed.")
    return redirect('GifsQuestionMark_view_quotes')

class editQuote(UpdateView):
    model = Quotes
    fields = '__all__'
    template_name_suffix = '_update'
    # success_url = '../../../quote_content/{id}/'  ##works but ugly get_success_url looks better and probably works better

    def get_object(self, queryset=None):
        return Quotes.objects.get(id=self.kwargs.get("id"))

    def get_success_url(self):
        return reverse('GifsQuestionMark_quote_content', kwargs={'id': self.kwargs['id']})

class QuestionsAPIView(generics.ListCreateAPIView):
    search_fields = ['question_text', 'author_text']
    filter_backends = (filters.SearchFilter,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer