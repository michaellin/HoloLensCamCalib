import sys
import numpy as np
import struct
import yaml

if (len(sys.argv) == 2):
  # Parameters to extend printing floating precision
  np.set_printoptions(suppress=True)
  np.set_printoptions(precision=4)
  np.set_printoptions(formatter={'float_kind': '{: 0.4f}'.format})

  # Read calibration parameters from readFileName
  readFileName = sys.argv[1] + ".yaml"
  # Dump this parameters into .dat file which can be used by HoloLens ARToolkit
  outFileName = sys.argv[1] + ".dat"

  fileIn = open(readFileName, 'rb')
  fileOut = open(outFileName, 'wb')

  yobj = yaml.load(fileIn)

  temp_mat = yobj['camera_matrix']
  [x.append(0) for x in temp_mat]
  cam_mat = np.array(temp_mat)
  dc = yobj['dist_coeff'][0]

  xsize = yobj['width']
  ysize = yobj['height']
  k1 = dc[0]
  k2 = dc[1]
  p1 = dc[2]
  p2 = dc[3]
  fx = cam_mat[0][0]
  fy = cam_mat[1][1]
  x0 = cam_mat[0][2]
  y0 = cam_mat[1][2]
  s = 1.0 # what is this last one? Does it matter?
  try:
    fileOut.write(struct.pack(">2i", xsize, ysize))
    fileOut.write(struct.pack(">12d", *cam_mat.reshape(-1).tolist()))
    fileOut.write(struct.pack(">9d", k1, k2, p1, p2, fx, fy, x0, y0, s))
  finally:
    fileIn.close()
    fileOut.close()
else:
  print("Usage: > python ARToolKitYAML2DATCalib.py [filename]")
