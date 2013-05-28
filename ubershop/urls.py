from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from eshop.views import EShopView
from auction.views import AuctionView
from groupbuy.views import GroupBuyView

from board.views import BoardView
from customerpanel.views import CustomerPanel

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ubershop.views.home', name='home'),
    # url(r'^ubershop/', include('ubershop.foo.urls')),
    
    url(r'^home/$','core.views.home_page'),
    url(r'^home/kontakt/$','core.views.contact'),
   
    
    # url dla Auction
    url(r'^aukcje/nowe/$', AuctionView.newest_items),
    url(r'^aukcje/popularne/$', AuctionView.popular_items),
    url(r'^aukcje/panel/$', AuctionView.auction_panel),
    url(r'^aukcje/kategorie/(?P<category>.+)/$', AuctionView.items_list),
    url(r'^aukcje/szukaj/(?P<term>.+)/$', AuctionView.search_item), 
    url(r'^aukcje/oferta/(?P<id>\d+)/$', AuctionView.bid_item), 
    url(r'^aukcje/(?P<id>\d+)/$', AuctionView.show_item),
    url(r'^aukcje/(?P<id>\d+)/get_pdf/$', AuctionView.get_item_pdf),
    url(r'^aukcje/(?P<id>\d+)/historia/$', AuctionView.bid_history),
    url(r'^aukcje/(?P<auction_id>\d+)/licytuj/$', AuctionView.bid),
    
    # url dla EShop
    url(r'^sklep/nowe/$', EShopView.newest_items),
    url(r'^sklep/popularne/$', EShopView.popular_items),
    url(r'^sklep/kategorie/(?P<category>.+)/$', EShopView.items_list),
    url(r'^sklep/szukaj/(?P<term>.+)/$', EShopView.search_item),  
    url(r'^sklep/(?P<id>\d+)/$', EShopView.show_item),
    url(r'^sklep/(?P<id>\d+)/dodaj/$', EShopView.add_to_cart),
    url(r'^sklep/(?P<id>\d+)/get_pdf/$', EShopView.get_item_pdf),
    
    # url dla GroupBuy
    url(r'^grupowe/nowe/$', GroupBuyView.newest_items),
    url(r'^grupowe/popularne/$', GroupBuyView.popular_items),
    url(r'^grupowe/kategorie/(?P<category>.+)/$', GroupBuyView.items_list),
    url(r'^grupowe/szukaj/(?P<term>.+)/$', GroupBuyView.search_item),  
    url(r'^grupowe/(?P<id>\d+)/$', GroupBuyView.show_item),
    url(r'^grupowe/(?P<id>\d+)/kupujacy/$', GroupBuyView.buyers_list),
    url(r'^grupowe/(?P<id>\d+)/get_pdf/$', GroupBuyView.get_item_pdf),
    
    # url dla forum
    url(r'^forum/$', BoardView.show_available_board),
    url(r'^forum/nowe_forum/$', BoardView.create_board),
    url(r'^forum/(?P<board_id>\d+)/$', BoardView.show_board),
    url(r'^forum/(?P<board_id>\d+)/nowy_temat/$', BoardView.create_topic),
    url(r'^forum/(?P<board_id>\d+)/(?P<topic_id>\d+)/$', BoardView.show_topic),
    url(r'^forum/(?P<board_id>\d+)/(?P<topic_id>\d+)/nowy_post/$', BoardView.submit_message),
    url(r'^forum/(?P<board_id>\d+)/(?P<topic_id>\d+)/(?P<message_id>\d+)/$', BoardView.show_message),  
    
    # url dla customerpanel
    url(r'^koszyk/$', CustomerPanel.shopping_cart),
    url(r'^accounts/login/$','django.contrib.auth.views.login'),
    url(r'^rejestracja/$', CustomerPanel.register),
    
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^mymedia/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
