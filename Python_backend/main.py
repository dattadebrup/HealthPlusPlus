
from flask import request, jsonify,Flask,render_template
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import translate
from google.auth import app_engine
from werkzeug import secure_filename
import os
import json
import logging
import io
import mysql.connector
import dialogflow
import datetime 
import time
import Intent
#from reply import Reply
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sih-app-739b1db0be0c.json'

speech_client = speech.SpeechClient()
translate_client = translate.Client()
app = Flask(__name__)
#intent_obj = Intent()
#app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = '/home/campusiitism0/sih/Audio/'

mydb = mysql.connector.connect(
  host="35.186.152.172",
  user="root",
  passwd="",
  database="sihf"
)

config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000, #16000
            model= 'command_and_search',
            language_code='hi-IN')   # hi-IN | en-US

mycursor = mydb.cursor()



@app.route('/')
def home():
    return "Hello World"

@app.route('/upload')
def upload():
   return render_template('upload.html')



@app.route('/latlong',methods= ['GET'])
def lat_long():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'latlong' in request.args:
        latlong = str(request.args['latlong'])
        latlong = latlong.split(",")
        lat = float(latlong[0])
        long_n = float(latlong[1])

        query = "SELECT DISTINCT title,CONCAT(local_disease,description) as text, timestmp as timestamp FROM notification WHERE (6731 * acos (cos ( radians(78.3232) )* cos( radians("+str(lat)+" ) )* cos( radians("+str(long_n)+" ) - radians(65.3234) )+ sin ( radians(78.3232) )* sin( radians( "+str(lat)+" ) ))) >10"
        #print("query",query)
        mycursor.execute(query)

        myresult = mycursor.fetchall()

        myresult_translated = []
        
        for i,each_result in enumerate(myresult):
            each_result = list(each_result)

            temp = translate_client.translate(each_result[0],target_language='hi')
            topic = temp['translatedText']
            temp  = translate_client.translate(each_result[1],target_language='hi')
            text = temp['translatedText']

            
            ret_json =  {   
                            
                                "title": topic,
                                "text": text,
                                "timestamp": str(each_result[2]).split(' ')[0]
                            
                        }
                        
            myresult_translated.append(ret_json)



            
        myresult_translated = {"notifications" : myresult_translated}
        print(myresult_translated)
        myresult_translated = jsonify(myresult_translated)
        #myresult=json.dumps(myresult)

        #{"notification":[{"title":"HEADINGFROMTABLE","text":"FROMSQL","timestamp":"120"}
        #print("type",type(myresult))
        #decoded_data = json.loads(myresult.text)

        #print()
        #print(myresult[0][0])
        return myresult_translated

@app.route('/uploader', methods=['GET','POST'])

def uploader():
    if request.method == 'POST': # PUT in android | POST in local
        
        f = request.files['uploadedfile']
        #filePath = "./somedir/"+secure_filename(f.filename)
        filename = secure_filename(f.filename)
        f.save("/home/campusiitism0/sih/Audio/"+filename)
        #response = transcribe_file(f)
        print(filename)
        with io.open("/home/campusiitism0/sih/Audio/"+filename, 'rb') as audio_file:
            content = audio_file.read()
        #content = f.read()

        audio = types.RecognitionAudio(content=content)
        

        response = speech_client.recognize(config, audio)
        print(response)
        final_result =""
        for result in response.results:
            final_result = final_result + result.alternatives[0].transcript

        # The text to translate
        text = final_result
        print(text)
        # The target language
        target = 'en'

        # Translates some text into 
        translated_query = translate_client.translate(
            text,
            target_language=target)

        #html_ret = "<h1>Distant Reading Archive</h1>" +  str(translated_query['translatedText'])
        ts = str(datetime.datetime.now())

        #st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        timestamp = str(ts).split(' ')[1]
        timestamp = timestamp.split('.')[0]
        return_text= Intent.analyze(translated_query['translatedText'])

        translated_response = translate_client.translate(return_text,target_language='hi')
        #timestamp = st.split(" ")[1]
        ret_json = { "message": 
                        [
                        {   
                            
                                "title": "आरोही",
                                "text": translated_response['translatedText'],
                                "timestamp": str(timestamp)
                            
                        }
                        ]
                    }

        ret_json = json.dumps(ret_json)
        print(translated_query)

        
        return (ret_json)
        #return (final_result)


@app.route('/user_history',methods= ['GET'])
def test():
    if 'userid' in request.args:
        userid = str(request.args['userid'])
        query = "SELECT food FROM dis inner join history ON history.disease=dis.disease where userid="+str(userid)+" group by dis.food having count(*)>=1;"
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        #myresult=jsonify(myresult)
        ret_result = ''
        for each_result in myresult:
            ret_result = ret_result + str(each_result[0]) + ' '
        print(ret_result)
        return(ret_result)
        



app.run( threaded= True,host='0.0.0.0', port=80, debug =True) 