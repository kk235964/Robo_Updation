from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('alumni/', views.alumni, name='alumni'),
    path('faculty/', views.faculty, name='faculty'),
    path('gallery/', views.gallery, name='gallery'),
    path('avishkar/', views.avishkar, name='avishkar'),
    path('prosang/', views.prosang, name='prosang'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('achievement/', views.achievement, name='achievement'),
    path('permission/', views.permission, name='permission'),
    path('team/', views.team, name='team'),
    path('coordinator/', views.coordinator, name='coordinator'),
    path('sponsor/', views.sponsor, name='sponsor'),
    path('web/', views.web, name='web'),
    path('collaborate/', views.collaborate, name='collaborate'),
    path('spinoff/', views.spinoff, name='spinoff'),
    path('error/', views.error, name='error'),
    path('contact_form/',views.contact,name='contact_form'),
    # path('themes/', views.themes, name='themes'),

]