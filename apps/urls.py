from django.urls import path

from apps.views import *

urlpatterns = [
    path('', HomeViewList.as_view(), name='home'),
    path('success', SuccessView.as_view(), name='success'),
    path('order/search', SearchOrderView.as_view(), name='search-order'),
    path('cannel', CannelView.as_view(), name='cannel'),
    path('detail/<int:id>', DetailViewList.as_view(), name='detail'),
    path('buy/<int:id>', BuyItemView.as_view(), name='buy'),

]
