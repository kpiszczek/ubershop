#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mandrill

from collections import namedtuple

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from base.models import BaseItem
from base.forms import SearchForm
from base.views import BaseView
from auction.forms import AuctionForm
from auction.models import AuctionItem
from eshop.models import ShoppingCart, ProductWatcher, EShopItem
from groupbuy.models import GroupOffer
from ordermanager.models import Order, OrderStatus, OrderItem
from auction.models import Bid
from core.models import ShopUser, Image
from customerpanel.forms import RegisterForm, EditUserForm, CartFormset
from ordermanager.forms import OrderForm

CartItem = namedtuple("CartItem", ["base", "concrete", "type", "quantity"])


class CustomerPanel:

    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def order_history(cls, request):
        # DZIALA
        current_user = ShopUser.objects.get(user__pk=request.user.pk)
        order_list = Order.objects.filter(placed_by__pk=current_user.pk)
        
        paginator = Paginator(order_list, 10)
        page = request.GET.get('page')

        try:
            list = paginator.page(page)
        except PageNotAnInteger:
            list = paginator.page(1)
        except EmptyPage:
            list = paginator.page(paginator.num_pages)
        return render_to_response("order_history.html", {'orders': list}, context_instance=RequestContext(request))
        #raise NotImplemented

    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def order_details(cls, request, order_id):
        # DZIALA
        order = Order.objects.get(pk=order_id)
        return render_to_response("order_details.html", {'order': order}, context_instance=RequestContext(request))
        #raise NotImplemented

    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def auction_history(cls, request):
        # DZIALA - aukcje które założył użyszkodnik
        current_user = ShopUser.objects.get(user__pk=request.user.pk)
        list = AuctionItem.objects.filter(created_by__pk=current_user.pk)
        return render_to_response("auctionitem_list.html",
                                  {'items': list, 'search_form': SearchForm(),
                                   'categories': BaseView.get_categories()},
                                  context_instance=RequestContext(request))
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
                base_item.is_active = True

                image = Image()
                image.image = form.cleaned_data["image"]
                image.save()

                base_item.images.add(Image.objects.get(pk=image.pk))
                base_item.save()

                auction = AuctionItem()
                auction.base = base_item
                auction.start_date = form.cleaned_data["start_date"]
                auction.planned_close_date = form.cleaned_data[
                    "planned_close_date"]
                auction.start_price = form.cleaned_data["start_price"]
                auction.current_price = auction.start_price
                auction.reserve_price = form.cleaned_data["reserve_price"]
                auction.properties = "{}"

                current_user = ShopUser.objects.get(user__pk=request.user.pk)
                auction.created_by = current_user

                auction.save()

                return HttpResponseRedirect("/aukcje/%s/" % str(auction.pk))
            else:
                return render_to_response("auction_add.html", {'form': form},
                                          context_instance=RequestContext(request))
        else:
            form = AuctionForm()
            return render_to_response("auction_add.html", {'form': form},
                                      context_instance=RequestContext(request))

    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def show_panel(cls, request):
        if request.method == "POST":
            form = EditUserForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]

                user = User.objects.get(pk=request.user.pk)
                user.set_password(password)
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                shop_user = ShopUser.objects.get(user__pk=user.pk)
                shop_user.address = form.cleaned_data["address"]
                shop_user.organisation = form.cleaned_data["organisation"]
                shop_user.tax_id = form.cleaned_data["tax_id"]
                shop_user.save()

                return HttpResponseRedirect("/accounts/logout/")
            else:
                return render_to_response("customerpanel.html", {'form': form}, context_instance=RequestContext(request))
        else:
            form = EditUserForm()
            return render_to_response("customerpanel.html", {'form': form}, context_instance=RequestContext(request))

    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def shopping_cart(cls, request):
        # DZIALA
        current_user = request.user
        #raise Http404(current_user)
        current_user = ShopUser.objects.get(user__pk=current_user.pk)

        # if ShoppingCart.objects.get(user=current_user):
        try:
            cart = ShoppingCart.objects.get_or_create(
                user__pk=current_user.pk)[0]
        except Exception:
            cart = ShoppingCart.objects.create(user=current_user)
            cart.save()

        cart_items = []
        formset_data = []

        for item in cart.items.all():
            try:
                concrete = EShopItem.objects.get(base__pk=item.item.pk)
                cart_items.append(CartItem(base=item.item, concrete=concrete,
                                           type="eshop", quantity=item.quantity))
            except EShopItem.DoesNotExist:
                concrete = GroupOffer.objects.get(base__pk=item.item.pk)
                cart_items.append(CartItem(base=item.item, concrete=concrete,
                                           type="group", quantity=item.quantity))

            formset_data.append({"quantity": item.quantity})

        formset = CartFormset(initial=formset_data)
        data = zip(cart_items, formset)

        total = sum([float(item.concrete.price * item.quantity)
                    for item in cart_items])
        total = "%.2f" % total

        return render_to_response("shopping_cart.html",
                                  {'cart': cart, 'search_form': SearchForm(), "data": data,
                                   'categories': BaseView.get_categories(), 'total': total,
                                   'formset': formset},
                                  context_instance=RequestContext(request))
        # else:
        #    cart=ShoppingCart(user=current_user)
        #    return render_to_response("shopping_cart.html",{'cart': cart},context_instance=RequestContext(request))
        #raise NotImplemented

    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def update_cart(cls, request):
        if request.method == "POST":
            current_user = request.user.username
            current_user = ShopUser.objects.get(user__username=current_user)

            cart = ShoppingCart.objects.get_or_create(
                user__pk=current_user.pk)[0]
            formset = CartFormset(request.POST)

            if formset.is_valid():
                for form, item in zip(formset.forms, cart.items.all()):
                    item.quantity = int(form.cleaned_data["quantity"])
                    if item.quantity == 0:
                        cart.items.remove(item)
                    item.save()
                cart.save()
            return HttpResponseRedirect("/koszyk/")
        else:
            return HttpResponseRedirect("/koszyk/")

    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def watched_products(cls, request):
        # DZIALA
        current_user = ShopUser.objects.get(user__pk=request.user.pk)
        product_list = ProductWatcher.objects.filter(user__pk=current_user.pk)
        
        paginator = Paginator(product_list, 10)
        page = request.GET.get('page')

        try:
            list = paginator.page(page)
        except PageNotAnInteger:
            list = paginator.page(1)
        except EmptyPage:
            list = paginator.page(paginator.num_pages)
            
        return render_to_response("watched_products.html", {'list': list}, context_instance=RequestContext(request))
        #raise NotImplemented

    @classmethod
    def shopping_cart_small(cls, request):
        raise NotImplemented

    @classmethod
    def login(cls, request):
        # DZIALA (chyba bo nie mam jeszcze strony profilu usera)
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                message = 'Nieprawidlowy login lub haslo'
                return render_to_response("login.html", {'message': message}, context_instance=RequestContext(request))
        else:
            form = login_form()
            return render_to_response("login.html", {'form': form}, context_instance=RequestContext(request))

    @classmethod
    def logout(cls, request):
        # ZAKALDAM ZE DZIALA BO TO STANDARD
        #raise NotImplemented
        logout(request)
        return render_to_response("logout.html", context_instance=RequestContext(request))

    @classmethod
    def register(cls, request):
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
                return render_to_response("registration.html", {'form': form}, context_instance=RequestContext(request))
        else:
            form = RegisterForm()
            return render_to_response("registration.html", {'form': form}, context_instance=RequestContext(request))
        #raise NotImplemented

    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def checkout(cls, request):
        data = {
            'search_form': SearchForm(), 'categories': BaseView.get_categories()}
        cart = ShoppingCart.objects.get(user__user__pk=request.user.pk)
        if request.method == "POST":
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = Order()

                order.placed_by = ShopUser.objects.get(
                    user__pk=request.user.pk)
                order.status = OrderStatus.objects.get(name="przyjete")
                order.shipment_method = order_form.cleaned_data[
                    "shipment_method"]
                order.details = order_form.cleaned_data["details"]
                order.save()

                for item in cart.items.all():
                    try:
                        offer = GroupOffer.objects.get(base__pk=item.pk)
                        offer.buyers.add(order.placed_by)
                        offer.save()
                    except Exception:
                        pass
                    order.items.add(item)

                user = ShopUser.objects.get(user__pk=request.user.pk)
                total = 0
                html_mail_content = '<p>Witaj' + user.user.first_name + ' ' + user.user.last_name + '</p>' + '<p>Potwierdzamy przyjęcie zamówienia nr ' + \
                    str(order.pk) + '<p>' + \
                    '<p>Szczegóły zamówienia<p><table border="1" rules="typ"><tr><td>Nazwa</td><td>ilość</td><td>cena</td></tr>'
                for item in order.items.all():
                    shop_item = EShopItem.objects.get(base__pk=item.item.pk)
                    html_mail_content = html_mail_content + '<tr><td>' + \
                        str(item.item.name) + '</td><td>' + str(
                            item.quantity) + '</td><td>' + str(shop_item.price) + '</td></tr>'
                    total = total + item.quantity * shop_item.price
                html_mail_content = html_mail_content + '</table></br>' + '<p>Razem: ' + \
                    str(total) + '</p>' + '<p>Adres do wysyłki:</p>' + \
                    user.address + \
                    '<p>Z poważaniem </br> Ekipa UberShop</p>'

                # Wysylka maila z potwierdzeniem
                try:
                    mandrill_client = mandrill.Mandrill(
                        'x03KMKaNVHHoV3g0APQt4g')
                    message = {'to': [{'email': user.user.email,
                                       'name': user.user.first_name + ' ' + user.user.last_name,
                                       'type': 'to'}],
                               #'bcc_address':'ubershop@o2.pl',
                               'from_email': 'ubershop@o2.pl',
                               'from_name': 'Ubershop',
                               'subject': 'Potwierdzenie zamówienia numer ' + str(order.pk),
                               'headers': {'Reply-To': 'ubershop@o2.pl'},
                               'html': html_mail_content,
                               }
                    result = mandrill_client.messages.send(
                        message=message, async=False)
                except mandrill.Error, e:
                    return render_to_response(
                        "error.html", {
                            "search_form": SearchForm(), "categories": BaseView.get_categories()},
                        context_instance=RequestContext(request))

                dummy=ShopUser.objects.get(user__username='dummy')#na chama
                for item in order.items.all():
                    item.belongs_to=dummy
                    item.save()

                cart.items.clear()

                cart.save()
                order.save()

                return render_to_response(
                    "thankyou.html", {
                        "search_form": SearchForm(), "categories": BaseView.get_categories()},
                    context_instance=RequestContext(request))
            data["order_form"] = order_form
            return render_to_response("checkout.html", data,
                                      context_instance=RequestContext(request))
        else:
            data["order_form"] = OrderForm()
            return render_to_response("checkout.html", data,
                                      context_instance=RequestContext(request))
