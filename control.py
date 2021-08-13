'''--------------------------------------------------------------
 File:    control.py
 Author:  Griffin Bonner      <griffi1@umbc.edu>                           
 Date:    8.3.2021
 Description: controlling process: receives NN-outputs, moves in 
 positive x-direction at specified velocity until NN-output 
 exceeds threshold, hovers in place, continues to move in 
 positive x-direction. 
--------------------------------------------------------------'''

# crazyflie dependencies 
import time
import logging
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# connection dependencies
from multiprocessing.connection import Listener

# crazyflie identifier
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')
logging.basicConfig(level=logging.ERROR)

# obstacle prediction threshold
THRESHOLD = 0.85

# crazyflie control algorithm 
def cf_controller():

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf
        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(2)

        # takeoff (0.8 meters)
        for y in range(20):
            cf.commander.send_hover_setpoint(0,0,0,y/25)
            time.sleep(0.1)

        # move forward (25 sec), hover if obstacle detected
        steps = 0
        while(steps <= 250): 
            inference = (cf_conn.recv() / 5)
            #print(inference)
            if (inference > THRESHOLD):
                cf.commander.send_hover_setpoint(0.0, 0.0, 0.0, 0.8)
                time.sleep(0.1)
            else:
                cf.commander.send_hover_setpoint(0.35, 0, 0, 0.8)
                steps += 1
                time.sleep(0.1)

        # land from (0.8 meters)
        for y in range(20):
            cf.commander.send_hover_setpoint(0, 0, 0, -y/25)
            time.sleep(0.1)


if __name__ == '__main__':

    # initialize low-level drivers 
    cflib.crtp.init_drivers()

    # connect to inference pipeline (stream.py)
    cf_rx = Listener(('localhost', 6000), authkey=b'crazyflie')
    cf_conn = cf_rx.accept()
    print('connection accepted from', cf_rx.last_accepted)

    # control crazyflie
    cf_controller()

    # close connection
    cf_rx.close()


