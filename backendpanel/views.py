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
    def remove_item(cls, request, item_id):
        item = EShopItem.objects.get(pk=item_id)
        item.delete()
        return HttpResponseRedirect("/manager/sklep/")
        #raise NotImplemented
    
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
    def remove_group(cls, request, item_id):
        item = GroupOffer.objects.get(pk=item_id)
        item.delete()
        return HttpResponseRedirect("/manager/grupowe/")
        #raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def auctions_list(cls, request):
        items = AuctionItem.objects.all()
        return render_to_response(
            "backpanel_auctions_list.html",
            {'items': items},
            context_instance=RequestContext(request))
    
    @classmethod
    @method_decorator(staff_member_required)
    def remove_auction(cls, request, auction_id):
        auction = AuctionItem.objects.get(pk=auction_id)
        auction.delete()
        return HttpResponseRedirect("/manager/aukcje/")
        #raise NotImplemented
        
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
    def edit_category(cls, request, item_id):
        if request.method == 'POST':
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                new_category = category_form.save()
                return HttpResponseRedirect("/manager/kategorie/")
        else:
            category=Category.objects.get(pk=item_id)
            category_name=category.name
            category_form = CategoryForm()
        return render_to_response('backpanel_new_category.html', 
                                  {'category_form': category_form, 'category_name': category_name}, 
                                  context_instance=RequestContext(request))        
        #raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def add_category(cls, request):
        if request.method == 'POST':
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                new_category = category_form.save()
                return HttpResponseRedirect("/manager/kategorie/")
        else:
            category_form = CategoryForm()
        return render_to_response('backpanel_new_category.html', 
                                  {'category_form': category_form}, 
                                  context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    @method_decorator(staff_member_required)
    def remove_category(cls, request, category_id):
        category = Category.objects.get(pk=category_id)
        category.delete()
        return HttpResponseRedirect("/manager/kategorie/")
        #raise NotImplemented
    
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
    def remove_order(cls, request, order_id):
        order = Order.objects.get(pk=order_id)
        order.delete()
        return HttpResponseRedirect("/manager/zamowienia/")
        #raise NotImplemented
    
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
        if request.method == 'POST':
            shipment_form = ShipmentMethodForm(request.POST)
            if shipment_form.is_valid():
                new_shipment_method = shipment_form.save()
                return HttpResponseRedirect("/manager/wysylka/")
        else:
            category_form = CategoryForm()
        return render_to_response('backpanel_new_shipment.html', 
                                  {'shipment_form': shipment_form}, 
                                  context_instance=RequestContext(request))
        #raise NotImplemented
    @classmethod
    @method_decorator(staff_member_required)
    def edit_shipmentmethod(cls, request, item_id):
        if request.method == 'POST':
            shipment_form = ShipmentMethodForm(request.POST)
            if shipment_form.is_valid():
                new_shipment_method = shipment_form.save()
                return HttpResponseRedirect("/manager/wysylka/")
        else:
            shipment_name=ShipmentMethod.objects.get(pk=item_id)
            category_form = CategoryForm()
        return render_to_response('backpanel_new_shipment.html', 
                                  {'shipment_form': shipment_form, 'shipment_name': shipment_name}, 
                                  context_instance=RequestContext(request))
    
    @classmethod
    @method_decorator(staff_member_required)
    def remove_shipmentmethod(cls, request, item_id):
        item = ShipmentMethod.objects.get(pk=item_id)
        item.delete()
        return HttpResponseRedirect("/manager/wysylka/")
        #raise NotImplemented
