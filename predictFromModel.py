import pandas as pd
from data_preprocessing.data_preprocessing import Preprocessing
from file_operations.file_methods import File_operation
from data_ingestion.data_loader_prediction import data_getter_prediction
from prediction_raw_data_validation.prediction_raw_data_validation import prediction_data_validation
from application_logging.logger import App_Logger


class prediction:

	"""
			   This class shall be used to predict the datasets received from the client
			  side.

	           Written By: JSL
               Version: 1.0
               Revisions: None



	"""

	def __init__(self):
		self.file_path = "prediction_logs/File_prediction_logs.txt"
		self.logger_object = App_Logger()
		self.path = "Prediction_Output_File/Predictions.csv"

	def predictionfrommodel(self):


		try:
			self.path = "Prediction_Output_File/Predictions.csv"
			self.file_object = open(self.file_path,'a+')
			self.logger_object.log(self.file_object,"Entered inside the prediction from class succesfully")


			self.pred_val = prediction_data_validation(self.path)
			self.pred_val.deletepredictionfile()
			self.logger_object.log(self.file_object, "Deleted the old prediction files succesfully !!!")
			self.file_object.close()

			data_load = data_getter_prediction()
			self.data = data_load.data_loader()

			preprocess = Preprocessing()
			X = preprocess.remove_columns(self.data,["Unnamed: 0"])

			is_null_present = preprocess.is_null_present(X)
			if (is_null_present):
				X_new = preprocess.missing_value_imputation(X)

			cols_drop_list = preprocess.cols_with_zero_std_deviation(X_new)

			X1 = preprocess.remove_columns(X_new,cols_drop_list)

			self.file_op = File_operation(self.file_path ,self.logger_object)
			model = self.file_op.load_model('KMeans')

			clusters = model.predict(X1.drop(["Wafer"],axis =1))    ###Drop the first column for the cluster prediction

			X1["clusters"] = clusters
			cluster_list = X1["clusters"].unique()

			for i in cluster_list:
				cluster_data = X1[X1["clusters"] ==i]
				wafer_names = list(X1["Wafer"])
				cluster_data = X1.drop("clusters",axis = 1)
				cluster_data = cluster_data.drop("Wafer",axis = 1)
				model_name = self.file_op.find_correct_model_file(i)
				model = self.file_op.load_model(model_name)
				result = list(model.predict(cluster_data))
				result = pd.DataFrame(list(zip(wafer_names,result)),columns = ["Wafer","Prediction"])
			result.to_csv(self.path,index= None,header = True,mode = 'a+')
			self.file_object = open(self.file_path, 'a+')
			self.logger_object.log(self.file_object, 'End of Prediction!! CSV file saved Successfully!!')
			self.file_object.close()
		except Exception as e:
			self.file_object = open(self.file_path, 'a+')
			self.logger_object.log(self.file_object,"Exception occurred while predictions!!.Exception message:: %s"%e)
			raise e
		return self.path,result.head().to_json(orient = "records")



p = prediction()
p.predictionfrommodel()
print("done")































