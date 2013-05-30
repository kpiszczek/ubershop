from django.shortcuts import render_to_response
from django.template import RequestContext

from core.forms import SearchForm
from core.models import Category
from eshop.models import EShopItem
from board.models import Message

from django.contrib.auth.models import User

def home_page(request):
    # DZIALA
    if request.method == "POST":
        form = SearchForm(request.POST)       
    else:      
        form = SearchForm()
    categories = Category.objects.all()
    products_query = EShopItem.objects.filter(is_on_sale=True)
    products_query = products_query.filter(current_stock__gte=1)
    products = products_query[:2]
    message_query = Message.objects.filter(topic__board__name="news")
    message_query = message_query.filter(topic__title="main")
    message = message_query.order_by("-id")[0]
    return render_to_response("home.html",{'search_form': form, 'categories': categories,
                                           'promotion_items': products, "message": message},
                              context_instance=RequestContext(request))
def contact(request):
    # NIE DZIALA - WYSWIETLA PUSTA STRONE ZAMIAST POJEDYNCZEGO ZDANIA KTORE TAM TESTOWO WPISALEM
    return render_to_response("contact.html", context_instance=RequestContext(request))