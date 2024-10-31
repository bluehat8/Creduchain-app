from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Notification
from django.contrib.auth.decorators import login_required

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
            "notification_type": notification.get_notification_type_display(),
        }
        for notification in notifications
    ]
    return JsonResponse({"notifications": notification_data})


@login_required
def mark_as_read(request, notification_id):
    """
    Marca una notificación como leída. Solo el destinatario puede marcar la notificación como leída.
    """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.read = True
    notification.save()
    return JsonResponse({"status": "success"})

