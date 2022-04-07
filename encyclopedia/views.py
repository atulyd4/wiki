from logging import error
from django.forms.models import fields_for_model
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import markdown2
from django.shortcuts import redirect, render
from django import forms
import secrets
from django.contrib import messages
from . import util
import encyclopedia


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_details(request, entry):
    entry_data = util.get_entry(entry)
    if entry_data is not None:
        html_data = markdown2.markdown(entry_data)
        return render(request, "encyclopedia/entry.html", {"detail": html_data, "entry": entry})
    return HttpResponse('Not found')


def search(request):

    if request.method == 'GET':
        query = request.GET.get('q')
        entry_data = util.get_entry(query)
        if entry_data is not None:
            html_data = markdown2.markdown(entry_data)
            return render(request, "encyclopedia/entry.html", {"entry": html_data})
        else:
            result = []
            for entry in util.list_entries():
                if query.upper() in entry.upper():
                    result.append(entry)
                    return render(request, "encyclopedia/index.html", {"entries": result,
                                                                       "search": True,
                                                                       "query": query})


class NewPageForm(forms.Form):
    Title = forms.CharField(label="Title", max_length=100, widget=forms.TextInput(
        attrs={'class': "form-control"}))
    Content = forms.CharField(
        label="Content", max_length=1000, widget=forms.Textarea(attrs={'class': "form-control"}))


def newpage(request):
    if request.method == "POST":
        form_data = NewPageForm(request.POST)
        if form_data.is_valid():
            title = form_data.cleaned_data.get("Title").upper()
            content = form_data.cleaned_data.get("Content")
            # # If an existing entry with the same title already exists
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html")
            else:
                util.save_entry(title, content)
                return redirect(f'/wiki/{title}')
    else:
        return render(request, "encyclopedia/newpage.html", {"form": NewPageForm()})


def editcontent(request, entry):
    entry_page = util.get_entry(entry)
    if entry_page is not None:
        form = NewPageForm()
        form.fields["Title"].initial = entry
        form.fields["Title"].widget = forms.HiddenInput()
        form.fields["Content"].initial = entry_page
        return render(request, "encyclopedia/edit.html", {"entrytitle": form.fields["Title"].initial, "form": form})


def random_page(request):
    entries = util.list_entries()
    selected_page = secrets.choice(entries)
    return HttpResponseRedirect(reverse('entry', kwargs={'entry': selected_page}))
