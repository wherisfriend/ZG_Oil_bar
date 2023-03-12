from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class PingSan2023DB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, '\xc8\xfd\xb9\xf5_\xc6\xbd\xc8\xfd\xbd\xc72023',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        fileName = os.path.join(thisDir, 'pingsanjiao.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=self, text='', ic=icon)
        AFXTextField(p=self, ncols=12, labelText='\xce\xc4    \xbc\xfe     \xc3\xfb:', tgt=form.partnameKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xd4\xfe\xb9\xf5\xd6\xb1\xbe\xb6ZD:', tgt=form.ZGDKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xc4\xda\xbd\xd3\xd4\xb2\xd6\xb1\xbe\xb6d:', tgt=form.DKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xc0\xed\xc2\xdb\xd1\xd3\xc9\xecL:', tgt=form.YSKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xb9\xf5\xb7\xec\xbf\xed\xb6\xc8S:', tgt=form.S_kKw, sel=0)
