from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class HUSAN_2023DB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, '\xc8\xfd\xb9\xf5\xbb\xa1\xc8\xfd\xbd\xc72023',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        fileName = os.path.join(thisDir, 'huxing2.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=self, text='', ic=icon)
        AFXTextField(p=self, ncols=12, labelText='\xce\xc4    \xbc\xfe     \xc3\xfb:', tgt=form.partname_kKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xd4\xfe\xb9\xf5\xd6\xb1\xbe\xb6Dh :', tgt=form.ZGDKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xc4\xda\xbd\xd3\xd4\xb2\xd6\xb1\xbe\xb6d:', tgt=form.D_kKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xd1\xd3 \xc9\xec \xb3\xa4 \xb6\xc8 L:', tgt=form.YS_kKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xbb\xa1 \xcf\xdf \xbc\xd0 \xbd\xc7 \xa6\xc2:', tgt=form.bata_kKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xb9\xf5\xb7\xec\xbf\xed\xb6\xc8 M\xa3\xba', tgt=form.S_kKw, sel=0)
