from django.db import models
from django.utils import timezone
from enum import Enum
from PIL import Image
from io import BytesIO
import os
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.base import ContentFile
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html
from django.conf import settings
from django.conf.urls.static import static
import datetime
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django import forms
# Create your models here.

class AllatFaj(models.TextChoices):
    kutya = "kutya", _("kutya")
    cica = "cica", _("cica")
    egyeb = "egyeb", _("egyéb")

class AllatMeret(models.TextChoices):
    kicsi = "kicsi", _("kistestű")
    kozepes = "kozepes", _("közepes testű")
    nagy = "nagy", _("nagytestű")

class Ivar(models.TextChoices):
    fiu = "fiu", _("fiú")
    lany = "lany", _("lány")

class Allat(models.Model):
    
    faj = models.CharField(max_length=200, choices=AllatFaj.choices, default=_("kutya"), verbose_name = _("kutya/cica"))
    meret = models.CharField(max_length=200, choices=AllatMeret.choices, default=_("kicsi"), verbose_name = _("méret"))
    ivar = models.CharField(max_length=200, choices=Ivar.choices, default=_("fiu"), verbose_name = _("ivar"))
    nev = models.CharField(max_length=200, verbose_name = "név")
    szuletesiideje = models.DateField()
    ivartalanitva = models.BooleanField()
    leiras = models.TextField(default="Leírás később érkezik. Amennyiben a képek alapján érdeklődnél, keress facebook messengeren vagy telefonon.")
    eletkor = models.IntegerField(blank=True, null=True, editable=False)
    orokbeadva = models.BooleanField(default = False)

    def __str__(self):
        return self.nev

    def save(self, *args, **kwargs):
        self.eletkor = int(((datetime.date.today()  - self.szuletesiideje).days)/365.25)
        print(self.eletkor)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Állat'
        verbose_name_plural = 'Állatok'

class AllatMainImage(models.Model):
    allat = models.ForeignKey(Allat, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='app_menhely/img/photos/', verbose_name = _("kiemelt kép"))
    photo_tumb = models.ImageField(upload_to='app_menhely/img/thumbs/', editable=False)

    def save(self, *args, **kwargs):
        if not self.photo.closed:
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(AllatMainImage, self).save(*args, **kwargs)


    def make_thumbnail(self):

        image = Image.open(self.photo)
        image.thumbnail((1000,1000), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.photo_tumb.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    class Meta:
        verbose_name = 'Kiemelt kép'
        verbose_name_plural = 'Kiemelt kép'

class AllatImage(models.Model):
    allat = models.ForeignKey(Allat, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='app_menhely/img/photos/', verbose_name = _("galéria kép"))
    photo_tumb = models.ImageField(upload_to='app_menhely/img/thumbs/', editable=False)
    
    def save(self, *args, **kwargs):
        if not self.photo.closed:
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(AllatImage, self).save(*args, **kwargs)


    def make_thumbnail(self):

        image = Image.open(self.photo)
        image.thumbnail((1000,1000), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.photo_tumb.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True            
 
    class Meta:
        verbose_name = 'Galéria kép'
        verbose_name_plural = 'Galéria képek'

        
class Hirek(TranslatableModel):
    translations = TranslatedFields(cim=models.CharField(max_length=200),
    tartalom=models.TextField())
    hir_main_img = models.ImageField(upload_to='app_menhely/img/photos', default= '/app_menhely/hiralap.jpg')
    hir_main_img_tumb = models.ImageField(upload_to='app_menhely/img/thumbs/', editable=False, default="/app_menhely/hiralap.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.hir_main_img.closed:
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(Hirek, self).save(*args, **kwargs)


    def make_thumbnail(self):

        image = Image.open(self.hir_main_img)
        image.thumbnail((1000,1000), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.hir_main_img.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.hir_main_img_tumb.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def __str__(self):
        return self.cim
    
    class Meta:
        verbose_name = "Hír"
        verbose_name_plural = "Hírek"


class Bemutatkozas(TranslatableModel):
    translations=TranslatedFields(cim = models.CharField(max_length=200),
    tartalom = models.TextField(),)
    bemutatkozas_main_img = models.ImageField(upload_to='app_menhely/img/photos')
    priority = models.IntegerField(default=5, validators=[MaxValueValidator(100), MinValueValidator(1)] )

    def save(self, *args, **kwargs):
        if not self.bemutatkozas_main_img.closed:
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(Bemutatkozas, self).save(*args, **kwargs)


    def make_thumbnail(self):

        image = Image.open(self.bemutatkozas_main_img)
        image.thumbnail((1000,1000), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.bemutatkozas_main_img.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE, quality=50, subsampling=3)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.bemutatkozas_main_img.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True
        
    def __str__(self):
        return self.cim
        
    class Meta:
        verbose_name = "Bemutatkozó szöveg"
        verbose_name_plural = "Bemutatkozó szöveg"

class Kapcsolat(TranslatableModel):
    translations=TranslatedFields(telefonszam = models.CharField(max_length=50),
    nyitvatartashp=models.CharField(max_length=50),
    nyitvatartassz=models.CharField(max_length=50),
    nyitvatartasv=models.CharField(max_length=50),
    emailcim=models.CharField(max_length=50, default=""),
    telephely=models.CharField(max_length=50, default=""),
    )
    

    class Meta:
        verbose_name = "Kapcsolat"
        verbose_name_plural = "Kapcsolat"

class Kimutatasok(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField()

    class Meta:
        verbose_name = "Kimutatás"
        verbose_name_plural = "Kimutatások"
        
    