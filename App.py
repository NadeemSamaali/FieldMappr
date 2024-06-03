import ElectricMap as em
# Print welcome message
print("\n: Welcome to FieldMappr :  ")
print("\n  The current build supports the visualization of\n  point charges, rods of charge and rings of charge. \n  More features coming soon .... \n\n  Designed by Nadeem Samaali\n\n  Type '# help' to get started\n")

E = em.E_map()

while True :
    try :
        u = input("# ")
        
        if u == 'help' :
            print("# Here's a table of currently supported commands\n")
            print("  point              Creates a point of charge on the map")        
            print("  rod                Creates a rod of charge on the map")
            print("  ring               Creates a ring of charge on the map\n")   
            print("  show               Shows the three dimensional vector field of the electric field")                
            print("  clear              Removes all charges from the test space\n")                              
            continue
        
        if u == "point" :
            P0 = input("# Insert the coordinates of the point charge, separated by a space as such 'x y z' : ")
            P1 = P0.split(' ')
            if len(P1) != 3 : raise ValueError("Only three dimensional numbers are supprted")
            p = (float(P1[0]),float(P1[1]),float(P1[2]))
            q = float(input('# Insert the charge value of the point charge : '))
            E.build_point(p, q)
            print('# Point charge added to map\n')
            continue
       
        if u == 'rod' :
            P00 = input("# Insert the coordinates of the first end of the rod, separated by a space as such 'x y z' : ")
            P01 = P00.split(' ')
            if len(P01) != 3 : raise ValueError("Only three dimensional numbers are supprted")
            p1 = (float(P01[0]),float(P01[1]),float(P01[2]))
            P10 = input("# Insert the coordinates of the last end of the rod, separated by a space as such 'x y z' : ")
            P11 = P10.split(' ')
            if len(P11) != 3 : raise ValueError("Only three dimensional numbers are supprted")
            p2 = (float(P11[0]),float(P11[1]),float(P11[2]))
            q = float(input('# Insert the charge value of the point charge (C) : '))
            E.build_rod(p1,p2,q,0.1)
            print('# Rod added to map\n')
            continue
        
        if u == 'ring' :
            P00 = input("# Insert the coordinates of the ring's center, separated by a space as such 'x y z' : ")
            P01 = P00.split(' ')
            if len(P01) != 3 : raise ValueError("Only three dimensional numbers are supprted")
            p1 = (float(P01[0]),float(P01[1]),float(P01[2]))
            P10 = input("# Insert the components the ring's normal vector, separated by a space as such 'a b c' : ")
            P11 = P10.split(' ')
            if len(P11) != 3 : raise ValueError("Only three dimensional numbers are supprted")
            p2 = (float(P11[0]),float(P11[1]),float(P11[2]))
            r = float(input('# Insert the radius of the ring (m) : '))
            q = float(input('# Insert the charge value of the point charge (C) : '))
            E.build_ring(p1,p2,r,q)
            print('# Ring added to map \n')
            continue
       
        if u == "show" :
            print('# Loading...\n')
            E.show_map()
            continue
        if u == 'clear' :
            E.charge_map.clear()
            print('# Map cleared\n')
            continue
        else :
            raise ValueError('Command does not exist')
    except ValueError as e :
        print(f'# ERROR : {e}')