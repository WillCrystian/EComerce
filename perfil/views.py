from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View
from .forms import PerfilForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import PerfilUsuario
import copy


class BasePerfil(View):
    template_name = 'criar.html'
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.perfil = None
        
        if self.request.user.is_authenticated:
            self.perfil = User.objects.get(username= self.request.user)
            
            contexto = {
                'perfilform': PerfilForm(data= self.request.POST or None,
                                        instance= self.perfil),
                
                'userform': UserForm(data= self.request.POST or None,
                                     usuario= self.request.user,
                    #  mostra as informações do usuário no formulario
                                     instance= self.request.user),                
            }
        else:
            contexto = {
                'perfilform': PerfilForm(data= self.request.POST or None),
                'userform': UserForm(data= self.request.POST or None)
            }           
        
        self.perfilform = contexto['perfilform']
        self.userform = contexto['userform']
        
        self.renderizar = render(self.request, self.template_name, contexto)
        
    
    def get(self, *args, **kwargs):

        return self.renderizar       


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.perfilform.is_valid() or not self.userform.is_valid():
            return self.renderizar
        
        # dados do USERFORM
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        usuario = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
       
        # dados do PERFILFORM
        idade = self.perfilform.cleaned_data.get('idade')
        cpf = self.perfilform.cleaned_data.get('cpf')
        endereco = self.perfilform.cleaned_data.get('endereco')
        numero = self.perfilform.cleaned_data.get('numero')
        complemento = self.perfilform.cleaned_data.get('complemento')
        bairro = self.perfilform.cleaned_data.get('bairro')
        cep = self.perfilform.cleaned_data.get('cep')
        cidade = self.perfilform.cleaned_data.get('cidade')
        estado = self.perfilform.cleaned_data.get('estado')
        
        
        # Atualizar dados do usuário
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username= self.request.user.username)
            usuario.first_name = first_name
            usuario.last_name = last_name
            
            if password:
                usuario.set_password(password)
                
            usuario.save()
            
            # incluindo o usuario no FORM
            self.perfilform.cleaned_data['usuario'] = usuario
            # obtendo os dados do perfil
            perfil = PerfilUsuario(**self.perfilform.cleaned_data)
            perfil.save()            
            
            messages.success(self.request, 'Dados atualizados com sucesso.')
            
        # Criar usuário
        else:
            usuario = self.userform.save(commit=False)
            usuario.password = password 
            usuario.save()
            
            perfil = self.perfilform.save(commit= False)
            # obtendo os dados do user e passando para PK
            perfil.usuario = usuario
            perfil.save()
            
            messages.success(self.request, 'Usuário cadastrado com sucesso.')
            
        # mudando a senha e logando  
        if password:
            autentica = authenticate(self.request, username= usuario, password=password)
            if autentica:
                login(self.request, user=usuario)
                
        # copiando o carrinho e salvando novamente 
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        
        return redirect('perfil:criar')

class Atualizar(View):
    pass


class Login(View):
    def post(self, *args, **kwargs):
        usuario = self.request.POST.get('usuario')
        senha = self.request.POST.get('senha')

        usuario = authenticate(self.request, username=usuario, password= senha)
           
        if not usuario:
            messages.error(self.request, 'Usuário ou senha invalido.')
            return redirect('perfil:criar')
        
        
        login(self.request, user= usuario)
        
        messages.success(self.request, 'Login realizado com sucesso.')
        return redirect('produto:lista')
        
       

class Logout(View):
    def get(self, *args, **kwargs):
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho'))
        
        logout(self.request)
        
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        
        return redirect('produto:lista')
     