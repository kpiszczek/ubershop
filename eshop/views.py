from base.views import BaseView
from eshop.models import EShopItem

class EShopView(BaseView):
    meta = EShopItem
    
    @staticmethod
    def onsale_products(request):
        raise NotImplemented
    
    @staticmethod
    def add_to_cart(request):
        raise NotImplemented
    
    @staticmethod
    def compare_items(request):
        raise NotImplemented
    
    