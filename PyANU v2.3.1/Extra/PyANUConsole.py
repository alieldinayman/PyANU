import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import numpy as np


class PyROV:

    def Crashmap(self):
        img = mpimg.imread('Lake Washington.PNG')
        imgplot = plt.imshow(img)

        heading, vASC, RoC, vDES, RoD, fail, windAng = 184, 93, 10, 64, 6, 43, 270  # RoC: RATE OF CLIMB, RoD: OF DECAY

        x_arr = []
        y_arr = []

        print('\nTaking off from "Naval" or "Renton"?')
        takeoff = input()

        if takeoff == 'Naval':
            x_arr.append(282.128)
            y_arr.append(761.84)
        elif takeoff == 'Renton':
            x_arr.append(350.805)
            y_arr.append(131.42)

        plt.ylim(0, 1040)  # INVERTING Y-AXIS WITHOUT INVERTING THE PIC

        # ASCENSION using vGS = cos(θ)∗vTAS+vwind
        print('\nASCENT\n')
        theta = math.degrees(math.atan(RoC / vASC))  # ANGLE OF ASCENDING
        vTAS = math.sqrt((RoC ** 2) + (vASC ** 2))  # VELOCITY OF TRUE AIR SPEED
        vGS = math.cos(theta * math.pi / 180) * vTAS  # VELOCITY OF GROUND SPEED
        dA = vGS * fail  # DISTANCE ASCENDED
        dAP = dA / 32.8  # DISTANCE IN PIXELS

        print('Plane covered ' + str(dA) + ' metres in ' + str(heading) + '° while ascending from take-off point')
        print('\nCoordinates on X: ' + str(x_arr[0] + math.sin(heading * math.pi / 180) * dAP))
        print('Coordinates on Y: ' + str(y_arr[0] + math.cos(heading * math.pi / 180) * dAP))

        print('\nMoved on X: ' + str(math.sin(heading * math.pi / 180) * dA) + ' metres and ' +
              str(math.sin(heading * math.pi / 180) * dAP) + ' pixels')
        print('Moved on Y: ' + str(math.cos(heading * math.pi / 180) * dA) + ' metres and ' +
              str(math.cos(heading * math.pi / 180) * dAP) + ' pixels')

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
        print('\nCoordinates on X: ' + str(x_arr[1] + math.sin(heading * math.pi / 180) * dDP))
        print('Coordinates on Y: ' + str(y_arr[1] + math.cos(heading * math.pi / 180) * dDP))

        print('\nMoved on X: ' + str(math.sin(heading * math.pi / 180) * dD) + ' metres and ' +
              str(math.sin(heading * math.pi / 180) * dDP) + ' pixels')
        print('Moved on Y: ' + str(math.cos(heading * math.pi / 180) * dD) + ' metres and ' +
              str(math.cos(heading * math.pi / 180) * dDP) + ' pixels')

        # WIND MOVEMENT
        print('\nWIND MOVEMENT\n')
        for i in range(int(fall + 1)):
            vW += -((1 / 720) * (i ** 2)) + 25

        vWP = vW / 32.8
        vWX = vWP * abs(math.sin(windAng * math.pi / 180))
        vWY = vWP * abs(math.cos(windAng * math.pi / 180))

        print('WIND COVERED ' + str(vW) + ' metres. On X: ' + str(vWX * 32.8) + ' metres & ' + str(
            vWX) + ' pixels, on Y: ' +
              str(vWY * 32.8) + ' metres & ' + str(vWY) + ' pixels.')

        x_arr.append(x_arr[1] + (math.sin(heading * math.pi / 180) * dDP) + vWX)
        y_arr.append(y_arr[1] + (math.cos(heading * math.pi / 180) * dDP) + vWY)

        plt.plot(x_arr, y_arr, 'ro-')
        plt.show(imgplot)

    def Seismo(self):
        '''x = np.array([0, 1.1, 1.3, 1.4, 1.5, 2, 2.2, 2.4, 2.6, 3, 3.1, 3.2, 3.3, 3.9])
        y = np.array([0, 0, 4.4, -4.3, 0, 0, 6.8, -7, 0, 0, 1.6, -1.6, 0, 0])'''
        x, y = [0]*16, [0]*16
        for i in range(16):
            data = input()
            datasplit = data.split()
            x[i] = float(datasplit[0])
            y[i] = float(datasplit[1])
        print(data)
        plt.xlabel('Time(s)')
        plt.ylabel('Amplitude')
        plt.plot(x, y, 'bo-')
        plt.grid(color='grey', linestyle='-', linewidth=0.5)
        plt.show()

    def Power(self):
        P, N, p, a, v, Cp = 0, 0, 0, 0, 0, 0

        print('\nInsert No. of Turbines')
        N = float(input())
        print('Insert the Density of the Water in kg/m^3')
        p = float(input())
        print('Insert the Radius of a Turbine in Metres')
        a = (float(input()) ** 2) * 3.14159
        print('Insert the Tide Strength in Knots')
        v = float(input()) * 0.51444
        print('Insert the Efficiency of the Turbines in %')
        Cp = float(input()) / 100

        P = (N * 0.5 * p * a * (v ** 3) * Cp) / (10 ** 6)
        print('Expected Power = ' + str(format(P, '.2f')) + 'MW')

    def Vertical(self):
        P1, P2, p, h = 0, 0, 0, 0
        print('\nInsert the Density of the Water in kg/m^3 at 20°C')
        p = float(input())
        print('Insert the Pressure at the Bottom point in Pascal')
        P2 = float(input())
        print('Insert the Pressure at the Top point in Pascal')
        P1 = float(input())

        '''P = ρgh'''
        h = (P2 - P1) / p * 9.81
        print('Distance between the two points= ' + str(format(h, '.2f')) + ' Metre(s)')

    def Horizontal(self):
        test_image = "Lake Washington.PNG"
        img = mpimg.imread(test_image)
        print('Enter known object distance in cm: ')
        ob_dis = int(input())
        NumberOfMouseClicks, x1, x2, y1, y2, distance_1, distance_2 = 0, 0, 0, 0, 0, 0, 0

        def onclick(event):
            x = event.xdata
            nonlocal NumberOfMouseClicks, x1, y1, x2, y2  #CHANGED FROM GLOBAL TO NONLOCAL
            print(event.xdata, event.ydata)
            if NumberOfMouseClicks == 0:
                x1 = x
            elif NumberOfMouseClicks == 1:
                y1 = x
            elif NumberOfMouseClicks == 2:
                x2 = x
            elif NumberOfMouseClicks == 3:
                y2 = x
                distance_1 = y1 - x1
                distance_2 = y2 - x2
                NumberOfMouseClicks = (-1)
                print('Unknown object distance = ', str(abs(ob_dis * distance_2 / distance_1)) + ' cm')
            NumberOfMouseClicks += 1

        fig, ax = plt.subplots()
        ax.plot(range(10))
        fig.canvas.mpl_connect('button_press_event', onclick)
        imgplot = plt.imshow(img)
        plt.show()


def main():
    ROV = PyROV()
    #ROV.Crashmap()
    ROV.Power()
    #ROV.Seismo()
    #ROV.Vertical()
    #ROV.Horizontal()


if __name__ == '__main__':
        main()
