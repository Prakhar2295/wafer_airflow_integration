import os
import shutil
import pandas as pd
from application_logging.logger import App_Logger
from data_preprocessing.data_preprocessing import Preprocessing
from data_ingestion.data_loader_prediction import data_getter_prediction
from data_ingestion.data_loader import Data_Getter
from file_operations.file_methods import File_operation
from prediction_raw_data_validation.prediction_raw_data_validation import prediction_data_validation
#from prediction_raw_data_validation.prediction_raw_data_validation import prediction_data_validation
from sklearn.metrics import precision_score,recall_score,roc_auc_score,accuracy_score,f1_score
from file_operations.model_production import File_operation_prod




class evaluate_model:
	"""
	     This class will be used to evaluate the models performance
	     based on the certain metrics.

	    Written By: JSL
        Version: 1.0
        Revisions: None

	"""
	def __init__(self):
		self.file_path = "prediction_logs/ModelEvaluation.txt"
		self.logger_object = App_Logger()
		self.path = "Training_Data_prediction/TestModelprediction.csv"

		self.test_metrics = {}
		self.prod_metrics = {}
		self.mode = ['Test', 'Production']

		#self.input_file_path = "PredictionFileFromDB/InputFile.csv"

	def model_prediction(self):
		"""
			 Method Name: model_prediction
		     Description: This method will be used to evaluate the performance of the model
		      on the new training data.

		     On output: Models performance metrics
		     Failure: Raises an exception

		     Written by: JSL
		     Revision: None
		     Version: 1.0


		"""
		try:

			for m in self.mode:
					print(m)
					if m == 'Test':
						self.file_object = open(self.file_path,"a+")
						self.logger_object.log(self.file_object,"Entered inside Test model performance method of the evaluate_model class")
						self.file_object.close()
						if os.path.exists("Training_Data_prediction/TestModelprediction.csv"):
							os.remove("Training_Data_prediction/TestModelprediction.csv")
						if os.path.exists("Training_Data_prediction/TestCluster_data.csv"):
							os.remove("Training_Data_prediction/TestCluster_data.csv")
						self.data_op = Data_Getter(self.file_object,self.logger_object)  ##initializing the object of data getter class
						self.data = self.data_op.get_data()  ###loading the training data

						preprocess = Preprocessing()
						X1 = preprocess.remove_columns(self.data, ["Unnamed: 0"])

						X, Y = preprocess.separate_label_features(X1, "Output")

						self.is_null_present = preprocess.is_null_present(X)

						if self.is_null_present:
							X_new = preprocess.missing_value_imputation(X)

						self.cols_drop_list = preprocess.cols_with_zero_std_deviation(X_new)

						X2 = preprocess.remove_columns(X_new, self.cols_drop_list)
						self.file_op = File_operation(self.file_path, self.logger_object)

						kmeans = self.file_op.load_model("KMeans")

						clusters = kmeans.predict(X2.drop(['Wafer'], axis=1))
						# clusters = kmeans.predict(X2.drop(["Wafer"], axis=1))

						X2["clusters"] = clusters
						X2["True"] = Y
						X2["clusters"] = clusters
						X2["True"] = Y

						list_of_clusters = X2["clusters"].unique()
						for i in list_of_clusters:
							cluster_data = X2[X2["clusters"] == i]
							# cluster_names = list(cluster_data["clusters"])
							Y_true = list(X2["True"])
							wafer_names = list(X2["Wafer"])
							cluster_data = X2.drop(["True"], axis=1)
							cluster_data = cluster_data.drop(["Wafer"], axis=1)
							cluster_data = cluster_data.drop(["clusters"], axis=1)
							model_name = self.file_op.find_correct_model_file(i)
							model = self.file_op.load_model(model_name)
							result = list(model.predict(cluster_data))
							result = pd.DataFrame(list(zip(wafer_names, result, Y_true)),columns=["Wafer", "Prediction", "Y_True"])
						result.to_csv(self.path, index=None, header=True, mode='a+')
						X2.to_csv("Training_Data_prediction/TestCluster_data.csv")
					else:
						self.file_object = open(self.file_path, "a+")
						self.logger_object.log(self.file_object,
						                       "Entered inside production model performance method of the evaluate_model class")
						if os.path.exists("Training_Data_prediction/ProductionModelprediction.csv"):
							os.remove("Training_Data_prediction/ProductionModelprediction.csv")
						if os.path.exists("Training_Data_prediction/ProductionCluster_data.csv"):
							os.remove("Training_Data_prediction/ProductionCluster_data.csv")
						self.data_op = Data_Getter(self.file_object,
						                           self.logger_object)  ##initializing the object of data getter class
						self.data = self.data_op.get_data()  ###loading the training data

						preprocess = Preprocessing()
						X1 = preprocess.remove_columns(self.data, ["Unnamed: 0"])

						X, Y = preprocess.separate_label_features(X1, "Output")

						self.is_null_present = preprocess.is_null_present(X)

						if self.is_null_present:
							X_new = preprocess.missing_value_imputation(X)

						self.cols_drop_list = preprocess.cols_with_zero_std_deviation(X_new)

						X2 = preprocess.remove_columns(X_new, self.cols_drop_list)

						self.file_prod = File_operation_prod(self.file_path, self.logger_object)

						kmeans = self.file_prod.load_model("KMeans")

						clusters = kmeans.predict(X2.drop(['Wafer'], axis=1))
						# clusters = kmeans.predict(X2.drop(["Wafer"], axis=1))

						X2["clusters"] = clusters
						X2["True"] = Y
						list_of_clusters = X2["clusters"].unique()

						for i in list_of_clusters:
							cluster_data = X2[X2["clusters"] == i]
							# cluster_names = list(cluster_data["clusters"])
							Y_true = list(X2["True"])
							wafer_names = list(X2["Wafer"])
							cluster_data = X2.drop(["True"], axis=1)
							cluster_data = cluster_data.drop(["Wafer"], axis=1)

							cluster_data = cluster_data.drop(["clusters"], axis=1)
							model_name = self.file_prod.find_correct_model_file(i)
							model = self.file_prod.load_model(model_name)
							result = list(model.predict(cluster_data))
							result = pd.DataFrame(list(zip(wafer_names, result, Y_true)),columns=["Wafer", "Prediction", "Y_True"])
						result.to_csv("Training_Data_prediction/ProductionModelprediction.csv", index=None,header=True, mode='a+')
						X2.to_csv("Training_Data_prediction/ProductionCluster_data.csv")

		except Exception as e:
			raise e









	def calculate_metrics_score_for_test(self):
		"""
			Method Name:calculate_metrics_score
			Description: This method will be used to calculate metrics scores for
			evaluating the performance of models with respect to their clusters.

			Written by: JSL
		    Revision: None
		    Version: 1.0


		"""
		try:
			self.data = "Training_Data_prediction/TestCluster_data.csv"
			#self.data = self.model_prediction()


			result = "Training_Data_prediction/TestModelprediction.csv"
			self.df = pd.read_csv(self.data)
			clusters = self.df["clusters"]
			self.df_result = pd.read_csv("Training_Data_prediction/TestModelprediction.csv")
			self.df_result["Clusters"] = clusters
			list_of_cluster = self.df_result["Clusters"].unique()
			for i in list_of_cluster:
				cluster_data = self.df_result[self.df_result["Clusters"] == i]
				if len(cluster_data["Y_True"].unique()) == 1:
					self.test_metrics['Test_accuracy_score::'+ str(i)] = str(accuracy_score(cluster_data["Y_True"],cluster_data["Prediction"]))
					print("accuracy_score_cluster_no.:%s"%i + " = " + str(accuracy_score(accuracy_score(cluster_data["Y_True"],cluster_data["Prediction"]))))
				else:
					self.test_metrics['Test_roc_auc_score_cluster_no::'+ str(i)] = str(roc_auc_score(cluster_data["Y_True"],cluster_data["Prediction"]))
					print("roc_auc_score_cluster_no.: %s" %i + " = " + str(roc_auc_score(cluster_data["Y_True"],cluster_data["Prediction"])))
					print("precision_score_cluster_no.: %s" % i + " = " + str(precision_score(cluster_data["Y_True"], cluster_data["Prediction"])))
					print("recall_score_cluster_no.: %s" % i + " = " + str(recall_score(cluster_data["Y_True"], cluster_data["Prediction"])))

			return self.test_metrics

		except Exception as e:
			raise e

	def calculate_metrics_score_for_production(self):
		"""
			Method Name:calculate_metrics_score
			Description: This method will be used to calculate metrics scores for
			evaluating the performance of models with respect to their clusters.

			Written by: JSL
		    Revision: None
		    Version: 1.0


		"""
		try:

			self.data = "Training_Data_prediction/ProductionCluster_data.csv"
			#self.data = self.model_prediction()

			result = "Training_Data_prediction/ProductionModelprediction.csv"
			self.df = pd.read_csv(self.data)
			clusters = self.df["clusters"]
			self.df_result = pd.read_csv("Training_Data_prediction/ProductionModelprediction.csv")
			self.df_result["Clusters"] = clusters
			list_of_cluster = self.df_result["Clusters"].unique()
			for i in list_of_cluster:
				cluster_data = self.df_result[self.df_result["Clusters"] == i]
				if len(cluster_data["Y_True"].unique()) == 1:
					self.prod_metrics['Prod_accuracy_score::' + str(i)] = str(accuracy_score(cluster_data["Y_True"], cluster_data["Prediction"]))
					print("prod_accuracy_score_cluster_no.: %s"%i + " = " + str(accuracy_score(accuracy_score(cluster_data["Y_True"],cluster_data["Prediction"]))))
				else:
					self.prod_metrics['Prod_roc_auc_score_cluster_no::' + str(i)] = str(roc_auc_score(cluster_data["Y_True"], cluster_data["Prediction"]))

					print("prod_roc_auc_score_cluster_no.: %s" %i + " = " + str(roc_auc_score(cluster_data["Y_True"],cluster_data["Prediction"])))
					print("prod_precision_score_cluster_no.: %s" % i + " = " + str(precision_score(cluster_data["Y_True"], cluster_data["Prediction"])))
					print("prod_recall_score_cluster_no.: %s" % i + " = " + str(recall_score(cluster_data["Y_True"], cluster_data["Prediction"])))
					#print('a:' + self.prod_metrics['Prod_roc_auc_score_cluster_no::0'])

			return self.prod_metrics


		except Exception as e:
			raise e


	def compare_models_performance(self):
		a_prod_key = []
		b_prod_val = []
		a_test_key = []
		b_test_val = []

		key_invalid = []

		try:
			for i,j in self.prod_metrics.items():
				a_prod_key.append(i)
				b_prod_val.append(j)
			for i, j in self.test_metrics.items():
				a_test_key.append(i)
				b_test_val.append(j)
			if len(a_prod_key) == len(a_test_key):
				for i in range(len(a_prod_key)):

					if a_prod_key[i][5:] in a_test_key[i][5:]:
						if self.prod_metrics[a_prod_key][i] < self.test_metrics[a_test_key]:
							print('all ok')
							pass

						elif self.prod_metrics[i] > self.test_metrics[i]:
							print('all ok1')
							pass
					elif i not in a_test_key:
						key_invalid.append(i)

			elif len(a_prod_key) != len(a_test_key):
				print('Production models clusters are different than the testing models')

			if len(key_invalid) != 0:
				print('model invalid')

		except Exception as e:
			raise e




















a = evaluate_model()
a.model_prediction()
a.calculate_metrics_score_for_production()
a.calculate_metrics_score_for_test()
#a.compare_models_performance()
print("done")
print(a.prod_metrics)
print(a.test_metrics)
#print(a.key_invalid)


