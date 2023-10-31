import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
#from application_logging.logger import App_Logger

class prepocessor:

    """
        This class will be used to clean & transform the data befor training.

        Written By: JSL
        Version: 1.0
        Revisions: None
        
    """
    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object


    def remove_columns(self,data,columns):

        """
             Method Name: remove_columns
             Description: This method removes the given columns from the pandas dataframe.
             Output: A dataframe after removing the specified dataframe.
             On failure: An Exception is raised


             Written By: JSL
             Version: 1.0
             Revisions: None  
        
        """

        self.logger_object.log(self.file_object,"Entered the remove column method of the preprocessing class")
        self.data = data
        self.columns = columns
        try:
            self.useful_data = self.data.drop(labels = self.columns,axis = 1)  # drop the labels specified in the columns
            self.logger_object.log(self.file_object,"Column Removal Successfull it's names are:: %s" %self.columns)

            return self.useful_data

        except Exception as e:
            self.logger_object.log(self.file_object,"Error occurred while removing columns it's names are:: %s" %self.columns)
            self.logger_object.log(self.file_object,"Error occurred while removing %s" %e)

            raise Exception()
        
    def separate_label_features(self,data,label_column_name):

        """
                  Method: separate_label_features
                  Description: This method separates the features and the label column.
                  Output: Returns two separate dataframes, one containing the features and the other containing labels.
                  On failure : Raises Exception


                  Written By: JSL
                  Version: 1.0
                  Revisions: None 

        """

        self.logger_object.log(self.file_object,"Entered the separate the label feature method inside the preprocessing class")
        try:
            self.X = data.drop(labels = label_column_name,axis = 1)  ###dropping the label column from the dataframe

            self.Y = data[label_column_name]  ##Assigning the label column to the Y dataframe.

            self.logger_object.log(self.file_object,"Exiting the separate label features method")

            return self.X,self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,"Exception occurred during separating the dataframe %s"%e)
            self.logger_object.log(self.file_object,"Label separation unsuccessfull.Exiting the separate column method of the preprocessing class")
            raise Exception()
        
    def is_null_present(self,data):

        """
             Method Name: is_null_present
             Description: This method is used to check whether the given dataframe 
             is having any null_values presnt in it.This method will further crate the dataframe 
             of all the columns with null_values present in the dataframe.

             Output: Returns a Boolean value True if the null values are present in the dataframe
             and FALSE if the null values are not present in the dataframe.

             On Failure: Raises an Exception

            Written By: JSL
            Version: 1.0
            Revisions: None 
        
        """
    
        self.logger_object.log(self.file_object,"Entered the is_null_present method in preprocessing class")
        self.null_present= False

        try:
            self.null_counts = data.isna().sum()  ##Check the number of null values in the data
            for i in self.null_counts:
                if i > 0:
                    self.null_present = True
                    break
            if(self.null_present):     ###write the logs to see which column have null values.
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null["columns"] = data.columns
                dataframe_with_null["missing value counts"] = np.array(self.null_counts)
                dataframe_with_null.to_csv("preprocessing_data/null_values.csv")   ##storing the null values of columns inside the file
            self.logger_object.log(self.file_object,"Finding Null values is a success.Data written to null values file.Exiting the is_nul_present method")
            return self.null_present
        except Exception as e:
            self.logger_object.log(self.file_object,"Exception occurred in is_bull_present method of the preprocessing class.Exception mesaages %s" %e)
            self.logger_object.log(self.file_object,"Find missing values failed for preprocessing class.Exiting the is_null_present method of the preprocessing class")
            raise Exception()
        
    def impute_missing_values(self,data):

        """
               Method Name: impute_missing_values
               Description: This method impute all the missing values using KNN imputer.

               Output:A dataframe which has all the missing values imputed.
               On failure: Raises an Exception

               Written By: JSL
               Version: 1.0
               Revisions: None
    
        
        """
        self.logger_object.log(self.file_object,"Entered the impute missing values method of the preprocessing class")
        self.data = data
        try:
            imputer = KNNImputer(n_neighbors=3,weights = "uniform",missing_values = np.nan)
            self.new_array = imputer.fit_transform(self.data)  # impute the missing values
            ##convert the ndarray to the dataframe return in the above step
            self.new_data = pd.DataFrame(data= self.new_array,columns = self.data.columns)
            self.logger_object.log(self.file_object,"Imputing the missing values succesfull exiting the impute values method")
            return self.new_data
        
        except Exception as e:
            self.logger_object.log(self.file_object,"Exception occurred while imputing the values %s"%e)
            self.logger_object.log(self.file_object,"Imputing the missing values failed in the presprocessing class")
            raise Exception()
        
    def get_columns_with_zero_std_deviation(self,data):
        """
                Method Name: get_columns_with_zero_std_deviation
                Description: This method will be used to compute the compute columns with zero
                standard deviation.

                Output: List of columns with zero standard deviation
                On failure: Raises an exception

                Written By: JSL
                Version: 1.0
                Revisions: None
              
        """
        self.logger_object.log(self.file_object,"Entered inside the method get columns with zero standard deviation in preprocessing class")
        self.columns = data.columns
        self.data_n = data.describe()
        self.col_to_drop = []
        try:
            for x in self.columns:
                if self.data_n[x]['std'] == 0:   # check if standard deviation is zero or not for any column
                    self.col_to_drop.append(x)  ##storing the column names to the list       
            self.logger_object.log(self.file_object,"Column Search for standard with zero is successsfull.Exiting from this method inside the preprocessing class")

            return self.col_to_drop
        except Exception as e:
            self.logger_object.log(self.file_object,"Exception occurred when searching for column with standard deviation with zero.Exiting from this method inside the preprocessing class")
            self.logger_object.log(self.file_object,"Columns Search for Standard deviation with zero is unsuccessfull.Exception Occurred.Exception message :: %s "%e)
            raise Exception()
            



        
        
       





                   



        







        


