'''--------------------------------------------------------------
 File:    dyn_control.py
 Author:  Griffin Bonner      <griffi1@umbc.edu>                           
 Date:    8.22.2021
 Description: controlling process: receives NN-outputs, moves in 
 positive x-direction at specified velocity modulated by the low
 pass filtered network prediction. 
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

# maximum drone velocity (m/s)
VEL_MAX = 0.40

# filter coefficient
ALPHA = 0.85

def cf_velocity(v_k1, alpha, inference):
    v_k = (1-alpha)*v_k1 + alpha*(1-inference)*VEL_MAX
    return v_k

# crazyflie control algorithm 
def cf_controller():

    v_k1 = 0

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

            v_k = cf_velocity(v_k1, ALPHA, cf_conn.recv()/5)
            cf.commander.send_hover_setpoint(v_k, 0, 0, 0.8)
            v_k1 = v_k
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