from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from app import views
from app.forms import loginform,passwordchangeform,passwordresetform,setpasswordform
app_name = "app"
urlpatterns = [
    path('', views.home),
    #path('buyer/',views.buyer,name='buyer'),
    path('buyers/',views.buyers.as_view(),name='buyers'),
    path('seller/',views.seller,name='seller'),
    path('product-detail/<int:pk>', views.product_detail.as_view(), name='product-detail'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    
    path('buy/', views.buy_now, name='buy-now'),
    #path('profile/', views.profile, name='profile'),
    path('profile/', views.profileview.as_view(), name='profile'),
    
    path('address/', views.addres.as_view(), name='address'),
    path('orders/', views.orders, name='orders'),
    #path('changepassword/', views.change_password, name='changepassword'),
    path('mobile/', views.mobile, name='mobile'),
    #path('login/', views.login, name='login'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=loginform),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/accounts/login/'),name='logout'),
    #path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=passwordchangeform,success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=passwordresetform,success_url='/password-reset-confirm/'),name='password_reset'),
    path('password-reset-confirm/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password-reset-confirm'),
    #path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password-reset-complete'),
    #path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=setpasswordform),name='password_reset_confirm'),
    




]
