# specification
Provide a simple interface for a battery used motor with limit switches for both directions.
The circuit should work as a simple state machine, which moves in the desired direction until a sensor of the matching direciton is triggered. Commands should mainly be sent over serial/network.

# power
Charging should primarily be controlled based on battery state. eg, charge if battery voltage has gone below 50% V/cell and stop when above 90%.
|pin |function    |
|----|------------|
|ADC0|VBat        |
|IO4|Charge      |

in addition this block should have external connectors for:
* battery with temperature sensor
* dc power for battery charger

There should be an option to bypass the whole charging circuitry for using external dc power or non rechargeable batteries.

## battery charger
* [BQ25172DSGR](https://www.ti.com/lit/ds/symlink/bq25172.pdf)

# motion
The sensors should provide information on which direction (H-bridge input) is allowed.
|pin |function    |
|----|------------|
|IO14|motor A|
|IO12|motor B|
|IO13|Sensor 1 (A ok)|
|IO15|sensor 2 (B ok)|

Connectors should be separated in to the following gropus:
* motor
* sensor 1 with VBAT
* sensor 2 with VBAT

# interface
|pin |function    |
|----|------------|
|IO2|ok LED (green)|
|IO0|Error LED (red)|
|IO16|button (wake)|
|IO3|RX|
|IO1|TX|

Pressing the button should set the state machine to move in an allowed direction or continue in the previous direction if both are allowed. If in an error state the button should soft reset the device.
separate connector should be provided for:
* serial
* user button & leds (optional)

# links
* [info on esp8266 pins](https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/)