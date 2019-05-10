from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.index,
        name='index'
    ),
    path(
        'jumpers',
        views.jumpers,
        name='jumpers'
    ),
    path(
        'jumps/<int:jumper_id>',
        views.jumps,
        name='jumps'
    ),
]
