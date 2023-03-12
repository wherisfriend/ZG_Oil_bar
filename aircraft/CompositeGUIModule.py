#!/usr/bin/python
#-*-coding: UTF-8-*-
#-*-coding: mbcs -*- 
from abaqusGui import *                                     


# 导入自定义两辊箱型孔组件
from abaqus_plugins.box_create.box_create_plugin import Box_create_plugin
# 导入自定义两辊椭圆孔组件
from abaqus_plugins.tuo_shell.tuo_shell_plugin import Tuo_shell_plugin
# 导入自定义两辊圆型孔组件
from abaqus_plugins.yuan2023.yuan2023_plugin import Yuan2023_plugin

# 导入三辊自定义弧三角形孔
from abaqus_plugins.HUSAN_2023.hUSAN_2023_plugin import HUSAN_2023_plugin
# 导入三辊自定义直三角形孔
from abaqus_plugins.PingSan2023.pingSan2023_plugin import PingSan2023_plugin
# 导入三辊自定义圆孔型
from abaqus_plugins.YUAN_2023.yUAN_2023_plugin import YUAN_2023_plugin
# 导入三辊自定义KOCKS型
from abaqus_plugins.KOCKS_2023.kOCKS_2023_plugin import KOCKS_2023_plugin

#导入功能组件五：材料力学性能查询
from aircraft.materialcheck.materialcheck_plugin import materialcheck_plugin

#导入快速建模系统       
from abaqus_plugins.PAF_test.pAF_test_plugin import PAF_test_plugin



class CompositeGUIModule(AFXModuleGui):
    
    def __init__(self):
        mw=getAFXApp().getAFXMainWindow()
        AFXModuleGui.__init__(self, moduleName='Composites', displayTypes=AFXModuleGui.PART)
        mw.appendApplicableModuleForTreeTab('Model', self.getModuleName() )
        #设置模型树的可用性
        mw.appendVisibleModuleForTreeTab('Model', self.getModuleName() )
        #设置模型树的可见性

        # 实例化两辊箱型孔
        box_create_Plugin1 = Box_create_plugin(self)
        

        # 
        #在模块中定义菜单
        #
        menu = AFXMenuPane(self)               
        #创建菜单栏
        AFXMenuTitle(self, '&两辊轧机', None, menu)
        AFXMenuCommand(self, menu, '&箱型孔轧辊', None,  box_create_Plugin1,  AFXMode.ID_ACTIVATE)
        AFXMenuCommand(self, menu, '&椭圆孔轧辊', None,  Tuo_shell_plugin(self),  AFXMode.ID_ACTIVATE)
        AFXMenuCommand(self, menu, '&圆孔型轧辊', None,  Yuan2023_plugin(self),  AFXMode.ID_ACTIVATE)

        menu2 = AFXMenuPane(self)               
        #创建菜单栏
        AFXMenuTitle(self, '&Y型三辊轧机', None, menu2)
        AFXMenuCommand(self, menu2, '&弧三角孔轧辊', None,  HUSAN_2023_plugin(self),  AFXMode.ID_ACTIVATE)
        AFXMenuCommand(self, menu2, '&直三角孔轧辊', None,  PingSan2023_plugin(self),  AFXMode.ID_ACTIVATE)
        AFXMenuCommand(self, menu2, '&圆孔型轧辊', None,  YUAN_2023_plugin(self),  AFXMode.ID_ACTIVATE)
        AFXMenuCommand(self, menu2, '&KOCKS轧辊', None,  KOCKS_2023_plugin(self),  AFXMode.ID_ACTIVATE)

        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~工具箱~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        #创建工具箱
        group = AFXToolboxGroup(self)   
        #定义工具箱 
        #在工具箱中创建功能组件二的功能键
        #
        
        AFXToolButton(p=group, label="\t两辊箱型孔",       icon = afxCreatePNGIcon(r"icon\box.BMP"),      tgt=Box_create_plugin(self), sel=AFXMode.ID_ACTIVATE)
        
        AFXToolButton(p=group, label="\t两辊椭圆孔",       icon = afxCreatePNGIcon(r"icon\tuo.BMP"),      tgt=Tuo_shell_plugin(self), sel=AFXMode.ID_ACTIVATE)
        
        AFXToolButton(p=group, label="\t两辊圆型孔",       icon = afxCreatePNGIcon(r"icon\yuan.BMP"),     tgt=Yuan2023_plugin(self), sel=AFXMode.ID_ACTIVATE)
        
        AFXToolButton(p=group, label="\t三辊弧三角孔轧辊",   icon = afxCreatePNGIcon(r"icon\huicon.PNG"),   tgt=HUSAN_2023_plugin(self), sel=AFXMode.ID_ACTIVATE)
        AFXToolButton(p=group, label="\t三辊直三角孔轧辊",   icon = afxCreatePNGIcon(r"icon\PING.PNG"),   tgt=PingSan2023_plugin(self), sel=AFXMode.ID_ACTIVATE)
        AFXToolButton(p=group, label="\t三辊圆孔型轧辊",   icon = afxCreatePNGIcon(r"icon\YUAN22.PNG"),   tgt=YUAN_2023_plugin(self), sel=AFXMode.ID_ACTIVATE)
        AFXToolButton(p=group, label="\tKOCKS孔型轧辊",   icon = afxCreatePNGIcon(r"icon\YUAN22.PNG"),   tgt=KOCKS_2023_plugin(self), sel=AFXMode.ID_ACTIVATE)
        AFXToolButton(p=group, label="\t快速建模",       icon = afxCreatePNGIcon(r"icon\pAF.png"),   tgt=PAF_test_plugin(self),   sel=AFXMode.ID_ACTIVATE) 


    
         #
        AFXToolButton(p=group, label="\t材料库查询",       icon = afxCreatePNGIcon(r"icon\findmaterial.png"),   tgt=materialcheck_plugin(self),   sel=AFXMode.ID_ACTIVATE) 




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

        #定义内核初始命令
#
CompositeGUIModule= CompositeGUIModule() 
#实例化自定义GUI模块