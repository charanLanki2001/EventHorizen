from django.conf import settings
from django.contrib import admin
from django.urls import path
from firstapp import views
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginPage, name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('verify_password/', views.verify_otp, name='verify_otp'),
    path('signup/', views.SignupPage, name='signup'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('Events/', views.new_events, name='new_events'),
    path('create_events/', views.create_events, name='create_events'),   
    path('update_event/', views.update_event, name='update_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events_list/', views.event_view, name='event_view'),
    path('delete_event/', views.delete_event, name='delete_event'),
    path('Aboutus/', views.about_us, name='about_us'),
    path('sucess/', views.success_page, name='success_page'),

    path('registration/<int:event_id>/', views.registration_details, name='registration_details'),
    path('payment/<int:event_id>/', views.payment, name='payment'),
    path('payment_success/<int:event_id>/', views.payment_success, name='payment_success'),

   path('List/', views.register_Event, name='register_Events'),
   path('Registered_List/', views.Registered_List, name='Registered_List'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)