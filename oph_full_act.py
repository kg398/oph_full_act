from oph_controller import controller
import time

def main():
    # servo = Dynamixel(ID=[1,2], descriptive_device_name=['dynx_1','dynx_2'], series_name=['xm','xm'], baudrate=57600, port_name='COM3')

    # servo.begin_communication(enable_torque=False)
    # servo.set_operating_mode("extended position","all")
    # servo.enable_torque(ID="all")

    # servo.write_position(pos=0, ID=1)
    # servo.write_position(pos=1000, ID=1)
    oph = controller(port='COM15', dynxIDs=[5,9,12,17,18,4,8,19,13,14,3,7,15,20,1,2,6,16,10,11], dynxLabels=['index_fa','index_fb','index_ea','index_eb','index_ec','middle_fa','middle_fb','middle_ea','middle_eb','middle_ec','ring_fa','ring_fb','ring_ea','ring_eb','ring_ec','thumb_fa','thumb_fb','thumb_ea','thumb_eb','thumb_ec'])

    # oph.write_finger_joints(0,[0,0,0,0])

    # time.sleep(1)

    # oph.write_finger_joints(0,[0,0,0,1])

    # time.sleep(1)

    # oph.write_finger_joints(0,[0,0,0,0])

    #oph.all_abs_pos(2048)

    #oph.home()

    # time.sleep(0.5)

    # oph.write_finger_joints(0,[0,0,0,0.5])

    # time.sleep(0.5)

    # oph.write_finger_joints(0,[0,0,0,-0.5])

    # time.sleep(0.5)

    # oph.write_finger_joints(0,[-0.5,0,0,0])

    # time.sleep(0.5)

    # oph.write_finger_joints(0,[0.5,0.5,0.5,0])

    oph.home()

    #time.sleep(1)

    #oph.admittance()

    ##oph.admittance(frame='test.json')

    #oph.admittance(frame='test2.json')

    #oph.admittance(frame='test3.json')

    #oph.admittance(frame='test4.json')

    # oph.write_frame('test6.json')

    # oph.admittance(frame='test6.json')

    # oph.write_frame('test.json')

    time.sleep(2)

    oph.write_frame('test2.json')

    time.sleep(2)

    oph.write_frame('test5.json')

    time.sleep(2)

    oph.write_frame('test4.json')

    time.sleep(2)

    oph.write_frame('test3.json')

    time.sleep(2)

    # oph.write_frame('test6.json')

    # time.sleep(2)

    # demand_pos = oph.servo.read_position(ID='all')

    # demand_pos[15]+=2000
    # demand_pos[1]+=500

    # oph.servo.write_position_list(demand_pos,ID='all')

    #time.sleep(2)

    oph.home()

    #oph.calibration()

    time.sleep(2)

    oph.write_finger_joints(0,[0,0.8,0,0])
    time.sleep(0.1)
    oph.write_finger_joints(1,[0.8,0.6,0.6,0])
    time.sleep(0.1)
    oph.write_finger_joints(2,[0.8,0.6,0.6,0])
    time.sleep(0.1)
    oph.write_finger_joints(3,[0.8,0.6,0.6,0])
    time.sleep(0.1)
    oph.write_finger_joints(0,[0,0,0,0])
    time.sleep(0.1)
    oph.write_finger_joints(1,[0,0,0,0])
    time.sleep(0.1)
    oph.write_finger_joints(2,[0,0,0,0])
    time.sleep(0.1)
    oph.write_finger_joints(3,[0,0,0,0])
    time.sleep(0.1)
    oph.write_finger_joints(0,[0,0.8,0.8,0])
    time.sleep(0.1)
    oph.write_finger_joints(1,[0.8,0.6,0.6,0])
    time.sleep(0.1)
    oph.write_finger_joints(2,[0.8,0.6,0.6,0])
    time.sleep(0.1)
    oph.write_finger_joints(3,[0.8,0.6,0.6,0])
    time.sleep(0.1)
    oph.write_finger_joints(0,[0,0,0,0])
    time.sleep(0.1)
    oph.write_finger_joints(1,[0,0,0,0])
    time.sleep(0.1)
    oph.write_finger_joints(2,[0,0,0,0])
    time.sleep(0.1)
    oph.write_finger_joints(3,[0,0,0,0])
    time.sleep(0.5)

    oph.home()

if __name__ == '__main__': main()
