# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Credential(models.Model):
    id= models.AutoField(primary_key=True)
    credential_hash = models.CharField(max_length=100, unique=True)
    student_name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=50)
    program = models.CharField(max_length=255)
    graduation_date = models.DateField()
    issued_at = models.DateTimeField(auto_now_add=True)
    issuer_address = models.CharField(max_length=100, default='unknown')
    issuer = models.ForeignKey(User, on_delete=models.CASCADE)
    credential_type = models.IntegerField(default=None)
    transaction_hash = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.student_name} - {self.credential_hash}"


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)   #llave foranea de la tabla usuario de django
    recipient = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    # Tipo de notificación, se definen las constantes para usar en un campo de tipo elección en el modelo, como ChoiceField o IntegerField con choices
    EMISION = 1
    VERIFICACION = 2
    CADUCIDAD = 3
    REVOCACION = 4
    INGRESO_ESTUDIANTE = 5

    NOTIFICATION_TYPE_CHOICES = [
        (EMISION, 'Emisión'),
        (VERIFICACION, 'Verificación'),
        (CADUCIDAD, 'Caducidad'),
        (REVOCACION, 'Revocación'),
        (INGRESO_ESTUDIANTE, 'Ingreso de Estudiante')
    ]
    
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.title} - {self.recipient}"
