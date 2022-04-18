import rhinoscriptsyntax as rs
import Rhino 
import System
import scriptcontext as sc
import math
import time
import random 
from math import radians


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

def RandomPointPlane(Number, MaxY, MaxZ,Radius,distance) :
    Plist = []
    Count = 0 
    Center = rs.AddPoint(distance,MaxY/2,MaxZ/2)
    X_point = float(0 + distance)
    
    while len(Plist) < Number :
        Count += 1  
        
        x = X_point
        y = random.randint(1,float(MaxY))
        z = random.randint(0,float(MaxZ))
        
        point = rs.AddPoint(x,y,z)
        
        
        if rs.Distance(Center,point) < Radius:
            Plist.append(point)
        else:
            rs.DeleteObject(point)
    return(Plist)

def square(Length,Plane):
    
    sL = Length
    Xlength = Length*Plane/2
    Count1 = 0
    
    point1 = rs.AddPoint(0,0,0)
    point2 = rs.AddPoint(0,0,sL)
    point3 = rs.AddPoint(0,sL,sL)
    point4 = rs.AddPoint(0,sL,0)
    
    curve = rs.AddPolyline( [point1,point2,point3,point4,point1] )
    
    randomHeight = random.random()


def LinearColor(R,G,B,R2,G2,B2,ColorPercentage):
    
    #This function defines linear color gradient by treating R,G,B as coordinates on a 3D line.
    #The base color that will be altered by the percentage should be entered in the second R2,G2,B2 valu
    
    Rdiff = R2 - R
    Gdiff = G2 - G
    Bdiff = B2 - B


    t = ColorPercentage


    R3 = float(R + Rdiff*t)
    G3 = float(G + Gdiff*t)
    B3 = float(B + Bdiff*t)



    return (R3,G3,B3)


def object_generator(object_type, points ,Length):
    
   
    Min_Radius = int(Length/16)
    Max_Radius = int(Length/8)
    
    List_objects =[]
    
    for i in P:
        count = i
        Count2 = 0 
        
        ###Random variable
        RandomX = random.randint(1,Length)
        RandomY = random.randint(1,Length)
        RandomZ = random.randint(1,Length)
        RandomX2 = random.randint(-Length*2,Length*2)
        RandomY2 = random.randint(-Length*2,Length*2)
        RandomZ2 = random.randint(-Length*2,Length*2)
        RandomRad = random.randint(Min_Radius,Max_Radius)
        ###
        
        ###Objects
        v = rs.VectorCreate((RandomZ2,RandomY2,RandomZ2),(RandomX,RandomY,RandomZ))
        Pl = rs.PlaneFromNormal(i,v)
        
        if object_type == "Cylinder":
            Cylinder = rs.AddCylinder(Pl,RandomZ2,RandomRad)
            List_objects.append(Cylinder)
        if object_type == "Cone":
            Cone = rs.AddCone(Pl,RandomY,RandomRad)
            List_objects.append(Cone)
        if object_type == "Sphere":
            Sphere = rs.AddSphere(Pl,RandomRad)
            List_objects.append(Sphere)
        ####
        
        
        

    return List_objects

def gradientcolor(List_objects):
    
    ####Color
    RandomR = random.uniform(0.0,255)
    RandomG = random.uniform(0.0,255)
    RandomB = random.uniform(0.0,255)
    RandomR2 = random.uniform(0.0,255)
    RandomG2 = random.uniform(0.0,255)
    RandomB2 = random.uniform(0.0,255)
    
    
    Inc = 255/(len(List_objects))
    Col = 0
    ColorVal = []
    Colors = []
    
    
    for i in range(len(List_objects)):
        Col += Inc/255
        ColorVal.append(Col)
        Color = LinearColor(RandomR,RandomG,RandomB,RandomR2,RandomG2,RandomB2,ColorVal[i])
        Colors.append(Color)
        Mat = rs.AddMaterialToObject(List_objects[i])
        rs.ObjectColor(List_objects[i],Colors[i])
        rs.MaterialColor(Mat,Colors[i])

    return List_objects

def Polyline_circulation(Polyline):
    
    Polyline = rs.AddPolyline(Polyline)
    pipe = rs.Command("Pipe")

#############################################
Extrude = rs.GetReal("Please provide desired height(From 10 to 250).",250,10)
Length = rs.GetReal("Please provide the Length of Square(From 100 to 250).",250,10)
Number = rs.GetInteger("Please provide the number of points(From 10 to 100).",100,10)
Plane = rs.GetInteger("Please provide number for planes(Min = 1)", 1)
######################


######################
All = rs.AllObjects()
rs.DeleteObjects(All)
######################

square(Length,Plane)


Cylinder = []
Cone = []
Sphere = [] 

###########Loop of geometry in X amount of planes###########
for i in range(Plane):
    
    #RandomPointPlane(Number, MaxY, MaxZ,Radius,distance)
    
    distance = i*(Length/2)
    
    P = RandomPointPlane(Number,Length,Length,Length,distance)
    
    Objects_Cylinder = object_generator("Cylinder",P,Length)
    Cylinder.extend(Objects_Cylinder)
    Objects_Cone = object_generator("Cone",P,Length)
    Cone.extend(Objects_Cone)
    Objects_Sphere = object_generator("Sphere",P,Length)
    Sphere.extend(Objects_Sphere)
    


####################
ColorCylinder = gradientcolor(Cylinder)
ColorCone = gradientcolor(Cone)
ColorSphere = gradientcolor(Sphere)

####################

Polysurface = rs.ObjectsByType(16,select=True)
Surface = rs.ObjectsByType(8,select=True)
Hide = rs.HideObjects(Polysurface)
Hide = rs.HideObjects(Surface)

####################

############# Polyline created to make circulation##########
Polyline = rs.GetPoints("Please select points to create circulation")
#Curve_circulation(Curve,MaxX,MaxY,MaxZ)
############################################################
Polyline_circulation(Polyline)
##########################################################

rs.ShowObjects(Polysurface)
rs.ShowObjects(Surface)

rs.Command("BooleanDifference")
