from base.views import BaseView
from auction.models import AuctionItem
from auction.forms import AuctionForm

class AuctionView(BaseView):
    meta = AuctionItem
    
    @staticmethod
    def bid_history(request, auction_id):
        auction=AuctionItem.objects.all()
        auction=AuctionItem.objects.filter(pk=auction_id)
        bid_history=auction.bids
        return render_to_response("bid_history.html",{'bid_history': bid_history, 'auction':auction},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @staticmethod
    def aution_panel(request):
        raise NotImplemented
    
    @staticmethod
    def bid_item(request, id):
        item = BidItem.objects.get(pk=id)
        return render_to_response("bid_item.html", {item: item})
        #raise NotImplemented