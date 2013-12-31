from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.files import File
import urllib
import os.path

from base.forms import SearchForm
from base.models import BaseItem
from core.models import Category
from core.models import ShopUser
from core.models import Image
from core.models import AvailiabilityStatus
from eshop.models import EShopItem
from groupbuy.models import GroupOffer
from auction.models import AuctionItem
from ordermanager.models import Order
from ordermanager.models import ShipmentMethod
from backendpanel.forms import CategoryForm
from backendpanel.forms import ShipmentMethodForm
from backendpanel.forms import GroupOfferForm
from backendpanel.forms import EshopItemForm

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
        if request.method == 'POST':
            form = EshopItemForm(request.POST)
            if form.is_valid():
                #nowy BaseItem
                base_name = request.POST['name']
                base_category_name = request.POST['category']
                base_category = Category.objects.get(pk=base_category_name)
                #properties konstrukcja Json
                json = '{'
                properties = [[request.POST['properties1'], request.POST['pname1']], [request.POST['properties2'], request.POST['pname2']], [request.POST['properties3'], request.POST['pname3']], [request.POST['properties4'], request.POST['pname4']],
                              [request.POST['properties5'], request.POST['pname5']], [request.POST['properties6'], request.POST['pname6']]]
                i=0
                for property in properties:
                    if property[0]:
                        if i<len(properties) and i>0:
                            json = json + ',\r\n'
                        i = i+1
                        json = json + '"' + property[1] + '":"' + property[0] +'"'
                        
                json = json +'}'
                    
                #
                base_description = request.POST['description']
                base_thumb = request.FILES.get('thumb')
                base_is_active = request.POST['is_active']
                #
                new_base = BaseItem(name=base_name, properties=json, description=base_description, thumb=base_thumb, is_active=base_is_active)
                new_base.save()
                
                #images
                image1 = request.FILES.get('image1')
                new_image1 = Image(image=image1)
                if image1:                    
                    new_image1.save()
                    new_base.images.add(new_image1)
                image2 = request.FILES.get('image2')
                new_image2 = Image(image=image2)
                if image2:                    
                    new_image2.save()
                    new_base.images.add(new_image2)
                image3 = request.FILES.get('image3')
                new_image3 = Image(image=image3)
                if image3:
                    new_image3.save()
                    new_base.images.add(new_image3)
                
                #dodaj kategorie i obrazy 
                new_base.categories.add(base_category)                
                new_base.save()
                #nowy EshopItem
                price = request.POST['price']
                is_on_sale = request.POST.get('is_on_sale', False)
                discount_price = request.POST.get('discount_price')
                availiability_status_name = request.POST['availiability_status']
                availiability_status = AvailiabilityStatus.objects.get(pk=availiability_status_name)
                current_stock = request.POST['current_stock']
                
                new_eshopitem = EShopItem(price=price, is_on_sale=is_on_sale, discount_price=discount_price, availiability_status=availiability_status, current_stock=current_stock, base=new_base)
                new_eshopitem.save()
                return HttpResponseRedirect("/manager/sklep/")
        else:
            form = EshopItemForm(initial={"discount_price":0})
        return render_to_response('backpanel_new_item.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))
        #raise NotImplemented

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
    def edit_group(cls, request, id):
        if request.method == 'POST':
            form = GroupOfferForm(request.POST)
            if form.is_valid():
                groupoffer = GroupOffer.objects.get(pk=id)
                base_name = request.POST['base']
                base = BaseItem.objects.get(pk=base_name)
                price = request.POST['price']
                min_num_buyers = request.POST['min_num_buyers']
                availiability_status_name = request.POST['availiability_status']
                availiability_status = AvailiabilityStatus.objects.get(pk=availiability_status_name)
                current_stock = request.POST['current_stock']
                groupoffer.base = base
                groupoffer.price = price
                groupoffer.min_num_buyers = min_num_buyers
                groupoffer.availiability_status = availiability_status
                groupoffer.current_stock = current_stock
                groupoffer.save()
                return HttpResponseRedirect("/manager/grupowe/")
        else:
            groupoffer = GroupOffer.objects.get(pk=id)
            base = groupoffer.base
            price = groupoffer.price
            min_num_buyers = groupoffer.min_num_buyers
            availiability_status = groupoffer.availiability_status
            current_stock = groupoffer.current_stock
            form = GroupOfferForm(initial={"base":base, "price":price, "min_num_buyers":min_num_buyers, "availiability_status":availiability_status, "current_stock":current_stock})
        return render_to_response('backpanel_new_groupoffer.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))

    @classmethod
    @method_decorator(staff_member_required)
    def add_group(cls, request):
        if request.method == 'POST':
            form = GroupOfferForm(request.POST)
            if form.is_valid():
                base_name = request.POST['base']
                base = BaseItem.objects.get(pk=base_name)
                price = request.POST['price']
                min_num_buyers = request.POST['min_num_buyers']
                availiability_status_name = request.POST['availiability_status']
                availiability_status = AvailiabilityStatus.objects.get(pk=availiability_status_name)
                current_stock = request.POST['current_stock']
                #user = ShopUser.objects.get(user__pk=request.user.pk)
                new_groupoffer = GroupOffer(price=price ,min_num_buyers=min_num_buyers, availiability_status=availiability_status, current_stock=current_stock, current_num_buyers=0, base=base)
                #new_groupoffer.buyers.add(user)
                new_groupoffer.save()
                return HttpResponseRedirect("/manager/grupowe/")
        else:
            form = GroupOfferForm()
        return render_to_response('backpanel_new_groupoffer.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))
    
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
        items_list = Order.objects.all()
        paginator = Paginator(items_list, 10)
        page = request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)
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
