from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.Homeview.as_view(),name="home"),
    path("register/", views.RegistrationView.as_view(),name="register"),
    path("login/", views.LoginView.as_view(),name="login"),
    path("logout/", views.LogoutView.as_view(),name="logout"),
    path("productlist/", views.ProductListView.as_view(),name="product_list"),
    path("productview/<int:pk>/",views.ProductDetailView.as_view(),name="product_detail"),
    path("category/<slug:slug>/",views.CategoryView.as_view(),name="categoryview"),
    path("productadd/", views.ProductAddView.as_view(),name="product_add"),
    path("productedit/<int:pk>/", views.ProductEditView.as_view(),name="product_edit"),
    path("productdelete/<int:pk>/", views.ProductDeleteView.as_view(),name="product_delete"),
    path("cartAdd/<int:pk>/", views.CartAddView.as_view(),name="cart_add"),
    path("cart/", views.CartView.as_view(),name="cart"),
    path("cartupdate/<int:pk>/",views.CartUpdateView.as_view(),name="cart_update"),
    path("cartremove/<int:pk>/",views.CartRemoveView.as_view(),name="cart_remove"),
    path("cartclear/",views.CartClearView.as_view(),name="cart_clear"),
    path("checkout/",views.CheckOutView.as_view(),name="checkout"),
    path("orderhistory/",views.OrderHistoryView.as_view(),name="order_history"),
    path("orderdetail/<int:pk>/",views.OrderDetailView.as_view(),name="order_detail"),
    path("ordersuccess/<int:pk>/",views.OrderSuccessView.as_view(),name="order_success"),
    path("adminconfirmation/",views.EmailConfirmationView.as_view(),name="admin_confirm"),




]
