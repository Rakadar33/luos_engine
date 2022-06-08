# coding:utf-8
from Parameters import log_init as enable_logging
enable_logging()
from Platform import erase_Node
from Parameters import config_F0, config_L4, config_G4, config_Gate

if __name__ == '__main__':
    erase_Node(config_G4)
    erase_Node(config_L4)
    erase_Node(config_F0)
    erase_Node(config_Gate)
