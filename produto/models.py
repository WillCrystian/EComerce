from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify

class Produto(models.Model):    
    
    nome = models.CharField(max_length= 255)
    descricao_curta = models.TextField(max_length= 255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to= 'produto_imagens/%Y/%m')
    slug =models.SlugField(unique= True, blank= True, null= True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default= 0)
    tipo = models.CharField(default= 'V',
                            max_length= 1,
                            choices= (('V', 'Variável'),
                                      ('S', 'Simples'),
                                           )
                            )
    
    
    def __str__(self) -> str:
        return self.nome
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}-{self.pk}'
            self.slug = slug
            
        super().save(*args, **kwargs)
    
        self.resize_image(self.imagem.name, 800)
        
    
    @staticmethod
    def resize_image(path_image, new_width= 800):
        image_path = os.path.join(settings.MEDIA_ROOT, path_image)        
        img = Image.open(image_path)
        width, heigth = img.size
        
        if width <= new_width:
            img.close()
            return
        
        new_heigth = round((new_width * heigth) / width)
        new_img = img.resize((new_width, new_heigth), Image.LANCZOS)
        new_img.save(image_path,
                     optimize= True,
                     quality = 60,)
        img.close()
        

class Variacao(models.Model):
    nome = models.CharField(max_length= 255)   
    produto = models.ForeignKey(Produto, on_delete= models.CASCADE)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)
    
    def __str__(self) -> str:
        return self.nome or self.produto
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Varições'

    
