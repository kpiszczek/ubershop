from base.models import BaseItem
from pdfgenerator.generator import PdfGenerator

class BaseView():
    meta = BaseItem
     
    @classmethod
    def items_list(cls, request):
        raise NotImplemented
    
    @classmethod
    def search_item(cls, request):
        raise NotImplemented
    
    @classmethod
    def show_item(cls, request):
        raise NotImplemented
    
    @classmethod
    def get_item_pdf(cls, request, id):
        generator = PdfGenerator(cls.meta, id)
        return generator.item_page()
    
    @classmethod
    def newest_items(cls, request):
        raise NotImplemented
    
    @classmethod
    def popular_items(cls, request):
        raise NotImplemented