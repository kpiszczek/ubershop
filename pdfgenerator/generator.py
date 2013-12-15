# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse, Http404

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import *
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

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
        pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
        pdfmetrics.registerFont(TTFont('Verdana-Bold', 'VERDANAB.TTF'))
        self.styles.add(ParagraphStyle(name='mystyle', fontName='Verdana'))
        self.styles.add(ParagraphStyle(name='mystyleb', fontName='Verdana-Bold'))
        item = self.model.objects.get(pk=self.obj_id)
        logo = "c:/projects/ubershop/static/img/logo1.png"
        image = Image(logo)
        image._restrictSize(4 * cm, 2 * cm)
        self.story.append(image)
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph('<para align="center"><b>Karta produktu</b></para>', self.styles['Heading1']))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("<b>Nazwa produktu: </b>", self.styles["mystyleb"]))
        self.story.append(Paragraph(item.base.name, self.styles["mystyle"]))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("<b>Cena: </b>", self.styles["mystyleb"]))
        self.story.append(Paragraph(str(item.price)+" zł", self.styles["mystyle"]))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("<b>Opis produktu: </b>", self.styles["mystyleb"]))
        self.story.append(Paragraph(u'<para align="justify">'+item.base.description+'</para>', self.styles["mystyle"]))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("<b>Cechy produktu: </b>", self.styles["mystyleb"]))
        if item.base.properties is not None:
            tmp = item.base.properties
            props = json.loads(tmp)
            data = [[key, props[key]] for key in props.keys()]
            self.story.append(Table(data))
        try:
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph("<b>Zdjęcia produktu: </b>", self.styles["mystyleb"]))
            self.story.append(Spacer(1, 12))
            thumb = Image(item.base.thumb)
            thumb._restrictSize(8 * cm, 6 * cm)
            self.story.append(thumb)
            #self.story.append(Image(item.base.images.all()[0].image))
        except Exception:
            pass
        return self.serve_file()
    
    def order_confirmation(self, order):
        raise NotImplemented