#!/bin/bash

URL="http://infomet.meteo.ub.edu/metdata/"

TMP="tmp.dat"
DAT="data.dat"

function getdata {
    WHAT=$1

    cat $TMP |
        grep -m 1 "${WHAT}:" |
        sed 's/^.*: //; s/[^0-9.]*$//'
}

function gettime {
    cat $TMP |
        grep -m 1 "Dades recollides" |
        sed 's/^.*a les //; s/UTC.*$/UTC/'
}

function getdate {
    cat $TMP |
        grep -m 1 "Dades recollides" |
        sed 's/^.*del dia //; s/  .*$//'
}

function countdown {
    N=$1

    while [ $N -gt 0 ]; do
        NSTR=
        echo -ne "\r                              "
        echo -ne "\rActualizando en $N..."

        sleep 1

        N=$(($N-1))
    done

    echo -ne "\r                              "
    echo -ne "\rActualizando..."
    echo ""

}

rm -f $TMP

if [ -e "$DAT" ]; then
    echo "Existe un fichero previo con datos, lo elimino? (s/n)"

    read REP

    if [ "$REP" = "s" ]; then
        rm -f $DAT
        echo "Eliminado"
    fi
fi

while true; do
    w3m -dump $URL > $TMP

    DATE=$(getdate)
    TIME=$(gettime)

    T=$(getdata 'Temperatura')
    H=$(getdata 'Humitat')
    P=$(getdata 'Pressió')
    R=$(getdata 'Punt de rosada')

    echo ""
    echo "Datos meteorológicos Barcelona"
    echo "=============================="
    echo "Fecha:        ${DATE}"
    echo "Hora:         ${TIME}"
    echo "Temperatura:  ${T}°C"
    echo "Humedad:      ${H}%"
    echo "Presión:      ${P} hPa"
    echo "Punto rocío:  ${R}°C"

    echo ""

    echo "$T $H $P $R" >> $DAT

    countdown 600
done
