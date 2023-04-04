import os.path
import tempfile
import image2text as im2t
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage ,ImageMessage

# Connect line to project (Under change your token and channel secret)
channel_access_token = "V9tkUBeoDhjSsZyxSWkPpNIHu7jBxDtwBK7GMmuJ+hr9jEHiRH/EpMnt7EeZU9sNHpANBKXdSFHgxQLl2M4WcJNWueknK7UP+UBXwWb6gMnCXtxjSx4wTPuCbZ/HFYGfmPfMwcScGBghW/8KQi3aNwdB04t89/1O/w1cDnyilFU="
channel_secret = "3e1a7e400022296a4f2d75ed2afd22b0"

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

#Copy code from training line chat bot course
@app.route("/", methods=["GET", "POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    return "Hello Line Chatbot"


@handler.add(MessageEvent, message=ImageMessage)
def handle_text_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp').replace("\\", "/")
    print(static_tmp_path)

    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='jpg' + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
    dist_path = tempfile_path + '.jpg'
    #dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    text_out = "Saved"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=text_out))
    print("saved")
    tsend = im2t.image2text(dist_path)
    print(tsend)

    #Use event.source.user_id because reply_token can use one time
    line_bot_api.push_message(event.source.user_id, TextMessage(text=tsend))

    #remove used image
    os.remove(dist_path)
    print("removed")

if __name__ == "__main__":
    app.run(debug=True) #debug=True #continuous run while changing code
