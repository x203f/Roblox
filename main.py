import os.path
import pickle
import random
import string
import threading
from flask import Flask, request, jsonify
randomemail = lambda: random.choice(open("SavedEmails.txt", "r").read().split("\n"))
def randemail():
  em = randomemail()
  print(em)
  getc = lambda: open("UsedEmails.txt", "r").read().split("\n")
  if em in getc():
     #  print("Used")
      return randemail()
  else:
     #  print("Not used",randomemail)
      return em
app = Flask('')
def make_current_maker_Session(sessionid):
    with open("current_session.data",'wb') as f:
        f.write(sessionid.encode())
        f.close()
def get_current_maker_Session():
    try:
        with open("current_session.data",'rb') as f:
            return f.read().decode()
    except:
        return -2
class sessionDatas:
    def __init__(self,cookie):
        if cookie == None:
            self.cookies = []
        else:
            self.cookies = [cookie]
    def push(self,cookie):
        self.cookies.append(cookie)

        for i, v in enumerate(self.cookies):
            if i == None:
               # print("IS NONE")
                del self.cookies[i]
            try:
                if self.cookies[i][8]["name"].lower() == '.roblosecurity':
                   # print("Has cookies")
                    continue
            except IndexError:
                del self.cookies[i]
            except:
                del self.cookies[i]


def create_session():
    id = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits,k=15))
    if not os.path.exists("sessions"):
        os.mkdir("sessions")
    with open( os.path.join("sessions" , "{}.pkl".format(id)),'wb') as f:
        pickle.dump(sessionDatas(None),f)
    make_current_maker_Session(id)
    return id
@app.route('/')
def home():
    return "<h>Error not found</h>"

@app.route('/roblox/create_session', methods=['POST'])
def start_session():
    id = create_session()
    return jsonify({"newId": id}), 200
@app.route('/roblox/current_session', methods=['GET'])
def get_session():
    if get_current_maker_Session() != -2:

        return open(os.path.join("sessions" , "{}.pkl".format(get_current_maker_Session())),'rb'),200
    else:
        return "File was not found", 400
@app.route('/roblox/current_id', methods=['GET'])
def get_id():

    if get_current_maker_Session() != -2:

        return jsonify({"id": get_current_maker_Session()}), 200
    else:
        return "File was not found", 400
@app.route('/alive')
def alive():
    return "IM ALIVE BRO", 200
@app.route('/roblox/set_session_content', methods=['POST'])
def set_con():
    try:
        idd = get_current_maker_Session()
        try:
            with open(os.path.join("sessions" , "{}.pkl".format(idd)),'wb') as f:
                f.write(request.data)
        except Exception as err:
            return jsonify({'success': False ,'reason': err}),500
        return jsonify({'success': True}), 200
    except Exception as err:
        return jsonify({"success":False, "reason": err})

@app.route('/start_session', methods=['POST'])
def get_email():
    return jsonify({"email": randemail(),"username":""}), 200
def run():
       app.run(host='0.0.0.0',port=8080)
def keep():
   thr = threading.Thread(target=run)
   thr.start()

if __name__ == '__main__':
    keep()