import rhinoscriptsyntax as rs
import Rhino 
import System
import scriptcontext as sc
import math
import time
import random 
from math import radians
from scriptcontext import doc

def RandomPoint(Number, MaxX, MaxY, MaxZ) :
    Plist = []
    Count = 0 
    while len(Plist) < Number :
        Count += 1  

        x = random.randint(0,float(MaxX))
        y = random.randint(1,float(MaxY))
        z = random.randint(1,float(MaxZ))
        
        point = rs.AddPoint(x,y,z)
 
        Plist.append(point)
 
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

def draw_site():
    
    point_1 = (0,0,0)
    point_2 = rs.GetPoint()
    
    
    plane = rs.CreatePlane(point_1)
    
    
#    corners = rs.GetPolyline()
#    
#    if corners:
#        point_1 = rs.GetPoints("Select a points to site.")
#        if point_1: rs.AddPolyline(point_1)
#        plane = rs.PlaneFromPoints(corners[0], corners[1], corners[2])
#        
    
    
    x_1, y_1, z_1 = point_1[0], point_1[1], point_1[2]
    x_2, y_2, z_2 = point_2[0], point_2[1], point_2[2]
    
    width  = abs(x_1 - x_2)
    height = abs(y_1 - y_2)
    length = abs(z_1 - z_2)
    
    rs.AddRectangle(plane, width, height)
    
    
    
    return(int(width), int(height))
#    return(point_1,int(height))


def object_generator(object_type, points ,Length):
    
   
    Min_Radius = int(Length/16)
    Max_Radius = int(Length/8)
    
    List_objects =[]
    
    for i in points:
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
        #this line of code will always place objects inside the circulation region. Try to fix
        v = rs.VectorCreate((RandomZ2,RandomY2,RandomZ2),(RandomX,RandomY,RandomZ))
        Pl = rs.PlaneFromNormal(i,v)
        
        if object_type == "Cylinder":
            Cylinder = rs.AddCylinder(Pl,25,RandomRad)
            List_objects.append(Cylinder)
        if object_type == "Cone":
            Cone = rs.AddCone(Pl,25,RandomRad)
            List_objects.append(Cone)
        if object_type == "Sphere":
            Sphere = rs.AddSphere(Pl,RandomRad)
            List_objects.append(Sphere)
            
    

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

def exclude_circulation(object, points):
    
    new_points = []
    brep = rs.coercebrep(object)
    for i in points:
        if brep.IsPointInside(i,.01,True) == False:
             
             
             
            new_point = rs.AddPoint(i)
            new_points.append(new_point)
            rs.EnableRedraw(False)
    return new_points


  


def vector_from_object(object, point_outside):
    
    centroid = rs.SurfaceVolumeCentroid(object)
    if centroid:
        new_point = rs.AddPoint(centroid[0])
        vector = rs.VectorCreate(point_outside, new_point)
    return(vector)

#main
##################################################
def main():
    message = rs.MessageBox("This program builds a randomized AR experienced based on site conditions. To begin you must have a closed BREP representing the space you would like to occupy. Are you ready?", 1, "Augmented Repetition")
    if message == 1:
        message2 = rs.MessageBox("Create your own Site Boundary! The site has to be a closed polyline to continue.",1)
        width, height = draw_site()
        
        
#        if message2 == 1:
#            point_1 = draw_site()
    
        if message == 1:
            message2 == rs.MessageBox("Select a space to exclude from the form. This will be the space that you move through.",1)
            circulation =  rs.GetObject("Select object")
        
        
            Cylinder = []
            Cone = []
            Sphere = [] 
            Length = 100
        
            point_list = RandomPoint(100,width,height,height)
#        point_list = RandomPoint(100,point_1,height,height)
            points = rs.coerce3dpointlist(point_list)
            new_points = exclude_circulation(circulation,points)
#        rs.DeleteObjects(circulation)
        
        
        Objects_Cylinder = object_generator("Cylinder",new_points,Length)
        Cylinder.extend(Objects_Cylinder)
        Objects_Cone = object_generator("Cone",new_points,Length)
        Cone.extend(Objects_Cone)
        Objects_Sphere = object_generator("Sphere",new_points,Length)
        Sphere.extend(Objects_Sphere)
        
        
        
        ###### Color #######
        ColorCylinder = gradientcolor(Cylinder)
        ColorCone = gradientcolor(Cone)
        ColorSphere = gradientcolor(Sphere)
        
        
    else:
        pass
        
        rs.DeleteObject(points)



main()


