from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from . import util
import encyclopedia
from random import choice

# view function for index
def index(request):
    entry = util.list_entries()
    entries = [x.lower() for x in entry]
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })
      
# view function for entry 
def entry(request, title):
    titles = util.list_entries()
    titles_lower = [x.lower() for x in titles]
    if title.lower() not in titles_lower:
        return render(request, "encyclopedia/error.html", {"title":title})
    else:
        return render(request, "encyclopedia/entry.html",{"title":title, "entry": markdown_to_html(title)})
    
 #GET and POST methods for search   
def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        titles = util.list_entries()
        titles_lower = [x.lower() for x in titles]
        suggestions = []
        if title.lower() not in titles_lower:
            for t in titles_lower:
                if title.lower() in t:
                    suggestions.append(t)
            if len(suggestions) < 1:
                return render(request, "encyclopedia/error.html",{"message":"This entry does not exist"})
            else:
                return render(request, "encyclopedia/search.html" ,{"title":title,"suggest": suggestions})
        else:
            return render(request, "encyclopedia/entry.html",{"title":title, "entry": markdown_to_html(title)})
    else:
        return HttpResponseRedirect(reverse("index"))
        
        
                             
    
# GET and POST methods for new page
def new(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        titles = [x.lower() for x in util.list_entries()]
        if title.lower() in titles:
            return render(request, "encyclopedia/error.html", {"message": "This Page Already Exists!!"})
        else:
            util.save_entry(title,content)
            return render(request, "encyclopedia/entry.html",{"title":title, "entry":util.get_entry(title)})
    else:
        return render(request, "encyclopedia/new.html")
 
 
 # POST function for Edit   
def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title":title, "content":content})
 
 # GET and POST methods for the edited view       
def edited(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title,content)
        return render(request, "encyclopedia/entry.html",{"title":title, "entry": content})
    else:
        return render(request, "encyclopedia/edit.html")
    
# GET method for the random view.
def random(request):
    random_list = [x.lower() for x in util.list_entries()]
    title = choice(random_list)
    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html",{"title":title, "entry":entry})
        
    
# function to convert markdown to html   
def markdown_to_html(title):
    markdowner = Markdown()
    md_file = util.get_entry(title)
    if not md_file:
        return None
    content = markdowner.convert(md_file)
    return content
    
    
    
        
        

