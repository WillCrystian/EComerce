from django.db import models
from django.contrib.auth.models import User
from utils.valida_cpf import validar_cpf
import re
from django.forms import ValidationError


class PerfilUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name= 'usuário')
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField
    cpf =models.CharField(max_length= 11)
    endereco = models.CharField(max_length= 50, verbose_name= 'endereço')
    numero =models.CharField(max_length= 5, verbose_name='número')
    complemento = models.CharField(max_length= 30)
    bairro =models.CharField(max_length= 30)
    cep = models.CharField(max_length= 8)
    cidade = models.CharField(max_length= 30)
    estado = models.CharField(
        max_length= 2,
        default= 'SP',
        choices= (
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
            
        )
    )
    
    def __str__(self) -> str:
        return f'{self.usuario}'
    
    
    # Adicionando mensagens de erros nos formulários
    def clean(self) -> None:
        erros_messages= {}
        
        if not validar_cpf(self.cpf):
            erros_messages['cpf'] = 'CPF inválido'
            
        if re.search(r'[^0-9]', self.cep):
            erros_messages['cep'] = 'Digite apenas números'
        
        if len(self.cep) < 8:
            erros_messages['cep'] = 'CEP precisa ter 8 digitos.'
            
        if erros_messages:
            raise ValidationError(erros_messages)
    
    class Meta:
        verbose_name_plural = 'Perfis'