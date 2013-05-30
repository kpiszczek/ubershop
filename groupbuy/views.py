from base.views import BaseView
from groupbuy.models import GroupOffer
from django.shortcuts import render_to_response
from django.template import RequestContext

class GroupBuyView(BaseView):
    model = GroupOffer
    
    @classmethod
    def buyers_list(cls, request, offer_id):
        # DZIALA
        offer = GroupOffer.objects.get(pk=offer_id)
        return render_to_response("groupoffer_buyers.html",{'buyers': offer.buyers, 'offer': offer},
                                  context_instance=RequestContext(request))
