from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class KOCKS_2023DB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, '\xc8\xfd\xb9\xf5KOCKS\xd4\xfe\xbb\xfa',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        fileName = os.path.join(thisDir, 'KOCKS.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=self, text='', ic=icon)
        GroupBox_1 = FXGroupBox(p=self, text='\xbf\xd7\xd0\xcd\xb2\xce\xca\xfd', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='partname:', tgt=form.partname_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='DSI_value:', tgt=form.DSIKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='PSI_value:', tgt=form.PSIKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='ZGD_VAL:', tgt=form.ZGDKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='YS__value:', tgt=form.YS_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='W_Kvalue:', tgt=form.W_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='R_Hu_VAL:', tgt=form.R_kKw, sel=0)
