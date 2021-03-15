from django.conf.urls import url
from azure_blob_app.views import downloadblob
from azure_blob_app.views import getblob
from azure_blob_app.views import UploadBlobClass
from azure_blob_app.views.getblob import GetBlobClass

urlpatterns = [
    #url('downloadblob', downloadblob.view_a, name='downloadblob'),
    #url('getblob', getblob.view_b, name='getblob'),
    url('uploadToBlobclass', UploadBlobClass.as_view(), name='uploadBlobClass'),
    url('getBlobClass',GetBlobClass.as_view(), name="getBlobClass"),  
]