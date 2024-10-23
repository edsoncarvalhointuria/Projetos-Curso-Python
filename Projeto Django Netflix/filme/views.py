from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, FormView, UpdateView
from django.views.generic.detail import DetailView
from .models import Filme, Serie, Usuario
from .forms import FormCriarConta, FormHomepage
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# def homepage(request):
#     return render(request, "homepage.html")

# def homefilme(request):
#     context = {"filmes": Filme.objects.all()}
#     return render(request, "homefilme.html", context=context)

class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomepage

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("filme:homefilmes")
        else:
            return super().get(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        email = self.request.POST.get('email')
        usuario = Usuario.objects.filter(email=email)
        if usuario:
            return reverse("filme:login")
        else:            
            return reverse("filme:criar_conta")



class Homefilmes(LoginRequiredMixin,ListView):
    template_name = 'homefilmes.html'
    model = Filme
    


class DetalhesFilme(LoginRequiredMixin,DetailView):
    template_name = 'detalhes_filme.html'
    model = Filme

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        request.user.filmes_assistidos.add(filme)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context= super(DetalhesFilme, self).get_context_data(**kwargs)
        context["relacionados"] = Filme.objects.filter(categoria=self.get_object().categoria)[:5]
        return context
    
class PesquisaFilme(LoginRequiredMixin,ListView):
    template_name = 'pesquisa.html'
    model = Filme

    def get_queryset(self) -> QuerySet[Any]:
        pesquisa = self.request.GET.get("query")
        if pesquisa:
            object_list = self.model.objects.filter(Q(titulo__icontains=pesquisa) | Q(categoria__icontains=pesquisa))
            return object_list
        else:
            return None
    

class EditarPerfil(LoginRequiredMixin, UpdateView):
    template_name = "editar_perfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse("filme:homefilmes")


class CriarConta(FormView):
    template_name="criar_conta.html"
    form_class = FormCriarConta

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

    def get_success_url(self) -> str:
        return reverse("filme:login")
    

class Categorias(TemplateView):
    template_name = "categorias.html"


class Categoria(ListView):
    template_name = "categoria.html"
    model = Filme
    
    def get_queryset(self) -> QuerySet[Any]:
        categoria = self.kwargs['categoria']
        for filme in self.model.objects.all():
            if filme.get_categoria_display() == categoria:
                categoria = filme.categoria
                break
        return self.model.objects.filter(categoria=categoria)
