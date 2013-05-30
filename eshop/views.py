#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponseRedirect

from base.views import BaseView
from base.models import BaseItem
from eshop.models import EShopItem, ShoppingCart
from ordermanager.models import OrderItem, Order
from core.models import ShopUser

class EShopView(BaseView):
    model = EShopItem
    
    @classmethod
    def onsale_products(cls, request):
        # DZIAŁA
        products_on_sale = EShopItem.objects.filter(is_on_sale=True)
        products_on_sale = products_on_sale.filter(current_stock__gte=1)
        return render_to_response("eshopitem_list.html",{'items': products_on_sale},
                                  context_instance=RequestContext(request))
           
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def add_to_cart(cls, request, id):
        #raise Http404(request.user.username)
        
        # DZIALA
        cart = ShoppingCart.objects.filter(user__pk=request.user.pk)
        if len(cart) == 0:
            cart = ShoppingCart()
            cart.user = ShopUser.objects.get(user__pk=request.user.pk)
            cart.save()
        else:
            cart = cart[0]
        
        item = EShopItem.objects.get(pk=id)
        
        order_items = OrderItem.objects.filter(belongs_to__user__pk=request.user.pk, item__pk=item.base.pk)
        
        if len(order_items) == 0:
            order_item = OrderItem()
            order_item.belongs_to = cart.user
            order_item.item = BaseItem.objects.get(pk=item.base.pk)
        else:
            order_item = order_items[0]
        
        order_item.quantity += 1
        order_item.save()
        
        cart.items.add(order_item)
        cart.save()
        return HttpResponseRedirect('/koszyk/')
        #raise NotImplemented
    
    @classmethod
    def compare_items(cls, request, id1, id2):
        # DZIAŁA
        item1 = EShopItem.objects.get(pk=id1)
        item2 = EShopItem.objects.get(pk=id2)
        
        prop1 = json.loads(item1.base.properties)
        prop2 = json.loads(item2.base.properties)
        
        keys = set(prop1.keys()) & set(prop2.keys())
        table = [[key, prop1[key], prop2[key]] for key in keys]
        
        return render_to_response("eshop_compare.html", 
                                  {'item1': item1, 'item2': item2, 'table': table},
                                  context_instance=RequestContext(request))
    
    