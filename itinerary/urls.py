from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('plan/', views.index, name='index'),
    path('generate/', views.generate_itinerary, name='generate_itinerary'),
    path('book-pandit/', views.book_pandit, name='book_pandit'),
    path('pandit-dashboard/', views.pandit_dashboard, name='pandit_dashboard'),
]
