from django.urls import path, include
from .views import Total, Products, Comex

urlpatterns = [
    path('total/', Total.as_view()),
    path('total/<str:year>/', Total.as_view()),
    path('products/', Products.as_view()),
    path('products/<str:ncm>/', Products.as_view()),
    path('comex/', Comex.as_view()),
    path('comex/<str:movement>/', Comex.as_view()),
    path('comex/<str:movement>/<str:products>/', Comex.as_view()),
    path('comex/<str:movement>/<str:products>/<str:vias>/', Comex.as_view()),
    path('comex/<str:movement>/<str:products>/<str:vias>/<str:year>/', Comex.as_view()),
]