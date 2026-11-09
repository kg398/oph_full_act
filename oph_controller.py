from dynamixel_controller import Dynamixel
from operator import add
import time
import kin
import numpy as np
from pynput import keyboard
import json

class controller():
    def __init__(self, port=False, dynxIDs=[], dynxLabels=[]):
        self.dynxIDs = dynxIDs
        self.dynxLabels = dynxLabels
        self.servo = Dynamixel(ID=dynxIDs, descriptive_device_name=dynxLabels, series_name=['xc']*len(dynxIDs), baudrate=1000000, port_name=port)

        self.current_set = 50

        self.servo.begin_communication(enable_torque=False)
        self.servo.set_operating_mode("current-based position","all")
        self.servo.write_current(self.current_set,ID="all")
        self.servo.enable_torque(ID="all")

        # self.servo.write_position(pos=0, ID=1)
        # self.servo.write_position(pos=1000, ID=1)

        self.h = kin.hand(imprt='hand_data.txt')

        self.pulley_radii = [-3,-3,-3,-3,-3,3,3,3,3,3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3]
        self.rad_to_enc = 4096/np.pi/2
        with open("calibration_data.json", "r") as f:
            self.extended_pos=json.load(f)

        self.zeroing()

        return

    ### calibration and mapping
    def zeroing(self):
        #self.zeros = self.servo.read_position(self.dynxIDs)
        self.zeros = self.extended_pos
        self.fingerDynxMapping = [[[],[],[],[],[]] for i in range(5)]
        self.fingerZeroMapping = [[[],[],[],[],[]] for i in range(5)]
        self.fingerLengthMapping = [[[],[],[],[],[]] for i in range(5)]

        for i in range(0, len(self.dynxLabels)):
            if 'index' in self.dynxLabels[i]:
                row = 0    
            if 'middle' in self.dynxLabels[i]:
                row = 1
            if 'ring' in self.dynxLabels[i]:
                row = 2
            # if 'little' in self.dynxLabels[i]:
            #     row = 3
            if 'thumb' in self.dynxLabels[i]:
                row = 3
            if 'fa' in self.dynxLabels[i]:
                column = 0
            if 'fb' in self.dynxLabels[i]:
                column = 1
            if 'ea' in self.dynxLabels[i]:
                column = 2
            if 'eb' in self.dynxLabels[i]:
                column = 3
            if 'ec' in self.dynxLabels[i]:
                column = 4
            self.fingerDynxMapping[row][column] = self.dynxIDs[i]
            self.fingerZeroMapping[row][column] = self.zeros[i]
            self.fingerLengthMapping[row][column] = self.rad_to_enc/self.pulley_radii[self.dynxIDs[i]-1]

        return

    def calibration(self):
        with open("calibration_data.json", "r") as f:
            self.extended_pos=json.load(f)
        #self.servo.write_position_list(self.extended_pos,ID="all")
        self.key = Key()
        demand_pos=self.servo.read_position("all")
        print("Start calibration position: ", demand_pos)
        print('Starting keyboard control\n1/q \t= \tfa \n2/w \t= \tfb\n3/e \t= \tea\n4/r \t= \teb\n5/t \t= \tec')
        
        for fingerID in range(0,4):
            print("finger {} start".format(fingerID))
            while self.key.keyPress!=keyboard.Key.esc:
                dist=50
                if self.key.keyPress=='1':
                    demand_pos[fingerID*5]+=dist
                elif self.key.keyPress=='q':
                    demand_pos[fingerID*5]-=dist
                elif self.key.keyPress=='2':
                    demand_pos[fingerID*5+1]+=dist
                elif self.key.keyPress=='w':
                    demand_pos[fingerID*5+1]-=dist
                elif self.key.keyPress=='3':
                    demand_pos[fingerID*5+2]+=dist
                elif self.key.keyPress=='e':
                    demand_pos[fingerID*5+2]-=dist
                elif self.key.keyPress=='4':
                    demand_pos[fingerID*5+3]+=dist
                elif self.key.keyPress=='r':
                    demand_pos[fingerID*5+3]-=dist
                elif self.key.keyPress=='5':
                    demand_pos[fingerID*5+4]+=dist
                elif self.key.keyPress=='t':
                    demand_pos[fingerID*5+4]-=dist
            
                self.servo.write_position_list(demand_pos,ID="all")
                time.sleep(0.001)
                
            print("Successfully calibrated finger {}".format(fingerID))
            while self.key.keyPress==keyboard.Key.esc:
                time.sleep(0.001)
            time.sleep(0.1)

        self.extended_pos=self.servo.read_position("all")
        with open('calibration_data.json','w') as f:
            json.dump(self.extended_pos, f, ensure_ascii=False)


        return

    def admittance(self, frame='home'):
        self.key = Key()

        current_set = 20
        kp_tension = 1
        kp_release = 0.5
        demand_current = [current_set]*20
        mapper = [None]*20
        err = [None]*20
        for i in range(0,20):
            mapper[i]=np.sign(self.pulley_radii[self.dynxIDs[i]-1])
        demand_current = np.multiply(demand_current,mapper)
        print(demand_current)
        pos = self.servo.read_position(ID="all")

        print("Start admittance mode")
        while self.key.keyPress!=keyboard.Key.esc:
            current = self.servo.read_current(ID="all")
            err = np.multiply(-1,np.add(current,demand_current))
            #print(np.multiply(-1,np.add(current,demand_current)))
            for i in range(0,20):
                if err[i]*mapper[i]<0:
                    err[i]=err[i]*kp_tension
                else:
                    err[i]=err[i]*kp_release
            pos = np.add(pos,err)
            print(current)
            self.servo.write_position_list(pos,ID="all")
            time.sleep(0.001)

        
        if frame=='home':
            self.extended_pos=self.servo.read_position("all")
            with open('calibration_data.json','w') as f:
                json.dump(self.extended_pos, f, ensure_ascii=False)
        else:
            with open(frame,'w') as f:
                json.dump(self.servo.read_position("all"), f, ensure_ascii=False)

        return

    def admittance2(self, frame='home'):
        self.key = Key()

        current_set = 20
        demand_current = [current_set]*20
        mapper = [None]*20
        for i in range(0,20):
            mapper[i]=np.sign(self.pulley_radii[self.dynxIDs[i]-1])
        demand_current = np.multiply(demand_current,mapper)
        
        self.servo.begin_communication(enable_torque=False)
        self.servo.set_operating_mode("current","all")
        self.servo.write_current_list(demand_current,ID="all")
        self.servo.enable_torque(ID="all")

        print("Start admittance mode")
        while self.key.keyPress!=keyboard.Key.esc:
            time.sleep(0.001)
        
        if frame=='home':
            self.extended_pos=self.servo.read_position("all")
            with open('calibration_data.json','w') as f:
                json.dump(self.extended_pos, f, ensure_ascii=False)
        else:
            with open(frame,'w') as f:
                json.dump(self.servo.read_position("all"), f, ensure_ascii=False)

        self.servo.begin_communication(enable_torque=False)
        self.servo.set_operating_mode("current-based position","all")
        self.servo.write_current(self.current_set,ID="all")
        self.servo.enable_torque(ID="all")

        return

    def home(self):
        self.servo.write_position_list(self.extended_pos,ID="all")
        return

    def write_frame(self, frame):
        with open(frame, "r") as f:
            demand_pos=json.load(f)
        self.servo.write_position_list(demand_pos,ID='all')
        return
        

    def all_abs_pos(self,pos):
        self.servo.write_position(pos,ID="all")
        return

    ### oph control
    def write_finger_joints(self, fingerID, thetas):
        Lfa, Lfb, Lea, Leb, Lec = self.h.fingers[fingerID].tendon_kin(thetas, start_thetas=[0,0,0,0])
        print(list(map(add,[Lfa*self.fingerLengthMapping[fingerID][0], Lfb*self.fingerLengthMapping[fingerID][1], Lea*self.fingerLengthMapping[fingerID][2], Leb*self.fingerLengthMapping[fingerID][3], Lec*self.fingerLengthMapping[fingerID][4]],self.fingerZeroMapping[fingerID])))
        self.servo.write_position_list(list(map(add,[Lfa*self.fingerLengthMapping[fingerID][0], Lfb*self.fingerLengthMapping[fingerID][1], Lea*self.fingerLengthMapping[fingerID][2], Leb*self.fingerLengthMapping[fingerID][3], Lec*self.fingerLengthMapping[fingerID][4]],self.fingerZeroMapping[fingerID])), self.fingerDynxMapping[fingerID])
        return





class Key():
    def __init__(self):
        self.keyPressLatching = None
        self._keyReleaseLatching = None
        self.keyPress = None
        self._start_keyboard_listener()
    def _on_press(self, key):
        try:
            self.keyPressLatching = key.char
            self.keyPress = key.char
        except AttributeError:
            self.keyPressLatching = key
            self.keyPress = key
    def _on_release(self, key):
        try:
            self._keyReleaseLatching = key.char
            if self._keyReleaseLatching == self.keyPress:
                self.keyPress = None
        except AttributeError:
            self._keyReleaseLatching = key
            if self._keyReleaseLatching == self.keyPress:
                self.keyPress = None
    def _start_keyboard_listener(self):
        listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        listener.start()
        print("keyboard listener started")