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



network_conf = ["N2_N3"]



# All confs
    #OK --   # network_conf = ["N1_N2"]
    #OK --   # network_conf = ["N1_N3"]
    #OK --   # network_conf = ["N1_N4"]
			### KO ###  network_conf = ["N1_N5"]  # Seule la gate a été vue
			### KO ###  network_conf = ["N2_N3"]  # Idem ici
    #OK --   # network_conf = ["N2_N4"]
    #OK --   # network_conf = ["N2_N5"]
			### KO ###  network_conf = ["N2_N1"]
    #OK --   # network_conf = ["N3_N4"]
			### KO ###  network_conf = ["N3_N5"]
			### KO ###  network_conf = ["N3_N1"]
			### KO ###  network_conf = ["N3_N2"]
    #OK --   network_conf = ["N4_N5"]
			### KO ###  network_conf = ["N4_N1"]
    #OK --   network_conf = ["N4_N2"]
    #OK --   network_conf = ["N4_N3"]
			### KO ###  network_conf = ["N5_N1"] 
			### KO ###  network_conf = ["N5_N2"]
			### KO ###  network_conf = ["N5_N3"]
			### KO ###  network_conf = ["N5_N4"]
#------------------------------------------------------
			### KO ###  network_conf = ["N2_N1"]
			### KO ###  network_conf = ["N3_N1"]
			### KO ###  network_conf = ["N4_N1"]
			### KO ###  etwork_conf = ["N5_N1"]
			### KO ###  network_conf = ["N3_N2"]
    #OK --   network_conf = ["N4_N2"]
			### KO ###  network_conf = ["N5_N2"]
    #OK --   network_conf = ["N1_N2"]
    #OK --   network_conf = ["N4_N3"]
			### KO ###  network_conf = ["N5_N3"]
    #OK --   network_conf = ["N1_N3"]
			### KO ###   network_conf = ["N2_N3"] # Seule la gate a été vue
			### KO ###  network_conf = ["N5_N4"]
    #OK --   network_conf = ["N1_N4"]
    #OK --   network_conf = ["N2_N4"]
    #OK --   network_conf = ["N3_N4"]
			### KO ###   network_conf = ["N1_N5"] # Seule la gate a été vue
    #OK --   network_conf = ["N2_N5"]
			####### KO -------------   # network_conf = ["N3_N5"]
    #OK --   network_conf = ["N4_N5"]





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
