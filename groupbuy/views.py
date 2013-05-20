from base.views import BaseView
from groupbuy.models import GroupOffer

class GroupBuyView(BaseView):
    meta = GroupOffer
    
    @staticmethod
    def buyers_list(request, offer_id):
        offer=GroupOffer.objects.get(pk=offer_id)
        buyers_list=offer.buyers
        return render_to_response("groupoffer_buyers.html",{'buyers': buyers_list, 'offer':offer},context_instance=RequestContext(request))
        #raise NotImplemented
