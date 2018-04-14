import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import numpy as np
import scipy.integrate
import sys

from PIL import Image
import pyscreenshot as ImageGrab

NewCapture = True #USED FOR SELECTING WHETHER THE HORIZONTAL FUNCTION WILL
                  #SCREENSHOT A NEW IMAGE OR USE THE LAST EXISTING ONE.

class PyANU:

    def Crashmap(self, takeoff, heading, vASC, RoC, vDES, RoD, fail, windAng, windSpd):
        img = mpimg.imread('Lake Washington.PNG')
        imgplot = plt.imshow(img)

        #heading, vASC, RoC, vDES, RoD, fail, windAng = 184, 93, 10, 64, 6, 43, 270  # RoC: RATE OF CLIMB, RoD: OF DECAY

        x_arr = []
        y_arr = []

        #print('\nTaking off from "Naval" or "Renton"?')
        #takeoff = input()

        if takeoff == 'Naval':
            x_arr.append(282.128)
            y_arr.append(761.84)
        elif takeoff == 'Renton':
            x_arr.append(350.805)
            y_arr.append(131.42)

        plt.ylim(0, 1040)  # INVERTING Y-AXIS WITHOUT INVERTING THE PIC

        # ----------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------

        # ASCENSION using vGS = cos(θ)∗vTAS+vwind
        print('\nASCENT\n')
        theta = math.degrees(math.atan(RoC / vASC))  # ANGLE OF ASCENDING
        vTAS = math.sqrt((RoC ** 2) + (vASC ** 2))  # VELOCITY OF TRUE AIR SPEED
        vGS = math.cos(theta * math.pi / 180) * vTAS  # VELOCITY OF GROUND SPEED
        dA = vGS * fail  # DISTANCE ASCENDED
        dAP = dA / 32.8  # DISTANCE IN PIXELS

        print('Plane covered ' + str(dA) + ' metres in ' + str(heading) + '° while ascending from take-off point')
        #print('\nCoordinates on X: ' + str(x_arr[0] + math.sin(heading * math.pi / 180) * dAP))
        #print('Coordinates on Y: ' + str(y_arr[0] + math.cos(heading * math.pi / 180) * dAP))

        print('\nMoved on X: ' + str(math.sin(heading * math.pi / 180) * dA) + ' metres')
        print('Moved on Y: ' + str(math.cos(heading * math.pi / 180) * dA) + ' metres')

        x_arr.append(x_arr[0] + math.sin(heading * math.pi / 180) * dAP)
        y_arr.append(y_arr[0] + math.cos(heading * math.pi / 180) * dAP)

        # ----------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------

        # DESCENT using vGS = cos(θ)∗vTAS+vwind
        print('\nDESCENT\n')
        vW = 0
        height = RoC * fail
        fall = height / RoD  # 71 secs
        theta = math.degrees(math.atan(RoD / vDES))  # ANGLE OF ASCENDING
        vTAS = math.sqrt((RoD ** 2) + (vDES ** 2))  # VELOCITY OF TRUE AIR SPEED
        vGS = math.cos(theta * math.pi / 180) * (vTAS + vW)  # VELOCITY OF GROUND SPEED
        dD = vGS * fall  # DISTANCE ASCENDED
        dDP = dD / 32.8  # DISTANCE IN PIXELS

        print('Plane covered ' + str(dD) + ' metres in ' + str(heading) + '° while descending from engine fail point')
        #print('\nCoordinates on X: ' + str(x_arr[1] + math.sin(heading * math.pi / 180) * dDP))
        #print('Coordinates on Y: ' + str(y_arr[1] + math.cos(heading * math.pi / 180) * dDP))

        print('\nMoved on X: ' + str(math.sin(heading * math.pi / 180) * dD) + ' metres')
        print('Moved on Y: ' + str(math.cos(heading * math.pi / 180) * dD) + ' metres')

        # ----------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------

        # WIND MOVEMENT
        print('\nWIND MOVEMENT\n')
        #for t in range(int(fall + 1)):
        #    vW += eval(windSpd)

        f = lambda t:eval(windSpd)
        vW = scipy.integrate.quad(f, 0, fall)

        print("\nvW: " + str(vW))

        vX = vW[0]
        vY = vW[1]

        vWX = vW[0] / 32.8 #X ON THE WORLD MAP IN PIXELS
        vWY = vW[1] / 32.8 #Y ON THE WORLD MAP IN PIXELS
        
        if (vY < 0.5): #FOR THE 270 WIND ANGLE SPECIAL CASE
            vY = 0

        print('On X: ' + str(vX) + ' metres' '\nOn Y: ' + str(vY) + ' metres')

        # ----------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------

        #TOTAL MOVEMENT
        print("\nTotal Movement: ")
        totalX = vX + (math.sin(heading * math.pi / 180) * dD) + (math.sin(heading * math.pi / 180) * dA)
        totalY = vY + (math.cos(heading * math.pi / 180) * dD) + (math.cos(heading * math.pi / 180) * dA)
        print("On X: " + str(totalX))
        print("On Y: " + str(totalY))
        print("\nReported Search Zone: " + str(((totalX**2)+(totalY**2))**0.5) + " meters, in direction: "
              + str(math.degrees(math.atan(totalX/totalY)) + 180) + " degrees from " + str(takeoff) + " point.")

        x_arr.append(x_arr[1] + (math.sin(heading * math.pi / 180) * dDP) + vWX)
        y_arr.append(y_arr[1] + (math.cos(heading * math.pi / 180) * dDP) + vWY)

        plt.plot(x_arr, y_arr, 'ro-')
        plt.show(imgplot)

    def Power(self, N, p, a, v, Cp):
        a = (float(a) ** 2) * 3.14159
        v = float(v) * 0.51444
        Cp = float(Cp) / 100

        P = (N * 0.5 * p * a * (v ** 3) * Cp) / (10 ** 6)
        print('Expected Power = ' + str(format(P, '.2f')) + 'MW')
        return str(format(P, '.2f'))

    def Vertical(self, p, P2, P1):
        '''P = ρgh'''
        h = (P2 - P1) / p * 9.81
        print('Distance between the two points= ' + str(format(h, '.2f')) + ' Metre(s)')
        return str(format(h, '.2f'))

    def Horizontal(self, ob_dis):
        if NewCapture is True:
            capture = ImageGrab.grab(bbox=(20, 80, 1050, 870))
            capture.save("Capture.png", "PNG")
        test_image = "Capture.png"
        img = mpimg.imread(test_image)
        NumberOfMouseClicks, x1, x2, y1, y2, distance_1, distance_2 = 0, 0, 0, 0, 0, 0, 0

        def onclick(event):
            x = event.xdata
            nonlocal NumberOfMouseClicks, x1, y1, x2, y2  #CHANGED FROM GLOBAL TO NONLOCAL
            print(event.xdata, event.ydata)

            #REFERENCE OBJECT
            if NumberOfMouseClicks == 0:
                x1 = x
            elif NumberOfMouseClicks == 1:
                y1 = x

            #STARTING POINT
            elif NumberOfMouseClicks == 2:
                x2 = x

            #UPDATE POINTS
            else:
                y2 = x
                distance_1 = y1 - x1
                distance_2 = y2 - x2
                #NumberOfMouseClicks = (-1)
                global objdist
                objdist = abs(ob_dis * distance_2 / distance_1)
                print('Unknown object distance = ', str(abs(ob_dis * distance_2 / distance_1)) + ' cm')
                #plt.close('all')
               
            NumberOfMouseClicks += 1

        fig, ax = plt.subplots()
        ax.plot(range(10))
        fig.canvas.mpl_connect('button_press_event', onclick)
        imgplot = plt.imshow(img)
        plt.show()
        plt.close()
        return format(objdist, '.2f')


def main():
    ROV = PyANU()
    #ROV.Crashmap()
    #ROV.Power()
    #ROV.Seismo()
    #ROV.Vertical()
    #ROV.Horizontal()


if __name__ == '__main__':
        main()
