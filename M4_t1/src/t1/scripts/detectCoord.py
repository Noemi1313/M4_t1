#!/usr/bin/env python
# Obtener las coordenadas de un objeto de color verde con la webcam
# Noemi Carolina Guerra Montiel - A00826944

# Librerias
# OpenCV
import cv2
# ROS
import rospy
from std_msgs.msg import Float64MultiArray
# Uso de lib de c++
import ctypes
# Adicionales
import numpy as np
import time


class m4_t1:
  """
    Clase para obtener las coordenadas de un objeto de color verde usando la webcam.

    Attributes:
        mylib (ctypes.CDLL): Biblioteca en C++ para multiplicar las coordenadas por 100.
        funct (ctypes.CFUNCTYPE): Función de la biblioteca en C++ para multiplicar las coordenadas por 100.
        pub (rospy.Publisher): Publicador de los datos de coordenadas y tiempo.
    """

  def __init__(self):
    """
        Inicializa una instancia de la clase m4_t1.
    """
    # Libreria en c++ para multiplicar las coordenadas *100
    path = "/home/noemi/M4/src/t1/lib/libmulti.so"
    self.mylib = ctypes.cdll.LoadLibrary(path)
    self.funct = self.mylib.multi
    self.funct.restype = ctypes.POINTER(ctypes.c_int)

    # Publicar datos de la coordenada y el tiempo
    self.pub = rospy.Publisher('coord', Float64MultiArray, queue_size=10)

  def video(self):
    """
        Inicia el proceso de captura de video y detección del objeto de color verde.
    """
    # Definir el uso de la webcam
    vid = cv2.VideoCapture(0)
      
    while(True):
        # Obtener el frame
        ret, frame = vid.read()

        # Convertir la imagen BGR a espacio de colores HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Definir los valores de la mascara para el color verde en HSV
        low = np.array([35,80,0])
        up = np.array([80,255,255])

        # Crear mascara
        maskG = cv2.inRange(hsv, low, up)

        # Eliminar ruido
        c, h = cv2.findContours(maskG, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        # Area minima aceptada para cosiderar el objeto
        threshold_blob_area = 1000

        # Encontrar y quitar ruido
        for i in range(1, len(c)):
          index_level = int(h[0][i][1])
          if index_level <= i:
            cnt = c[i]
            area = cv2.contourArea(cnt)
          if(area) <= threshold_blob_area:
            cv2.drawContours(maskG, [cnt], -1, 0, -1, 1)

        # Encontrar el contorno del objeto
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        contour = cv2.morphologyEx(maskG, cv2.MORPH_OPEN, kernel, iterations=4)
        
        # Obtener las coordenadas
        x,y,w,h = cv2.boundingRect(contour)
        
        # Dibujar un rectangulo
        cv2.rectangle(frame, (x, y), (x + w, y + h), (139,0,0), 4)
        # Mostrar los valores de x y y en el video
        cv2.putText(frame, "x: "+str(x), (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2, cv2.LINE_AA)
        cv2.putText(frame, "y: "+str(y), (x+130, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2, cv2.LINE_AA)

        # Usar libreria de c++
        ret_ptr = self.funct(ctypes.c_int(x), ctypes.c_int(y))
        ret_arr = ret_ptr[:2]
      
        # Pasar las coordenads y el timestamp a un arreglo de floats
        coordR = Float64MultiArray()
        coordR.data = [ret_arr[0], ret_arr[1], time.time()]
        print(coordR)

        # Publicar las coordenadas al topico
        self.pub.publish(coordR)

        # Eliminar el valor de retorno
        self.mylib.delete_arr.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.mylib.delete_arr.restype = None
        self.mylib.delete_arr(ret_ptr)

        # Mostrar video
        cv2.imshow('Frame', frame)
        #cv2.imshow("Contour", contour)

        # 'q' = quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
  
    vid.release()
    # Salir
    cv2.destroyAllWindows()    

if __name__ == '__main__':
  m = m4_t1()
  rospy.init_node('m4_t1', anonymous=True)
  m.video()
  try:
    while not rospy.is_shutdown():
      rospy.Rate(100)
  except KeyboardInterrupt:
    pass