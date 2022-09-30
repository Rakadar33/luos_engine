# coding:utf-8
from pathlib import Path

# For Debug
DEBUG_MODE = "OFF" # "ON" to enable "breakpoint()"" method

# Platform parameters
expected_topology = {'Gate':  ['gate', 'Pipe', 'led'], 'blinker':  ['blinker']}
expected_nodes    = ['Gate', 'blinker']
expected_services = ['gate', 'Pipe', 'led', 'blinker']


# TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!
# TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!
# TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!
# TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!    
#network_conf = ["N1_N2", "N2_N5", "N3_N4", "N4_N1", "N5_N3"]

# OK
#network_conf = ["N2_N5"] # OK :-)
#network_conf = ["N1_N2"] # OK :-) 
#network_conf = ["N3_N4"] # OK :-)
#network_conf = ["N1_N2", "N2_N5", "N3_N4"] # OK ;-)


#network_conf = ["N5_N2"] # parfois OK / cf ci-dessous
network_conf = ["N5_N3"]



# All confs
    #OK --   # network_conf = ["N1_N2"]
    #OK --   # network_conf = ["N1_N3"]
    #OK --   # network_conf = ["N1_N4"]
    #OK --   #network_conf = ["N2_N3"]
    #OK --   # network_conf = ["N2_N4"]
    #OK --   # network_conf = ["N2_N5"]
    #OK --   # network_conf = ["N3_N4"]
    #OK --   network_conf = ["N3_N2"]
    #OK --   network_conf = ["N4_N5"]
    #OK --   network_conf = ["N4_N2"]
    #OK --   network_conf = ["N4_N3"]

            # ---- Vers N1 : aucun ne marche ----
			### KO ###  network_conf = ["N2_N1"] # L'inverse (N1_N2) marche donc GPIO et IT ont l'air OK. Prob de tempo ? N2 seul = OK
			### KO ###  network_conf = ["N3_N1"]
			### KO ###  network_conf = ["N4_N1"] # Gate N4 seule est détectée. Bloqué ds  detection si on allume l'Arduino. Prob IT Arduino ???
                                                 # A été vu OK une fois ???

            # ---- De N5 (Gate + Blinker)----
            # GATE N5 seule ne marche pas : cf salae sur Bureau.
            #                               Prob de time init pas bon ? Non car pas cablé (en fait si, le prob doit venir des tempos)
            #                               prob du blinker (enlever blinker pour voir) ? Peut être mettre init pf hardware
            #                               avant blinker_init puis attendre 500ms
            # Par contre, avec pyluos-shell, ça a l'air de marcher Gate + Led, mais arrêt après 5 détections (+ 1 avant). Mais pas rtb affichée par pyluos ???
            # Avec le script scenario.py, ça ressembe à gate seule :  Le blinker fait une détection 700 us avant que Tx ne soit init.
            # ----> Rajouter une tempo !! Ceci dit je comprends pas pk Tx mets autant de temps à s'init à 1...
            # -----> Contournement rapide : enlever le blinker
            # MAJ 28/09
            # - Code : ajout tempo + inversion ptp c, power on :
            #            -> N5_N2 marche avec pyluos-shell en mettant EXPLICITEMENT le port /dev/N5
            #            -> Ne marche pas avec mon script alors que SALAE a l'air OK (cf n5_n2_tempo.sal)
            #            -> Ah si, mon script a marché. Mais pas à tous les coups
            #
            ### KO ###  network_conf = ["N5_N1"] -- de N5 / vers N1 #double!
			### KO ###  network_conf = ["N5_N2"] --de N5
			### KO ###  network_conf = ["N5_N3"]
			### KO ###  network_conf = ["N5_N4"]

            # ---- Vers N5 ----
			### KO ###  network_conf = ["N1_N5"]  # Seule la gate a été vue. Encore prob de tempo à l'init ??? voir à la salae
            ### KO ###  network_conf = ["N3_N5"]  # Mettre salae

#-----------------------------------------------------------------------------
# KO N4_N1
#-----------------------------------------------------------------------------
#network_conf = ["N4_N1"]
   # OK :-)
   # Redevenu ko............. Gate N4 seule est détectée. Mais bloqué dans la detection si on allume l'Arduino. prob IT Arduino ???
#network_conf = ["N1_N4"] # on inverse N4/N1 pour voir : OK ça marche. Donc IT ok dans ce sens (Arduino est une Gate)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# KO N5_N3
#-----------------------------------------------------------------------------
#network_conf = ["N5_N3"]   # KO : idem
#network_conf = ["N3_N5"] # on inverse N3/N5 pour voir : KO. Prob conf
#-----------------------------------------------------------------------------


config_N1 = {"environment": "mkrzero",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/Arduino",
             "interruption": "",
             "source": "Arduino.cpp",
             "target": "at91samd",
             "flashing_port": "N1_Arduino",
             "flashing_options": {"config": "", "serial": ""}}

config_N2 = {"environment": "nucleo_f072rb",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-F072RB",
             "interruption": "stm32f0xx_it.c",
             "source": "main.c",
             "target": "nucleo_f072rb",
             "flashing_port": "N2_F072RB",
             "flashing_options": {"config": "stm32f0x.cfg", "serial": "066AFF544949878667153627"}}

config_N3 = {"environment": "nucleo_f401re",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-F401RE",
             "interruption": "stm32f4xx_it.c",
             "source": "main.c",
             "target": "nucleo_f401re",
             "flashing_port": "N3_F401RE",
             "flashing_options": {"config": "stm32f4x.cfg", "serial": "066FFF555054877567045540"}}

config_N4 = {"environment": "nucleo_l432kc",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-L432KC",
             "interruption": "stm32l4xx_it.c",
             "source": "main.c",
             "target": "stm32l4x",
             "flashing_port": "N4_L432KC",
             "flashing_options": {"config": "stm32l4x.cfg", "serial": "0671FF485688494867102626"}}

config_N5 = {"environment": "nucleo_g431kb",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-G431KB",
             "interruption": "stm32g4xx_it.c",
             "source": "main.c",
             "target": "stm32g4x",
             "flashing_port": "N5_G431KB",
             "flashing_options": {"config": "stm32g4x.cfg", "serial": "001100174741500720383733"}}
