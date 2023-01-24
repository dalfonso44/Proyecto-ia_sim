#! /bin/bash

#primeras tres lineas los tipos del jugador
nice -5 python3 app_test.py MCTSPlayer MC_Player RandomPlayer 70 80 &
#nice -5 python3 app_test.py MCTSPlayer MC_Player RandomPlayer 80 90 &
#nice -5 python3 app_test.py MCTSPlayer MC_Player RandomPlayer 90 100 &
#por cada tipo de jugador en orden cada uno de los argumentos(es obligado pasarselo)
