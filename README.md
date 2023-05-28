# M4_t1

### Diagrama DFD
---
![Diagram](diagramas/DFD_Tarea_Interfases.drawio.png)

### Demo
https://drive.google.com/file/d/1ZOs1unn6kA5U5rV5y0QQWPOcXgRjD0eg/view?usp=drive_link
---

### Programa de ROS para detectar coordenadas
```
rosrun t1 detectCoord.py
```
Cambiar el path de la libreria en detectCoord.py

### Servidor gRPC
```
virtualenv -p python3 env
source env/bin/activate
pip install grpcio grpcio-tools
python3 wrapper.py
```

### Cliente gRPC en C#
```
mono cliente_cs.exe
```
