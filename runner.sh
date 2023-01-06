#! /bin/bash

#primeras tres lineas los tipos del jugador
nice -1 python3 app_test.py MCTSPlayer MC_Player RandomPlayer 6 &
nice -1 python3 app_test.py MCTSPlayer MC_Player RandomPlayer 2 &
nice -1 python3 app_test.py MCTSPlayer MC_Player RandomPlayer 7 &
nice -1 python3 app_test.py MCTSPlayer MC_Player RandomPlayer 4 &
nice -1 python3 app_test.py MCTSPlayer MC_Player RandomPlayer 5 &
nice -1 python3 app_test.py MCTSPlayer MC_Player RandomPlayer 8 &
nice -1 python3 app_test.py MCTSPlayer MC_Player RandomPlayer 9 &
#por cada tipo de jugador en orden cada uno de los argumentos(es obligado pasarselo)
