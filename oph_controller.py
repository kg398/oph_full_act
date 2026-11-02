from dynamixel_controller import Dynamixel
from operator import add
import kin
from numpy import pi

class controller():
    def __init__(self, port=False, dynxIDs=[], dynxLabels=[]):
        self.dynxIDs = dynxIDs
        self.dynxLabels = dynxLabels
        self.servo = Dynamixel(ID=dynxIDs, descriptive_device_name=dynxLabels, series_name=['xc']*len(dynxIDs), baudrate=57600, port_name=port)

        self.servo.begin_communication(enable_torque=False)
        self.servo.set_operating_mode("current-based position","all")
        self.servo.write_current(50,ID="all")
        self.servo.enable_torque(ID="all")

        # self.servo.write_position(pos=0, ID=1)
        # self.servo.write_position(pos=1000, ID=1)

        self.h = kin.hand(imprt='hand_data.txt')

        self.pulley_radii = [3]*len(dynxIDs)
        self.rad_to_enc = 4096/pi/2

        self.calibrate()

        return

    ### calibration and mapping
    def calibrate(self):
        self.zeros = self.servo.read_position(self.dynxIDs)
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
            if 'little' in self.dynxLabels[i]:
                row = 3
            if 'thumb' in self.dynxLabels[i]:
                row = 4
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
            self.fingerLengthMapping[row][column] = self.rad_to_enc/self.pulley_radii[i]

        return

    def all_abs_zero(self):
        self.servo.write_position(0,ID="all")

    ### oph control
    def write_finger_joints(self, fingerID, thetas):
        Lfa, Lfb, Lea, Leb, Lec = self.h.fingers[fingerID].tendon_kin(thetas, start_thetas=[0,0,0,0])
        print(list(map(add,[Lfa*self.fingerLengthMapping[fingerID][0], Lfb*self.fingerLengthMapping[fingerID][1], Lea*self.fingerLengthMapping[fingerID][2], Leb*self.fingerLengthMapping[fingerID][3], Lec*self.fingerLengthMapping[fingerID][4]],self.fingerZeroMapping[fingerID])))
        self.servo.write_position_list(list(map(add,[Lfa*self.fingerLengthMapping[fingerID][0], Lfb*self.fingerLengthMapping[fingerID][1], Lea*self.fingerLengthMapping[fingerID][2], Leb*self.fingerLengthMapping[fingerID][3], Lec*self.fingerLengthMapping[fingerID][4]],self.fingerZeroMapping[fingerID])), self.fingerDynxMapping[fingerID])
