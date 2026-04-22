from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registro/', views.registrar_usuario, name='registro'),
    path('', views.dashboard, name='dashboard'),
    path('empresas/', views.lista_empresas, name='lista_empresas'),
    path('empresas/nova/', views.criar_empresa, name='criar_empresa'),
    path('empresas/<int:id>/editar/', views.editar_empresa, name='editar_empresa'),
    path('empresas/<int:id>/excluir/', views.excluir_empresa, name='excluir_empresa'),
    path('funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),
    path('funcionarios/novo/', views.criar_funcionario, name='criar_funcionario'),
    path('funcionarios/<int:id>/editar/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionarios/<int:id>/excluir/', views.excluir_funcionario, name='excluir_funcionario'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]