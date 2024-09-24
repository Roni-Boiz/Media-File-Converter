import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)

mongo_video = PyMongo(
    server,
    uri="mongodb://host.minikube.internal:27017/videos"
)
mongo_mp3 = PyMongo(
    server, 
    uri="mongodb://host.minikube.internal:27017/mp3s"
)

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    "rabbitmq",
    heartbeat=60
))
channel =  connection.channel()

channel.queue_declare(os.environ.get("VIDEO_QUEUE"), durable=True, exclusive=False)

### LOCALHOST to MINIKUBE RabbitMQ CONNECTION ###
# # Replace with your RabbitMQ service ClusterIP -> minikube service rabbitmq
# rabbitmq_host = '127.0.0.1'
# rabbitmq_port = 45915  # Default RabbitMQ port

# # Example credentials, adjust as per your setup
# credentials = pika.PlainCredentials('guest', 'guest')
# parameters = pika.ConnectionParameters(host=rabbitmq_host,
#                                        port=rabbitmq_port,
#                                        credentials=credentials)

# connection = pika.BlockingConnection(parameters)
# channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err

def reconnect_channel():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            "rabbitmq",
            heartbeat=60
        ))
        channel = connection.channel()
        return channel
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Connection failed: {e}")
        return None

@server.route("/upload", methods=["POST"])
def upload():
    global channel
    
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "only 1 file is allowed", 400

        # Reconnect if the channel is closed
        if channel is None or channel.is_closed:
            channel = reconnect_channel()
        
        for _, f in request.files.items():
            err = util.upload(f, fs_videos, channel, access)

            if err: 
                return err
            
        return "success!", 200
    
    else:
        return "not authorized", 401
    
@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400
        
        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f'convert_{fid_string}.mp3')

        except Exception as err:
            print(err)
            return "internal server error", 500

    return "not authorized", 401
    

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080, debug=True)