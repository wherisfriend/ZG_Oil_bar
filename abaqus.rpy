# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2021 replay file
# Internal Version: 2020_03_06-22.50.37 167380
# Run by 14415 on Fri Mar 10 21:20:01 2023
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=189.9052734375, 
    height=200.41667175293)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
from abaqus_plugins.box_create import box02
from abaqus_plugins.tuo_shell import tuo
from abaqus_plugins.yuan2023 import yuan2023
from abaqus_plugins.PingSan2023 import ping3_2023
from abaqus_plugins.YUAN_2023 import yuan2023_fun
from abaqus_plugins.HUSAN_2023 import hu3_2023
from abaqus_plugins.KOCKS_2023 import kocks_2023
from abaqus_plugins.PAF_test import PAFSystem
