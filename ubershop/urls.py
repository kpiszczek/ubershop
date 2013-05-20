from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from eshop.views import EShopView
from board.views import BoardView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ubershop.views.home', name='home'),
    # url(r'^ubershop/', include('ubershop.foo.urls')),
    
    url(r'^home/$','core.views.home_page'),
    
    # url dla Auction
    # TODO
    
    # url dla EShop
    url(r'^eshop/nowe/$', EShopView.newest_items),
    url(r'^eshop/popularne/$', EShopView.popular_items),
    url(r'^eshop/(?P<id>\d+)/$', EShopView.show_item),
    url(r'^eshop/(?P<id>\d+)/get_pdf', EShopView.get_item_pdf),
    url(r'^eshop/kategorie/(?P<category>.+)/$', EShopView.items_list),
    url(r'^eshop/szukaj/(?P<term>.+)/$', EShopView.search_item),  
    
    # url dla GroupBuy
    # TODO
    
    # url dla forum
    url(r'^forum/$', BoardView.show_available_board),
    url(r'^forum/nowe_forum/$', BoardView.create_board),
    url(r'^forum/(?P<board_id>\d+)/$', BoardView.show_board),
    url(r'^forum/(?P<board_id>\d+)/nowy_temat/$', BoardView.create_topic),
    url(r'^forum/(?P<board_id>\d+)/(?P<topic_id>\d+)/$', BoardView.show_topic),
    url(r'^forum/(?P<board_id>\d+)/(?P<topic_id>\d+)/nowy_post/$', BoardView.create_message),
    url(r'^forum/(?P<board_id>\d+)/(?P<topic_id>\d+)/(?P<message_id>\d+)/$', BoardView.show_message),  
    
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
