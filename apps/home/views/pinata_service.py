import datetime
import json
import os
from django.http import JsonResponse
import requests
from dotenv import load_dotenv

load_dotenv()


PINATA_API_KEY = os.environ.get("PINATA_API_KEY")  
PINATA_SECRET_API_KEY = os.environ.get("PINATA_SECRET_API_KEY")
PINATA_JWT = os.environ.get("PINATA_JWT")



def upload_json_to_pinata(data):
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PINATA_JWT}"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()  # Devuelve el hash de IPFS
    else:
        # Manejo de errores
        raise Exception(f"Error al subir a Pinata: {response.text}")
    

def upload_to_pinata(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        name = data.get('credential', {}).get('credentialSubject', {}).get('name')
        student_id = data.get('credential', {}).get('credentialSubject', {}).get('id').split(':')[-1] 
        program = data.get('credential', {}).get('credentialSubject', {}).get('program')
        graduation_date = data.get('credential', {}).get('credentialSubject', {}).get('graduationDate')
        credential_type = data.get('credential', {}).get('credentialSubject', {}).get('credentialType')

        # Construir el objeto de credencial W3C
        credential_data = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "type": ["VerifiableCredential", credential_type],
            "issuer": f"did:ethr:{data.get('issuerAddress')}", 
            "issuanceDate": datetime.datetime.now().isoformat(),
            "credentialSubject": {
                "id": f"did:example:student:{student_id}",
                "name": name,
                "program": program,
                "graduationDate": graduation_date,
                "credentialType": credential_type
            }
        }

        try:
            # Subir a Pinata y obtener el hash
            ipfs_hash = upload_json_to_pinata(credential_data)
            return JsonResponse({'status': 'success', 'ipfs_hash': ipfs_hash})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

