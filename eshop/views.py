from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from base.views import BaseView
from eshop.models import EShopItem

class EShopView(BaseView):
    model = EShopItem
    
    @classmethod
    def onsale_products(cls, request):
        #raise NotImplemented
        products_on_sale = EShopItem.objects.filter(is_on_sale=True)
        products_on_sale = products_on_sale.filter(current_stock__gte=1)
        return render_to_response("eshop_list.html",{'products': products_on_sale},
                                  context_instance=RequestContext(request))
    
    @method_decorator(login_required)
    @classmethod
    def add_to_cart(cls, request, id):
        cart=ShoppingCart.objects.get(user=request.user)
        item = cls.model.objects.get(pk=id)
        cart.items.add(item)
        #raise NotImplemented
    
    @classmethod
    def compare_items(cls, request, id1, id2):
        item1 = cls.model.objects.get(pk=id1)
        item2 = cls.model.objects.get(pk=id2)
        
        keys = set(item1.base.properties.keys()) & set(item2.base.properties.keys())
        table = [[key, item1.base.properties[key], item2.base.properties[key]] for key in keys]
        
        return render_to_response("eshop_compare.html", 
                                  {'item1': item1, 'item2': item2, 'table': table},
                                  context_instance=RequestContext(request))
    
    