from oph_controller import controller
import time

def main():
    # init oph controller: serial port ID, dynamixel IDs mapped to tendon names
    oph = controller(port='COM15', dynxIDs=[5,9,12,17,18,4,8,19,13,14,3,7,15,20,1,2,6,16,10,11], dynxLabels=['index_fa','index_fb','index_ea','index_eb','index_ec','middle_fa','middle_fb','middle_ea','middle_eb','middle_ec','ring_fa','ring_fb','ring_ea','ring_eb','ring_ec','thumb_fa','thumb_fb','thumb_ea','thumb_eb','thumb_ec'])

    # turn on admittance control (ends when you press ESC), if frame name is kept empty, last position frame is stored to home (calibration_data.json)
    oph.admittance()

    # alternative calibration method stepping individual motor positions (last position frame saved to calibration_data.json)
    # oph.calibration()

    # return to home position stored in 'calibration_data.json'. 
    oph.home()

    # position control is non-blocking, the code here doesn't currently know if the move has finished
    time.sleep(1)

    # turn on admittance control and store final frame in json. Note this is stored in absolute position, not relative to home
    # oph.admittance(frame='test.json')

    # go to position stored in json
    # oph.write_frame('test.json')

    # oph.admittance(frame='test6.json')

    # oph.write_frame('test.json')

    # control finger joint angles with forward kinematics for loaded hand data (initialised in oph_controller/self.h = kin.hand(imprt='hand_data.txt'))
    # fingerID 0--3=index, middle, ring, thumb; thetas=[mcp,pip,dip,abduction]
    oph.write_finger_joints(fingerID=0,thetas=[0,0.8,0,0])
    time.sleep(1)

    # alternative control options reading and writing individual or all servos
    # demand_pos = oph.servo.read_position(ID='all')
    # demand_pos[15]+=2000
    # demand_pos[1]+=500
    # oph.servo.write_position_list(demand_pos,ID='all')
    # time.sleep(2)

    # try to end on or near home for safe startup next time
    oph.home()

if __name__ == '__main__': main()
