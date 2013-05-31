#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.template import RequestContext

from base.models import BaseItem
from auction.forms import AuctionForm
from auction.models import AuctionItem
from eshop.models import ShoppingCart, ProductWatcher
from ordermanager.models import Order, OrderStatus, OrderItem
from auction.models import Bid
from core.models import ShopUser, Image
from customerpanel.forms import RegisterForm
from ordermanager.forms import OrderForm

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
    def auction_history(cls, request):
        # DZIALA - aukcje które założył użyszkodnik
        current_user = ShopUser.objects.get(user__pk=request.user.pk)
        list = AuctionItem.objects.filter(created_by__pk=current_user.pk)
        return render_to_response("auctionitem_list.html",{'items': list},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def add_auction(cls, request):
        if request.method == "POST":
            form = AuctionForm(request.POST, request.FILES)
            if form.is_valid():
                base_item = BaseItem()
                base_item.name = form.cleaned_data["name"]
                base_item.save()
                base_item.categories = form.cleaned_data["categories"]
                base_item.description = form.cleaned_data["description"]
                base_item.thumb = form.cleaned_data["thumb"]
                
                image = Image()
                image.image = form.cleaned_data["image"]
                image.save()
                
                base_item.images.add(Image.objects.get(pk=image.pk))
                base_item.save()
                
                auction = AuctionItem()
                auction.base = base_item
                auction.start_date = form.cleaned_data["start_date"]
                auction.planned_close_date = form.cleaned_data["planned_close_date"]
                auction.start_price = form.cleaned_data["start_price"]
                auction.current_price = auction.start_price
                auction.reserve_price = form.cleaned_data["reserve_price"]
                
                current_user = ShopUser.objects.get(user__pk=request.user.pk)
                auction.created_by = current_user
                
                auction.save()
                
                return HttpResponseRedirect("/aukcje/%s/" % str(auction.pk))
            else:
                raise Http404(form._errors)
                return render_to_response("auction_add.html", {'form': form},
                                      context_instance=RequestContext(request))
        else:
            form = AuctionForm()
            return render_to_response("auction_add.html", {'form': form},
                                      context_instance=RequestContext(request))
    
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
        # DZIALA
        current_user = ShopUser.objects.get(user__pk=request.user.pk)
        list = ProductWatcher.objects.filter(user__pk=current_user.pk)
        return render_to_response("watched_products.html",{'list': list},context_instance=RequestContext(request))
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
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def checkout(cls,request):
        cart = ShoppingCart.objects.get(user__user__pk=request.user.pk)
        if request.method == "POST":
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = Order()
                         
                order.placed_by = ShopUser.objects.get(user__pk=request.user.pk)
                order.status = OrderStatus.objects.get(name="przyjete")
                order.shipment_method = order_form.cleaned_data["shipment_method"]
                order.details = order_form.cleaned_data["details"]
                order.save()
                
                for item in cart.items.all(): order.items.add(item)
                cart.items.clear()
                
                cart.save()    
                order.save()
                
                return render_to_response("thankyou.html", {},
                                          context_instance=RequestContext(request))
            return render_to_response("checkout.html",{"order_form": order_form},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response("checkout.html",{"order_form": OrderForm()},
                                      context_instance=RequestContext(request))
