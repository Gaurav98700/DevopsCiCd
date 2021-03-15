from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
import json
from azure_blob_app.constants import constant
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.storage.blob import generate_blob_sas, BlobSasPermissions, generate_account_sas, ResourceTypes, AccountSasPermissions

connect_str = constant.CONNECT_STR
# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

AZURE_ACC_NAME = constant.BLOB_AC_NAME
AZURE_PRIMARY_KEY = constant.ACCESS_KEY_AZ

class UploadBlobClass(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request):

        res_lst= []
            
        try:
            container_name = request.POST['container']
            file_obj = request.FILES
            fdata = file_obj['file']
            filename = fdata.name

            fdata = request.data
            print(file_obj)
            print(fdata.path)
            # Create a blob client using the local file name as the name for the blob
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

            with open(fdata, "rb") as data:
                blob_client.upload_blob(data)
        
        except Exception as ex:
            print("exception :")
            print(ex)

        return JsonResponse({"result": res_lst})