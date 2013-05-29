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
        #raise NotImplemented
        products_on_sale = EShopItem.objects.filter(is_on_sale=True)
        products_on_sale = products_on_sale.filter(current_stock__gte=1)
        return render_to_response("eshop_list.html",{'products': products_on_sale},
                                  context_instance=RequestContext(request))
           
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def add_to_cart(cls, request, id):
        #raise Http404(request.user.username)
        
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
        item1 = cls.model.objects.get(pk=id1)
        item2 = cls.model.objects.get(pk=id2)
        
        keys = set(item1.base.properties.keys()) & set(item2.base.properties.keys())
        table = [[key, item1.base.properties[key], item2.base.properties[key]] for key in keys]
        
        return render_to_response("eshop_compare.html", 
                                  {'item1': item1, 'item2': item2, 'table': table},
                                  context_instance=RequestContext(request))
    
    