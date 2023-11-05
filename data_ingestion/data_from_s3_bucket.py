import boto3
import os




class data_loader_from_s3:
  
    """
         This class shall be used to load the data from the s3 bucket.
         
         Written by: 
         Version: 1.0
         Revision: None
    
    
    """
    
    def __init__(self,bucket_name):
        self.bucket_name = bucket_name
        self.local_folder = 'raw_data_from_s3'
        self.s3_client = boto3.client('s3')
        
    def get_file_names(self):
        self.file_names = []
        
        #self.s3_client = boto3.client('s3')
        
        objects = self.s3_client.list_objects_v2(Bucket = self.bucket_name)
        
        for obj in objects['Contents']:
            self.file_names.append(obj['key'])
            
        return self.file_names
    
    def download_files(self):
        
        self.file_names = get_file_names()
        
        for file in self.file_names:
            if not os.path.isdir(self.local_folder):
                os.makedirs(self.local_folder)
            else:
                file_path = os.path.join(self.local_folder,file)
                self.s3_client.download_file(self.bucket_name,file,str(file_path))
                
                
        
        
        
            
        
        
            
    
   

