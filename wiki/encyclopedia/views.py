from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from markdown2 import Markdown
from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="search")

class AddForm(forms.Form):
    addtitle = forms.CharField(label="Title")
    addtext = forms.CharField(widget=forms.Textarea, label=mark_safe('Enter text using <a href="https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax" target="_blank">Markdown Language</a>'))

def convert(title):
    content = util.get_entry(title)
    if content == None:
        return None
    markdowner = Markdown()
    return markdowner.convert(content)


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            return display(request,search)
        
        else:
            return search(request, search)

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form" : SearchForm
        })

def display(request, title):
    entry = convert(title)

    if not entry:
          return search(request, title)
    
    else:
        return render(request, "encyclopedia/display.html", {
            "title": title,
            "content": entry,
            "form": SearchForm
        })
    

def search(request, form):
    page_list = util.list_entries()
    for i in range(len(page_list)):
        page_list[i] = page_list[i].lower()

    strings = [i for i in page_list if form.lower() in i]

    return render(request, "encyclopedia/search.html", {
        "search": form,
        "entries": strings,
        "form": SearchForm
    })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html",{
            "form": SearchForm,
            "addform": AddForm
        })
    
    else:
        #if request method is "POST"

        #Insert form data into a variable
        create = AddForm(request.POST)

        if create.is_valid():
            title = create.cleaned_data["addtitle"]
            markdown_text = create.cleaned_data["addtext"]

            #if title exists in form, display error message
            if util.get_entry(title):
                return HttpResponse("Unable to create this page as current page exists")
            
            else:
                #Save entry if it's a unique title
                util.save_entry(title, markdown_text)
                return display(request, title)
        
        else:
            return HttpResponse("404. An error has occured.")

