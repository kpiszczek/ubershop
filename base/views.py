#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.models import BaseItem
from core.models import Category
from eshop.models import EShopItem
from auction.models import AuctionItem
from groupbuy.models import GroupOffer
from pdfgenerator.generator import PdfGenerator

class BaseView():
    model = BaseItem
     
    @classmethod
    def items_list(cls, request, page=0):
        if cls.model == BaseItem:
            raise Http404
        items = cls.model.objects.filter(base__is_active=True).order_by("-created_at")[page:(page+1)*15]
        
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
    def show_item(cls, request, id):
        # cls.model w każdej klasie podklasie CośtamView jest podmieniany na odpowiednią klasę modelu.
        # cls.model odpowiada EShopItem, AuctionItem, GroupOffer w zależnosci od klasy, z której zostanie wywołane.
        item = cls.model.objects.get(pk=id)
        # raise Http404(item.base.name)
        # podmieniamy początek nazwy szablony na nazwę klasy modelu (pisanej małymi literami)
        return render_to_response("%s_detail.html" % cls.model.__name__.lower(),
                                  {"item": item},
                                  context_instance=RequestContext(request))
    
    @classmethod
    def get_item_pdf(cls, request, id):
        generator = PdfGenerator(cls.model, id)
        return generator.item_page()
    
    @classmethod
    def newest_items(cls, request):
        #raise NotImplemented
        if(section=='auction'):
            auctions = AuctionItem.objects.all
            auctions = auctions.filter(close_date>datetime.now())
            auctions = auctions.filter(start_date<datetime.now())
            auctions = auctions.order_by('start_date')
            auctions = auctions[:10]
            return render_to_response("auction_list.html",{'auctions': auctions, 'next_page': page+1}, context_instance=RequestContext(request))       
        if(section=='eshop'):
            categories = Category.objects.all()
            products_query = EShopItem.objects.all
            products_query = products_query.filter(availiability_status='available') 
            products_query = products.order_by('created_at')     
            products = products_query[:20]
            return render_to_response("eshop_list.html",{'categories': categories, 'promotion_items': products, 'next_page': page+1}, context_instance=RequestContext(request))            
        if(section=='groupbuy'):
            offers = GroupOffer.objects.all()
            offers = offers.filter(availiability_status='available')
            offers = offers.order_by('created_at')
            offers = offers[:10]
            return render_to_response("groupbuy_list.html",{'offers': offers, 'next_page': page+1}, context_instance=RequestContext(request))
    
    
    @classmethod
    def popular_items(cls, request):
        raise NotImplemented