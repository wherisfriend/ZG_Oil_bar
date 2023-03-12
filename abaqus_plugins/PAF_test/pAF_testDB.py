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

class PAF_testDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #
        # 覆层抽油杆建模系统
        AFXDataDialog.__init__(self, form, '\xd2\xbb\xd6\xd6Y\xd0\xcd\xc8\xfd\xb9\xf5\xd4\xfe\xbb\xfa\xbf\xd7\xd0\xcd\xbf\xec\xcb\xd9\xbd\xa8\xc4\xa3\xcf\xb5\xcd\xb3',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            
        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')

        #  轧件参数
        GroupBox_1 = FXGroupBox(p=self, text='\xd4\xfe\xbc\xfe\xb2\xce\xca\xfd', opts=FRAME_GROOVE)
        HFrame_1 = FXHorizontalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        
        # GroupBox_3 = FXGroupBox(p=HFrame_1, text='\xd4\xfe\xbc\xfe\xca\xbe\xd2\xe2\xcd\xbc', opts=FRAME_GROOVE)
        # 三辊孔型
        GroupBox_3 = FXGroupBox(p=HFrame_1, text='\xc8\xfd\xb9\xf5\xbf\xd7\xd0\xcd', opts=FRAME_GROOVE)
        # 加载png图片
        fileName = os.path.join(thisDir, 'KOCKS.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=GroupBox_3, text='', ic=icon)

        # 轧件参数：直径、覆层厚度、长度
        GroupBox_2 = FXGroupBox(p=HFrame_1, text='\xd4\xfe\xbc\xfe\xb3\xdf\xb4\xe7', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_2, ncols=12, labelText='\xd4\xfe\xbc\xfe\xd6\xb1\xbe\xb6:', tgt=form.DKw, sel=0)
        AFXTextField(p=GroupBox_2, ncols=12, labelText='\xb8\xb2\xb2\xe3\xb1\xda\xba\xf1:', tgt=form.ThickKw, sel=0)
        AFXTextField(p=GroupBox_2, ncols=12, labelText='\xd4\xfe\xbc\xfe\xb3\xa4\xb6\xc8:', tgt=form.LKw, sel=0)
        # AFXTextField(p=GroupBox_2, ncols=12, labelText='Label4:', tgt=form.keyword04Kw, sel=0)


        GroupBox_4 = FXGroupBox(p=HFrame_1, text='\xb7\xc2\xd5\xe6\xb2\xce\xca\xfd', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_4, ncols=12, labelText='\xd4\xfe\xbc\xfe\xb3\xf6\xc2\xaf\xce\xc2\xb6\xc8:', tgt=form.TmpKw, sel=0)
        AFXTextField(p=GroupBox_4, ncols=12, labelText='\xd4\xfe\xbc\xfe\xb3\xf5\xca\xbc\xcb\xd9\xb6\xc8:', tgt=form.VelKw, sel=0)
        # 空气温度
        AFXTextField(p=GroupBox_4, ncols=12, labelText='\xd4\xfe\xd6\xc6\xbf\xd5\xc6\xf8\xce\xc2\xb6\xc8:', tgt=form.SN_TmpKw, sel=0)
        # 摩擦系数
        AFXTextField(p=GroupBox_4, ncols=12, labelText='\xb7\xc2\xd5\xe6\xc4\xa6\xb2\xc1\xcf\xb5\xca\xfd:', tgt=form.MCKw, sel=0)
        # 质量缩放系数
        AFXTextField(p=GroupBox_4, ncols=12, labelText='\xd6\xca\xc1\xbf\xcb\xf5\xb7\xc5\xcf\xb5\xca\xfd:', tgt=form.ZLSFKw, sel=0)
        # MeshSize
        AFXTextField(p=GroupBox_4, ncols=12, labelText='Mesh\xcd\xf8\xb8\xf1\xb7\xd6\xb2\xbc:', tgt=form.MeshSizeKw, sel=0)


        frame = FXHorizontalFrame(GroupBox_2, 0, 0,0,0,0, 0,0,0,0)
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
        msgCount = 83
        form.modelNameKw.setTarget(self)
        form.modelNameKw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        msgHandler = str(self.__class__).split('.')[-1] + '.onComboBox_1MaterialsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount, msgHandler) )

        # Materials combo
        # 芯棒材料
        self.ComboBox_1 = AFXComboBox(p=frame, ncols=0, nvis=1, text='\xd0\xbe\xb2\xbf\xb2\xc4\xc1\xcf:', tgt=form.materialXinKw, sel=0)
        self.ComboBox_1.setMaxVisible(10)

        self.form = form
        self.regModelName = None
        frame = FXHorizontalFrame(GroupBox_2, 0, 0,0,0,0, 0,0,0,0)

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
        msgCount = 84
        form.modelName2Kw.setTarget(self)
        form.modelName2Kw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        msgHandler = str(self.__class__).split('.')[-1] + '.onComboBox_2MaterialsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount, msgHandler) )

        # Materials combo
        # 覆层材料
        self.ComboBox_2 = AFXComboBox(p=frame, ncols=0, nvis=1, text='\xb8\xb2\xb2\xe3\xb2\xc4\xc1\xcf:', tgt=form.materialTaoKw, sel=0)
        self.ComboBox_2.setMaxVisible(10)

        self.form = form
        self.regModelName = None
        GroupBox_6 = FXGroupBox(p=HFrame_1, text='\xb7\xc2\xd5\xe6\xb2\xce\xca\xfd:', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_6, ncols=12, labelText='\xbf\xd5\xc6\xf8\xc9\xa2\xc8\xc8\xcf\xb5\xca\xfd:', tgt=form.AirFilmCoffKw, sel=0)
        AFXTextField(p=GroupBox_6, ncols=12, labelText='\xb7\xc2\xd5\xe6\xc4\xa3\xc4\xe2\xca\xb1\xbc\xe4:', tgt=form.TimwWorKw, sel=0)
        # AFXTextField(p=GroupBox_6, ncols=12, labelText='Job_name', tgt=form.LKw, sel=0)


        l = FXLabel(p=GroupBox_6, text='\xd6\xc7\xc4\xdc\xb2\xe2\xbf\xd8\xca\xb5\xd1\xe9\xca\xd2', opts=JUSTIFY_LEFT)
        l = FXLabel(p=GroupBox_6, text='\xb5\xa5\xce\xbb\xd6\xc6:SI_mm', opts=JUSTIFY_LEFT)
        l = FXLabel(p=GroupBox_6, text='Version 0.1', opts=JUSTIFY_LEFT)
        # l = FXLabel(p=GroupBox_6, text='\xb8\xb2\xb2\xe3\xb8\xd6\xbd\xee', opts=JUSTIFY_LEFT)
        
        # 分割线
        if isinstance(self, FXHorizontalFrame):
            FXVerticalSeparator(p=self, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=self, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)

        GroupBox_5 = FXGroupBox(p=self, text='\xd4\xfe\xb9\xf5\xb2\xce\xca\xfd', opts=FRAME_GROOVE)
            
        vf = FXVerticalFrame(GroupBox_5, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X, 0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table = AFXTable(vf, 16, 14, 16, 14, form.ZgTableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        table.setPopupOptions(AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_INSERT_ROW|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_READ_FROM_FILE)
        # table.setColumnType(0, AFXTable.FLOAT)
        table.setColumnWidth(0, 50)
        table.setLeadingRows(1)
        table.setLeadingColumns(1)
        table.setColumnWidth(1, 50)
        table.setColumnType(1, AFXTable.FLOAT)
        table.setColumnWidth(2, 80)
        table.setColumnType(2, AFXTable.FLOAT)
        table.setColumnWidth(3, 60)
        table.setColumnType(3, AFXTable.FLOAT)
        table.setColumnWidth(4, 60)
        table.setColumnType(4, AFXTable.FLOAT)
        table.setColumnWidth(5, 60)
        table.setColumnType(5, AFXTable.FLOAT)
        table.setColumnWidth(6, 60)
        table.setColumnType(6, AFXTable.FLOAT)
        table.setColumnWidth(7, 60)
        table.setColumnType(7, AFXTable.FLOAT)
        table.setColumnWidth(8, 60)
        table.setColumnType(8, AFXTable.FLOAT)
        table.setColumnWidth(9, 60)
        table.setColumnType(9, AFXTable.FLOAT)
        table.setColumnWidth(10, 60)
        table.setColumnType(10, AFXTable.FLOAT)
        table.setColumnWidth(11, 60)
        table.setColumnType(11, AFXTable.FLOAT)
        table.setColumnWidth(12, 60)
        table.setColumnType(12, AFXTable.FLOAT)
        table.setColumnWidth(13, 60)
        table.setColumnType(13, AFXTable.FLOAT)

        # 表头：：：：：布置、孔型、孔型直径、槽底宽度、孔型高度、倾斜度、轧辊直径、延伸长度、辊缝宽度、圆角系数、轧机间距、轧辊转速、轧辊温度
        table.setLeadingRowLabels('\xb2\xbc\xd6\xc3\t\xbf\xd7\xd0\xcd\t\xbf\xd7\xd0\xcd\xd6\xb1\xbe\xb6\t\xb2\xdb\xb5\xd7\xbf\xed\xb6\xc8\t\xbf\xd7\xd0\xcd\xb8\xdf\xb6\xc8\t\xc7\xe3\xd0\xb1\xb6\xc8\t\xd4\xfe\xb9\xf5\xd6\xb1\xbe\xb6\t\xd1\xd3\xc9\xec\xb3\xa4\xb6\xc8\t\xb9\xf5\xb7\xec\xbf\xed\xb6\xc8\t\xd4\xb2\xbd\xc7\xcf\xb5\xca\xfd\t\xd4\xfe\xbb\xfa\xbc\xe4\xbe\xe0\t\xd4\xfe\xb9\xf5\xd7\xaa\xcb\xd9\t\xd4\xfe\xb9\xf5\xce\xc2\xb6\xc8')
        table.setStretchableColumn( table.getNumColumns()-1 )
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)

        # 表格第一列下拉菜单 （卧式，立式）
        listId=table.addList('\xce\xd4\xca\xbd\t\xc1\xa2\xca\xbd')
        table.setColumnType(1,AFXTable.LIST)
        table.setColumnListId(1,listId)

        # 表格第2列下拉菜单 （箱型孔轧辊，椭圆孔轧辊，圆型孔轧辊）
        listId=table.addList('\xcf\xe4\xd0\xcd\xbf\xd7\xd4\xfe\xb9\xf5\t\xcd\xd6\xd4\xb2\xbf\xd7\xd4\xfe\xb9\xf5\t\xd4\xb2\xd0\xcd\xbf\xd7\xd4\xfe\xb9\xf5')
        table.setColumnType(2,AFXTable.LIST)
        table.setColumnListId(2,listId)

        # 分割线
        if isinstance(self, FXHorizontalFrame):
            FXVerticalSeparator(p=self, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=self, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        
        # ######################################################### 三辊轧机参数######################################################
        GroupBox_6 = FXGroupBox(p=self, text='\xc8\xfd\xb9\xf5\xd4\xfe\xbb\xfa\xb2\xce\xca\xfd', opts=FRAME_GROOVE)
        vf = FXVerticalFrame(GroupBox_6, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X, 0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be

        vf.setSelector(99)
        table = AFXTable(vf, 6, 14, 6, 14, form.TZgTableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        table.setPopupOptions(AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_INSERT_ROW|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_READ_FROM_FILE)
        # table.setColumnType(0, AFXTable.FLOAT)
        table.setColumnWidth(0, 50)
        table.setLeadingRows(1)
        table.setLeadingColumns(1)
        table.setColumnWidth(1, 50)
        table.setColumnType(1, AFXTable.FLOAT)
        table.setColumnWidth(2, 80)
        table.setColumnType(2, AFXTable.FLOAT)
        table.setColumnWidth(3, 60)
        table.setColumnType(3, AFXTable.FLOAT)
        table.setColumnWidth(4, 60)
        table.setColumnType(4, AFXTable.FLOAT)
        table.setColumnWidth(5, 60)
        table.setColumnType(5, AFXTable.FLOAT)
        table.setColumnWidth(6, 60)
        table.setColumnType(6, AFXTable.FLOAT)
        table.setColumnWidth(7, 60)
        table.setColumnType(7, AFXTable.FLOAT)
        table.setColumnWidth(8, 60)
        table.setColumnType(8, AFXTable.FLOAT)
        table.setColumnWidth(9, 60)
        table.setColumnType(9, AFXTable.FLOAT)
        table.setColumnWidth(10, 60)
        table.setColumnType(10, AFXTable.FLOAT)
        table.setColumnWidth(11, 60)
        table.setColumnType(11, AFXTable.FLOAT)
        table.setColumnWidth(12, 60)
        table.setColumnType(12, AFXTable.FLOAT)
        table.setColumnWidth(13, 60)
        table.setColumnType(13, AFXTable.FLOAT)


        # 表头：：：：：布置、孔型、孔型直径、轧辊直径DSI、辊缝宽度W、延伸长度、辊缝宽度、扩展圆角α、弧线夹角β、 PSI、槽底圆弧R、轧机间距、轧辊转速、轧辊温度
        table.setLeadingRowLabels('\xb2\xbc\xd6\xc3\t\xbf\xd7\xd0\xcd\t\xbf\xd7\xd0\xcd\xd6\xb1\xbe\xb6\t\xd4\xfe\xb9\xf5\xd6\xb1\xbe\xb6\t\xb9\xf5\xb7\xec\xbf\xed\xb6\xc8\t\xd1\xd3\xc9\xec\xb3\xa4\xb6\xc8\t\xc0\xa9\xd5\xb9\xd4\xb2\xbd\xc7\xa6\xc1\t\xbb\xa1\xcf\xdf\xbc\xd0\xbd\xc7\xa6\xc2\tPSI\t\xb2\xdb\xb5\xd7\xd4\xb2\xbb\xa1R\t\xd4\xfe\xbb\xfa\xbc\xe4\xbe\xe0\t\xd4\xfe\xb9\xf5\xd7\xaa\xcb\xd9\t\xd4\xfe\xb9\xf5\xce\xc2\xb6\xc8')
        table.setStretchableColumn( table.getNumColumns()-1 )
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)

        # 表格第一列下拉菜单 （正Y，倒Y）
        listId=table.addList('\xd5\xfdY\t\xb5\xb9Y')
        table.setColumnType(1,AFXTable.LIST)
        table.setColumnListId(1,listId)

        # 表格第2列下拉菜单 （平三角孔，圆三角孔，弧三角孔）
        listId=table.addList('\xbb\xa1\xc8\xfd\xbd\xc7\xbf\xd7\t\xd4\xb2\xc8\xfd\xbd\xc7\xbf\xd7\t\xc6\xbd\xc8\xfd\xbd\xc7\xbf\xd7\tKOCKS')
        table.setColumnType(2,AFXTable.LIST)
        table.setColumnListId(2,listId)



        # 注释旁白
        # l = FXLabel(p=self, text='\xd4\xb2\xd0\xcd\xbf\xd7\xa3\xba\xb2\xbc\xd6\xc3\xa1\xa2\xbf\xd7\xd0\xcd\xa1\xa2\xbf\xd7\xd0\xcd\xd6\xb1\xbe\xb6\xa1\xa2\xd4\xfe\xb9\xf5\xd6\xb1\xbe\xb6\xa1\xa2\xd1\xd3\xc9\xec\xb3\xa4\xb6\xc8\xa1\xa2\xb9\xf5\xb7\xec\xbf\xed\xb6\xc8\xa1\xa2\xd4\xb2\xbd\xc7\xcf\xb5\xca\xfd', opts=JUSTIFY_LEFT)
        # l = FXLabel(p=self, text='\xcf\xe4\xd0\xcd\xbf\xd7\xa3\xba\xb2\xbc\xd6\xc3\xa1\xa2\xbf\xd7\xd0\xcd\xa1\xa2\xb2\xdb\xb5\xd7\xbf\xed\xb6\xc8\xa1\xa2\xbf\xd7\xd0\xcd\xb8\xdf\xb6\xc8\xa1\xa2\xc7\xe3\xd0\xb1\xb6\xc8\xa1\xa2\xd4\xfe\xb9\xf5\xd6\xb1\xbe\xb6\xa1\xa2\xd1\xd3\xc9\xec\xb3\xa4\xb6\xc8\xa1\xa2\xb9\xf5\xb7\xec\xbf\xed\xb6\xc8\xa1\xa2\xd4\xb2\xbd\xc7\xcf\xb5\xca\xfd', opts=JUSTIFY_LEFT)
        # l = FXLabel(p=self, text='\xcd\xd6\xd4\xb2\xbf\xd7\xa3\xba\xb2\xbc\xd6\xc3\xa1\xa2\xbf\xd7\xd0\xcd\xa1\xa2\xb2\xdb\xb5\xd7\xbf\xed\xb6\xc8\xa1\xa2\xbf\xd7\xd0\xcd\xb8\xdf\xb6\xc8\xa1\xa2\xd4\xfe\xb9\xf5\xd6\xb1\xbe\xb6\xa1\xa2\xd1\xd3\xc9\xec\xb3\xa4\xb6\xc8\xa1\xa2\xb9\xf5\xb7\xec\xbf\xed\xb6\xc8\xa1\xa2\xd4\xb2\xbd\xc7\xcf\xb5\xca\xfd', opts=JUSTIFY_LEFT)

       
        
        # 下拉菜单
        # ComboBox_2 = AFXComboBox(p=self, ncols=0, nvis=1, text='\xcf\xc2\xc0\xad\xb2\xcb\xb5\xa5:', tgt=form.List1Kw, sel=0)
        # ComboBox_2.setMaxVisible(10)
        # ComboBox_2.appendItem(text='Item 1')
        # ComboBox_2.appendItem(text='Item 2')
        # ComboBox_2.appendItem(text='Item 3')

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

