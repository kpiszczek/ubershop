from base.views import BaseView
from groupbuy.models import GroupOffer

class GroupBuyView(BaseView):
    meta = GroupOffer
    
    @staticmethod
    def buyers_list(request):
        raise NotImplemented
