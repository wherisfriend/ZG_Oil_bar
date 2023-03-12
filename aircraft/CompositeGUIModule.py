#!/usr/bin/python
#-*-coding: UTF-8-*-
#-*-coding: mbcs -*- 
from abaqusGui import *                                     


# �����Զ����������Ϳ����
from abaqus_plugins.box_create.box_create_plugin import Box_create_plugin
# �����Զ���������Բ�����
from abaqus_plugins.tuo_shell.tuo_shell_plugin import Tuo_shell_plugin
# �����Զ�������Բ�Ϳ����
from abaqus_plugins.yuan2023.yuan2023_plugin import Yuan2023_plugin

# ���������Զ��廡�����ο�
from abaqus_plugins.HUSAN_2023.hUSAN_2023_plugin import HUSAN_2023_plugin
# ���������Զ���ֱ�����ο�
from abaqus_plugins.PingSan2023.pingSan2023_plugin import PingSan2023_plugin
# ���������Զ���Բ����
from abaqus_plugins.YUAN_2023.yUAN_2023_plugin import YUAN_2023_plugin
# ���������Զ���KOCKS��
from abaqus_plugins.KOCKS_2023.kOCKS_2023_plugin import KOCKS_2023_plugin

#���빦������壺������ѧ���ܲ�ѯ
from aircraft.materialcheck.materialcheck_plugin import materialcheck_plugin

#������ٽ�ģϵͳ       
from abaqus_plugins.PAF_test.pAF_test_plugin import PAF_test_plugin



class CompositeGUIModule(AFXModuleGui):
    
    def __init__(self):
        mw=getAFXApp().getAFXMainWindow()
        AFXModuleGui.__init__(self, moduleName='Composites', displayTypes=AFXModuleGui.PART)
        mw.appendApplicableModuleForTreeTab('Model', self.getModuleName() )
        #����ģ�����Ŀ�����
        mw.appendVisibleModuleForTreeTab('Model', self.getModuleName() )
        #����ģ�����Ŀɼ���

        # ʵ�����������Ϳ�
        box_create_Plugin1 = Box_create_plugin(self)
        

        # 
        #��ģ���ж���˵�
        #
        menu = AFXMenuPane(self)               
        #�����˵���
        AFXMenuTitle(self, '&��������', None, menu)
        AFXMenuCommand(self, menu, '&���Ϳ�����', None,  box_create_Plugin1,  AFXMode.ID_ACTIVATE)
        AFXMenuCommand(self, menu, '&��Բ������', None,  Tuo_shell_plugin(self),  AFXMode.ID_ACTIVATE)
        AFXMenuCommand(self, menu, '&Բ��������', None,  Yuan2023_plugin(self),  AFXMode.ID_ACTIVATE)

        menu2 = AFXMenuPane(self)               
        #�����˵���
        AFXMenuTitle(self, '&Y����������', None, menu2)
        AFXMenuCommand(self, menu2, '&�����ǿ�����', None,  HUSAN_2023_plugin(self),  AFXMode.ID_ACTIVATE)
        AFXMenuCommand(self, menu2, '&ֱ���ǿ�����', None,  PingSan2023_plugin(self),  AFXMode.ID_ACTIVATE)
        AFXMenuCommand(self, menu2, '&Բ��������', None,  YUAN_2023_plugin(self),  AFXMode.ID_ACTIVATE)
        AFXMenuCommand(self, menu2, '&KOCKS����', None,  KOCKS_2023_plugin(self),  AFXMode.ID_ACTIVATE)

        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~������~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        #����������
        group = AFXToolboxGroup(self)   
        #���幤���� 
        #�ڹ������д�������������Ĺ��ܼ�
        #
        
        AFXToolButton(p=group, label="\t�������Ϳ�",       icon = afxCreatePNGIcon(r"icon\box.BMP"),      tgt=Box_create_plugin(self), sel=AFXMode.ID_ACTIVATE)
        
        AFXToolButton(p=group, label="\t������Բ��",       icon = afxCreatePNGIcon(r"icon\tuo.BMP"),      tgt=Tuo_shell_plugin(self), sel=AFXMode.ID_ACTIVATE)
        
        AFXToolButton(p=group, label="\t����Բ�Ϳ�",       icon = afxCreatePNGIcon(r"icon\yuan.BMP"),     tgt=Yuan2023_plugin(self), sel=AFXMode.ID_ACTIVATE)
        
        AFXToolButton(p=group, label="\t���������ǿ�����",   icon = afxCreatePNGIcon(r"icon\huicon.PNG"),   tgt=HUSAN_2023_plugin(self), sel=AFXMode.ID_ACTIVATE)
        AFXToolButton(p=group, label="\t����ֱ���ǿ�����",   icon = afxCreatePNGIcon(r"icon\PING.PNG"),   tgt=PingSan2023_plugin(self), sel=AFXMode.ID_ACTIVATE)
        AFXToolButton(p=group, label="\t����Բ��������",   icon = afxCreatePNGIcon(r"icon\YUAN22.PNG"),   tgt=YUAN_2023_plugin(self), sel=AFXMode.ID_ACTIVATE)
        AFXToolButton(p=group, label="\tKOCKS��������",   icon = afxCreatePNGIcon(r"icon\YUAN22.PNG"),   tgt=KOCKS_2023_plugin(self), sel=AFXMode.ID_ACTIVATE)
        AFXToolButton(p=group, label="\t���ٽ�ģ",       icon = afxCreatePNGIcon(r"icon\pAF.png"),   tgt=PAF_test_plugin(self),   sel=AFXMode.ID_ACTIVATE) 


    
         #
        AFXToolButton(p=group, label="\t���Ͽ��ѯ",       icon = afxCreatePNGIcon(r"icon\findmaterial.png"),   tgt=materialcheck_plugin(self),   sel=AFXMode.ID_ACTIVATE) 




    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       
    def getKernelInitializationCommand(self):
        return 'from abaqus_plugins.box_create import box02\
                \nfrom abaqus_plugins.tuo_shell import tuo\
                \nfrom abaqus_plugins.yuan2023 import yuan2023\
                \nfrom abaqus_plugins.PingSan2023 import ping3_2023\
                \nfrom abaqus_plugins.YUAN_2023 import yuan2023_fun\
                \nfrom abaqus_plugins.HUSAN_2023 import hu3_2023\
                \nfrom abaqus_plugins.KOCKS_2023 import kocks_2023\
                \nfrom abaqus_plugins.PAF_test import PAFSystem'

        #�����ں˳�ʼ����
#
CompositeGUIModule= CompositeGUIModule() 
#ʵ�����Զ���GUIģ��