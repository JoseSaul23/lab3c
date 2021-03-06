from datetime import date
from urllib.parse import urlparse, parse_qs
from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.validators import MaxLengthValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

""" Only delete the file if no other instances of that model are using it"""    
def delete_file_if_unused(model, instance, field, instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)

""" Whenever ANY model is deleted, if it has a file field on it, delete the associated file too"""
@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            instance_file_field = getattr(instance,field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)

""" Delete the file if something else get uploaded in its place"""
@receiver(pre_save)
def delete_files_when_file_changed(sender,instance, **kwargs):
    # Don't run on initial save
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            #its got a file field. Let's see if it changed
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                # Don't worry about deleting attachments if they aren't actually saved yet.
                return
            instance_in_db_file_field = getattr(instance_in_db, field.name)
            instance_file_field = getattr(instance, field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender, instance, field, instance_in_db_file_field)

""" Gets the id from url of video """
def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre de la categor??a")

    class Meta:
        db_table = 'Categoria'
        verbose_name = 'Categoria de propuestas'
        verbose_name_plural = 'Categorias de propuestas'
    
    def __str__(self):
        return self.name

    @property
    def count(self):
        return Proposal.objects.filter(category=self, approved=True).count()

class Locality(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre de la localidad")
    
    class Meta:
        db_table = 'Localidad'
        verbose_name = 'Localidad de propuestas'
        verbose_name_plural = 'Localidades de propuestas'
    
    def __str__(self):
        return self.name
    
    @property
    def count(self):
        return Proposal.objects.filter(locality=self, approved=True).count()

class Proposal(models.Model):
    group_name = models.CharField(max_length=200, verbose_name="Nombre de la organizaci??n/grupo")
    contact_name = models.CharField(max_length=200, verbose_name="Persona de contacto")
    contact_charge = models.CharField(max_length=200, verbose_name="Cargo o posici??n de la persona de contacto")
    email = models.EmailField(verbose_name="Correo electr??nico")
    contact_number = models.PositiveIntegerField(verbose_name="N??mero de contacto")
    name = models.CharField(max_length=200, verbose_name="Nombre de la iniciativa")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='proposals', verbose_name="Categor??a en que incide")
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, related_name='proposals', verbose_name="Localidad de ubicaci??n de la propuesta")
    impact_sector = models.CharField(max_length=200, null=True, blank=True, verbose_name="Barrio o sector impactado por la propuesta")
    objective = models.TextField(max_length=200, verbose_name="Objetivo de la iniciativa", validators=[MaxLengthValidator(200)])
    problematic = models.TextField(max_length=500, verbose_name="Descripci??n de la problem??tica que se identific??", validators=[MaxLengthValidator(500)])
    description = models.TextField(max_length=1000, verbose_name="Descripci??n breve de la iniciativa", validators=[MaxLengthValidator(1000)])
    justification = models.TextField(max_length=1000, verbose_name="Justificaci??n de la iniciativa", validators=[MaxLengthValidator(1000)])
    estimated_value = models.PositiveIntegerField(verbose_name="Indique el valor estimado de su iniciativa")
    pdf = models.FileField(upload_to='pdf/iniciativas', verbose_name="Adjunte aqu?? su propuesta en PDF", validators=[FileExtensionValidator( ['pdf'] )])
    annex = models.FileField(upload_to='pdf/anexos_iniciativas', verbose_name="Adjunte aqu?? los anexos requeridos en un solo archivo",  validators=[FileExtensionValidator( ['pdf'] )])
    url_video = models.URLField(max_length=400, verbose_name="Pegue aqu?? la URL en Youtube con el video resumen de su propuesta")
    approved = models.BooleanField(default=False, verbose_name="??Aprobado?")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creaci??n")
    terms_service = models.CharField(max_length=2, verbose_name="Acepta los t??rminos de la pol??tica de tratamiento de datos personales")

    @property
    def video_id(self):
        return video_id(self.url_video)

    class Meta:
        db_table = 'Propuesta'
        verbose_name = 'Propuesta'
        verbose_name_plural = 'Propuestas'
        ordering = ('-created', 'approved')

    def __str__(self):
        return self.name

class Phase(models.Model):
    title = models.CharField(max_length=200, verbose_name="T??tulo")
    description = models.TextField(max_length=1000, verbose_name="Descripci??n", validators=[MaxLengthValidator(1000)])
    number = models.PositiveIntegerField(verbose_name="Orden de la fase")
    pdf = models.FileField(upload_to='pdf/fases', verbose_name="Archivo PDF", validators=[FileExtensionValidator( ['pdf'] )])
    url_video = models.URLField(max_length=400, verbose_name="URL en Youtube")

    @property
    def video_id(self):
        return video_id(self.url_video)

    class Meta:
        db_table = 'Fase'
        verbose_name = 'Fase'
        verbose_name_plural = 'Fases'
        ordering = ('number',)

    def __str__(self):
        return self.title

class Inscription(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre de la convocatoria")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creaci??n")
    begins = models.DateField(verbose_name="Fecha de inicio")
    ends = models.DateField(verbose_name="Fecha final")
    pdf = models.FileField(upload_to='pdf/convocatorias', validators=[FileExtensionValidator( ['pdf'] )])

    @property
    def state(self):
        if self.ends:
            if date.today() > self.ends:
                return 'Cerrada'
            else: 
                return 'Abierta'
        else:
            return '-'
    state.fget.short_description = 'Estado actual'

    class Meta:
        db_table = 'Convocatoria'
        verbose_name = 'Convocatoria'
        verbose_name_plural = 'Convocatorias'
        ordering = ('-created',)

    def __str__(self):
        return self.name

class KeyConcepts(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del concepto")
    description = models.TextField(max_length=400, verbose_name="Descripci??n del concepto", validators=[MaxLengthValidator(400)])
    pdf = models.FileField(upload_to='pdf/conceptos', validators=[FileExtensionValidator( ['pdf'] )])
        
    class Meta:
        db_table = 'Concepto'
        verbose_name = 'Concepto'
        verbose_name_plural = 'Conceptos'
        ordering = ('-name',)

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de la herramienta")
    description = models.TextField(max_length=400, verbose_name="Descripci??n de la herramienta", validators=[MaxLengthValidator(400)])
    pdf = models.FileField(upload_to='pdf/herramientas', validators=[FileExtensionValidator( ['pdf'] )])
        
    class Meta:
        db_table = 'Herramienta'
        verbose_name = 'Herramienta'
        verbose_name_plural = 'Herramientas'
        ordering = ('-name',)

    def __str__(self):
        return self.name

class Testimony(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creaci??n")
    url_video = models.URLField(max_length=400, verbose_name="URL en Youtube con el video testimomio")

    @property
    def video_id(self):
        return video_id(self.url_video)

    class Meta:
        db_table = 'Testimonio'
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'
        ordering = ('-created',)

    def __str__(self):
        return self.name

class Partner(models.Model):
    name =  models.CharField(max_length=100, verbose_name="Nombre")
    image = models.ImageField(upload_to='images', verbose_name="Imagen")
    number = models.PositiveIntegerField(verbose_name="Orden de la alianza")

    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = 'Alianza'
        verbose_name = 'Alianza'
        verbose_name_plural = 'Alianzas'
        ordering = ('number',)

class Contact(models.Model):
    name =  models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo electr??nico")
    issue =  models.CharField(max_length=100, verbose_name="Asunto")
    message = models.TextField(max_length=500, verbose_name="Mensaje", validators=[MaxLengthValidator(500)])
    view = models.BooleanField(default=False, verbose_name="??Visto?")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Enviado")

    def __str__(self):
        return str(self.issue)
    
    class Meta:
        db_table = 'Mensaje'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ('-created',)

class SocialMedia(models.Model):
    name =  models.CharField(max_length=100, verbose_name="Nombre")
    url = models.URLField(max_length=400, verbose_name="URL")
    number = models.PositiveIntegerField(verbose_name="Orden de la red social")

    @property
    def domain(self):
        return 'https://' + urlparse(self.url).hostname + '/favicon.ico'

    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = 'SocialMedia'
        verbose_name = 'Red social'
        verbose_name_plural = 'Redes sociales'
        ordering = ('number',)

class Settings(models.Model):
    logo = models.ImageField(upload_to='images', verbose_name="Logo en men??")
    title_intro =  models.CharField(max_length=200, verbose_name="T??tulo introductorio")
    introduction = models.TextField(max_length=1000, verbose_name="Texto introductorio")
    intro_image = models.ImageField(upload_to='images', verbose_name="Imagen introductoria (1920x1080)")
    pdf_general = models.FileField(upload_to='pdf_fases', validators=[FileExtensionValidator( ['pdf'] )], verbose_name="Unidad general")
    form_intro = models.TextField(max_length=1000, verbose_name="Introducci??n de formulario")
    data_agreement = models.TextField(max_length=1000, verbose_name="Autorizaci??n de tratamiento de datos personales")
    contact_text = models.TextField(max_length=1000, verbose_name="Texto de contacto")
    contact_address = models.TextField(max_length=100, verbose_name="Direcci??n contacto")
    contact_phone = models.CharField(max_length=100, verbose_name="Telefono contacto")

    def __str__(self):
        return 'Preferencias p??gina principal'
    
    class Meta:
        db_table = 'Configuracion'
        verbose_name = 'Configuraci??n'
        verbose_name_plural = 'Configuraciones'