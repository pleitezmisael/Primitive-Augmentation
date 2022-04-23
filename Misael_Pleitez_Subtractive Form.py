
#*****************************************************************************
#Arch 431//Medium//Spring 2022//Ericson
#
#Misael Pleitez
#03.08.22
#
#Subtractive Forms with Primitive Geometry
#This project begins to use primitive geometry to subtract from a squared form. 
#
#Source:  
#Source:
#source:
#
#*****************************************************************************
#imported Libraries
#
import rhinoscriptsyntax as rs
import Rhino 
import System
import scriptcontext as sc
import math
import time
import random

import rhinoscriptsyntax as rs
from math import radians
#
#*****************************************************************************
#Functions:

def GetCaptureView(Scale,FileName,NewFolder):
    #Source: https://github.com/mcneel/rhino-developer-samples/blob/6/rhinopython/SampleViewCaptureToFile.py
    #Modified by Mark Ericson to include file/folder directory and scale. 2.18.21

    #this function saves the current viewport to the desktop in a specified folder as a png.
    #Use scale to scale up or down the viewport size to inccrease/ecrease resolution
    #Will overwrite folders and files with same name. 


    view = sc.doc.Views.ActiveView;
    if view:
        view_capture = Rhino.Display.ViewCapture()
        view_capture.Width = view.ActiveViewport.Size.Width*Scale
        view_capture.Height = view.ActiveViewport.Size.Height*Scale
        view_capture.ScaleScreenItems = False
        view_capture.DrawAxes = False
        view_capture.DrawGrid = False
        view_capture.DrawGridAxes = False
        view_capture.TransparentBackground = False
        bitmap = view_capture.CaptureToBitmap(view)
        if bitmap:
            #locate the desktop and get path
            folder = System.Environment.SpecialFolder.Desktop
            path = System.Environment.GetFolderPath(folder)
            #convert foldername and file name sto string
            FName = str(NewFolder)
            File = str(FileName)
            #combine foldername and desktop path
            Dir = System.IO.Path.Combine(path,FName)
            #creat path to tje new folder
            NFolder = System.IO.Directory.CreateDirectory(Dir)
            Dir = System.IO.Path.Combine(Dir,FileName +".png")
            print (Dir)
            #save the file
            bitmap.Save(Dir, System.Drawing.Imaging.ImageFormat.Png);


def SaveObj(Objects,FileName,NewFolder):


    #This function exports an obj file of whatever geometry is placed in to the objects position.
    #Mark Ericson 3.19.21

    rs.SelectObjects(Objects)
    
    folder = System.Environment.SpecialFolder.Desktop
    path = System.Environment.GetFolderPath(folder)
    #convert foldername and file name sto string
    FName = str(NewFolder)
    File = str(FileName)
    #combine foldername and desktop path
    Dir = System.IO.Path.Combine(path,FName)
    NFolder = System.IO.Directory.CreateDirectory(Dir)
    Dir = System.IO.Path.Combine(Dir,FileName +".obj")
    cmd = "_-Export " + Dir + " _Enter PolygonDensity=1 _Enter"
    rs.Command(cmd)


def SaveVariant():
    #save png and obj of current geometry
    
    views = rs.ViewNames()
    
    for view in views:
        rs.ViewDisplayMode(view,"Rendered")
        rs.ShowGrid(view,show=False)
        rs.ShowGridAxes(view,show=False)
        rs.ShowWorldAxes(view,show=False)
    
    
    Save = rs.GetString("Save View and Obj of file? Please set your view to desired position and hit y/n when ready?")
    
    if Save == "y": 
        
        rs.ZoomExtents()
        
        FolderName = rs.GetString("Pkease provide a name for the folder")
        FileName = rs.GetString("Please provide a name for the file")
        
        GetCaptureView(2,FileName,FolderName)
        
        objects = rs.AllObjects()
        Saveobj(Objects,FileName,FolderName)


def SaveImage():
    views = rs.ViewNames()
    

    for view in views:
        rs.ViewDisplayMode(view,'Rendered')
        rs.ShowGrid(view,show=False)
        rs.ShowGridAxes(view, show=False)
        rs.ShowWorldAxes(view, show=False)
    

    Save = rs.GetString("SaveImage and Obj?  Adjust your model to desired view. y/n")

    if Save == "y":

        rs.ZoomExtents()

        FileName = rs.GetString("Please Provide a File Name")
        FolderName = rs.GetString("Please Provide a Folder Name")

        GetCaptureView(2,FileName, FolderName)
        Objects = rs.AllObjects()
        SaveObj(Objects,FileName,FolderName)



def RotateOblique(RotateX, RotateZ):
    
    Rx = float(RotateX)
    Rz = float(RotateZ)
    
    rs.RotateView(None,2,angle = Rx)
    rs.RotateView(None,3, angle = Rz)
    
    print("your object has been rotated")

def RandomPoint(Number, MaxX, MaxY, MaxZ,Radius) :
    Plist = []
    Count = 0 
    Center = rs.AddPoint(MaxX/2,MaxY/2,MaxZ/2)
        
    while len(Plist) < Number :
        Count += 1  
        
        x = random.randint(0,float(MaxX))
        y = random.randint(1,float(MaxY))
        z = random.randint(0,float(MaxZ))
        
        point = rs.AddPoint(x,y,z)
        
        
        if rs.Distance(Center,point) < Radius:
            Plist.append(point)
        else:
            rs.DeleteObject(point)
    return(Plist)

#### I want to add in more geomtries to use besides a square#####

def square(Length):
    
    sL = Length
    Count1 = 0
    
    point1 = rs.AddPoint(0,0,0)
    point2 = rs.AddPoint(sL,0,0)
    point3 = rs.AddPoint(sL,sL,0)
    point4 = rs.AddPoint(0,sL,0)
    
    curve = rs.AddPolyline( [point1,point2,point3,point4,point1] )
    
    randomHeight = random.random()
    
    
    path = rs.AddLine([0,0,-Extrude],[0,0,0])
    square = rs.ExtrudeCurve(curve,path)
    solid = rs.CapPlanarHoles(square)
    

#def square(Length2):
#    
#    sL = Length2
#    Count1 = 0
#    
#    point5 = rs.AddPoint(150,150,0)
#    point6 = rs.AddPoint(sL,150,0)
#    point7 = rs.AddPoint(sL,sL,0)
#    point8 = rs.AddPoint(150,sL,0)
#    
#    curve2 = rs.AddPolyline( [point5,point6,point7,point8,point5] )
#    
#    randomHeight = random.random()
#    
#    
#    path = rs.AddLine([150,150,-Extrude],[150,150,0])
#    square = rs.ExtrudeCurve(curve2,path)
#    solid = rs.CapPlanarHoles(square)



#*****************************************************************************
#MAIN
#Place all functions to be called inside the Main() function.
#Call the Main function when complete50



######## Start of Python Script ##############
####### Random Points within a square #######


Extrude = rs.GetReal("Please provide desired height(From 10 to 150).",150,10)

Length = rs.GetReal("Please provide the Length of Square(From 100 to 150).",150,10)

Number = rs.GetInteger("Please provide the number of points(From 10 to 100).",100,10) 

#Extrude2 = rs.GetReal("Please provide desired height(From 10 to 150).",150,10)

#Length2 = rs.GetReal("Please provide the Length of Square(From 100 to 150).",150,10)

#Number2 = rs.GetInteger("Please provide the number of points(From 10 to 100).",100,10) 

#Radius = rs.GetReal("Please provide the radius for the primitive forms(From 5 to 15).",15,5)

All = rs.AllObjects()

rs.DeleteObjects(All)

square(Length)
#square(Length2)

P = RandomPoint(Number,Length,Length,Length,Length)

origin = rs.AddPoint(0,0,0)
height = rs.AddPoint(0,0,Length)
path = rs.AddLine(origin,height)

Inc = 255/(len(P))
Col = 0 
Col2 = 0
Col3 = 0
Col4 = 0 
Col5 = 0
paths = []
paths.append(path)
CY = []
REC = []
Con = []
Circ = []
Sp = []
Tor = []

#Random RGB Render material that is assigned to forms

for i in P:
    
    count = i
    Count2 = 0 
    Col += Inc
    RandomX = random.randint(-1,150)
    RandomY = random.randint(-1,150)
    RandomZ = random.randint(1,150)
    RandomR = random.uniform(0.0,254.0)
    RandomG = random.uniform(0.0,254.0)
    RandomB = random.uniform(0.0,254.0)
    
    
    RandomRad = random.randint(1,10)
    v = rs.VectorCreate((RandomX,RandomY,0),(0,45,45))
    Pl = rs.PlaneFromNormal(i,v)
    Cylinder = rs.AddCylinder(Pl,RandomZ,RandomRad)
    CY.append(Cylinder)
    NewCol = rs.CreateColor(RandomR,RandomG,RandomB)
    rs.AddMaterialToObject(Cylinder)
    NewCol2 = rs.CreateColor (RandomR,RandomG,RandomB)
    Index1 = rs.ObjectMaterialIndex(Cylinder)
    rs.MaterialColor(Index1,NewCol2)

Cone = []
for i in P:
    
    
    count = i
    Count3 = 0
    Col2 += Inc
    RandomX = random.randint(1,150)
    RandomY = random.randint(1,150)
    RandomZ = random.randint(1,150)
    
    RandomR = random.uniform(0.0,254.0)
    RandomG = random.uniform(0.0,254.0)
    RandomB = random.uniform(0.0,254.0)
    
    RandomRad = random.randint(1,10)
    v = rs.VectorCreate((RandomX,RandomY,RandomZ),(180,-90,270))
    Pl = rs.PlaneFromNormal(i,v)
    Con = rs.AddCone(Pl,-45,RandomRad)
    Cone.append(Con)
    rs.AddMaterialToObject(Con)
    NewCol2 = rs.CreateColor(RandomR,RandomG,RandomB)
    Index = rs.ObjectMaterialIndex(Con)
    rs.MaterialColor(Index,NewCol2)

Sphere = []
for i in P:
    
    
    count = i
    Count4 = 0
    Col3 += Inc
    RandomX = random.randint(0,5)
    RandomY = random.randint(-0,20)
    RandomZ = random.randint(0,25) 
    
    RandomR = random.uniform(0.0,254.0)
    RandomG = random.uniform(0.0,254.0)
    RandomB = random.uniform(0.0,254.0)
    
    RandomRad = random.randint(1,100)
    v = rs.VectorCreate((0,0,0),(RandomZ,RandomY,RandomZ))
    Pl = rs.PlaneFromNormal(i,v)
    Sp = rs.AddSphere(Pl,10)
    Sphere.append(Sp)
    NewCol = rs.CreateColor(RandomR,RandomG,RandomB)
    rs.AddMaterialToObject(Sp)
    NewCol3 = rs.CreateColor(RandomR,RandomG,RandomB)
    Index = rs.ObjectMaterialIndex(Sp)
    rs.MaterialColor(Index,NewCol3)

######### Creates Boolean variants within the form ############
#rs.Command("BooleanDifference")
rs.Command("BooleanUnion")
rs.Command("BooleanIntersection")
#rs.Command("Booleansplit")

######### Enables user to delete excess geometry #######
Delete = rs.GetObjects("Select geometry to delete")
rs.DeleteObjects(Delete)
##################

############## Contoru Model for Depth#############
rs.Command("Contour")
#####################

###########Rotate model##########
All = rs.GetObjects("Select geometry to rotate")
rs.Command("Rotate")
###################Shear model for axonometrics############
rs.Command("Shear")
######################


################# Begin to make drawings ####################
rs.Command("Make2D")
######################



########## Takes images to create composaition video#############

#time.localtime()
#count = 0
#while count < 1000:
#    count+=1
#    rs.Sleep(1)
#    
#    if count < 50:
#        rs.RotateView(direction = 1, angle = radians(-20))
#    
#    else:
#        rs.RotateView(direction = 1, angle = radians(-45))
#        rs.RotateView(direction = 2, angle = radians(-20))
#    
#    GetCaptureView(1,str("%04d"%count),"Pleitez_Misael_Final6")

#SavevVariant()
#print (Result)

