# Script que grafica la variable T2 de una salida de WRF en NetCDF
# El script recibe los siguientes par'ametros:
# 1 (obligatorio): Archivo NetCDF a graficar

# Los dem'as parametros  son opcionales y se pasan como banderas
# --lat_n	latitud norte del subdominio a graficar
# --lat_s	latitud sur del subdominio a graficar
# --long_e	longitud este del subdominio a graficar
# --long_o	longitud oeste del subdominio a graficar
# --barra 	archivo de la barra de color a utilizar
# --rango_i		
# --rango_s
# --proc	numero de procesadores para graficado en paralelo

import sys
import getopt
import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from netCDF4 import Dataset
from matplotlib import cm

import cartopy.crs as ccrs
from cartopy import feature
from cartopy.io.shapereader import Reader

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

proj=ccrs.Mercator()
states= feature.ShapelyFeature(
        Reader('shp/ne_10m_admin_1_states_provinces_lines.shp' ).geometries(),
        ccrs.PlateCarree(),
        )
borders= feature.ShapelyFeature(
        Reader('shp/ne_50m_admin_0_boundary_lines_land.shp' ).geometries(),
        ccrs.PlateCarree(),
        )

land= feature.ShapelyFeature(
        Reader('shp/ne_50m_land.shp' ).geometries(),
        ccrs.PlateCarree(),
        )

# Funcion que realiza una grafica de una variable escalar
def graficar_temparatura(i, tmp2m, levels, cmap1, long_o, long_e, lat_s, lat_n, Fechas):
        dpi=100
        w=986/dpi
        h=785/dpi
        fig=plt.figure(figsize=(w,h),dpi=dpi)
        fig.subplots_adjust(left=0.01,right=0.99,top=0.94,bottom=0.03)
        ax=plt.subplot(1,1,1,
            #projection=proj,
            projection=ccrs.PlateCarree(),
            )
        ax.add_feature(
                borders,
                edgecolor='black',
                facecolor='none',
                lw=0.5,

                )
        ax.add_feature(
                states,
                edgecolor='black',
                facecolor='none',
                lw=0.5,

                )
        ax.add_feature(
                land,
                edgecolor='black',
                facecolor='none',
                lw=0.5,

                )
        # Formato de las etiquetas de los ejes (ticks)
        #plt.rc('font', weight='bold', size=8)

        # Hora de salida
        fecha=Fechas.astype('|S1').tostring().decode('utf-8')

        ax_leg=ax.gridlines(
                draw_labels=True,
                linestyle='--',
                )
        ax_leg.xlabels_top=False
        ax_leg.ylabels_right=False
        #ax_leg.xlocator=mticker.FixedLocator(range(int(lon_min),int(lon_max)+1,1))
        ax_leg.xformatter=LONGITUDE_FORMATTER
        #ax_leg.ylocator=mticker.FixedLocator(range(int(lat_min),int(lat_max)+2,1))
        ax_leg.yformatter=LATITUDE_FORMATTER
        ax_leg.ypadding=-27
        ax_leg.xpadding=-11

        plt.contourf(lon,lat,tmp2m,levels,cmap=cm.get_cmap(cmap1))
        title='Modelo WRF ' + str(fecha) +' UTC'+50*' '+'Pronóstico a '+str(i)+' horas\n'
        title+='Temperatura en superficie [°C] '+50*' '+'Hora Local:'
        plt.title(title, fontdict=font)
        cbar=plt.colorbar(
                ticks=np.arange(-10,50,10),
                orientation="horizontal",
                aspect=70,
                #pad=0.15,
                pad=0.04,
                #fraction=0.056,
                fraction=0.02,
                )
        #plt.axis('scaled')

        cbar.ax.set_xlabel('Temperatura[C]',
                labelpad=-40,
                )
        # Coordenadas del dominio
        plt.axis([float(long_o), float(long_e), float(lat_s), float(lat_n)], crs=ccrs.PlateCarree())

        # Crear y guardar la figura
        nombre='Temperatura_2m_' + str(i) +'.png'
        plt.savefig(nombre, dpi=dpi)
        plt.close(fig)


# Formato del texto de la gr'afica
font={'family': 'sans-serif','color': 'black','weight': 'normal','size': 10,}

# Cargar el archivo NetCDF
dataset=Dataset(sys.argv[1])

# Cargar individualmente las variables de latitud, longitud, temparatura y tiempo
lat=np.array(dataset.variables['XLAT'][0,:,0])
lon=np.array(dataset.variables['XLONG'][0,0,:])
T2=np.array(dataset.variables['T2'][:])
T2-=273.15
Tiempo=len(dataset.variables['Times'])
Fechas=dataset.variables['Times']

# Valores por defecto, tomados del NetCDF de entrada
lat_n=lat[-1]		# Latitud norte
lat_s=lat[0]			# Latitud sur
long_e=lon[-1]	# Longitud este
long_o=lon[0]			# Longitud oeste
file="./barra_temperatura.txt"
rango_i=-14
rango_s=51
numproc=1

# Obtener los parametros si es que el usuario ha definido algunos
argv=sys.argv[2:]
try:
    opts, args=getopt.getopt(argv,"b:n:s:e:o:i:u:p:",["barra=","lat_n=","lat_s=","long_e=","long_o=","rango_i=","rango_s=","numproc="])
except getopt.GetoptError as err:
    print(err)
    opts=[]

for opt, arg in opts:
    if opt in ['-n','--lat_n']:
        lat_n=arg
    elif opt in ['-b','--barra']:
        file=arg
    elif opt in ['-s','--lat_s']:
        lat_s=arg
    elif opt in ['-e','--long_e']:
        long_e=arg
    elif opt in ['-o','--long_o']:
        long_o=arg
    elif opt in ['-i','--rango_i']:
        rango_i=int(arg)
    elif opt in ['-u','--rango_s']:
        rango_s=int(arg)+1
    elif opt in ['-p','--numproc']:
        numproc=arg

# Cargar el archivo con la barra de color
cmap=np.loadtxt(file)
cmap1=colors.ListedColormap(cmap)

# Rango de la grafica
levels=range(rango_i,rango_s,1)

# Ciclo que realiza una grafica para cada uno de los tiempos encontrados en el archivo NetCDF
if numproc==1:
	# Lo corremos en serie
	for i in range(1,Tiempo,1):
		graficar_temparatura(i, T2[i,:,:], levels, cmap1, long_o, long_e, lat_s, lat_n, Fechas[i])
else:
	# Lo corremos en paralelo
	pool = mp.Pool(int(numproc))
	results=pool.starmap_async(graficar_temparatura, [(i, T2[i,:,:], levels, cmap1, long_o, long_e, lat_s, lat_n, Fechas[i]) for i in range(1,Tiempo,1)]).get()
	pool.close()
