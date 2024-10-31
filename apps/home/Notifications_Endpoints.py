from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Notification
from django.contrib.auth.decorators import login_required
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import NotificationSerializer
from django.template.loader import render_to_string


@login_required
def get_notifications(request):
    """
    Obtiene todas las notificaciones para el usuario autenticado y las ordena por timestamp de forma descendente.
    """
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    notification_data = [
        {
            "sender": notification.sender.username,
            "title": notification.title,
            "message": notification.message,
            "timestamp": notification.timestamp,
            "read": notification.read,
            "notification_type": notification.notification_type,
        }
        for notification in notifications
    ]
    return JsonResponse({"notifications": notification_data})

@login_required

def get_notifications_items_template(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')  # Ajusta según tu lógica
    notifications_html = []

    for notification in notifications:
        html = render_to_string('items/notification_item.html', {'notification': notification})
        notifications_html.append(html)

    return JsonResponse({'notifications': notifications_html})


@login_required
def mark_as_read(request, notification_id):
    """
    Marca una notificación como leída. Solo el destinatario puede marcar la notificación como leída.
    """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.read = True
    notification.save()
    return JsonResponse({"status": "success"})


# Endpoint para crear una nueva notificación de emisión o verificación de credenciales
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_notification(request):
    """
    Crea una nueva notificación.
    Se puede especificar si es una notificación de 'emisión' o 'verificación' de credenciales
    a través del campo 'tipo' que se envía en el cuerpo de la solicitud.
    """
    data = request.data

    # Validar el campo 'tipo' para asegurarse de que sea una emisión o verificación
    tipo = data.get('tipo')
    if tipo not in [Notification.EMISION, Notification.VERIFICACION]:
        return Response({"error": "Tipo de notificación no válido. Debe ser 'emisión' o 'verificación'."},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = NotificationSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save(sender=request.user)  # El remitente es el usuario autenticado
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)