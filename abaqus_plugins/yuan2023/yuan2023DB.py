from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class Yuan2023DB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, '\xd4\xb2\xbf\xd7\xd0\xcd\xd4\xfe\xb9\xf5\xbd\xa8\xc4\xa3v2.0',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        fileName = os.path.join(thisDir, 'yuan.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=self, text='', ic=icon)
        GroupBox_1 = FXGroupBox(p=self, text='\xb2\xce\xca\xfd\xca\xe4\xc8\xeb:', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xc1\xe3\xbc\xfe\xc3\xfb\xb3\xc6\xa3\xba', tgt=form.partname_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xbf\xd7\xd0\xcd\xd6\xb1\xbe\xb6\xa3\xba', tgt=form.ZJKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xd4\xfe\xb9\xf5\xd6\xb1\xbe\xb6\xa3\xba', tgt=form.D_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xd1\xd3\xc9\xec\xb3\xa4\xb6\xc8\xa3\xba', tgt=form.YS_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xb9\xf5\xb7\xec\xbf\xed\xca\xfd\xa3\xba', tgt=form.S_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xd4\xb2\xbd\xc7\xcf\xb5\xca\xfd\xa3\xba', tgt=form.r_radisKw, sel=0)
        if isinstance(GroupBox_1, FXHorizontalFrame):
            FXVerticalSeparator(p=GroupBox_1, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=GroupBox_1, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        l = FXLabel(p=GroupBox_1, text='\xb9\xf5\xb7\xec\xcf\xb5\xca\xfdS = (0.10~0.15)h', opts=JUSTIFY_LEFT)
        l = FXLabel(p=GroupBox_1, text='\xb5\xb9\xd4\xb2\xbd\xc7r=1.5~2.0', opts=JUSTIFY_LEFT)
