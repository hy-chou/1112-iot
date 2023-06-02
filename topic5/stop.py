import board
from adafruit_motorkit import MotorKit as Kit

# rear motor
THROTTLE_SLOW = 0.8
THROTTLE_STOP = 0
DC_LEFT = 5
DC_CENTER = 7.25
DC_RIGHT = 8.5


kit = Kit(i2c=board.I2C())  # pi hat v.5, M2 L+R-

kit.motor1.throttle = THROTTLE_STOP
