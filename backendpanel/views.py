from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from base.forms import SearchForm
from core.models import Category
from eshop.models import EShopItem
from groupbuy.models import GroupOffer
from auction.models import AuctionItem
from ordermanager.models import Order
from ordermanager.models import ShipmentMethod


class BackendPanel:
    # TU NIE MA CO DZIALAC ;)

    @classmethod
    @method_decorator(staff_member_required)
    def main(cls, request):
        return render_to_response("backendpanel.html",
            {'search_form': SearchForm()},
            context_instance=RequestContext(request))

    @classmethod
    @method_decorator(staff_member_required)
    def items_list(cls, request):
        items = EShopItem.objects.all()
        return render_to_response(
            "backpanel_items_list.html",
            {'items': items},
            context_instance=RequestContext(request))

    @classmethod
    @method_decorator(staff_member_required)
    def edit_item(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def add_item(cls, request):
        raise NotImplemented
    
    @classmethod
    @method_decorator(staff_member_required)
    def remove_item(cls, request):
        raise NotImplemented
    
    @classmethod
    @method_decorator(staff_member_required)
    def group_list(cls, request):
        items = GroupOffer.objects.all()
        return render_to_response(
            "backpanel_group_list.html",
            {'items': items},
            context_instance=RequestContext(request))

    @classmethod
    @method_decorator(staff_member_required)
    def edit_group(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def add_group(cls, request):
        raise NotImplemented
    
    @classmethod
    @method_decorator(staff_member_required)
    def remove_group(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def auctions_list(cls, request):
        items = AuctionItem.objects.all()
        return render_to_response(
            "backpanel_auction_list.html",
            {'items': items},
            context_instance=RequestContext(request))
    
    @classmethod
    @method_decorator(staff_member_required)
    def remove_auction(cls, request):
        raise NotImplemented
        
    @classmethod
    @method_decorator(staff_member_required)
    def category_list(cls, request):
        items = Category.objects.all()
        return render_to_response(
            "backpanel_category_list.html",
            {'items': items},
            context_instance=RequestContext(request))

    @classmethod
    @method_decorator(staff_member_required)
    def edit_category(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def add_category(cls, request):
        raise NotImplemented
    
    @classmethod
    @method_decorator(staff_member_required)
    def remove_category(cls, request):
        raise NotImplemented
    
    @classmethod
    @method_decorator(staff_member_required)
    def orders_list(cls, request):
        items = Order.objects.all()
        return render_to_response(
            "backpanel_orders_list.html",
            {'items': items},
            context_instance=RequestContext(request))
    
    @classmethod
    @method_decorator(staff_member_required)
    def remove_order(cls, request):
        raise NotImplemented
    
    @classmethod
    @method_decorator(staff_member_required)
    def shipmentmethod_list(cls, request):
        items = ShipmentMethod.objects.all()
        return render_to_response(
            "backpanel_shipmentmethod_list.html",
            {'items': items},
            context_instance=RequestContext(request))
    
    @classmethod
    @method_decorator(staff_member_required)
    def add_shipmentmethod(cls, request):
        raise NotImplemented
    
    @classmethod
    @method_decorator(staff_member_required)
    def remove_shipmentmethod(cls, request):
        raise NotImplemented
