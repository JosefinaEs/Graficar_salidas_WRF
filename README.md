# Graficar_salidas_WRF
Script en Python para graficar temperatura en superficie. Utiliza multiprocesamiento (varios CPU's para realizar la graficación) Toma los datos de un archivo netCDF los gráfica. Se puede modificar el tamaño del domino, el rango de la barra y el numero de procesadores a utilizar. 

Las librerias que utiliza son: sys, getopt, numpy, multiprocessing, matplotlib y netCDF4.

El script recibe los siguientes parámetros:

1 (obligatorio): Archivo NetCDF a graficar 

Los demás parámetros  son opcionales y se pasan como banderas

--lat_n	 o  -n    latitud norte del subdominio a graficar 

--lat_s  o  -s	  latitud sur del subdominio a graficar 

--long_e o  -e    longitud este del subdominio a graficar

--long_o o  -o    longitud oeste del subdominio a graficar

--barra  o  -b  	archivo de la barra de color a utilizar

--rango_i	o -i	  

--rango_s o -u    

--proc   o  -p   	número de procesadores para graficado en paralelo 

