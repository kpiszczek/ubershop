from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

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
        return render_to_response("order_history.html",{'orders': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @login_required
    @classmethod
    def order_details(cls,request, order_id):
        order=Order.objects.get(pk=order_id)
        
        return render_to_response("order_details.html",{'order': order},context_instance=RequestContext(request))
        #raise NotImplemented     

    @classmethod
    def auction_history(cls,request):
        #te w ktorych bral udzial
        list=Bid.objects.all()
        list=list.objects.filter(user=request.user)
        return render_to_response("auction_list.html",{'auctions': list},context_instance=RequestContext(request))
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
        cart=ShoppingCart.objects.get(user=request.user)
        return render_to_response("shopping_cart.html",{'cart': cart},context_instance=RequestContext(request))
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            HttpResponseRedirect('/home/')
        else:
            message='Nieprawidłowy login lub hasło'
            return render_to_response("login.html", {'message': message}, context_instance=RequestContext(request))
                
                
    @classmethod
    def logout(cls,request):
        #raise NotImplemented
        logout(request)
        return render_to_response("logout.html",context_instance=RequestContext(request))
    
    @classmethod
    def register(cls,request):
        raise NotImplemented
    
    @login_required
    @classmethod
    def checkout(cls,request):
        raise NotImplemented
