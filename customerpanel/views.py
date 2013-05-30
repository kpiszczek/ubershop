from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.template import RequestContext

from auction.forms import AuctionForm
from auction.models import AuctionItem
from eshop.models import ShoppingCart, ProductWatcher
from ordermanager.models import Order
from auction.models import Bid
from core.models import ShopUser
from customerpanel.forms import RegisterForm

class CustomerPanel:
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def order_history(cls,request):
        # DZIALA
        current_user = ShopUser.objects.get(user__pk=request.user.pk)
        list = Order.objects.filter(placed_by__pk=current_user.pk)
        return render_to_response("order_history.html",{'orders': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def order_details(cls,request, order_id):
        # DZIALA
        order=Order.objects.get(pk=order_id)
        return render_to_response("order_details.html",{'order': order},context_instance=RequestContext(request))
        #raise NotImplemented     

    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def auction_history(cls,request):
        # NIE DZIALA - Cannot resolve keyword 'user' into field.
        #te w ktorych bral udzial
        list=AuctionItem.objects.get(bids__user__username=request.user.username)
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
        # DZIALA
        current_user = request.user.username
        #raise Http404(current_user)
        current_user = ShopUser.objects.get(user__username=current_user)
        #if ShoppingCart.objects.get(user=current_user):
        cart = ShoppingCart.objects.get_or_create(user__pk=current_user.pk)[0]
        return render_to_response("shopping_cart.html",{'cart': cart},context_instance=RequestContext(request))
        #else:
        #    cart=ShoppingCart(user=current_user)
        #    return render_to_response("shopping_cart.html",{'cart': cart},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def watched_products(cls,request):
        # NIE DZIALA - NIE WYSWIETLA LISTY PRODUCT WATCHEROW DLA DANEGO USERA
        current_user = request.user.username
        #raise Http404(current_user)
        current_user = ShopUser.objects.get(user__username=current_user)
        list=ProductWatcher.objects.get_or_create(user__pk=current_user.pk)[0]
        return render_to_response("watched_products.html",{'products': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    def shopping_cart_small(cls,request):
        raise NotImplemented
    
    @classmethod
    def login(cls,request):
        # DZIALA (chyba bo nie mam jeszcze strony profilu usera)
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
        # ZAKALDAM ZE DZIALA BO TO STANDARD
        #raise NotImplemented
        logout(request)
        return render_to_response("logout.html",context_instance=RequestContext(request))
    
    @classmethod
    def register(cls,request):
        # DZIALA
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                
                shop_user = ShopUser()
                shop_user.user = user
                shop_user.address = form.cleaned_data["address"]
                shop_user.organisation = form.cleaned_data["organisation"]
                shop_user.tax_id = form.cleaned_data["tax_id"]
                shop_user.discount = 0
                shop_user.total_spendings = 0
                shop_user.save()
                
                return HttpResponseRedirect("/accounts/login/")
        else:
            form = RegisterForm()
            return render_to_response("registration.html", {'form': form}, context_instance=RequestContext(request))
        #raise NotImplemented
    
    @login_required
    @classmethod
    def checkout(cls,request):
        raise NotImplemented
