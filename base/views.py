#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.utils.decorators import method_decorator

from base.models import BaseItem
from core.models import Category
from base.models import BaseItem
from eshop.models import EShopItem
from auction.models import AuctionItem
from groupbuy.models import GroupOffer
from base.forms import SearchForm
from pdfgenerator.generator import PdfGenerator

def inject_search_form(view):
    def inner(request, id, injected=None):
        search_form = SearchForm()
        data = {"search_form": search_form}
        if injected is not None:
            data.update(injected)
        return view(request, id, data)
    return inner

class BaseView():
    model = BaseItem
     
    @classmethod
    def get_categories(cls):
        return Category.objects.all()
    
    @classmethod
    def items_list(cls, request, page=0):
        # DZIALA
        if cls.model == BaseItem:
            raise Http404
        items = cls.model.objects.filter(base__is_active=True).order_by("-base__created_at")[page:(page+1)*15]
        
        # sprawdzamy czy istnieje następna/poprzednia strona
        next_page = page+1 if len(items) == 15 else None
        prev_page = page-1 if page > 0 else None
        
        return render_to_response("%s_list.html" % cls.model.__name__.lower(),
                                  {"items": items, "prev_page": prev_page, "next_page": next_page,
                                   "categories": cls.get_categories(), "search_form": SearchForm()},
                                  context_instance=RequestContext(request))   
    
    @classmethod
    def search_item(cls, request):
        # DZIALA
        if request.method == "POST":
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                phrase = search_form.cleaned_data["phrase"]
                words = phrase.replace(';',' ').replace(',',' ').replace('.',' ').split(' ')
                items = cls.model.objects.filter(reduce(
                    lambda x, y: x | y, [Q(base__description__contains=word) for word in words]))  
                return render_to_response("%s_list.html" % cls.model.__name__.lower(),
                                  {"items": items, "categories": cls.get_categories(),
                                   'search_form': search_form},
                                  context_instance=RequestContext(request))
    
    @classmethod
    @method_decorator(inject_search_form)   
    def show_item(cls, request, id, injected=None):
        # DZIALA
        # cls.model w każdej klasie podklasie CośtamView jest podmieniany na odpowiednią klasę modelu.
        # cls.model odpowiada EShopItem, AuctionItem, GroupOffer w zależnosci od klasy, z której zostanie wywołane.
        item = cls.model.objects.get(pk=id)
        data = {"item": item, "categories": cls.get_categories()}
        if injected is not None:
            data.update(injected)
        # raise Http404(item.base.name)
        # podmieniamy początek nazwy szablony na nazwę klasy modelu (pisanej małymi literami)
        return render_to_response("%s_detail.html" % cls.model.__name__.lower(),
                                  data,
                                  context_instance=RequestContext(request))
    
    @classmethod
    def get_item_pdf(cls, request, id):
        # DZIALA
        generator = PdfGenerator(cls.model, id)
        return generator.item_page()
    
    @classmethod
    def newest_items(cls, request):
        # DZIALA
        return cls.items_list(request, page=0)
    
    @classmethod
    def popular_items(cls, request):
        raise NotImplemented