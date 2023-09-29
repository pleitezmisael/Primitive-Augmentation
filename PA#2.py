import rhinoscriptsyntax as rs
import random

def create_site_boundary():
    site_boundary = None
    
    while True:
        choice = rs.GetString("Choose site shape (Polyline or Rectangle):", "Polyline,Rectangle", "Polyline,Rectangle")
        
        if not choice:
            break
        
        if choice.lower() == "polyline":
            # Initialize an empty list to store polyline points
            points = []
            
            # Prompt the user to draw the polyline by clicking points
            print("Draw the site boundary by clicking points. Press Enter when finished.")
            
            while True:
                point = rs.GetPoint("Click a point for the site boundary")
                
                # Check if the user pressed Enter (point will be None) to finish drawing
                if point is None:
                    break
                
                points.append(point)
                rs.AddPoint(point)
            
            # Check if at least three points were collected
            if len(points) < 3:
                print("You must select at least three points to create a polyline.")
                continue
            
            # Close the polyline by connecting the last point to the first point
            points.append(points[0])
            
            # Add the closed polyline to the Rhino document
            site_boundary = rs.AddPolyline(points)
            
        
        elif choice.lower() == "rectangle":
            point_1 = (0, 0, 0)
            point_2 = rs.GetPoint("Click a corner point of the rectangle")
            
            
            plane = rs.CreatePlane(point_1)
            x_1, y_1, z_1 = point_1
            x_2, y_2, z_2 = point_2
            width = abs(x_1 - x_2)
            height = abs(y_1 - y_2)
            length = abs(z_1 - z_2)
            rs.AddRectangle(plane, width, height)
            site_boundary = rs.ExtrudeCurve(10,50)
            
    return site_boundary

def extrude_site_boundary(site_boundary):
    if site_boundary:
        if rs.IsPolyline(site_boundary):
            # Generate a random extrusion height between 10 and 30 units
            extrusion_height = random.uniform(10, 30)
            
            # Extrude the site boundary to create a closed Brep
            brep = rs.ExtrudeCurve(site_boundary, extrusion_height)
            
            if brep:
                print("Site boundary extruded to create a closed Brep.")
                return brep
    
    return None

def random_point_in_site_boundary(boundary, number):
    Plist = []
    
    if boundary is None:
        return Plist
    
    bounding_box = rs.BoundingBox(boundary)
    
    if not bounding_box:
        return Plist
    
    x_min, y_min, _, x_max, y_max, _ = bounding_box
    
    for _ in range(number):
        while True:
            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            point = rs.AddPoint(x, y, 0)
            
            if rs.IsPointInPlanarClosedCurve(point, boundary):
                Plist.append(point)
                break
    
    return Plist

def create_random_objects(points):
    objects = []
    
    for point in points:
        # Randomly choose an object type (Cylinder, Cone, Sphere)
        object_type = random.choice(["Cylinder", "Cone", "Sphere"])
        
        if object_type == "Cylinder":
            radius = random.uniform(1, 5)
            height = random.uniform(5, 20)
            obj = rs.AddCylinder(rs.MoveObject(point, [0, 0, height / 2]), height, radius)
        
        elif object_type == "Cone":
            radius = random.uniform(1, 5)
            height = random.uniform(5, 20)
            obj = rs.AddCone(rs.MoveObject(point, [0, 0, height / 2]), height, radius)
        
        elif object_type == "Sphere":
            radius = random.uniform(1, 5)
            obj = rs.AddSphere(point, radius)
        
        if obj:
            objects.append(obj)
    
    return objects

def main():
    site_boundary = create_site_boundary()
    
    if site_boundary is None:
        print("Script canceled.")
        return
    
    # Extrude the site boundary to create a closed Brep
    brep = extrude_site_boundary(site_boundary)
    
    if brep is None:
        print("Script canceled.")
        return
    
    num_points = 100
    
    random_points = random_point_in_site_boundary(brep, num_points)
    
    if random_points:
        objects = create_random_objects(random_points)
        print("{0} random objects created within the site boundary.".format(len(objects)))
    else:
        print("No valid points found within the site boundary.")

if __name__ == "__main__":
    main()
