import json
from datetime import datetime

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext

from base.views import BaseView
from base.forms import SearchForm
from auction.models import AuctionItem, Bid
from auction.forms import AuctionForm, BidForm, EditAuctionForm
from core.models import ShopUser, Image

def inject_bid_form(view):
    def inner(request, id):
        bid_form = BidForm()
        return view(request, id, {"bid_form": bid_form})
    return inner

class AuctionView(BaseView):
    model = AuctionItem
    
    @classmethod
    def bid_history(cls, request, auction_id):
        # DZIALA
        auction = AuctionItem.objects.get(pk=auction_id)
        bid_history = auction.bids
        return render_to_response("bid_history.html",
                                  {'bid_history': bid_history, 'auction': auction, 
                                   'search_form': SearchForm(), 'categories': cls.get_categories()})
        #raise NotImplemented       
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def auction_edit(cls, request, id):
        auction = AuctionItem.objects.get(pk=id)
        base = auction.base
        if request.method == "POST":
            form = EditAuctionForm(request.POST, request.FILES)
            if form.is_valid():
                base.name = form.cleaned_data["name"]
                base.categories = form.cleaned_data["categories"]
                base.description = form.cleaned_data["description"]
                base.thumb = form.cleaned_data["thumb"]
                
                image = Image()
                image.image = form.cleaned_data["image"]
                image.save()
                
                base.images.clear()
                base.images.add(Image.objects.get(pk=image.pk))
                
                props = {}
                for line in form.cleaned_data["properties"].split("\n"):
                    line = line.split(":")
                    if len(line) == 2:
                        key, value = line
                        props[key] = value
                    else:
                        continue
                
                props = json.dumps(props, sort_keys=True)
                base.properties = props
                base.save()
                
                auction.base = base
                auction.start_date = form.cleaned_data["start_date"]
                auction.planned_close_date = form.cleaned_data["planned_close_date"]
                auction.reserve_price = form.cleaned_data["reserve_price"]
                
                auction.save()
                
                return HttpResponseRedirect("/aukcje/%s/" % str(auction.pk))
            else:
                return render_to_response("auction_edit.html", {"form": form},
                                      context_instance=RequestContext(request))
        else:
            fields = {}
            for cat in base.categories.all():
                try:
                    fields.update(json.loads(cat.properties))
                except Exception:
                    pass
            props = "\n".join([str(key) + ": \n" for key in fields.keys()])
            form = EditAuctionForm(initial={"name": base.name,
                                    "categories": base.categories.all(),
                                    "properties": props,
                                    "thumb": base.thumb,
                                    "image": base.images.all()[0],
                                    "start_date": auction.start_date,
                                    "planned_close_date": auction.planned_close_date,
                                    "reserve_price": auction.reserve_price
                                    })
            return render_to_response("auction_edit.html", {"form": form},
                                      context_instance=RequestContext(request))
            
    
    @classmethod
    def bid_item(cls, request, id):
        # DZIALA
        item = Bid.objects.get(pk=id)
        return render_to_response("bid_item.html", {'item': item},
                                  context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))   
    def bid(cls, request, auction_id):
        # DZIALA
        form = BidForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data["bid"]
                        
            current_user = ShopUser.objects.get(user__pk=request.user.pk)
            auction = AuctionItem.objects.get(pk=auction_id)
            
            if auction.current_price < price:
                bid = Bid()
                bid.user = current_user
                bid.item = auction
                bid.date = datetime.now()
                bid.price = price
                bid.save()    
            
                auction.bids.add(bid)
                
                auction.current_price = price
                auction.save()
        return HttpResponseRedirect('/aukcje/%s/' % str(auction_id))
            
            