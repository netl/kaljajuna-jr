from umqtt.simple import MQTTClient
from machine import idle,lightsleep, Pin
import network
from motor import motor

RLED = Pin(15, Pin.OUT)
GLED = Pin(13, Pin.OUT)
stop_fw = Pin(0, Pin.IN, Pin.PULL_UP)
stop_rw = Pin(2, Pin.IN, Pin.PULL_UP)

RLED.on()
GLED.off()

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
    global state
    global move_dir

    if state != "stopped":
        return
    
     #forwards
    if direction > 0:
        move_dir = 0b10
    
    #reverse
    elif direction < 0:
        move_dir = 0b01

    #stop
    else:
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
    if move_dir and  move_dir ^ (move_dir & stops):
        mv = ((move_dir>>1) & 0b1) - (move_dir & 0b01)
        print(mv)
        mtr.move( mv ) #subtract reverse direction from forward direction
        setState("leaving")
        m.publish(f"{train_topic}/stops", str(stops))
        m.publish(f"{train_topic}/dir", str(move_dir))

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
    m.publish(f"{train_topic}/stops", str(stops))
    move_dir = 0b00
    mtr.move(0)
    setState("stopped")

def runStates():
    #get stop status
    #stops = pina<<1|pinb #high if stop present?
    global stops
    stops = stop_fw.value()<<1 | stop_rw.value()

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
RLED.off()
try:
    while True:
        GLED.on()
        m.check_msg()
        runStates()
        GLED.off()
        lightsleep(100)
except Exception as E:
    GLED.off()
    import sys
    sys.print_exception(E)
    while True:
        RLED.on()
        lightsleep(100)
        RLED.off()
        lightsleep(100)
