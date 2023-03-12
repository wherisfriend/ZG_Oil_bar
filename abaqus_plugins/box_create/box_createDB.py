from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class Box_createDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, '\xcf\xe4\xd0\xcd\xbf\xd7\xd4\xfe\xb9\xf5\xbd\xa8\xc4\xa3',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        fileName = os.path.join(thisDir, 'box.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=self, text='', ic=icon)
        GroupBox_1 = FXGroupBox(p=self, text='\xb2\xce\xca\xfd\xc1\xd0\xb1\xed', opts=FRAME_GROOVE|LAYOUT_FILL_X|LAYOUT_FILL_Y)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xce\xc4  \xbc\xfe \xc3\xfb:', tgt=form.partname_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xb9\xa4\xd7\xf7\xd6\xb1\xbe\xb6:', tgt=form.D_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xb2\xdb\xb5\xd7\xbf\xed\xb6\xc8:', tgt=form.b_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xbf\xd7\xd0\xcd\xb8\xdf\xb6\xc8:', tgt=form.H_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xb2\xe0\xd0\xb1\xb6\xc8%:', tgt=form.y_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xd4\xfe\xb9\xf5\xb9\xf5\xb7\xec:', tgt=form.S_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xcf\xf2\xcd\xe2\xd1\xd3\xc9\xec:', tgt=form.yanshen_kKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='\xd4\xb2\xbd\xc7\xcf\xb5\xca\xfd:', tgt=form.r_rateKw, sel=0)
