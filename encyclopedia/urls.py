from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry_details, name="entry"),
    path("search/", views.search, name="search"),
    path("newpage/", views.newpage, name="newpage"),
    path("wiki/<str:entry>/Edit", views.editcontent, name="edit"),
    path("random/", views.random_page, name="random"),
]
