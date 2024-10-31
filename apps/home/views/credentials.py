import json
import os
from django.shortcuts import redirect, render
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.home.models import Credential

load_dotenv()

with open("apps/contracts/artifacts/CredentialRegistry_metadata.json") as f: 
    info_json = json.load(f)

with open("apps/contracts/contract_abi.json") as f: 
    abi_json = json.load(f)

CONTRACT_ABI = abi_json
CONTRACT_ADDRESS = os.environ.get("CONTRACT_ADDRESS")  

@login_required
def credentials_management(request):
    if CONTRACT_ABI is None or CONTRACT_ADDRESS is None:
        raise RuntimeError("Smart contract ABI or address not set")
    
    if request.method == 'POST':
        return handle_post_request(request)

    credentials = Credential.objects.all()
    contract_abi_json = json.dumps(abi_json)
    return render(request, 'home/emit-credentials.html', {
        'credentials': credentials,
        'contract_abi': contract_abi_json,
        'contract_address': CONTRACT_ADDRESS,
    })

def handle_post_request(request):

    # Parsear el JSON en el cuerpo de la solicitud
    data = json.loads(request.body)
    student_name = data.get('name')
    credential_hash = data.get('credentialHash')
    student_id = data.get('studentId')
    program = data.get('program')
    graduation_date = data.get('graduationDate')
    credential_type = int(data.get('credentialType'))
    issuer_address = data.get('issuerAddress')
    transactionHash = data.get('transactionHash')

    # Crea la instancia de Credential, incluyendo credential_type
    credential = Credential.objects.create(
        credential_hash=credential_hash,
        student_name=student_name,
        student_id=student_id,
        program=program,
        graduation_date=graduation_date,
        issuer=request.user, 
        issuer_address=issuer_address,
        credential_type=credential_type,
        transaction_hash= transactionHash  
    )

    credential.save()

    return JsonResponse({'status': 'success', 'redirect': ''})
