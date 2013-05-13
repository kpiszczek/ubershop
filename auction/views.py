from base.views import BaseView
from auction.models import AuctionItem
from auction.forms import AuctionForm

class AuctionView(BaseView):
    meta = AuctionItem
    
    @staticmethod
    def bid_history(request):
        raise NotImplemented
    
    @staticmethod
    def aution_panel(request):
        raise NotImplemented
    
    @staticmethod
    def bid_item(request):
        raise NotImplemented