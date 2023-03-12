# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class WORKPIECEDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Title',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        fileName = os.path.join(thisDir, 'zhajian.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=self, text='', ic=icon)
        AFXTextField(p=self, ncols=12, labelText='\xd4\xfe\xbc\xfe\xd6\xb1\xbe\xb6:', tgt=form.DKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xb8\xb2\xb2\xe3\xb1\xda\xba\xf1:', tgt=form.ThickKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='\xd4\xfe\xbc\xfe\xb3\xa4\xb6\xc8:', tgt=form.LKw, sel=0)
        frame = FXHorizontalFrame(self, 0, 0,0,0,0, 0,0,0,0)

        # Model combo
        # Since all forms will be canceled if the  model changes,
        # we do not need to register a query on the model.
        #
        self.RootComboBox_1 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Model:', tgt=form.modelNameKw, sel=0)
        self.RootComboBox_1.setMaxVisible(10)

        names = mdb.models.keys()
        names.sort()
        for name in names:
            self.RootComboBox_1.appendItem(name)
        if not form.modelNameKw.getValue() in names:
            form.modelNameKw.setValue( names[0] )
        msgCount = 136
        form.modelNameKw.setTarget(self)
        form.modelNameKw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        msgHandler = str(self.__class__).split('.')[-1] + '.onComboBox_1MaterialsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount, msgHandler) )

        # Materials combo
        # 芯材料
        self.ComboBox_1 = AFXComboBox(p=frame, ncols=0, nvis=1, text='\xd0\xbe\xb2\xbf\xb2\xc4\xc1\xcf:', tgt=form.materialXinKw, sel=0)
        self.ComboBox_1.setMaxVisible(10)

        self.form = form
        self.regModelName = None
        if isinstance(self, FXHorizontalFrame):
            FXVerticalSeparator(p=self, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=self, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        frame = FXHorizontalFrame(self, 0, 0,0,0,0, 0,0,0,0)

        # Model combo
        # Since all forms will be canceled if the  model changes,
        # we do not need to register a query on the model.
        # 
        self.RootComboBox_2 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Model:', tgt=form.modelName2Kw, sel=0)
        self.RootComboBox_2.setMaxVisible(10)

        names = mdb.models.keys()
        names.sort()
        for name in names:
            self.RootComboBox_2.appendItem(name)
        if not form.modelName2Kw.getValue() in names:
            form.modelName2Kw.setValue( names[0] )
        msgCount = 137
        form.modelName2Kw.setTarget(self)
        form.modelName2Kw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        msgHandler = str(self.__class__).split('.')[-1] + '.onComboBox_2MaterialsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount, msgHandler) )

        # Materials combo
        # 覆层材料
        self.ComboBox_2 = AFXComboBox(p=frame, ncols=0, nvis=1, text='\xb8\xb2\xb2\xe3\xb2\xc4\xc1\xcf:', tgt=form.materialTaoKw, sel=0)
        self.ComboBox_2.setMaxVisible(10)

        self.form = form
        # self.regModelName = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)

        # Register a query on materials
        #
        self.currentModelName = getCurrentContext()['modelName']
        self.form.modelNameKw.setValue(self.currentModelName)
        # mdb.models.registerQuery(self.updateComboBox_1Models, False)
        # self.registerComboBox_1PartQuery(currentModelName)

        mdb.models[self.currentModelName].materials.registerQuery(self.updateComboBox_1Materials)

        # Register a query on materials
        #
        self.currentModelName = getCurrentContext()['modelName']
        self.form.modelName2Kw.setValue(self.currentModelName)
        # 新版本的
        # mdb.models.registerQuery(self.updateComboBox_2Models, False)
        # self.registerComboBox_2PartQuery(currentModelName)

        mdb.models[self.currentModelName].materials.registerQuery(self.updateComboBox_2Materials)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)

        mdb.models[self.currentModelName].materials.unregisterQuery(self.updateComboBox_1Materials)

        mdb.models[self.currentModelName].materials.unregisterQuery(self.updateComboBox_2Materials)

        # self.registerComboBox_1PartQuery(None)
        # mdb.models.unregisterQuery(self.updateComboBox_1Models)

        # self.registerComboBox_2PartQuery(None)
        # mdb.models.unregisterQuery(self.updateComboBox_2Models)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def registerComboBox_1PartQuery(self, modelName):

        if modelName == self.regModelName:
           return

        cbFunc = self.updateComboBox_1Materials
        modelKeys = mdb.models.keys()
        if self.regModelName in modelKeys:
           mdb.models[self.regModelName].unregisterQuery(cbFunc)
        self.regModelName = None

        if modelName in modelKeys:
           mdb.models[modelName].registerQuery(cbFunc, False)
           self.regModelName = modelName

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_1Models(self):

        # Update the names in the Models combo
        #
        self.RootComboBox_1.clearItems()
        names = mdb.models.keys()
        names.sort()
        for name in names:
           self.RootComboBox_1.appendItem(name)

        modelName = self.form.modelNameKw.getValue()
        if not modelName in names:
           modelName = names[0]
        self.form.modelNameKw.setValue(modelName) # Triggers parts combo update

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onComboBox_1MaterialsChanged(self, sender, sel, ptr):

        self.updateComboBox_1Materials()
        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_1Materials(self):
        modelName = self.form.modelNameKw.getValue()

        # Update the names in the Materials combo
        #
        self.ComboBox_1.clearItems()
        names = mdb.models[modelName].materials.keys()
        names.sort()
        for name in names:
            self.ComboBox_1.appendItem(name)
        if names:
            if not self.form.materialXinKw.getValue() in names:
                self.form.materialXinKw.setValue( names[0] )
        else:
            self.form.materialXinKw.setValue('')

        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )

        # # This is needed to handle lost registrations caused by model rename
        # if not self.regModelName:
        #    return 1

        # # Update the names in the Parts combo
        # # 
        # modelName = self.form.modelNameKw.getValue()

        # self.ComboBox_1.clearItems()
        # names = mdb.models[modelName].materials.keys()
        # names.sort()
        # for name in names:
        #     self.ComboBox_1.appendItem(name)
        # if names:
        #     if not self.form.materialXinKw.getValue() in names:
        #         self.form.materialXinKw.setValue( names[0] )
        # else:
        #     self.form.materialXinKw.setValue('')

        # self.resize( self.getDefaultWidth(), self.getDefaultHeight() )

        # # Change parts container registration if the model has changed
        # self.registerComboBox_1PartQuery(modelName)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def registerComboBox_2PartQuery(self, modelName):

        if modelName == self.regModelName:
           return

        cbFunc = self.updateComboBox_2Materials
        modelKeys = mdb.models.keys()
        if self.regModelName in modelKeys:
           mdb.models[self.regModelName].unregisterQuery(cbFunc)
        self.regModelName = None

        if modelName in modelKeys:
           mdb.models[modelName].registerQuery(cbFunc, False)
           self.regModelName = modelName

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_2Models(self):

        # Update the names in the Models combo
        #
        self.RootComboBox_2.clearItems()
        names = mdb.models.keys()
        names.sort()
        for name in names:
           self.RootComboBox_2.appendItem(name)

        modelName = self.form.modelName2Kw.getValue()
        if not modelName in names:
           modelName = names[0]
        self.form.modelName2Kw.setValue(modelName) # Triggers parts combo update

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onComboBox_2MaterialsChanged(self, sender, sel, ptr):

        self.updateComboBox_2Materials()
        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_2Materials(self):

        modelName = self.form.modelName2Kw.getValue()

        # Update the names in the Materials combo
        #
        self.ComboBox_2.clearItems()
        names = mdb.models[modelName].materials.keys()
        names.sort()
        for name in names:
            self.ComboBox_2.appendItem(name)
        if names:
            if not self.form.materialTaoKw.getValue() in names:
                self.form.materialTaoKw.setValue( names[0] )
        else:
            self.form.materialTaoKw.setValue('')

        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )


        # # This is needed to handle lost registrations caused by model rename
        # if not self.regModelName:
        #    return 1

        # # Update the names in the Parts combo
        # # 
        # modelName = self.form.modelName2Kw.getValue()

        # self.ComboBox_2.clearItems()
        # names = mdb.models[modelName].materials.keys()
        # names.sort()
        # for name in names:
        #     self.ComboBox_2.appendItem(name)
        # if names:
        #     if not self.form.materialTaoKw.getValue() in names:
        #         self.form.materialTaoKw.setValue( names[0] )
        # else:
        #     self.form.materialTaoKw.setValue('')

        # self.resize( self.getDefaultWidth(), self.getDefaultHeight() )

        # # Change parts container registration if the model has changed
        # self.registerComboBox_2PartQuery(modelName)

