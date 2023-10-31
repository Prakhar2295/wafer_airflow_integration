from wsgiref import simple_server
from flask import Flask, request, render_template
#from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_validation_insertion import pred_validation
from trainingmodel2 import train_model
from training_Validation_insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction
import json

#os.putenv('LANG', 'en_US.UTF-8')
#os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
#dashboard.bind(app)
#CORS(app)


#@app.route("/", methods=['GET'])
#@cross_origin()
#def home():
    #return render_template('index.html')

@app.route("/predict", methods=['POST'])
#@cross_origin()
def predictRouteClient():
    try:
        if (request.method == ['POST']):
            path = request.json['filepath']

            #pred_val = pred_validation(path) #object initialization

            #pred_val.prediction_validation() #calling the prediction_validation function

            #pred = prediction(path) #object initialization

            # predicting for dataset present in database
            #path,json_predictions = pred.predictionfrommodel()
            #return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(json.loads(json_predictions) ))
        elif request.form is not None:
            path = request.form['filepath']

            #pred_val = pred_validation(path) #object initialization

            #pred_val.prediction_validation() #calling the prediction_validation function

            #pred = prediction(path) #object initialization

            # predicting for dataset present in database
            #path,json_predictions = pred.predictionfrommodel()
            #return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(json.loads(json_predictions) ))
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



@app.route("/train", methods=['POST'])
#@cross_origin()
def trainRouteClient():

    try:
        if (request.method == ['POST']):
            path = request.json['folderPath']

            #train_valObj = train_validation(path) #object initialization

            #train_valObj.train_validation()#calling the training_validation function


            #trainModelObj = train_model() #object initialization
            #trainModelObj.model_training() #training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")

#port = int(os.getenv("PORT",5000))
#if __name__ == "__main__":
    #app.run()
    #host = '0.0.0.0'
    #port = 5000
    #httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    #httpd.server_activate()
    #app.run()