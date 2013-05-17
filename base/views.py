from base.models import BaseItem
from core.models import Category
from eshop.models import EShopItem
from auction.models import AuctionItem
from groupbuy.models import GroupOffer
from pdfgenerator.generator import PdfGenerator

class BaseView():
    meta = BaseItem
     
    @classmethod
    def items_list(cls, request):
        #raise NotImplemented
        
        if(section=='auction'):
            auctions = AuctionItem.objects.all
            auctions = auctions.filter(close_date>datetime.now())
            auctions = auctions.filter(start_date<datetime.now())
            auctions = auctions[:page*15]
            return render_to_response("auction_list.html",{'auctions': auctions, 'next_page': page+1}, context_instance=RequestContext(request))       
        if(section=='eshop'):
            categories = Category.objects.all()
            products_query = EShopItem.objects.all
            products_query = products_query.filter(availiability_status='available')      
            products = products_query[:page*15]
            return render_to_response("eshop_list.html",{'categories': categories, 'promotion_items': products, 'next_page': page+1}, context_instance=RequestContext(request))            
        if(section=='groupbuy'):
            offers = GroupOffer.objects.all()
            offers = offers.filter(availiability_status='available')
            offers = offers[:page*15]
            return render_to_response("groupbuy_list.html",{'offers': offers, 'next_page': page+1}, context_instance=RequestContext(request))
    
    
    @classmethod
    def search_item(cls, request):
        raise NotImplemented
    
    @classmethod
    def show_item(cls, request, id):
        if(section=='auction'):
            auction = AuctionItem.objects.all
            auction=auction.filter(pk=id)
            return render_to_response("auction_detail.html",{'auction': auction}, context_instance=RequestContext(request))       
        if(section=='eshop'):
            product = EShopItem.objects.all
            product = product.filter(pk=id) 
            return render_to_response("eshop_detail.html",{'product': product}, context_instance=RequestContext(request))            
        if(section=='groupbuy'):
            offer = GroupOffer.objects.all()
            offer = offers.filter(pk=id)
            return render_to_response("groupbuy_detail.html",{'offer': offer}, context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    def get_item_pdf(cls, request, id):
        generator = PdfGenerator(cls.meta, id)
        return generator.item_page()
    
    @classmethod
    def newest_items(cls, request):
        #raise NotImplemented
        if(section=='auction'):
            auctions = AuctionItem.objects.all
            auctions = auctions.filter(close_date>datetime.now())
            auctions = auctions.filter(start_date<datetime.now())
            auctions = auctions.order_by('start_date')
            auctions = auctions[:10]
            return render_to_response("auction_list.html",{'auctions': auctions, 'next_page': page+1}, context_instance=RequestContext(request))       
        if(section=='eshop'):
            categories = Category.objects.all()
            products_query = EShopItem.objects.all
            products_query = products_query.filter(availiability_status='available') 
            products_query = products.order_by('created_at')     
            products = products_query[:20]
            return render_to_response("eshop_list.html",{'categories': categories, 'promotion_items': products, 'next_page': page+1}, context_instance=RequestContext(request))            
        if(section=='groupbuy'):
            offers = GroupOffer.objects.all()
            offers = offers.filter(availiability_status='available')
            offers = offers.order_by('created_at')
            offers = offers[:10]
            return render_to_response("groupbuy_list.html",{'offers': offers, 'next_page': page+1}, context_instance=RequestContext(request))
    
    
    @classmethod
    def popular_items(cls, request):
        raise NotImplemented