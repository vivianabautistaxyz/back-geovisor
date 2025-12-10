from django.db import models


class Form(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class FormSection(models.Model):
    id = models.AutoField(primary_key=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.form.name + " - " + self.section.name


class TypeChoice(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)

    @classmethod
    def create_default_types(cls):
        """Crear tipos por defecto si no existen"""
        default_types = [
            {
                'name': 'Pregunta abierta',
                'description': 'Pregunta que requiere una respuesta detallada'
            },
            {
                'name': 'Selección única',
                'description': 'Solo una opción puede ser seleccionada'
            },
            {
                'name': 'Selección múltiple',
                'description': 'Varias opciones pueden ser seleccionadas'
            },
            {
                'name': 'Desplegable',
                'description': 'Selección única en formato dropdown'
            },
            {
                'name': 'Escala de valoración',
                'description': 'Ej: de 1 a 5, de “muy en desacuerdo” a “muy de acuerdo”'
            },
            {
                'name': 'Rango',
                'description': 'Slider para seleccionar un valor dentro de un rango numérico'
            },
            {
                'name': 'Número',
                'description': 'Solo acepta valores numéricos'
            },
            {
                'name': 'Fecha / Hora',
                'description': 'Calendario o selector de hora'
            },
            {
                'name': 'Sí / No',
                'description': 'Pregunta cerrada de respuesta binaria'
            },
            {
                'name': 'Binaria',
                'description': 'Pregunta cerrada de respuesta binaria'
            },
            {
                'name': 'Clasificación',
                'description': 'Ordenar elementos según preferencia'
            },
            {
                'name': 'Carga de archivo',
                'description': 'Permite subir un documento, imagen, etc.'
            },
            {
                'name': 'Ubicación',
                'description': 'Para indicar una posición geográfica'
            },
            {
                'name': 'Firma digital',
                'description': 'Campo para firmar con el dedo o mouse'
            },
            {
                'name': 'Condicional',
                'description': 'Define lógica de salto (si responde X, entonces mostrar Y)'
            }
        ]
        
        for type_data in default_types:
            cls.objects.get_or_create(
                name=type_data['name'],
                defaults=type_data
            )

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    typeChoice = models.ForeignKey(TypeChoice, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=200)
    options = models.TextField(default="")

    def save(self, *args, **kwargs):
        if self.typeChoice is None:
            self.typeChoice, _ = TypeChoice.objects.get_or_create(
                name="Pregunta Abierta",
                defaults={"description": "Pregunta abierta para respuestas de texto"},
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question

    def get_options(self):
        return self.options


class SectionQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.section.name + " - " + self.question.question_text


class Visitor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.JSONField()


class Visit(models.Model):
    id = models.AutoField(primary_key=True)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    visit_date = models.DateTimeField("date visited")
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.visit_date


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    address = models.CharField(max_length=200)
    phon1e = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
