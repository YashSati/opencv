import cv2 as cv
import numpy as np

path = r"C:\Users\DELL\Desktop\Rubiks cube\INPUT\1.jpeg"
filepath = r"C:\Users\DELL\Desktop\text.txt"
file = open(filepath, 'w')
matrix = {}

colors = {"GREEN" : ([43,60,47],[103,255,255]),
          "RED"   : ([0,55,0],[10,255,255]),
          "BLUE"  : ([82,51,0],[170,255,255]),
          "ORANGE": ([8,58,0],[17,255,255]),
          "YELLOW": ([17,58,0],[60,255,255]),
          "WHITE" : ([13,0,63],[56,22,221])}

img = cv.imread(path)
img1 = img.copy()

def getcontours(str,img,img1):
    contours, heirarchy = cv .findContours(img1, cv .RETR_EXTERNAL, cv .CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        peri = cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
        if area<800:
            continue

        x, y, w, h = cv.boundingRect(approx)
        val = (x//150,y//150)
        matrix[val] = str

        col = (0,0,0)
        if str == 'GREEN':
            col=(0,255,0)
        elif str == 'RED':
            col=(0,0,255)
        elif str == 'BLUE':
            col=(255,0,0)
        elif str == 'YELLOW':
            col=(0,255,255)
        elif str == 'ORANGE':
            col=(0,165,255)
        elif str == 'WHITE':
            col=(255,255,255)

        org = (x+h//4-4,y+w//2-4)
        cv.putText(img,str,org,cv.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),1)
        cv.rectangle(img, (x,y), (x + w, y + h), col, 3)

    return img

def getcolor(str,img,imgg):
    val = colors[str]

    min = np.array(val[0])
    max = np.array(val[1])

    mask = cv.inRange(img, min, max)
    ret, thrash = cv.threshold(mask, 55, 255, cv.THRESH_BINARY)
    imgg = getcontours(str,imgg,thrash)

    return imgg

def funx(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 100, 255, cv.THRESH_BINARY_INV)[1]
    cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    rect = cv.minAreaRect(cnts[0])
    box = np.int0(cv.boxPoints(rect))
    cv.drawContours(image, [box], 0, (36, 255, 12), 3)
    width = int(rect[1][0])
    height = int(rect[1][1])
    src_pts = box.astype("float32")
    dst_pts = np.array([[0, height - 1],
                        [0, 0],
                        [width - 1, 0],
                        [width - 1, height - 1]], dtype="float32")
    M = cv.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv.warpPerspective(
        image, M, (width, height))  # will be used further
    warped = cv.resize(warped, (480, 480))

    if rect[2]>45:
        warped = cv.rotate(warped, cv.cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif rect[2]< -45:
        warped = cv.rotate(warped, cv.cv2.ROTATE_90_CLOCKWISE)
    warped[:, 0:4, :] = 0
    warped[:, warped.shape[0] - 4:, :] = 0
    warped[0:4, :, :] = 0
    warped[warped.shape[1] - 3:, :, :] = 0
    warped = cv.resize(warped,(480,480))

    return warped

def funx1(a):
    pass

img1 = funx(img)

img2 = img1.copy()
img1 = cv.cvtColor(img1,cv.COLOR_BGR2HSV)

for clrs in colors:
    img2 = getcolor(clrs,img1,img2)

cv.imshow('OUTPUT',img2)

for i in range(3):
    for j in range(3):
        text = "({},{}) : {}\n".format(i,j,matrix[(i,j)])
        file.write(text)
        print(text)

cv.waitKey(0)