from django.shortcuts import render
from markdown2 import Markdown
from . import util

def convert(title):
    content = util.get_entry(title)
    if content == None:
        return None
    markdowner = Markdown()
    return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display(request, title):
    entry = convert(title)

    if not entry:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
        
    return render(request, "encyclopedia/display.html", {
        "title": title,
        "content": entry
    })

