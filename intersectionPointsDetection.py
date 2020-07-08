import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString


""" print(np.polyfit(x1, y1, 1))
print(np.polyfit(x2, y2, 1))
print(np.polyfit(x3, y3, 1))
 """


def solveTwoStraightLines(x1, y1, x2, y2):
    # make the fit
    m1, c1 = np.polyfit(x1, y1, 1)
    m2, c2 = np.polyfit(x2, y2, 1)

    # make linear system from y1 = mx1 + c to AX = b
    """
        - m1x + y = c1
        - m2x + y = c2
        hence,
        1 - m1     x   c1
        1 - m2     y   c2
    """

    A = np.array([[-m1, 1], [-m2, 1]])
    B = np.array([c1, c2])

    X = np.linalg.inv(A).dot(B)
    return X


def getPointsOfIntersections(straightLines):
    # straightLines is an array of the form:
    # [[x1, y1], [x2, y2], ... , [xn, yn]]

    intersectionPoints = []

    for i in range(len(straightLines)):
        currentLine = straightLines[i]
        for j in range(len(straightLines)):
            if j <= i:
                continue
            else:
                # i.e if j> i
                targetLine = straightLines[j]
                # find intersection of currentLine and targetLine iff there is a true visual intersection
                targetLineEntry_lastIndex = len(targetLine[0])-1
                targetLine_xInitial = targetLine[0][0]
                targetLine_yInitial = targetLine[1][0]
                targetLine_xFinal = targetLine[0][targetLineEntry_lastIndex]
                targetLine_yFinal = targetLine[1][targetLineEntry_lastIndex]

                currentLineEntry_lastIndex = len(currentLine[0])-1
                currentLine_xInitial = currentLine[0][0]
                currentLine_yInitial = currentLine[1][0]
                currentLine_xFinal = currentLine[0][currentLineEntry_lastIndex]
                currentLine_yFinal = currentLine[1][currentLineEntry_lastIndex]

                targetLineSegment = LineString(
                    [(targetLine_xInitial, targetLine_yInitial),
                     (targetLine_xFinal, targetLine_yFinal)]
                )
                currentLineSegment = LineString(
                    [(currentLine_xInitial, currentLine_yInitial),
                     (currentLine_xFinal, currentLine_yFinal)]
                )

                doesIntersect = targetLineSegment.intersects(
                    currentLineSegment)

                if(doesIntersect == True):
                    # perform the fit
                    currentPOI = solveTwoStraightLines(
                        currentLine[0], currentLine[1], targetLine[0], targetLine[1])
                    intersectionPoints.append(currentPOI)

    return intersectionPoints


# domains
x1 = np.arange(0, 10)
x2 = np.arange(-5, 2)
x3 = np.arange(-5, 5)
x4 = np.arange(-10, 10)

# parameters
m1 = 1
c1 = 10
m2 = -10
c2 = -10
m3 = 10
c3 = -20
m4 = 0
c4 = 0

# sample lines
y1 = m1*x1 + c1
y2 = m2*x2 + c2
y3 = m3*x3 + c3
y4 = m4*x4 + c4

# plotting
# plt.grid(True, which="both")
plt.axhline(y=0, color='lightgray')
plt.axvline(x=0, color='lightgray')
plt.plot(x1, y1)
plt.plot(x2, y2)
plt.plot(x3, y3)
plt.plot(x4, y4)


POI_all = getPointsOfIntersections([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
print(POI_all)


for i in range(len(POI_all)):
    poi = POI_all[i]
    plt.scatter(poi[0], poi[1], color="red")


plt.show()
