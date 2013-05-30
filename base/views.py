#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.models import BaseItem
from core.models import Category
from base.models import BaseItem
from eshop.models import EShopItem
from auction.models import AuctionItem
from groupbuy.models import GroupOffer
from pdfgenerator.generator import PdfGenerator

class BaseView():
    model = BaseItem
     
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
                                  {"items": items, "prev_page": prev_page, "next_page": next_page},
                                  context_instance=RequestContext(request))   
    
    @classmethod
    def search_item(cls, request):
        raise NotImplemented
    
    @classmethod
    def show_item(cls, request, id, injected=None):
        # NIE DZIALA - nie wyswietla zawartosci bazy (brak danych produktu, brak danych o tym kto dał nawyższa oferte
        # nie zmienia sie to po dodaniu recznie bid_itema dla tej aukcji do bazy
        
        # cls.model w każdej klasie podklasie CośtamView jest podmieniany na odpowiednią klasę modelu.
        # cls.model odpowiada EShopItem, AuctionItem, GroupOffer w zależnosci od klasy, z której zostanie wywołane.
        item = cls.model.objects.get(pk=id)
        data = {"item": item}
        if injected is not None:
            data.update(injected)
        # raise Http404(item.base.name)
        # podmieniamy początek nazwy szablony na nazwę klasy modelu (pisanej małymi literami)
        return render_to_response("%s_detail.html" % cls.model.__name__.lower(),
                                  data,
                                  context_instance=RequestContext(request))
    
    @classmethod
    def get_item_pdf(cls, request, id):
        generator = PdfGenerator(cls.model, id)
        return generator.item_page()
    
    @classmethod
    def newest_items(cls, request):
        # NIE DZIALA - brak przedmiotow na liscie
        return cls.items_list(request, page=0)
    
    @classmethod
    def popular_items(cls, request):
        raise NotImplemented