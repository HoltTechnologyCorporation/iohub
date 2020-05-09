from django.urls import path

from board import views

app_name = 'board'
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('api/public/ping', views.api_ping, name='api_ping'),
    path('session/<slug:session_id>', views.session_page, name='session_page'),
]
