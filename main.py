
import requests 
import codecs, json
from flask import Flask, jsonify
from threading import Thread
from flask_restful import Resource, Api
from flask import Flask, request
from splitname import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gevent.pywsgi import WSGIServer
from flask import make_response
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Chatby Setup").sheet1  #Abrir spreadhseet
#data = sheet.get_all_records()  # Get a list of all records
headers={"Accept":"application/json","Authorization":"","Content-Type":"application/json"}
url ="https://api.manychat.com/fb/subscriber/createSubscriber"
url1 ="https://api.manychat.com/fb/subscriber/setCustomFieldByName"

#"https://api.manychat.com/fb/subscriber/setCustomFieldByName"
app = Flask('')
api = Api(app)
result = {}
class Test(Resource):
  def post(selft):
      #req = request.get_json(silent=True, force=True)code
      pageID = request.args.get('pageID')
      if not  pageID:
          result = {"message":"error no pageid","status": 0}
          result = make_response(json.dumps(result))
          return result
     # code = request.args.get('code')
      #if not  code:
       #   result = {"message":"error","status": 0}
        #  return result
      request_json = request.get_json() 
      print( request_json)
      if not request_json:
          result = {"message":"is data incomple","status": 0}
          result = make_response(json.dumps(result))
          return result
      idj = request_json.get("id") 
      if not idj:
          result = {"message":"is not id","status": 0}
          result = make_response(json.dumps(result))
          return result
        
      created = request_json.get("creation_date") 
      if not created:
          result = {"message":"is not created","status": 0}
          result = make_response(json.dumps(result))
          return result 

      event = request_json.get("event") 
      if not event:
          result = {"message":"is not event","status": 0}
          result = make_response(json.dumps(result))
          return result
      version = request_json.get("version") 
      if not version:
          result = {"message":"is not version","status": 0}
          result = make_response(json.dumps(result))
          return result
     
    
      data = request_json.get("data")
      affiliate=data.get("affiliate")
      #if not affiliate:
       #   result = {"message":"is not affiliate","status": 0}
        #  return result
      prod=data.get("product")
      if not prod:
          result = {"message":"is not product","status": 0}
          result = make_response(json.dumps(result))
          return result
      prodid=prod.get("id")
      if not prodid:
          result = {"message":"is not product id","status": 0}
          result = make_response(json.dumps(result))
          return result
      prodname=prod.get("name")
      if not prodname:
          result = {"message":"is not product name","status": 0}
          result = make_response(json.dumps(result))
          return result
      buyer=data.get("buyer")
      name=buyer.get("name")
      email=buyer.get("email")
      pho=buyer.get("phone")
      code = request.args.get('code')
      if code:
        pho=code+pho
        print(pho)
      #result = {"pageID":pageID ,"code":code,"buyer":buyer,"status": 1}
      #columpid=sheet.col_values(4)
      nameps=sheet.find( pageID )  
      names=SplitNames(name)
      whatsppnum="+"+pho
      print(pho)
    
      if not nameps:
        
        result = {"message":"no page id  in data base","status": 0}
        result = make_response(json.dumps(result))
        return result
  
      appname=sheet.cell(nameps.row, 1).value
      apppwr=sheet.cell(nameps.row, 2).value
      pageid=sheet.cell(nameps.row, 4).value
      appn=sheet.cell(nameps.row, 5).value
      appver=sheet.cell(nameps.row, 6).value
      appid=sheet.cell(nameps.row, 7).value
      mess=sheet.cell(nameps.row,11 ).value
      token=sheet.cell(nameps.row,8).value
      enddate=sheet.cell(nameps.row,9).value
      FieldString=sheet.cell(nameps.row,13).value
      FieldArray=sheet.cell(nameps.row,14).value
      print(type(token))
      if not token:
        result = {"message":"no token","status": 0}
        result = make_response(json.dumps(result))
        return  result
      headers["Authorization"]="Bearer "+token
   
      if not ((sheet.cell(nameps.row, 10).value)=="TRUE"):
        result = {"message":"no status enable","status": 0}
        result = make_response(json.dumps(result))
        return  result
      N=names[0]+" "+names[1]
      print(names[0]+" "+names[1])
      jsonforpost={
        "first_name":names[0],
        "last_name":names[1],
        "phone": pho,
        "whatsapp_phone":whatsppnum,
        "email": email,
        "has_opt_in_sms": True,
        "has_opt_in_email": True,
          "consent_phrase": "Event Cart by Hotmart"}
      print(jsonforpost)
      x =requests.post(url,data = json.dumps(jsonforpost), headers=headers )
      reponse=x.json()
      print(x.text)
      #print(reponse["data"]["id"])
      print(reponse["status"])
      print(not reponse["status"]=="success")
      if not (reponse["status"]=="success"):
         result = {"pageID":pageID,"buyer":buyer,"chatby":{"user": name,"app_name": 
                    appn,"app_id": appid, "app_version":  appver },"message":mess,"many_contact": 
                     {"status": reponse["status"]},"status":0 }
         print("error")
         result = make_response(json.dumps(result)) 
         return result
      contact_id=reponse["data"]["id"]
      data_2 = {
              "subscriber_id":contact_id,
               "field_value": prodname,
               "field_name":  FieldString}
      #}["id", "created", "event", "affiliate", "id", "name", "name", "email", "phone"]}

      x1 =requests.post(url1,data = json.dumps(  data_2), headers=headers )
      reponse1=x1.json()
      print(x1.text)
      print(reponse1["status"])
      if not (reponse1["status"]=="success"):
         result = {"pageID":pageID,"buyer":buyer,"chatby":{"user": name,"app_name": 
              appn,"app_id": appid, "app_version":  appver },"message":mess,"many_contact": 
               {"status": reponse1["status"]},"status": 1}     
      data_2 = {
              "subscriber_id":contact_id,
                "field_name":   FieldArray,
               "field_value": [str(idj), int(created), str(event), str(affiliate),int( prodid),str(prodname),  str(N), str( email),str(pho)]
              }
      x2 =requests.post(url1,data = json.dumps(  data_2), headers=headers )
      reponse2=x2.json()
      print(x2.text)
      #result = {"pageID":pageID,"buyer":buyer,"app_name": appname, "app_passsword":apppwr, "app_token":token,"field strig": FieldString,"field array":FieldArray,"chatby":{"user":name,"app_name":appn,"app_id": appid, "app_version":  appver},"message":mess,"many_contact": {"status": reponse["status"],"contact_id": contact_id},"status": 1}  
      result= { "hotmart": {"pageID": pageID, "id":  idj,"creation_date": created,"event": event,
    "version": version,
    "data": {
      "affiliate": affiliate,
      "product": {
        "id": prodid,
        "name": prodname
      },
      "buyer": {
        "name": name,
        "email":  email,
        "phone": pho
      }
    }
  },
  "chatby": {
    "app_id": appid,
    "page_id": pageid,
    "app_name":   appn,
    "app_user":  appname,
    "app_token": token,
    "app_version": appver,
    "field_array": FieldArray,
    "field_string": FieldString,
    "app_passsword": apppwr,
    "status": "active",
    "message": mess,
    "end_date": enddate
  },
  "many_contact": {
    "status": reponse["status"],
    "contact_id": contact_id
  },
  "many_field_string": {
    "status": reponse1["status"]
  },
  "many_field_array": {
    "status": reponse2["status"]
  }
} 
  
      result = make_response(json.dumps(result))  
      return result
  def get(self):
      #return "Example with Flask-Restful"
      return result
    
#creating api endpoint
api.add_resource(Test, '/webhooks/cart-event')

if __name__ == "__main__":
  app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  
  #app.run(host='0.0.0.0', port='8080',debug=True)
  http_server = WSGIServer(('0.0.0.0', 8080), app)
  http_server.serve_forever()