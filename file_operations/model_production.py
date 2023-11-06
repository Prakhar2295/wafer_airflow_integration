import os
import pickle
import shutil
from datetime import datetime

class File_operation_prod:

    """
            This Class Shall be used to save the model to a file after training and
            load the saved model for prediction.

            Written By: JSL
            Version: 1.0
            Revisions: None

    
    
    """
    def __init__(self,file_path,logger_object):
        self.file_path = file_path
        self.logger_object = logger_object
        self.model_directory = "production"
        
    def load_model(self,filename):

        """
             Method Name: load_model
             Description: This method will load the trained model saved in a pickle file.
             Output: Load the trained model into memory
             On failure: Raises an exception

             Written By: JSL
             Version: 1.0
             Revisions: None

        """
        self.file_object = open(self.file_path, 'a+')
        self.logger_object.log(self.file_object, 'Entered the load_model method of the file_operation class')


        try:
            with open(self.model_directory +"/" + filename + '/' + filename + '.sav','rb') as f:

                self.logger_object.log(self.file_object,'Model File' + filename+ 'loaded.Exited The load_model method of the file_operation class')
                self.file_object.close()
                return pickle.load(f)
        except Exception as e:
            self.file_object = open(self.file_path, 'a+')
            self.logger_object.log(self.file_object," Exception occurred model loading unsuccessfull.Exception meassage ::%s" %e)
            self.logger_object.log(self.file_object,"Model loading failed.Exiting the load_model method from file_operation class")
            self.file_object.close()
            raise Exception() 
        
    def find_correct_model_file(self,cluster_number):

        """
             Method Name: find_correct_model_file
             Description: Selects the correct model file for the given cluster number.

             Output: The model file.
             On failure: Raises an Exception

             Written By: JSL
             Version: 1.0
             Revisions: None

    
        """
        self.file_object = open(self.file_path,'a+')
        self.logger_object.log(self.file_object,"Entered inside the find_correct_model_file inside file_operations class")
        self.file_object.close()

        try:
            self.cluster_number = cluster_number
            self.folder_name = self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file in self.list_of_files:
                try:
                    if self.file[-1] == str(self.cluster_number):
                        self.model_name = self.file
                except:
                    continue
            self.model_name = self.model_name.split('.')[0]
            self.file_object = open(self.file_path, 'a+')
            self.logger_object.log(self.file_object,"Exited the find_correct_model_file method of the file opration class")
            self.file_object.close()
            return self.model_name

        except Exception as e:
            self.file_object = open(self.file_path, 'a+')
            self.logger_object.log(self.file_object,"Failed to finds the  correct model file")
            self.logger_object.log(self.file_object,"Exception occurred.Exception message :: %s" %e)
            self.file_object.close()
            raise Exception()
        
        

