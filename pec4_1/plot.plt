set multiplot layout 2,1

# campos:
# - temperatura
# - humedad
# - presion
# - rocio

set xlabel 'Tiempo (1 muestra cada 10 min)'
set ylabel 'Temperatura (°C)'

# primer grafico
plot 'data.dat' u 1 w lp title 'Temperatura (°C)', \
'data.dat' u 4 w lp title 'Punto rocío (°C)'

set xlabel 'Tiempo (1 muestra cada 10 min)'
set ylabel 'Humedad (%), Presión (kPa)'

# segundo grafico
plot 'data.dat' u 2 w lp title 'Humedad (%)', \
'data.dat' u ($3/10) w lp title 'Presión (kPa)'

pause 600
reread
