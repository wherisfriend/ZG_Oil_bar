# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class PAF_test_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='Process',
            objectName='PAFSystem', registerQuery=False)
        pickedDefault = ''

        self.DKw = AFXStringKeyword(self.cmd, 'D', True, '168')
        self.ThickKw = AFXStringKeyword(self.cmd, 'Thick', True, '6')
        self.LKw = AFXStringKeyword(self.cmd, 'L', True, '1000')
        self.SN_TmpKw = AFXStringKeyword(self.cmd, 'SN_Tmp', True, '298.15')
        self.TmpKw = AFXStringKeyword(self.cmd, 'Tmp', True, '1473.15')
        self.VelKw = AFXStringKeyword(self.cmd, 'Vel', True, '231')
        self.MCKw = AFXStringKeyword(self.cmd, 'frictCoeff', True, '0.3')
        self.ZLSFKw = AFXStringKeyword(self.cmd, 'ZLSF', True, '10000')
        self.MeshSizeKw = AFXStringKeyword(self.cmd, 'MeshSize', True, '10')
        self.AirFilmCoffKw = AFXStringKeyword(self.cmd, 'AirFilmCoff', True, '0.3')
        self.TimwWorKw = AFXStringKeyword(self.cmd, 'TimwWork', True, '10.0')

        self.modelNameKw = AFXStringKeyword(self.cmd, 'modelName', True)
        self.materialXinKw = AFXStringKeyword(self.cmd, 'materialXin', True)
        self.modelName2Kw = AFXStringKeyword(self.cmd, 'modelName2', True)
        self.materialTaoKw = AFXStringKeyword(self.cmd, 'materialTao', True)

        self.ZgTableKw = AFXTableKeyword(self.cmd, 'ZgTable', True)
        
        self.ZgTableKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(1, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(2, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(3, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(4, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(5, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(6, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(7, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(8, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(9, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(10, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(11, AFXTABLE_TYPE_STRING)
        self.ZgTableKw.setColumnType(12, AFXTABLE_TYPE_STRING)

        # 三辊轧机
        self.TZgTableKw = AFXTableKeyword(self.cmd, 'TZgTable', True)
        self.TZgTableKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(1, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(2, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(3, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(4, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(5, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(6, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(7, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(8, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(9, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(10, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(11, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(12, AFXTABLE_TYPE_STRING)
        self.TZgTableKw.setColumnType(13, AFXTABLE_TYPE_STRING)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import pAF_testDB
        return pAF_testDB.PAF_testDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='\xd4\xfe\xb9\xf5\xc9\xfa\xb3\xc9\xb2\xe2\xca\xd4', 
    object=PAF_test_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import PAFSystem',
    applicableModules=ALL,
    version='N/A',
    author='N/A',
    description='N/A',
    helpUrl='N/A'
)
