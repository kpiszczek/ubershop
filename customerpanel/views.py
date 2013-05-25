from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.template import RequestContext

from auction.forms import AuctionForm
from eshop.models import ShoppingCart, ProductWatcher
from ordermanager.models import Order
from auction.models import Bid
from core.models import ShopUser

class CustomerPanel:
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def order_history(cls,request):
        list=Order.objects.all()
        list=list.objects.filter(user=request.user)
        return render_to_response("order_history.html",{'orders': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def order_details(cls,request, order_id):
        order=Order.objects.get(pk=order_id)
        
        return render_to_response("order_details.html",{'order': order},context_instance=RequestContext(request))
        #raise NotImplemented     

    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def auction_history(cls,request):
        #te w ktorych bral udzial
        list=Bid.objects.all()
        list=list.objects.filter(user=request.user)
        return render_to_response("auction_list.html",{'auctions': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def add_auction(cls,request):
        raise NotImplemented
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def show_panel(cls,request):
        raise NotImplemented
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def shopping_cart(cls,request):
        current_user = request.user.username
        #raise Http404(current_user)
        current_user = ShopUser.objects.get(user__username=current_user)
        #if ShoppingCart.objects.get(user=current_user):
        cart = ShoppingCart.objects.get_or_create(user=current_user)
        return render_to_response("shopping_cart.html",{'cart': cart},context_instance=RequestContext(request))
        #else:
        #    cart=ShoppingCart(user=current_user)
        #    return render_to_response("shopping_cart.html",{'cart': cart},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def watched_products(cls,request):
        list=ProductWatcher.objects.get_or_create(user=request.user)
        return render_to_response("watched_products.html",{'products': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    def shopping_cart_small(cls,request):
        raise NotImplemented
    
    @classmethod
    def login(cls,request):
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                HttpResponseRedirect('/home/')
            else:
                message='Nieprawidlowy login lub haslo'
                return render_to_response("login.html", {'message': message}, context_instance=RequestContext(request))
        else:
            form=login_form()
            return render_to_response("login.html", {'form': form}, context_instance=RequestContext(request))
                
                
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
