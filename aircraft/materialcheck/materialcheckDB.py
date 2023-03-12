#!/usr/bin/python
#-*-coding: UTF-8-*-
#-*-coding: mbcs -*- 
from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class materialcheckDB(AFXDataDialog):
    [ID_TABLE,ID_CHECK,ID_LASTONE,ID_NEXTONE]=range(AFXForm.ID_LAST, AFXForm.ID_LAST+4)      
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):
       
        # Construct the base class.
        #
        FXMAPFUNC(self, SEL_CLICKED, self.ID_TABLE,
                       materialcheckDB.onClickTable)

        AFXDataDialog.__init__(self, form, '���ý���������ѧ���ܲ�ѯ����',
            self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

#        okBtn = self.getActionButton(self.ID_CLICKED_OK)
#        okBtn.setText('OK')
#            
#
#        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
#        applyBtn.setText('Apply')
#
        cancelBtn = self.getActionButton(self.ID_CLICKED_CANCEL )
        cancelBtn.setText('�ر�')

           
        GroupBox_1 = FXGroupBox(p=self, text='', opts=FRAME_GROOVE)
        vf = FXVerticalFrame(GroupBox_1, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
#���ò������ݿ��ļ�
        thisPath = os.path.abspath(__file__)                                                      
        thisDir = os.path.dirname(thisPath)                                                              
        filename= os.path.join(thisDir, 'material_database.dat') 
        f=file(filename,'r')
        k=0
        while True:
            line=f.readline()
            k+=1
            if len(line)==0:
                break
        self.num=k #��������������
        self.table = AFXTable(vf, 16, 11, k, 11, self,self.ID_TABLE, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.table.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_WRITE_TO_FILE)
        self.table.setLeadingRows(1)
        self.table.setLeadingColumns(1)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnType(1, AFXTable.TEXT)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnType(2, AFXTable.FLOAT)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnType(3, AFXTable.FLOAT)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnType(4, AFXTable.FLOAT)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnType(5, AFXTable.FLOAT)
        self.table.setColumnWidth(6, 100)
        self.table.setColumnType(6, AFXTable.FLOAT)
        self.table.setColumnWidth(7, 100)
        self.table.setColumnType(7, AFXTable.FLOAT)
        self.table.setColumnWidth(8, 100)
        self.table.setColumnType(8, AFXTable.FLOAT)
        self.table.setColumnWidth(9, 100)
        self.table.setColumnType(9, AFXTable.FLOAT)
        self.table.setColumnWidth(10, 100)
        self.table.setColumnType(10, AFXTable.FLOAT)

        self.table.setLeadingRowLabels('��������	����ģ��\n(N/m^2)	���ɱ�	�����ܶ�\n(kg/m^3)	����ģ��\n(N/m^2)	����ǿ��\n(N/m^2)	����ǿ��\n(N/m^2)	������ϵ��\n(/Kelven)	����\n(J/(kg.K))	�ȵ���\n(W/(m.k))')

        self.table.setStretchableColumn( self.table.getNumColumns()-1 )
        self.table.showHorizontalGrid(True)
        self.table.showVerticalGrid(True)
        self.table.setColumnSortable(1, True)
        self.table.setColumnSortable(2, True)
        self.table.setColumnSortable(3, True)
        self.table.setColumnSortable(4, True)
        self.table.setColumnSortable(5, True)
        self.table.setColumnSortable(6, True)
        self.table.setColumnSortable(7, True)
        self.table.setColumnSortable(8, True)
        self.table.setColumnSortable(9, True)
        self.table.setColumnSortable(10, True)

################################�����ݿ⸳ֵ
        f=file(filename,'r')
        k=1
        while True:
            line=f.readline()
            if len(line)==0:
                break
            data=line.strip().split(',')
            self.table.setItemText(k,1, data[0])
            self.table.setItemText(k,2, data[1])
            self.table.setItemText(k,3, data[2])            
            self.table.setItemText(k,4, data[3])
            self.table.setItemText(k,5, data[4])
            self.table.setItemText(k,6, data[5])
            self.table.setItemText(k,7, data[6])
            self.table.setItemText(k,8, data[7])
            self.table.setItemText(k,9, data[8])
            self.table.setItemText(k,10, data[9])
            k+=1

        for i in range(1,11):
            self.table.setColumnEditable(i, False) #����������Ϊ���ɱ༭
##############################
        f.close()
        for i in range(2,11):
            self.table.setColumnJustify(i, self.table.CENTER)
        HFrame_1 = FXHorizontalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=HFrame_1, ncols=18, labelText='����Ҫ��ѯ�Ĳ�������ؼ���:', tgt=form.searchnameKw, sel=0)
        FXButton(p=HFrame_1, text='����', ic=None, tgt=self, sel=self.ID_CHECK) 
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CHECK, 
             materialcheckDB.onCmdCheck)
        FXButton(p=HFrame_1, text='��һ��', ic=None, tgt=self, sel=self.ID_LASTONE,x=100,y=0)     #������ǰ���Ұ�ť
        FXButton(p=HFrame_1, text='��һ��', ic=None, tgt=self, sel=self.ID_NEXTONE,x=100,y=0)     #�������Ϻ���Ұ�ť
        FXMAPFUNC(self, SEL_COMMAND, self.ID_LASTONE, 
             materialcheckDB.onCmdLastone)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_NEXTONE, 
             materialcheckDB.onCmdNextone)
        self.form=form
        self.resultnum=[]
    def onClickTable(self, sender, sel, ptr):    #����������

        status, x, y, buttons = self.table.getCursorPosition()
        column = self.table.getColumnAtX(x)
        row = self.table.getRowAtY(y)

        # Ignore clicks on table headers.
        if row != 0 or column == 0:
            return

        values = []
        index = 1
        for row in range(1, self.table.getNumRows()):
            values.append( (self.table.getItemFloatValue(
                row, column), index) )
            index += 1

        values.sort()
        if self.table.getColumnSortOrder(column) == \
            AFXTable.SORT_ASCENDING:
                values.reverse()

        items = []
        for value, index in values:
            name = self.table.getItemText(index, 1)
            Value2 = self.table.getItemFloatValue(index, 2)
            Value3 = self.table.getItemFloatValue(index, 3)
            Value4 = self.table.getItemFloatValue(index, 4)
            Value5 = self.table.getItemFloatValue(index, 5)
            Value6 = self.table.getItemFloatValue(index, 6)
            Value7 = self.table.getItemFloatValue(index, 7)
            Value8 = self.table.getItemFloatValue(index, 8)
            Value9 = self.table.getItemFloatValue(index, 9)
            Value10 = self.table.getItemFloatValue(index, 10)
            items.append( (name, Value2, Value3,Value4,Value5,Value6,Value7,Value8,Value9,Value10) )

        row = 1
        for name, Value2, Value3, Value4, Value5, Value6, Value7, Value8, Value9, Value10 in items:
            self.table.setItemText(row, 1, name)
            self.table.setItemFloatValue(row, 2, Value2)
            self.table.setItemFloatValue(row, 3, Value3)
            self.table.setItemFloatValue(row, 4, Value4)
            self.table.setItemFloatValue(row, 5, Value5)
            self.table.setItemFloatValue(row, 6, Value6)
            self.table.setItemFloatValue(row, 7, Value7)
            self.table.setItemFloatValue(row, 8, Value8)
            self.table.setItemFloatValue(row, 9, Value9)
            self.table.setItemFloatValue(row, 10, Value10)
            row += 1
 
    def  onCmdCheck(self, sender, sel, ptr):                    
        k=1
        self.table.makeRowVisible(1)   #ÿ�β���֮ǰ������ع鵽���У��ɷ�ֹ��ǰ����ʱ�����Ҷ��󲻾�����ʾ
        self.resultnum=[]         #ÿ�β��ҿ�ʼ֮ǰ���
        NO_result=0
        if self.form.searchnameKw.getValue()=='':
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea('�������ѯ����' )
            return False            
        while True:
            if k==self.num:           #���������һ��ʱ����ѭ��
                break
            for i in range(1,11):
                self.table.setItemBackColor(k,i,FXRGB(255,255,255))  #������ɫ FXRGB(255,255,255),"Default"
            line=self.table.getItemText(k, 1)
            findname=self.form.searchnameKw.getValue() 
            data=line.strip().split(findname)
            if len(data)>1:
                NO_result+=1
                if  NO_result==1: 
                    self.table.setCurrentItem(k, 1)  #���õ�һ���������Ϊ��ǰѡ����                                                    
                    self.table.makeRowVisible(k+11)    #ʹĳһ�н������ ��+8��֤����   
                for i in range(1,11):
                    self.table.setItemBackColor(k,i, 'Cyan1')
                self.resultnum.append(k)
            k+=1
        mw = getAFXApp().getAFXMainWindow()
        mw.writeToMessageArea('�����ҵ�%i �����,����������ɫ��ע��' % NO_result)
#        print self.resultnum
        
    def  onCmdNextone(self, sender, sel, ptr):                    
        curren_row_num=self.table.getCurrentRow()   #���ص�ǰѡ�е���
        N=len(self.resultnum)
        if N==0:
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea('��δ���ҵ����' ) 
            return False                  
        if self.resultnum[0]!=curren_row_num  :
            self.table.setCurrentItem(self.resultnum[0], 1)                
        for  i in range(0,N-1):
            if  self.resultnum[i]==curren_row_num and self.resultnum[i]!=self.num:   #��֤�������һ��          
                self.table.setCurrentItem(self.resultnum[i+1], 1)  #���õ�һ���������Ϊ��ǰѡ����
                self.table.makeRowVisible(self.resultnum[i+1])    #ʹĳһ�н������ ��+8��֤����          
                for j in range(1,11):
                    self.table.setItemBackColor(self.resultnum[i],j, 'Cyan1')   #�ָ���һ��ԭɫ
                    self.table.setItemBackColor(self.resultnum[i+1],j, 'Red')  #���µĵ�ǰ���ź�ɫ
#                mw = getAFXApp().getAFXMainWindow()
#                mw.writeToMessageArea('���������Ľ����%i������ǰΪ��%i����' % (N,i+1))                
    def  onCmdLastone(self, sender, sel, ptr): 
        curren_row_num=self.table.getCurrentRow()
        N=len(self.resultnum)     
        if N==0:
            mw = getAFXApp().getAFXMainWindow()
            mw.writeToMessageArea('��δ���ҵ����' )
            return False     
        if self.resultnum[N-1]!=curren_row_num  :
            self.table.setCurrentItem(self.resultnum[N-1], 1)   
        for  i in range(1,N):
            if  self.resultnum[i]==curren_row_num and self.resultnum[i]!=self.num:   #��֤�������һ��          
                self.table.setCurrentItem(self.resultnum[i-1], 1)  #���õ�һ���������Ϊ��ǰѡ����
                self.table.makeRowVisible(self.resultnum[i-1])    #ʹĳһ�н������ ��+8��֤����          
                for j in range(1,11):
                    self.table.setItemBackColor(self.resultnum[i],j, 'Cyan1')   #�ָ���һ��ԭɫ
                    self.table.setItemBackColor(self.resultnum[i-1],j, 'Red')  #���µĵ�ǰ���ź�ɫ 
#                mw = getAFXApp().getAFXMainWindow()
#                mw.writeToMessageArea('���������Ľ����%i������ǰΪ��%i����' % (N,i))         