from django.conf.urls import url, include
from rest_framework import routers
from accounts import views

router = routers.DefaultRouter()
router.register(r'^signup', views.SignupView, basename='signup')
router.register(r'^login', views.LoginView, basename='login')
router.register(r'^change-password', views.ChangePasswordView, basename='changepassword')
router.register(r'^password-reset', views.PasswordResetView, basename='passwordreset')
router.register(r'^profile', views.UserProfile, basename='profile')
router.register(r'^profile-update', views.UserProfileUpdate, basename='profileupdate')

router.register(r'^category', views.CategoryView, basename='category')
router.register(r'^subcategory', views.SubcategoryView, basename='subcategory')
router.register(r'^service', views.ServiceView, basename='service')
router.register(r'^item', views.ItemView, basename='item')
router.register(r'^search', views.SearchItemView, basename='search')
router.register(r'^review', views.ReviewView, basename='review')
router.register(r'^logout', views.LogoutView, basename='logout')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^social-login/',views.SocialLoginView.as_view()),
    url(r'^password-reset-confirm/', views.PasswordResetConfirmView.as_view()),
 ]