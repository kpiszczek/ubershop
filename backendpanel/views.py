from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

from base.forms import SearchForm
from core.models import Category
from eshop.models import EShopItem
from groupbuy.models import GroupOffer
from auction.models import AuctionItem
from ordermanager.models import Order
from ordermanager.models import ShipmentMethod
from backendpanel.forms import CategoryForm
from backendpanel.forms import ShipmentMethodForm
#from backendpanel.forms import EshopItemForm

class BackendPanel:
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def main(cls, request):
        return render_to_response("backendpanel.html",
            {'search_form': SearchForm()},
            context_instance=RequestContext(request))
    #DZIALA
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

    #POWINNO DZIALAC ALE NIE CHCE MI SIE POZNIEJ DODAWAC PRODUKTU OD NOWA ;)    
    @classmethod
    @method_decorator(staff_member_required)
    def remove_item(cls, request, id):
        item = EShopItem.objects.get(pk=id)
        item.delete()
        return HttpResponseRedirect("/manager/sklep/")
        #raise NotImplemented
    
    #DZIALA
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
    
    #POWINNO DZIALAC ALE NIE CHCE MI SIE POZNIEJ DODAWAC GRUPOWEJ OFERTY OD NOWA ;)
    @classmethod
    @method_decorator(staff_member_required)
    def remove_group(cls, request, id):
        item = GroupOffer.objects.get(pk=id)
        item.delete()
        return HttpResponseRedirect("/manager/grupowe/")
        #raise NotImplemented
    
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def auctions_list(cls, request):
        items = AuctionItem.objects.all()
        return render_to_response(
            "backpanel_auctions_list.html",
            {'items': items},
            context_instance=RequestContext(request))
        
    #POWINNO DZIALAC ALE NIE CHCE MI SIE POZNIEJ DODAWAC AUKCJI OD NOWA ;)
    @classmethod
    @method_decorator(staff_member_required)
    def remove_auction(cls, request, id):
        auction = AuctionItem.objects.get(pk=id)
        auction.delete()
        return HttpResponseRedirect("/manager/aukcje/")
        #raise NotImplemented
    
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def category_list(cls, request):
        items = Category.objects.all()
        return render_to_response(
            "backpanel_category_list.html",
            {'items': items},
            context_instance=RequestContext(request))
    
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def edit_category(cls, request, id):
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                name = request.POST['name']
                category = Category.objects.get(pk=id)
                category.name=name
                category.save()
                return HttpResponseRedirect("/manager/kategorie/")
        else:
            category=Category.objects.get(pk=id)
            category_name=category.name
            form = CategoryForm(initial={"name":category_name})
        return render_to_response('backpanel_new_category.html', 
                                  {'form': form, 'category_name': category_name}, 
                                  context_instance=RequestContext(request))        
    
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def add_category(cls, request):
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                name = request.POST['name']
                new_category = Category(name=name)
                new_category.save()
                return HttpResponseRedirect("/manager/kategorie/")
        else:
            form = CategoryForm()
        return render_to_response('backpanel_new_category.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))
    
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def remove_category(cls, request, id):
        category = Category.objects.get(pk=id)
        category.delete()
        return HttpResponseRedirect("/manager/kategorie/")
    
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def orders_list(cls, request):
        items = Order.objects.all()
        return render_to_response(
            "backpanel_orders_list.html",
            {'items': items},
            context_instance=RequestContext(request))
    
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def remove_order(cls, request, id):
        order = Order.objects.get(pk=id)
        order.delete()
        return HttpResponseRedirect("/manager/zamowienia/")
        #raise NotImplemented
    
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def shipmentmethod_list(cls, request):
        items = ShipmentMethod.objects.all()
        return render_to_response(
            "backpanel_shipmentmethod_list.html",
            {'items': items},
            context_instance=RequestContext(request))
    
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def add_shipmentmethod(cls, request):
        if request.method == 'POST':
            form = ShipmentMethodForm(request.POST)
            if form.is_valid():
                name = request.POST['name']
                description = request.POST['description']
                price = request.POST['price']
                new_shipment_method = ShipmentMethod(name = name, description = description, price = price)
                new_shipment_method.save()
                return HttpResponseRedirect("/manager/wysylka/")
        else:
            form = ShipmentMethodForm()
        return render_to_response('backpanel_new_shipment.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))
        
    #DZIALA        
    @classmethod
    @method_decorator(staff_member_required)
    def edit_shipmentmethod(cls, request, id):
        if request.method == 'POST':
            form = ShipmentMethodForm(request.POST)
            if form.is_valid():
                shipment_method = ShipmentMethod.objects.get(pk=id)
                name = request.POST['name']
                description = request.POST['description']
                price = request.POST['price']
                shipment_method.name = name
                shipment_method.description = description
                shipment_method.price = price
                shipment_method.save()
                return HttpResponseRedirect("/manager/wysylka/")
        else:
            shipment = ShipmentMethod.objects.get(pk=id)
            shipment_name = shipment.name
            price = shipment.price
            description = shipment.description
            form = ShipmentMethodForm(initial={"name": shipment_name,
                                               "description": description,
                                               "price": price})
        return render_to_response('backpanel_new_shipment.html', 
                                  {'form': form,}, 
                                  context_instance=RequestContext(request))
    
    #DZIALA
    @classmethod
    @method_decorator(staff_member_required)
    def remove_shipmentmethod(cls, request, id):
        item = ShipmentMethod.objects.get(pk=id)
        item.delete()
        return HttpResponseRedirect("/manager/wysylka/")
        #raise NotImplemented
