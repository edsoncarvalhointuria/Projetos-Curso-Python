# URL - VIEW - TEMPLATE
from django.urls import path, reverse_lazy
from .views import Homepage, Homefilmes, DetalhesFilme, PesquisaFilme, EditarPerfil, CriarConta, Categorias, Categoria
from django.contrib.auth import views as auth_view

app_name="filme"

urlpatterns = [
    path('', Homepage.as_view()),
    path('filme/', Homefilmes.as_view(), name="homefilmes"),
    path('filme/<int:pk>', DetalhesFilme.as_view(), name="detalhes_filme"),
    path('pesquisa/', PesquisaFilme.as_view(), name="pesquisa_filme"),
    path("login/", auth_view.LoginView.as_view(template_name="login.html") , name="login"),
    path("logout/", auth_view.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("editarperfil/<int:pk>", EditarPerfil.as_view(), name ="editar_perfil"),
    path("criarconta/", CriarConta.as_view(), name="criar_conta" ),
    path("alterarsenha/", auth_view.PasswordChangeView.as_view(template_name="editar_perfil.html", success_url=reverse_lazy("filme:homefilmes")), name="alterarsenha"),
    path("categorias/", Categorias.as_view(), name="categorias"),
    path("categoria/<str:categoria>", Categoria.as_view(), name="categoria")
]