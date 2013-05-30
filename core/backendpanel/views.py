from django.contrib.auth.decorators import login_required

class BackendPanel:
    # PO CO NAM 2 BACKEDNPANEL?
    @login_required
    @classmethod
    def items_list(cls,request):
        raise NotImplemented
    
    @login_required
    @classmethod
    def edit_item(cls,request):
        raise NotImplemented    

    @login_required
    @classmethod
    def add_item(cls,request):
        raise NotImplemented
 
    @login_required   
    @classmethod
    def popular_items(cls,request):
        raise NotImplemented
    
    @login_required
    @classmethod
    def login(cls,request):
        raise NotImplemented
    
    @login_required
    @classmethod
    def logout(cls,request):
        raise NotImplemented