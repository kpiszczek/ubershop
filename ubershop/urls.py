import os

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from eshop.views import EShopView
from auction.views import AuctionView, inject_bid_form
from base.views import inject_search_form, BaseView
from groupbuy.views import GroupBuyView

from board.views import BoardView
from customerpanel.views import CustomerPanel
from backendpanel.views import BackendPanel


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ubershop.views.home', name='home'),
    # url(r'^ubershop/', include('ubershop.foo.urls')),
    
    url(r'^home/$','core.views.home_page'),
    url(r'^home/szukaj/$', EShopView.search_item),
    url(r'^home/kontakt/$', EShopView.contact),#'core.views.contact'),
    url(r'^home/.+/szukaj/$', EShopView.search_item),
   
    
    # url dla Auction
    url(r'^aukcje/nowe/$', AuctionView.newest_items),
    url(r'^aukcje/nowe/(?P<page>\d+)/$', AuctionView.newest_items),
    url(r'^aukcje/popularne/$', AuctionView.popular_items),
    #url(r'^aukcje/panel/$', AuctionView.auction_panel),
    url(r'^aukcje/kategorie/(?P<id>.+)/$', AuctionView.category),
    url(r'^aukcje/kategorie/(?P<id>.+)/(?P<page>\d+)/$', AuctionView.category),
    url(r'^aukcje/szukaj/$', AuctionView.search_item), 
    url(r'^aukcje/oferta/(?P<id>\d+)/$', AuctionView.bid_item), 
    url(r'^aukcje/(?P<id>\d+)/$', inject_bid_form(AuctionView.show_item)),
    url(r'^aukcje/(?P<id>\d+)/edytuj/$', AuctionView.auction_edit),
    url(r'^aukcje/(?P<id>\d+)/get_pdf/$', AuctionView.get_item_pdf),
    url(r'^aukcje/(?P<auction_id>\d+)/historia/$', AuctionView.bid_history),
    url(r'^aukcje/(?P<auction_id>\d+)/licytuj/$', AuctionView.bid),
    url(r'^aukcje/.+/szukaj/$', AuctionView.search_item), 
    
    # url dla EShop
    url(r'^sklep/nowe/$', EShopView.newest_items),
    url(r'^sklep/nowe/(?P<page>\d+)/$', EShopView.newest_items),
    url(r'^sklep/popularne/$', EShopView.popular_items),
    url(r'^sklep/wyprzedaz/$', EShopView.onsale_products),
    url(r'^sklep/wyprzedaz/(?P<page>\d+)/$', EShopView.onsale_products),
    url(r'^sklep/porownaj/$', EShopView.compare_items),
    url(r'^sklep/kategorie/(?P<id>.+)/$', EShopView.category),
    url(r'^sklep/kategorie/(?P<id>.+)/(?P<page>\d+)/$', EShopView.category),
    url(r'^sklep/szukaj/$', EShopView.search_item),  
    url(r'^sklep/(?P<id>\d+)/$', EShopView.show_item),
    url(r'^sklep/(?P<id>\d+)/komentuj/$', EShopView.comment),
    url(r'^sklep/(?P<id>\d+)/obserwuj/$', EShopView.add_to_watchlist),
    url(r'^sklep/(?P<id>\d+)/porownaj/$', EShopView.add_to_compare),
    url(r'^sklep/(?P<id>\d+)/dodaj/$', EShopView.add_to_cart),
    url(r'^sklep/(?P<id>\d+)/get_pdf/$', EShopView.get_item_pdf),
    url(r'^sklep/.+/szukaj/$', EShopView.search_item), 
    
    # url dla GroupBuy
    url(r'^grupowe/nowe/$', GroupBuyView.newest_items),
    url(r'^grupowe/nowe/(?P<page>\d+)/$', GroupBuyView.newest_items),
    url(r'^grupowe/popularne/$', GroupBuyView.popular_items),
    url(r'^grupowe/kategorie/(?P<id>.+)/$', GroupBuyView.category),
    url(r'^grupowe/kategorie/(?P<id>.+)/(?P<page>\d+)/$', GroupBuyView.category),
    url(r'^grupowe/szukaj/(?P<term>.+)/$', GroupBuyView.search_item),  
    url(r'^grupowe/(?P<id>\d+)/$', GroupBuyView.show_item),
    url(r'^grupowe/(?P<id>\d+)/dodaj/$', GroupBuyView.add_to_cart),
    url(r'^grupowe/(?P<offer_id>\d+)/kupujacy/$', GroupBuyView.buyers_list),
    url(r'^grupowe/(?P<id>\d+)/get_pdf/$', GroupBuyView.get_item_pdf),
    url(r'^grupowe/.+/szukaj/$', GroupBuyView.search_item),  
    url(r'^grupowe/porownaj/$', GroupBuyView.compare_items),
    url(r'^grupowe/(?P<id>\d+)/porownaj/$', GroupBuyView.add_to_compare),
    
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
    url(r'^koszyk/przelicz/$', CustomerPanel.update_cart),
    url(r'^kasa/$', CustomerPanel.checkout),
    url(r'^accounts/login/$','django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),#BackendPanel.logout),    
    url(r'^accounts/profile/$', CustomerPanel.show_panel),
    url(r'^rejestracja/$', CustomerPanel.register),
    url(r'^zamowienia/$', CustomerPanel.order_history),
    url(r'^zamowienia/(?P<order_id>\d+)/$', CustomerPanel.order_details),
    url(r'^aukcje_historia/$', CustomerPanel.auction_history),
    url(r'^obserwowane/$', CustomerPanel.watched_products),
    url(r'^aukcje/dodaj/$', CustomerPanel.add_auction),
    url(r'^panel_klienta/$', CustomerPanel.show_panel),

    # url dla backendpanel
    url(r'^manager/$', BackendPanel.main),
    url(r'^manager/sklep/$', BackendPanel.items_list),
    url(r'^manager/sklep/(?P<id>\d+)/edytuj/$', BackendPanel.edit_item),
    url(r'^manager/sklep/nowy/$', BackendPanel.add_item),
    #url(r'^manager/sklep/usun/$', BackendPanel.remove_item),
    url(r'^manager/grupowe/$', BackendPanel.group_list),
    url(r'^manager/grupowe/(?P<id>\d+)/edytuj/$', BackendPanel.edit_group),
    url(r'^manager/grupowe/nowy/$', BackendPanel.add_group),
    #url(r'^manager/grupowe/usun/$', BackendPanel.remove_group),
    #url(r'^manager/aukcje/$', BackendPanel.auctions_list),
    #url(r'^manager/aukcje/usun/$', BackendPanel.remove_auction),
    url(r'^manager/kategorie/$', BackendPanel.category_list),
    url(r'^manager/kategorie/(?P<id>\d+)/edytuj/$', BackendPanel.edit_category),
    url(r'^manager/kategorie/nowy/$', BackendPanel.add_category),
    #url(r'^manager/kategorie/usun/$', BackendPanel.remove_category),
    #url(r'^manager/zamowienia/$', BackendPanel.orders_list),
    #url(r'^manager/zamowienia/usun$', BackendPanel.remove_order),
    #url(r'^manager/wysylka/$', BackendPanel.shipmentmethod_list),
    #url(r'^manager/wysylka/nowy/$', BackendPanel.add_shipmentmethod),
    #url(r'^manager/wysylka/usun/$', BackendPanel.remove_shipmentmethod),

    url(r'^.+/szukaj/$', EShopView.search_item),
 
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