from umqtt.simple import MQTTClient
from machine import idle, Pin
import network
from motor import motor

mtr = motor()

with open("train.json", 'r') as f:
    import json
    config = json.load(f)

train_id = config["name"]

#connect to wlan
wlan = network.WLAN(network.STA_IF)
wlan.config(dhcp_hostname = train_id)
wlan.active(True)
wlan.connect(config["wifi"], config["wifi_pass"])
while not wlan.isconnected():
    idle()

#interfacing
def set_direction(direction):
    global move_dir
    
     #forwards
    if direction > 0 and state == "stopped":
        print("moving")
        move_dir = 0b10
    
    #reverse
    elif direction < 0 and state == "stopped":
        print("moving")
        move_dir = 0b01

    #stop
    else:
        print("stopping")
        setState("stopping")

def message(topic, msg):
    print(f"{topic} {msg}")
    t = topic.decode()
    m = msg.decode()
        
    if t == train_topic+"/move":
        print("move")
        set_direction(int(m))

#mqtt
train_topic = f"beertrain/train/{train_id}"

m = MQTTClient(train_id, config["mqtt_server"])
m.set_callback(message)
m.keepalive = 60 #fixes invalid argument error on connect
m.connect()
m.subscribe(train_topic+"/move")

#state machine
move_dir = 0b00
stops = 0b00
state = None

def setState(new_state):
    global state
    state = new_state
    m.publish(f"{train_topic}/state", state)
    print("new state")

def stopped():
    global move_dir
    global stops
    #check if current direction is allowed
    if move_dir ^ stops:
        mv = ((move_dir>>1) & 0b1) - (move_dir & 0b01)
        print(mv)
        mtr.move( mv ) #subtract reverse direction from forward direction
        setState("leaving")

def leaving():
    if not stops:
        setState("moving")

def moving():
    global move_dir
    global stops
    #check for a stop in current direction
    if stops & move_dir:
       setState("stopping")

def stopping():
    global move_dir
    move_dir = 0b00
    mtr.move(0)
    setState("stopped")

def runStates():
    #get stop status
    #stops = pina<<1|pinb #high if stop present?

    # run states
    states[state]()

states = {
    "stopped":stopped,
    "leaving":leaving,
    "moving":moving,
    "stopping":stopping
}

m.publish(f"{train_topic}", "hello")
setState("stopped")
print(state)
while True:
    m.check_msg()
    runStates()
