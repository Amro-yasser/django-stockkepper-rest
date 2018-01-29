from django.conf.urls import url
from . import views

app_name = 'webapp'
urlpatterns = [
    url(r'products$', views.ListCreateProduct.as_view(), name='product_list'),
    url(r'products/(?P<pk>\d+)/$', views.RetrieveUpdateDestroyProduct.as_view(), name='product_detail'),
    
    url(r'purchases$', views.ListCreatePurchase.as_view(), name='purchase_list'),
    url(r'purchases/(?P<pk>\d+)/$', views.RetrieveUpdateDestroyPurchase.as_view(), name='purchase_detail'),
    url(r'purchases-for/(?P<product_pk>\d+)/$', views.RTU.as_view(), name='product_purchase_detail'),
    url(r'purchase-items/$', views.PurchaseAllItems.as_view(), name='purchase_items_detail'),
    
    url(r'purchases/(?P<purchase_pk>\d+)/items$', views.ListCreatePurchaseItem.as_view(), name='purchase_item_list'),
    url(r'purchases/(?P<purchase_pk>\d+)/items/(?P<pk>\d+)/$', views.RetrieveUpdateDestroyPurchaseItem.as_view(), name='purchase_item_detail'),
    
    url(r'requests$', views.ListCreateRequest.as_view(), name='request_list'),
    url(r'requests/(?P<pk>\d+)/$', views.RetrieveUpdateDestroyRequest.as_view(), name='request_detail'),
    
    url(r'requests/(?P<request_pk>\d+)/items$', views.ListCreateRequestItem.as_view(), name='request_item_list'),
    url(r'requests/(?P<request_pk>\d+)/items/(?P<pk>\d+)/$', views.RetrieveUpdateDestroyRequestItem.as_view(), name='request_item_detail'),

    url(r'requests/(?P<request_item_pk>\d+)/allocate$', views.ListCreateAllocatedItem.as_view(), name='allocate_list'),
    url(r'requests/(?P<request_item_pk>\d+)/allocate/(?P<pk>\d+)$', views.RetrieveUpdateDestroyAllocatedItem.as_view(), name='allocate_detail'),
    url(r'allocations-for/(?P<purchase_pk>\d+)/(?P<product_pk>\d+)$', views.getPurchaseAllocatedItem.as_view(), name='allocate_list'),
]