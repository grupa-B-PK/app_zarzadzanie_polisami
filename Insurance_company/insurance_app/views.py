from django.shortcuts import render
from django.views.generic import View, TemplateView


class IndexView(TemplateView):
    template_name = 'index'
