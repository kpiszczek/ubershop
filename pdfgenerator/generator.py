import json

from django.http import HttpResponse

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class PdfGenerator():
    def __init__(self, model, obj_id):
        self.story = []
        self.model = model
        self.obj_id = obj_id
        self.styles = getSampleStyleSheet()
      
    def go(self):
        raise NotImplemented
    
    def serve_file(self):
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="opis_produktu.pdf"'
        
        buffer = StringIO()
        doc = SimpleDocTemplate(buffer)
        
        doc.build(self.story)
        pdf = buffer.getvalue()
        response.write(pdf)
        
        self.story = []
        
        return response
    
    def item_page(self):
        item = self.model.objects.get(pk=self.obj_id)
        
        self.story.append(Paragraph(item.base.name, self.styles["Normal"]))
        if item.base.properties is not None:
            props = json.loads(item.base.properties)
            data = [[key, props[key]] for key in props.keys()]
            self.story.append(Table(data))
        
        return self.serve_file()
    
    def order_confirmation(self,order):
        raise NotImplemented