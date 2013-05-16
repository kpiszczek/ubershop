from base.models import BaseItem
from pdfgenerator.generator import PdfGenerator

class BaseView():
    meta = BaseItem
     
    @staticmethod
    def items_list(request):
        raise NotImplemented
    
    @staticmethod
    def search_item(request):
        raise NotImplemented
    
    @staticmethod
    def show_item(request):
        raise NotImplemented
    
    @classmethod
    def get_item_pdf(cls, request, id):
        generator = PdfGenerator(cls.meta, id)
        return generator.item_page()
    
    @staticmethod
    def newest_items(request):
        raise NotImplemented
    
    @staticmethod
    def popular_items(request):
        raise NotImplemented