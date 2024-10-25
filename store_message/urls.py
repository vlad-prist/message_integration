from django.urls import path
from store_message.apps import StoreMessageConfig
from store_message import views


app_name = StoreMessageConfig.name


urlpatterns = [
    # path('', views.home, name='index'),
    path('', views.StoreListView.as_view(), name='index'),
    path('email_login/', views.email_login, name='email_login'),
    path('message_store/create/', views.StoreCreateView.as_view(), name='store_create'),
    path('message_store/view/<int:pk>', views.StoreDetailView.as_view(), name='store_view'),
    path('message_store/update/<int:pk>', views.StoreUpdateView.as_view(), name='store_update'),
    path('message_store/delete/<int:pk>', views.StoreDeleteView.as_view(), name='store_delete'),
]
