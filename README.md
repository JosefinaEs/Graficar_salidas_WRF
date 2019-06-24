# Graficar_salidas_WRF
Script en Python para graficar temperatura en superficie. Utiliza multiprocesamiento (varios CPU's para realizar la graficación) Toma los datos de un archivo netCDF los gráfica. Se puede modificar el tamaño del domino, el rango de la barra y el numero de procesadores a utilizar. 

El script recibe los siguientes par'ametros:
\t
1 (obligatorio): Archivo NetCDF a graficar \t

Los demás parámetros  son opcionales y se pasan como banderas \t
--lat_n	 o  -n    latitud norte del subdominio a graficar \t
--lat_s  o  -s	  latitud sur del subdominio a graficar \t
--long_e o  -e    longitud este del subdominio a graficar \t
--long_o o  -o    longitud oeste del subdominio a graficar \t
--barra  o  -b  	archivo de la barra de color a utilizar \t
--rango_i	o -i	  \t 
--rango_s o -u    \t
--proc   o  -p   	número de procesadores para graficado en paralelo \t
