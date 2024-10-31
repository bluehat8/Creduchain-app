import json
import os
from datetime import datetime
from django.shortcuts import render
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.home.models import Credential, Notification
from apps.home.serializers import NotificationSerializer

load_dotenv()

# Carga de ABI y dirección del contrato
def load_contract_info():
    with open("apps/contracts/artifacts/CredentialRegistry_metadata.json") as f:
        info_json = json.load(f)
    with open("apps/contracts/contract_abi.json") as f:
        abi_json = json.load(f)
    return abi_json, os.environ.get("CONTRACT_ADDRESS")

CONTRACT_ABI, CONTRACT_ADDRESS = load_contract_info()

@login_required
def credentials_management(request):
    if not CONTRACT_ABI or not CONTRACT_ADDRESS:
        raise RuntimeError("Smart contract ABI or address not set")
    
    if request.method == 'POST':
        return handle_post_request(request)

    credentials = Credential.objects.all()
    return render(request, 'home/emit-credentials.html', {
        'credentials': credentials,
        'contract_abi': json.dumps(CONTRACT_ABI),
        'contract_address': CONTRACT_ADDRESS,
    })

def handle_post_request(request):
    data = json.loads(request.body)

    # Validar y extraer los datos del JSON
    required_fields = ['name', 
                       'credentialHash', 
                       'studentId', 
                       'program', 
                       'graduationDate', 
                       'credentialType', 
                       'issuerAddress', 
                       'transactionHash']
    
    for field in required_fields:
        if field not in data:
            return JsonResponse({'status': 'error', 'error': f'Missing field: {field}'}, status=400)

    # Crear la credencial
    credential = create_credential(data, request)

    # Crear la notificación
    if create_notification(credential, request.user):
        return JsonResponse({'status': 'success', 'redirect': ''})
    else:
        return JsonResponse({'status': 'error', 'error': 'Failed to create notification'}, status=400)

def create_credential(data, request):
    return Credential.objects.create(
        credential_hash=data['credentialHash'],
        student_name=data['name'],
        student_id=data['studentId'],
        program=data['program'],
        graduation_date=data['graduationDate'],
        issuer=request.user, 
        issuer_address=data['issuerAddress'],
        credential_type=int(data['credentialType']),
        transaction_hash=data['transactionHash']
    )

def create_notification(credential, user):
    notification_data = {
        "recipient": user.id,
        "sender": user.id,
        "title": "Credential Issued",
        "message": f"'{user.username}' issued a '{credential.program}' degree to '{credential.student_name}'.",
        "notification_type": Notification.EMISION,
    }
    
    serializer = NotificationSerializer(data=notification_data)
    if serializer.is_valid():
        serializer.save()
        return True
    return False
