from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from pathlib import Path
import urllib.parse
from datetime import datetime, timedelta, timezone
import time
import dateutil
import ftfy

import pandas as pd
import json
import sys
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.storage.blob import generate_blob_sas, BlobSasPermissions, generate_account_sas, ResourceTypes, AccountSasPermissions
from azure_blob_app.constants import constant

encoding = sys.getdefaultencoding()

#connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = ''
connect_str = constant.CONNECT_STR
# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
# dt_now_utc = datetime.utcnow()+ timedelta(hours=5)
dt_now_utc = datetime.utcnow()+ timedelta(weeks=+4)
# sas_token = generate_account_sas(
#     account_name=constant.BLOB_AC_NAME,
#     account_key=constant.ACCESS_KEY_AZ,
#     resource_types=ResourceTypes(service=True),
#     permission=AccountSasPermissions(read=True),
#     expiry=dt_now_utc.isoformat()
#     #expiry=(datetime.utcnow() + timedelta(seconds=5)).strftime("%m/%d/%Y, %H:%M:%S")
# )
AZURE_ACC_NAME = constant.BLOB_AC_NAME
AZURE_PRIMARY_KEY = constant.ACCESS_KEY_AZ

class GetBlobClass(APIView):

    def post(self, request):
            
        try:
            ar_lst = []
            pdtas = request.POST['blob_obj']

            print(dt_now_utc)
            
            container_name = request.POST['container']

            status = 'Automated' if container_name == constant.CONTAINER_NAME else 'Manually'
                      
            if pdtas != '':
                pobj = json.loads(pdtas)
                
                ddetails = self.getDocDetails(pobj)                
                ar_lst.append(ddetails)
            
            else:
           
                container_client = blob_service_client.get_container_client(container_name)
                # List the blobs in the container
                blob_list = container_client.list_blobs()                
                
                burl = constant.BASE_URL+container_name+'/'
                astr=''
                lbl_str=''
                ocr_str=''
                output_str=''
                sasFileUrl=''
                pobj = {}
                fobj = { 'container':container_name, 'file_name':''}
                # self.formDataNode( pobj ,  )

                for blob in blob_list:
                    # print("\t" + blob.name)
                    fpt = burl+blob.name
                    ext = Path(fpt).suffixes
                                                                                               
                    try:
                        if astr == '' and len(ext) == 1:
                            astr = blob.name
                            fobj['file_name'] = blob.name
                            # sasFileUrl = self.generate_sas_token(fobj)
                           
                       
                        # elif (blob.name.find(ext[0]+'.output.json') > 0) and len(ext) > 1 :
                        elif (blob.name.find(ext[0]+'.output.json') > 0) and len(ext) > 1 :
                            # ocr_str = burl+blob.name 

                            # create output file sas token
                            fobj['file_name'] = blob.name                            
                            output_str = self.generate_sas_token(fobj)

                            # create original file sas token
                            fobj['file_name']=astr
                            sasFileUrl = self.generate_sas_token(fobj)

                            pobj = {"container":container_name ,"file_name":astr, "file":sasFileUrl,"ocr":ocr_str, "output":output_str ,"label":lbl_str, "ocr_dt":'', "label_dt":'',"category":'Invoice',"invoice_date":datetime.utcnow(), "status":status}
                            # astr = blob.name
                            lbl_str=''
                            ocr_str=''
                            output_str=''
                           
                            ar_lst.append(pobj)
                           
                            # pobj = {"container":container_name ,"file_name":astr, "file":sasFileUrl,"ocr":ocr_str, "output":output_str ,"label":lbl_str, "ocr_dt":'', "label_dt":'',"category":'Invoice',"invoice_date":datetime.utcnow(), "status":status}
                                                        
                            # ar_lst.append(pobj)
                                                            
                        # elif output_str != '' and astr != blob.name and len(ext) == 1:
                        elif astr !='' and astr != blob.name and len(ext) == 1:
                                                   
                            # fobj['file_name']=astr
                            # sasFileUrl = self.generate_sas_token(fobj)
                            # pobj = {"container":container_name ,"file_name":astr, "file":sasFileUrl,"ocr":ocr_str, "output":output_str ,"label":lbl_str, "ocr_dt":'', "label_dt":'',"category":'Invoice',"invoice_date":datetime.utcnow(), "status":status}
                            astr = blob.name
                            lbl_str=''
                            ocr_str=''
                            output_str=''
                            
                            # ar_lst.append(pobj)
                                    
                    except Exception as ex:
                        print(ex)
                        continue


           # print(ar_lst)    
        except Exception as ex:
            print("exception :")
            print(ex)

        return JsonResponse({"result": ar_lst})

    def get(self, request):

        return JsonResponse({"key": "Hey"})
       
        #return render(request, 'view_a.html')
    
    def generate_sas_token(self, fobj):
        # create zulu timestamp
        # print(dt_now_utc)
        exdt = (dt_now_utc.isoformat()).split('.')[0]
        # print(exdt)
        sas = generate_blob_sas(account_name=AZURE_ACC_NAME,
                            account_key=AZURE_PRIMARY_KEY,
                            container_name=fobj['container'],
                            blob_name=fobj['file_name'],
                            permission=BlobSasPermissions(read=True),
                            expiry= exdt+'Z')

    
        sas_url ='https://'+AZURE_ACC_NAME+'.blob.core.windows.net/'+fobj['container']+'/'+urllib.parse.quote(fobj['file_name'])+'?'+sas
        
        # sas_url = urllib.parse.quote(sas_url)
        # print(sas_url)
        return sas_url
    
    def getDocDetails(self, dobj):
        
        # print(dobj['output'])
        ocr_dt=''
        # code for read json file
        # if dobj['container'] != 'manual':
        #     ocr_dt = pd.read_json(dobj['ocr'])
        #     dobj['ocr_dt'] = ocr_dt.to_json()
        #     label_dt = pd.read_json(dobj['label'])
        #     dobj['label_dt'] = label_dt.to_json()
        # else:     
       

        # for ubnatu server , uncomment for deployment
        ocr_dt = pd.read_json(dobj['output'])

        # for local windows encoding
        #ocr_dt = pd.read_json(dobj['output'])

        head_val = ocr_dt['headers']
        for hvl in head_val:
            print(isinstance(hvl, dict))
            if isinstance(hvl, dict) == True:
               hvl['text'] = ftfy.fix_encoding(hvl['text'])
                

               
        hconfig = self.getHeaderConfig()
        # convert to dictionary
        hconf_obj = hconfig.to_dict(orient='record')

        table = ocr_dt['tables']
        for pno in table['page']:
            
            for pg in table['page'][pno]:

                for ind, tdt in enumerate(table['page'][pno][pg]):
                    
                    if ind == 0:               
                        for ix, thr in enumerate(tdt):
                             
                            # match text in config ui translation
                            if str(isinstance(thr, str)) == 'True' :
                                tdt[ix] = {	
                                    "columnIndex": ix, "elements": '' ,
                                    "rowIndex": ind,
                                    "text": thr,
                                    "header": 'small',
                                    "ui_label":''
                                }                                

                            elif str(isinstance(thr, str)) == 'False' and thr['text'] != '':
                              
                                hcl = list(filter(lambda x: x['JSON Lable(order tree)'] == thr['text'], hconf_obj))
                                
                                thr['header'] =  'small'
                                thr['ui_label'] = ''

                                if len(hcl) != 0:
                                    thr['header'] =  hcl[0]['Text Size']
                                    thr['ui_label'] = hcl[0]['UI Lable']

                    elif tdt != "":
                        
                        for jv, tvl in enumerate(tdt):
                            
                            if tvl != "":
                                tvl['text'] = ftfy.fix_encoding(tvl['text'])
                               


                                
        # print(table)
        dobj['output_dt'] = ocr_dt.to_json()
        # dobj['output_dt'] = ftfy.fix_encoding(dobj['output_dt'])

        # print(dobj['output_dt'])

        return dobj

    def getHeadsize(self, vl, th):
        
        return vl
    
    def getHeaderConfig(self):
        
        # generate sas url
        fobj = {}
        fobj['container'] = constant.CONFIG_CONTAINER
        fobj['file_name'] = constant.CONFIG_FILE_NAME
        
        config_sas_url = self.generate_sas_token(fobj)
        
        head_config = pd.read_excel(config_sas_url,usecols=['Table headers(Unique element)', 'Translation', 'JSON Lable(order tree)', 'UI Lable','Text Size'], engine='openpyxl')
        # print(head_config.columns.ravel())
        # print(head_config['Translation'])
        return head_config

def view_b(request):
    return render(request, 'view_b.html')
