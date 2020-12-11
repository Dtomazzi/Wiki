from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from . import util
from . import rand
from django import forms
import markdown2



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def new(request):

    class NewEntryForm(forms.Form):
        title = forms.CharField(label="Title:")
        body = forms.CharField(widget=forms.Textarea, max_length=250)

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            body=form.cleaned_data["body"]

        if util.get_entry(title) == None:
             util.save_entry(title, body)
             return HttpResponseRedirect(reverse("encyclopedia:show", args=[title]))
        else:
            return render(request, "encyclopedia/new.html", {
            "form":form,
            "errors": "This title already exists, please select a different one."
            } )

    else:
        return render(request, "encyclopedia/new.html", {
        "form":NewEntryForm()
        })


def show(request, name):
    return render(request, "encyclopedia/show.html", {
    "entry":util.get_entry(name),
    "name":name.capitalize()
    })

def random(request):

    entries = util.list_entries()
    count=len(entries)
    selected=entries[rand.randint(1,5)]
    print(selected)
    return HttpResponseRedirect(reverse("encyclopedia:show", args=[selected]))



def edit(request, entry, name):

    if request.method == "POST":
        util.save_entry(title, body)

    else:
        return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "name":name
        })



def search(request):
    if request.method == "POST":

        if request.POST['query'] == "":
           return render(request, "encyclopedia/search.html",{
           "error": "Please specify a search term."
           })
        else:
          query=request.POST['query'].lower()
          entries = util.list_entries()
          results=[]

          if query in entries:
              return render(request, "encyclopedia/show.html", {
              "entry":util.get_entry(query)
              })
          else:
           for x in entries:
              if x.lower().find(query) > -1:
                  results.append(x)
           return render(request, "encyclopedia/search.html",{
           "results": results
          })
