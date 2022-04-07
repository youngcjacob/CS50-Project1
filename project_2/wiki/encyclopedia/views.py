from django.shortcuts import render
from . import util
from django import forms
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


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
    search = request.POST.get('q')
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
        return render(request, "encyclopedia/index.html", {
            "Title": "Error",
            "Contents": "The requested page was not found"
        })
