from oph_controller import controller
import time

def main():
    # servo = Dynamixel(ID=[1,2], descriptive_device_name=['dynx_1','dynx_2'], series_name=['xm','xm'], baudrate=57600, port_name='COM3')

    # servo.begin_communication(enable_torque=False)
    # servo.set_operating_mode("extended position","all")
    # servo.enable_torque(ID="all")

    # servo.write_position(pos=0, ID=1)
    # servo.write_position(pos=1000, ID=1)
    oph = controller(port='COM15', dynxIDs=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], dynxLabels=['index_fa','index_fb','index_ea','index_eb','index_ec','middle_fa','middle_fb','middle_ea','middle_eb','middle_ec','ring_fa','ring_fb','ring_ea','ring_eb','ring_ec','thumb_fa','thumb_fb','thumb_ea','thumb_eb','thumb_ec'])

    oph.write_finger_joints(0,[0,0,0,0])

    time.sleep(1)

    oph.write_finger_joints(0,[0,0,0,1])

    time.sleep(1)

    oph.write_finger_joints(0,[0,0,0,0])

    #oph.all_abs_zero()

if __name__ == '__main__': main()
