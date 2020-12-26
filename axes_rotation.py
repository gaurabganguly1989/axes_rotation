#!/usr/bin/env python

# A basic rotation:
# The following three basic rotation matrices rotate vectors by an angle θ about
# the x-, y-, or z-axis, in three dimensions, using the right-hand rule

import os
import re
import numpy as np
from math import sin, cos, pi

def deg_to_rad(theta):
    return theta*(pi/180.0) 

def list_to_array(list):
    return np.array([list]).transpose() 

def main(old_coord, new_coord, thetax, thetay, thetaz):
    print('')
    print('              Axis Rotation Program ')
    print('Written by Gaurab Ganguly [gaurabganguly1989@gmail.com]')
    print('')
    print('Requested rotation around X-axis =', thetax)
    print('Requested rotation around X-axis =', thetay)
    print('Requested rotation around X-axis =', thetaz)
    print('')
    radx = deg_to_rad(thetax)  
    rady = deg_to_rad(thetay)  
    radz = deg_to_rad(thetaz)   

    Rx = [[ 1,  0,          0         ],
          [ 0,  cos(radx), -sin(radx) ],
          [ 0,  sin(radx),  cos(radx) ]] 

    Ry = [[ cos(rady),  0,  sin(rady) ],
          [ 0,          1,  0         ],
          [-sin(rady),  0,  cos(rady) ]] 

    Rz = [[ cos(radz), -sin(radz),  0 ],
          [ sin(radz),  cos(radz),  0 ],
          [ 0,          0,          1 ]] 

    Rxy = np.zeros((3,3), dtype=float) 
    Rxyz = np.zeros((3,3)) 
    # Rxyz = Rx*Ry*Rz = (Rx*Ry)*Rz
    for i in range(len(Rx)):
        for j in range(len(Ry[0])):
            for k in range(len(Ry)):
                Rxy[i][j] += float(Rx[i][k])*float(Ry[k][j])
    for i in range(len(Rxy)):
        for j in range(len(Rz[0])):
            for k in range(len(Rz)):
                Rxyz[i][j] += float(Rxy[i][k])*float(Rz[k][j])
    # print(Rxyz)

    if os.path.exists(old_coord):
        print('Initial Cartesian coordinates are read from: ', old_coord)
        pass
    else:
        raise FileNotFoundError("File {} NOT found, provide correct file name".\
                                format(old_coord))
    if os.path.exists(new_coord): 
        os.remove(new_coord)
    else:
        pass
    with open(old_coord, 'r') as rfile:
        with open(new_coord, 'a') as afile:
            afile.write(rfile.readline()) # natoms
            afile.write(rfile.readline()) # comment line 
        for line in rfile:
            if re.search(r'^\w+', line):
                if not line.isspace():
                    tmp = []
                    tmp.append(float(line.split()[1]))
                    tmp.append(float(line.split()[2]))
                    tmp.append(float(line.split()[3]))
                    old = list_to_array(tmp)
                    # print(old)
                    new = np.zeros((3,1), dtype=float)
                    for i in range(len(Rxyz)):
                        for j in range(len(old[0])):
                            for k in range(len(old)):
                                new[i][j] += float(Rz[i][k])*float(old[k][j])
                    with open(new_coord, 'a') as afile:
                        afile.write('{} {:> 10.6f} {:> 10.6f} {:>10.6f}\n' \
                        .format(line.split()[0], \
                        float(str(new[0]).strip("[]")), \
                        float(str(new[1]).strip("[]")), \
                        float(str(new[2]).strip("[]")))) 
    print('Final Cartesian coordinates are written to: ', new_coord)
    print('')

if __name__ == "__main__":
    import argparse, pathlib
    parser = argparse.ArgumentParser(description="This program rotates \
                                    molecular coordinate around X/Y/X axis")
    parser.add_argument('old_coord', type=pathlib.Path, metavar='1) OldFile.xyz',
                        help="Name of original .xyz file before rotation.")
    parser.add_argument('new_coord', type=pathlib.Path, metavar='2) NewFile.xyz',
                        help="Name of new .xyz file after rotation.")
    parser.add_argument('-tx',  '--thetax', type=float, \
                        metavar='[rotation X-axis]', required=True,
                        help="Angle of rotation around X-axis")
    parser.add_argument('-ty',  '--thetay', type=float, \
                        metavar='[rotation Y-axis]', required=True,
                        help="Angle of rotation around Y-axis")
    parser.add_argument('-tz',  '--thetaz', type=float, \
                        metavar='[rotation Z-axis]', required=True,
                        help="Angle of rotation around Z-axis")
    args = parser.parse_args()
    main(args.old_coord, args.new_coord, args.thetax, args.thetay, args.thetaz)

