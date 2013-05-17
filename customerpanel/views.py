from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from auction.forms import AuctionForm
from eshop.models import ShoppingCart, ProductWatcher
from ordermanager import Order
from auction import Bid

class CustomerPanel:
    @login_required
    @classmethod
    def order_history(cls,request):
        list=Order.objects.all()
        list=list.objects.filter(user=request.user)
        return render_to_response("order_history.html",{'products': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @login_required
    @classmethod
    def order_details(cls,request, order_id):
        list=Order.objects.all()
        list=list.objects.filter(user=request.user)
        list=list.objects.filter(pk=order_id)
        return render_to_response("order_details.html",{'products': list},context_instance=RequestContext(request))
        #raise NotImplemented     

    @classmethod
    def auction_history(cls,request):
        #te w ktorych bral udzial
        list=Bid.objects.all()
        list=list.objects.filter(user=request.user)
        return render_to_response("auction_list.html",{'products': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @login_required
    @classmethod
    def add_auction(cls,request):
        raise NotImplemented
    
    @login_required
    @classmethod
    def show_panel(cls,request):
        raise NotImplemented
    
    @classmethod
    def shopping_cart(cls,request):
        list=ShoppingCart.objects.all()
        list=list.objects.filter(user=request.user)
        return render_to_response("shopping_cart.html",{'products': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @login_required
    @classmethod
    def watched_products(cls,request):
        list=ProductWatcher.objects.all()
        list=list.objects.filter(user=request.user)
        return render_to_response("watched_products.html",{'products': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    def shopping_cart_small(cls,request):
        raise NotImplemented
    
    @classmethod
    def login(cls,request):
        raise NotImplemented
    
    @classmethod
    def logout(cls,request):
        #raise NotImplemented
        logout(request)
        return HttpResponseRedirect('/home/')
    
    @classmethod
    def register(cls,request):
        raise NotImplemented
    
    @login_required
    @classmethod
    def checkout(cls,request):
        raise NotImplemented
