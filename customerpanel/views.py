from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from auction.forms import AuctionForm
from eshop.models import ShoppingCart, ProductWatcher

class CustomerPanel:
    @login_required
    @classmethod
    def order_history(cls,request):
        raise NotImplemented
    
    @login_required
    @classmethod
    def order_details(cls,request):
        raise NotImplemented    

    @classmethod
    def auction_history(cls,request):
        raise NotImplemented
    
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
        raise NotImplemented
    
    @login_required
    @classmethod
    def watched_products(cls,request):
        raise NotImplemented
    
    @classmethod
    def shopping_cart_small(cls,request):
        raise NotImplemented
    
    @classmethod
    def login(cls,request):
        raise NotImplemented
    
    @classmethod
    def logout(cls,request):
        raise NotImplemented
    
    @classmethod
    def register(cls,request):
        raise NotImplemented
    
    @login_required
    @classmethod
    def checkout(cls,request):
        raise NotImplemented
