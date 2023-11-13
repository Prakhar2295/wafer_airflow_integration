import os




class data_loader_from_s3:
  
    """
         This class shall be used to load the data from the s3 bucket.
         
         Written by: 
         Version: 1.0
         Revision: None
    
    
    """
    
    def __init__(self,bucket_name):
        self.bucket_name='waferbucket'
        self.local_folder = 'raw_data_from_s3'
        #self.s3_client = boto3.client('s3')
        #self.file_names = []
        
    def get_file_names(self):
        command = f'aws s3 ls s3://{self.bucket_name}'
        os.system(command)

    
    def download_files(self):
        
        #if os.path.exists(self.local_folder):
            #for file in os.listdir(self.local_folder):
                #os.remove(file)
        
        self.command = f'aws s3 cp s3://{self.bucket_name} {self.local_folder} --recursive'
        os.system(self.command)
        return self.local_folder
        
        





                
                
        
a =data_loader_from_s3('waferbucket')
#l = a.get_file_names()
a.download_files()
print('done')



        
            
        
        
            
    
   

