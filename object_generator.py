import rhinoscriptsyntax as rs
import Rhino 
import System
import scriptcontext as sc
import math
import time
import random 
from math import radians


def BoundingBox(bbox):
    bbox = rs.BoundingBox(bbox)
    
    
    rs.AddBox(bbox)

def RandomPoint(Number,bbox) :
    Plist = []
    Count = 0 
    
    MinXpt = rs.GetPoint("Please select left bottom coner")
    MinX = MinXpt[0]
    MinYpt = MinXpt
    MinY = MinYpt[1]
    MinZ = MinXpt[2]
    
    
    MaxXpt = rs.GetPoint("Please select right top coner")
    MaxX = MaxXpt[0]
    MaxYpt = MaxXpt
    MaxY = MaxYpt[1] 
    MaxZ = MaxXpt[2]
    
    Center = rs.AddPoint(int(MaxX+MinX)/2,int(MaxY+MinY)/2,int(MaxZ+MinZ)/2)
        
    while len(Plist) < Number :
        Count += 1  
        
        x = random.randint(int(MinX),int(MaxX))
        y = random.randint(int(MinY),int(MaxY))
        z = random.randint(int(MinZ),int(MaxZ))
        
        point = rs.AddPoint(x,y,z)
        
        
        if rs.Distance(Center,point) < object:
            Plist.append(point)
        else:
            rs.DeleteObject(point)
    return(Plist)

def object_generator(object_type, points):
    
    P = points
    Inc = 255/(len(P))
    Col = 0
    
    CY = []
    for i in P:
        count = i
        Count2 = 0 
        Col += Inc
        RandomX = random.randint(1,180)
        RandomY = random.randint(1,180)
        RandomZ = random.randint(1,180)
        RandomR = random.uniform(0.0,254.0)
        RandomG = random.uniform(0.0,254.0)
        RandomB = random.uniform(0.0,254.0)
        
        
        RandomRad = random.randint(1,5)
        v = rs.VectorCreate((RandomX,RandomY,RandomZ),(RandomY,RandomX,RandomY))
        Pl = rs.PlaneFromNormal(i,v)
        if object_type == "Cylinder":
            object = rs.AddCylinder(Pl,RandomZ,RandomRad)
        if object_type == "Cone":
            object = rs.AddCone(Pl,RandomZ,RandomRad)
        CY.append(object)
        NewCol = rs.CreateColor(RandomR,RandomG,RandomB)
        rs.AddMaterialToObject(object)
        NewCol2 = rs.CreateColor(RandomR,RandomG,RandomB)
        Index1 = rs.ObjectMaterialIndex(object)

def exclude_points(bbox, points):
    brep = rs.coercebrep(bbox)
    point_list = []
    for i in points:
        if brep.IsPointInside(i,.01,True) == False:
            point = rs.AddPoint(i)
            point_list.append(point)
            rs.EnableRedraw(False)
    return point_list


Object = rs.GetObjects("Select the objects")
bbox = BoundingBox(Object)

Number = rs.GetInteger("Please provide the number of points(From 10 to 100).",100,10)

R_Points = RandomPoint(Number,bbox)
new_points = exclude_points(bbox, R_Points)

P = object_generator("Cylinder",new_points)
P = object_generator("Cone",new_points)



