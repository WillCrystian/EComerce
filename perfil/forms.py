from logging.config import valid_ident
from urllib import request
from xml.etree.ElementTree import fromstringlist
from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.PerfilUsuario
        fields = '__all__'
        exclude = ('usuario',)


###################################################################################################################

class UserForm(forms.ModelForm):
    first_name = forms.CharField(required= True,
                                 label= 'Primeiro Nome',
                               )
    
    last_name = forms.CharField(required= True,
                                 label= 'Último Nome',
                               )
    
    # modificando o campo password do formulário
    password = forms.CharField(required= False,
                               widget= forms.PasswordInput(),
                               label= 'Senha'
                               )
    
    # criando um campo a mais no forms
    password2 = forms.CharField(required= False,
                               widget= forms.PasswordInput(),
                               label= 'Repetir Senha'
                               )
    
    def __init__(self, usuario= None, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        
        self.usuario = usuario
        
 ##########################################################################################       
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password', 'password2', 'email')
        
 ##########################################################################################       
      
    def clean(self, *args, **kwargs):
        # recebe dados do formulário
        data = self.data
        # recebe dados do formulário
        cleaned = self.cleaned_data
        validation_error_msgs = {}
        
        
        usuario_data = cleaned.get('username').strip()
        password_data = cleaned.get('password').strip()
        password2_data = cleaned.get('password2').strip()
        email_data = cleaned.get('email').strip()
        
        usuario_db = User.objects.filter(username= usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()
        
                
        # Usuário logado: atualização
        if self.usuario:            
            usuario_logado = User.objects.get(username= self.usuario.username)
            
            if usuario_data != usuario_logado.username:
                validation_error_msgs['username'] = 'Usuário inválido.' 
            
            if email_data != usuario_logado.email:
                    validation_error_msgs['email'] = 'E-mail inválido.'
                    
            if password_data: 
                if password_data != password2_data:
                    validation_error_msgs['password'] = 'As duas senhas não conferem.'
                    validation_error_msgs['password2'] = 'As duas senhas não conferem.'
        
                if len(password_data) < 6:
                    validation_error_msgs['password'] = 'Senha deve conter pelo menos 6 caracteres.'   
                    
        # Usuários não logados: cadastro
        else:
            if usuario_db:
                validation_error_msgs['username'] = 'Usuário já existe.' 
            
            if email_db:
                validation_error_msgs['email'] = 'E-mail já existe.'
            
            if not email_data:
                validation_error_msgs['email'] = 'Digite um e-mail.'
            
            if password_data != password2_data:
                validation_error_msgs['password'] = 'As duas senhas não conferem.'
                validation_error_msgs['password2'] = 'As duas senhas não conferem.'
    
            if len(password_data) < 6:
                validation_error_msgs['password'] = 'Senha deve conter pelo menos 6 caracteres.'  
        
        
        
        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))
        
        return data
        