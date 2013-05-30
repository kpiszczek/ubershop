from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from base.views import BaseView
from auction.models import AuctionItem, Bid
from auction.forms import AuctionForm, BidForm

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
                                  {'bid_history': bid_history, 'auction': auction})
        #raise NotImplemented       
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def auction_panel(cls, request):
        raise NotImplemented
    
    @classmethod
    def bid_item(cls, request, id):
        # NIE DZIALA - nie wyswietla danych z bazy
        item = Bid.objects.get(pk=id)
        return render_to_response("bid_item.html", {item: item})
        #raise NotImplemented
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))   
    def bid(cls, request, auction_id):
        raise NotImplemented