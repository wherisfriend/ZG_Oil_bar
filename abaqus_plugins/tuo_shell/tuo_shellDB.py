from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class Tuo_shellDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, '\xcd\xd6\xd4\xb2\xbf\xd7\xd0\xcd\xd4\xfe\xb9\xf5\xbd\xa8\xc4\xa3v1.0', self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        GroupBox_1 = FXGroupBox(p=self, text='\xb2\xce\xca\xfd\xca\xe4\xc8\xeb\xa3\xba', opts=FRAME_GROOVE)
        fileName = os.path.join(thisDir, 'tuo.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=GroupBox_1, text='', ic=icon)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xce\xc4  \xbc\xfe \xc3\xfb:', tgt=form.partname_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xb9\xa4\xd7\xf7\xd6\xb1\xbe\xb6:', tgt=form.D_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xb2\xdb\xbf\xda\xbf\xed\xb6\xc8:', tgt=form.b_valueKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xbf\xd7\xd0\xcd\xb8\xdf\xb6\xc8:', tgt=form.H_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xd4\xfe\xb9\xf5\xb9\xf5\xb7\xec:', tgt=form.S_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xcf\xf2\xcd\xe2\xd1\xd3\xc9\xec:', tgt=form.YS_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xb5\xb9\xd4\xb2\xbd\xc7\xd6\xb5:', tgt=form.r_rateKw, sel=0)
