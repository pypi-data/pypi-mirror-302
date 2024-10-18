from django.urls import path
from . import views

urlpatterns = [
    path("<str:channel>/rpush", views.rpush),
    path("<str:channel>/lpush", views.lpush),
    path("<str:channel>/pop", views.pop),
    path("<str:channel>/ack", views.ack),
    path("<str:channel>/ret", views.ret),
    path("<str:channel>/query", views.query),
    path("<str:channel>/cancel", views.cancel),
    # path("<str:channel>/delete", views.delete),
    # path("backup", views.backup),
]
