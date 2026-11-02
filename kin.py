import numpy as np
import time
import serial
import socket
import math
from math import pi
import import_hand as ih

class hand():
    def __init__(self, fingers=False, imprt=False):
        if fingers!=False:
            self.fingers=fingers
        elif imprt!=False:
            self.load_hand(imprt)
            default_labels=['index','middle','ring','little','thumb']
            nfingers = len(self.h['bl'])
            self.fingers = []
            for i in range(0,nfingers):
                self.fingers.append(finger(self.h['bl'][i], self.h['jd'][i], self.h['o'][i], self.h['a'][i], self.h['ap'], default_labels[i]))
        else:
            print("No hand data")
            exit
        return

    ### hand import
    def load_hand(self, filename):
        self.h = ih.load_hand_config(filename)

    ### finger setup


class finger():
    def __init__(self, bl, jd, o, a, ap, fID=False):
        self.id=fID
        self.bl=bl
        self.jd=jd
        self.o=o
        self.a=a
        self.ap=ap

        return

    ### finger kinematics
    def joint_kin(self, thetas):
        x = [0,0,0];
        y = [0,0,0];
        phi = [0,0,0];

        ## joint angles to tendon lengths
        for i in range(0,3):
            l1 = self.jd[i]
            l2 = self.jd[i]/2
            x[i] = self.jd[i]/2*(2*np.sin(thetas[i]/2)+np.cos(thetas[i])-1)+l2*np.sin(thetas[i])
            y[i] = self.jd[i]/2*(2*np.cos(thetas[i]/2)-np.sin(thetas[i]))+l1+l2*np.cos(thetas[i])
            phi[i] = np.arctan2(x[i],y[i])
        
        return x, y, phi

    def tendon_kin(self, thetas, start_thetas):
        [x,y,phi] = self.joint_kin(thetas)
        [startx,starty,start_phi] = self.joint_kin(start_thetas)

        ## change in tendon lengths driven by thetas
        Lfa = (np.sqrt(x[0]*x[0] + y[0]*y[0]) + np.sqrt(x[1]*x[1] + y[1]*y[1]) + np.sqrt(x[2]*x[2] + y[2]*y[2])) - (np.sqrt(startx[0]*startx[0] + starty[0]*starty[0]) + np.sqrt(startx[1]*startx[1] + starty[1]*starty[1]) + np.sqrt(startx[2]*startx[2] + starty[2]*starty[2]))
        Lfb = (np.sqrt(x[0]*x[0] + y[0]*y[0]) + np.sqrt(x[1]*x[1] + y[1]*y[1])) - (np.sqrt(startx[0]*startx[0] + starty[0]*starty[0]) + np.sqrt(startx[1]*startx[1] + starty[1]*starty[1]))
        Lea = self.jd[0]/2*(thetas[0]-start_thetas[0]) + self.jd[1]/2*(thetas[2]-start_thetas[2])
        Leb = self.jd[1]/2*(thetas[1]-start_thetas[1]) + self.jd[3]/2*(thetas[3]-start_thetas[3])
        Lec = self.jd[1]/2*(thetas[1]-start_thetas[1]) - self.jd[3]/2*(thetas[3]-start_thetas[3])

        return Lfa, Lfb, Lea, Leb, Lec

    def finger_kin(self, thetas):
        x_tip = self.jd[0]*np.sin(thetas[0]/2) + (b[0]-self.jd[0]/2-self.jd[1]/2)*np.sin(thetas[0]) + self.jd[1]*np.sin(thetas[0]+thetas[1]/2) + (b[1]-self.jd[1]/2-self.jd[2]/2)*np.sin(thetas[0]+thetas[1]) + self.jd[2]*np.sin(thetas[0]+thetas[1]+thetas[2]/2) + (b[2]-self.jd[2])*np.sin(thetas[0]+thetas[1]+thetas[2])
        y_tip = self.jd[0]*np.cos(thetas[0]/2) + (b[0]-self.jd[0]/2-self.jd[1]/2)*np.cos(thetas[0]) + self.jd[1]*np.cos(thetas[0]+thetas[1]/2) + (b[1]-self.jd[1]/2-self.jd[2]/2)*np.cos(thetas[0]+thetas[1]) + self.jd[2]*np.cos(thetas[0]+thetas[1]+thetas[2]/2) + (b[2]-self.jd[2])*np.cos(thetas[0]+thetas[1]+thetas[2])
        z_tip = y_tip*np.sin(thetas[3])
        y_tip = y_tip*np.cos(thetas[3])

        return x_tip, y_tip, z_tip

    def finger_inverse_kin(self, x, y, z, theta_dip=False, method='minE'):
        if method=='minE':
            #solve for minimum 'energy'
            thetas = [0,0,0,0]
        if method=='dip_constrained':
            #regular solve with dip angle defined
            thetas = [0,0,0,0]

        return thetas
