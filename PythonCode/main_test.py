import RPi.GPIO as GPIO
import time

from move import CarMove
from ultrasound import CarUltrasound
from infrared import CarInfrared

GPIO.setwarnings(False)  # Disable warning
GPIO.setmode(GPIO.BCM)  # BCM coding 

class Car(CarMove, CarUltrasound, CarInfrared):  # create class Car, which derives all the modules
    def __init__(self):
        CarMove.__init__(self)
        CarUltrasound.__init__(self)
        CarInfrared.__init__(self)


if __name__ == '__main__':
    try:
        car = Car() 

        car.motor_1.start(0)  # motors start
        car.motor_4.start(0)
        car.motor_5.start(0)
        car.motor_6.start(0)

        dist_list = []

        while True:
            dist = car.disMeasure()
            dist_list.append(dist)
            if len(dist_list) > 5:  dist_list.pop(0)
            dist_ave = sum(dist_list)/len(dist_list)  # For error reduction, using the moving average of distance measured by ultrasonic module 
            print('Distance', dist_ave)

            [left_measure, right_measure] = car.InfraredMeasure()

            if left_measure == 0 and right_measure == 1:
                print("Going right")
                car.right(80)
            elif left_measure == 1 and right_measure == 0:
                print("Going left")
                car.left(80)
            elif left_measure == 0 and right_measure == 0:
                print("Going back")
                car.back(50)
            else:
                if dist_ave < 15:
                    car.left(80)
                    time.sleep(1)
                elif dist_ave < 100:
                    car.forward(dist_ave/2 + 40)
                else:
                    car.forward(90)




    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()