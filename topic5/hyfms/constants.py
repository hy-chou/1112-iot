PIN_FRONT_MOTOR = 17  # 11 -> 17
PWM_FREQ = 50
STEP = 15
THROTTLE_SLOW = 0.82
THROTTLE_STOP = 0
DC_LEFT = 5
DC_RIGHT = 8.5
DC_CENTER = (DC_LEFT + DC_RIGHT) / 2
DC_L3 = DC_LEFT
DC_L2 = (DC_LEFT * 2 + DC_CENTER) / 3
DC_L1 = (DC_LEFT + DC_CENTER * 2) / 3
DC_R1 = (DC_RIGHT + DC_CENTER * 2) / 3
DC_R2 = (DC_RIGHT * 2 + DC_CENTER) / 3
DC_R3 = DC_RIGHT
CROP_TOP = 0
CROP_BOTTOM = 160
CROP_LEFT = 0
CROP_RIGHT = 640 - CROP_LEFT
CROP_AREA = (CROP_BOTTOM - CROP_TOP) * (CROP_RIGHT - CROP_LEFT)
IDEAL_POS = (CROP_RIGHT - CROP_LEFT) / 2
TIME_TURN90 = 3.6
TIME_GO45 = 1.2
TIME_TURN45 = 1.7
varBlurBlur_THRESHOLD = 129
FAR_COUNT_GAIN_MIN = 500
FAR_COUNT_GAIN_MAX = 4115
FAR_COUNT_GAIN_PREDICT_MIN = 800
