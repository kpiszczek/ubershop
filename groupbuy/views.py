from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from base.views import BaseView
from groupbuy.models import GroupOffer
from base.forms import SearchForm
from eshop.models import ShoppingCart
from ordermanager.models import OrderItem

class GroupBuyView(BaseView):
    model = GroupOffer
    
    @classmethod
    def buyers_list(cls, request, offer_id):
        # DZIALA
        offer = GroupOffer.objects.get(pk=offer_id)
        return render_to_response("groupoffer_buyers.html",{'buyers': offer.buyers, 'offer': offer, 
                                                            "categories": cls.get_categories(), 
                                                            "search_form": SearchForm()},
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
        
        item = GroupOffer.objects.get(pk=id)
        
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