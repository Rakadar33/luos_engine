import usb.core
import usb.util


capableRobot={"idVendor": 0x0424,"idProduct": 0x494c}
#capableRobot={"idVendor": 0x1d6b,"idProduct": 0x002}

device = usb.core.find(idVendor= capableRobot["idVendor"], idProduct= capableRobot["idProduct"])
