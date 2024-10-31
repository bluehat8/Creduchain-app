# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
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
