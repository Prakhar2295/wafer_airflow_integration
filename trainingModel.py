"""

This is the entry point for Training the Machine Learning Model.

Written By: JSL
Version: 1.0
Revision: None


"""


###Doing the necessary imports

from sklearn.model_selection import train_test_split
from data_ingestion import data_loader
from data_preprocessing import preprocessing
from data_preprocessing import clustering
from best_model_finder import tuner
from file_operations import file_methods
from application_logging import logger


class trainmodel:


    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt",'a+')

    def trainingmodel(self):
        ###Logging the start of the training
        self.log_writer.log(self.file_object,"Start Of Training!!")
        try:
            ###Getting the data from the source
            data_getter = data_loader.Data_Getter(self.file_object,self.log_writer)
            data = data_getter.get_data()

            ###Doing the data preprocessing
            preprocess = preprocessing.prepocessor(self.file_object,self.log_writer)
            data = preprocess.remove_columns(data,["Unnamed: 0","Wafer"])
            self.log_writer.log(self.file_object,"Removal of columns done successfully.Exited the remove column methods from preprocessor class")

            ###Create separe features and labels

            X,Y = preprocess.separate_label_features(data,label_column_name= "Output")

            ###Checking if missing value is present in the dataset

            is_null_present = preprocess.is_null_present(data)

             ####if missing values are present impute them appropriately
            if (is_null_present):
                X = preprocess.impute_missing_values(X)    ###missing values imputation

            col_to_drop = preprocess.get_columns_with_zero_std_deviation(X)


            X = preprocess.remove_columns(X,col_to_drop)

            ###Applying the clustering approach


            kmeans = clustering.KMeansClustering(self.log_writer,self.file_object)
            number_of_clusters = kmeans.elbow_plot(X)    ####Plotting the elbow plot using method inside the Kmeansclustering class

            X = kmeans.create_clusters(X,number_of_clusters)    ###To divide the data into clusters

            ##create a new column in the datasetconsisting of the corresponsingcluster assignmenst

            X['Labels'] = Y

            list_of_clusters =X['Cluster'].unique()

            for i in list_of_clusters:
                cluster_data = X[X['Cluster']==i]   ##Filter the data for each cluster

                ###Prepare the feature and label columns

                cluster_features = cluster_data.drop(['Labels','Cluster'],axis = 1)
                cluster_label = cluster_data['Labels']


                ###Splitting the data into train_test_split
                x_train,x_test,y_train,y_test = train_test_split(cluster_features,cluster_label,test_size = 1/3,random_state = 150)

                model_finder = tuner.Model_finder(self.file_object,self.log_writer)

                ###getting the best model for each of the clusters
                best_model_name,best_model =model_finder.get_best_model(x_train,y_train,x_test,y_test)


                ###saving the best model to the directory
                file_op =file_methods.File_operation(self.file_object,self.log_writer)
                save_model = file_op.save_model(best_model,best_model_name + str(i))

            #self.log_writer.log(self.file_object,"Training Ended Successfully!!")
            #self.file_object.close()
        except Exception as e:
            #self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            #self.file_object.close()
            raise e



#p = trainmodel()
#p.trainingmodel()
#print("don#e")






























































