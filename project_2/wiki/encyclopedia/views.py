from turtle import update
from django.shortcuts import render
from . import util
from django import forms
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from random import randint


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Creates hyperlink to each entry and brings user to entry page when selected


def return_title(request, Title):
    entries = util.list_entries()
    if (str(Title) in entries):
        return render(request, "encyclopedia/wiki.html", {
            "Title": Title,
            "Contents": util.get_entry(Title)
        })
    else:
        return render(request, "encyclopedia/wiki.html", {
            "Title": "Error",
            "Contents": "The requested page was not found"
        })

# Search for entries


def search(request):
    search = request.POST.get('entry_search')
    entries = util.list_entries()
    matches = []
    for entry in entries:
        if search == entry:
            return render(request, "encyclopedia/wiki.html", {
                "Title": search,
                "Contents": util.get_entry(search)
            })
        elif search.lower() in entry.lower():
            matches.append(entry)
    if matches != []:
        return render(request, "encyclopedia/index.html", {
            "entries": matches})
    else:
        return render(request, "encyclopedia/wiki.html", {
            "Title": "Error",
            "Contents": "The requested page was not found"
        })


def new_page(request):
    return render(request, "encyclopedia/new_page.html")


def add_page(request):
    title = request.POST.get('entry_title')
    content = request.POST.get('body_content')
    if title in util.list_entries():
        return render(request, "encyclopedia/wiki.html", {
            "Title": "Error",
            "Contents": "The requested entry already exists, please try again"
        })
    else:
        util.save_entry(title, content)
        return render(request, "encyclopedia/wiki.html", {
            "Title": title,
            "Contents": util.get_entry(title)
        })


def edit_page(request):
    title = request.POST.get("title")
    contents = request.POST.get("contents")
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "contents": contents
    })


def save_edit(request):
    title = request.POST.get("entry_title")
    updated_content = request.POST.get("body_content")
    util.save_entry(title, updated_content)
    return render(request, "encyclopedia/wiki.html", {
        "Title": title,
        "Contents": markdown(util.get_entry(title))
    })


def rand_entry(request):
    entries = util.list_entries()
    rand_entry = entries[randint(0, len(entries)-1)]
    return render(request, "encyclopedia/wiki.html", {
        "Title": rand_entry,
        "Contents": util.get_entry(rand_entry)
    })
