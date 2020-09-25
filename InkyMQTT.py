import paho.mqtt.client as mqtt

from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw

font_ttf = "/home/pi/RA/RubikR.ttf" # add font
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)
text1 = ImageFont.truetype(font_ttf, 20)
text2 = ImageFont.truetype(font_ttf, 40)
text3 = ImageFont.truetype(font_ttf, 25)
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# The callback for when the client receives a CONNACK response from the server.
#def on_connect(client, userdata, flags, rc):
#    print("Connected with result code "+str(rc))
#def on_publish(client, userdata, mid):
#    print("mid: "+str(mid))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    weight_split = msg.payload.split(".", 1)
    num_front = weight_split[0]
    num_rear = weight_split[1]
    print(num_front + "." + num_rear)

    message2 = num_front
    w2, h2 = font2.getsize(message2)
    x2 = (inky_display.WIDTH / 5)
    y2 = (inky_display.HEIGHT / 2) - (h2 / 2)

    message3 = "." + num_rear
    w3, h3 = font3.getsize(message3)
    x3 = (inky_display.WIDTH / 5) + x2 + 5
    y3 = (inky_display.HEIGHT / 2) - h3 + (h2 / 2)

    draw.text((0, 0), "title", inky_display.BLACK, text1)
    draw.text((x2, y2), message2, inky_display.RED, text2)
    draw.text((x3, y3), message3, inky_display.RED, text3)

    flipped = img.rotate(180)
    inky_display.set_image(flipped)
    inky_display.show()

    exit()

broker_address = "192.168.1.2" #MQTT broker IP
client = mqtt.Client("instance_id") #create new instance
#client.on_connect = on_connect
#client.on_publish = on_publish
client.on_message = on_message

client.username_pw_set("username", "password") #login detail, comment out if no use
client.connect(broker_address, 1883) #connect to broker
client.subscribe("mqtt/topic")

client.loop_forever()
