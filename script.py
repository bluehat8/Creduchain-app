import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.home.models import Credential

def read_credentials():
    credentials = Credential.objects.all()


    for credential in credentials:
        print('gelk')
        print(f'Hash: {credential.credential_hash}, Transaction hash: {credential.transaction_hash}, '
              f'ID: {credential.student_id}, Programa: {credential.program}, '
              f'Fecha de Graduación: {credential.graduation_date}, '
              f'Tipo: {credential.credential_type}, Emitido el: {credential.issued_at}')
        
def delete_credentials():
    # Eliminar todos los registros de Credential
    deleted_count, _ = Credential.objects.all().delete()
    print(f'Se han eliminado {deleted_count} registros de Credential.')

if __name__ == "__main__":
    read_credentials()
    delete_credentials()