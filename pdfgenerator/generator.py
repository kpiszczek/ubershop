# import reportlab - trzeba sciągnąć i zainstalować!!!

class PdfGenerator():
    def __init__(self):
        self.story = []
      
    def go(self):
        raise NotImplemented
    
    def serve_file(self,file):
        raise NotImplemented
    
    def item_page(self,item):
        raise NotImplemented
    
    def order_confirmation(self,order):
        raise NotImplemented