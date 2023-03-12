# -*- coding: mbcs -*-
# Do not delete the following import lines
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
from abaqus import *
from abaqusConstants import *
from sys import getsizeof as getsize
from caeModules import *
from driverUtils import executeOnCaeStartup
from Bar_Tao_fu import bar
import math


# 这是轧辊生成程序
# 装配测试
# 2023年2月15日

# 轧件直径、覆层厚度、轧件长度、芯部材料、套筒材料、室内温度、轧件温度、空气温度、轧件温度、轧件初速度、摩擦系数、质量缩放系数、网格尺寸、空气热交换系数、时间段
def Process(ZgTable, TZgTable, D, Thick, L, materialXin, materialTao,modelName, modelName2, SN_Tmp,Tmp, Vel,frictCoeff, ZLSF, MeshSize, AirFilmCoff, TimwWork):
    du = math.pi/180

    # 轧件建模
    bar(D=D,Thick=Thick, L=L, materialXin=materialXin,materialTao=materialTao,modelName=modelName,modelName2=modelName2)
    session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=160.412414550781,  height=157.169631958008)
    session.viewports['Viewport: 1'].makeCurrent()
    session.viewports['Viewport: 1'].maximize()

    executeOnCaeStartup()

    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=ON)

    # 导入轧辊建模模块"icon\air.PNG"
    import sys
    sys.path.insert(8, r"abaqus_plugins\box_create")
    import box02
    sys.path.insert(9, r"abaqus_plugins\tuo_shell")
    import tuo
    sys.path.insert(10, r"abaqus_plugins\yuan2023")
    import yuan2023

    sys.path.insert(11,   r"abaqus_plugins\PingSan2023")
    import ping3_2023
    sys.path.insert(12,    r"abaqus_plugins\HUSAN_2023")
    import hu3_2023
    sys.path.insert(13,    r"abaqus_plugins\YUAN_2023")
    import yuan2023_fun
    sys.path.insert(14,    r"abaqus_plugins\KOCKS_2023")
    import kocks_2023


    # 轧辊位置Location，
    L = float(0)
    # 获取表格行数
    C_nums = len(ZgTable)
    print('There are '+str(C_nums) + ' rows in the table1')

    # 计数标记
    tag_nums = int(1)

    # 放置坐标
    Pos = float(0)
    
    # *************************************    一、从两棍轧机的表格读取参数(一行一行来,建模轧辊，及装配)*******************************************
    for item in ZgTable:
        partname = 'ZG'+str(tag_nums)
        tag_nums = tag_nums+1

        print(partname)

        # 判断各道次轧辊类型
        # print(item[1])
        # 判断是否是箱型孔轧辊
        if item[1]=='\xcf\xe4\xd0\xcd\xbf\xd7\xd4\xfe\xb9\xf5':
            box02.box(partname_k=partname, D_k=item[6], b_k=item[3], H_k=item[4], y_k=item[5], S_k=item[8], yanshen_k=item[7], r_rate=float(item[9]))
            
        # 判断是否是椭圆孔轧辊
        elif item[1]=='\xcd\xd6\xd4\xb2\xbf\xd7\xd4\xfe\xb9\xf5':
            tuo.tuo2023(partname_k=partname, D_k=item[6], b_value=item[3], H_k=item[4],  S_k=item[8], YS_k=item[7], r_rate=float(item[9]))

        # 判断是否是圆型孔轧辊
        elif item[1]=='\xd4\xb2\xd0\xcd\xbf\xd7\xd4\xfe\xb9\xf5':
            yuan2023.yuan2023(ZJ=item[2], D_k=item[6], S_k=item[8], YS_k=item[7], partname_k=partname, r_radis=item[9])

        else:
            print("weizhicanshu")


        # 添加参考点
        p = mdb.models['Model-1'].parts[partname]
        p.ReferencePoint(point=(0.0, 0.0, 0.0))

        a = mdb.models['Model-1'].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
        
        # 导入零件
        a = mdb.models['Model-1'].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        p = mdb.models['Model-1'].parts[partname]
        a.Instance(name=str(partname+'-1'), part=p, dependent=ON)
        a = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts[partname]
        a.Instance(name=str(partname+'-2'), part=p, dependent=ON)
        session.viewports['Viewport: 1'].view.setValues(width=1883.24, height=931.587, viewOffsetX=39.1868, viewOffsetY=0.952762)
        a = mdb.models['Model-1'].rootAssembly

        # 轧辊在X轴的位置
        ZG = float(item[6])
        # 轧辊在Z轴的位置
        L = L+float(item[10])

        # 如果是卧式
        if item[0] == '\xce\xd4\xca\xbd':
            a = mdb.models['Model-1'].rootAssembly
            a.translate(instanceList=(str(partname+'-1'), ), vector=(ZG/2, 0.0, L))
            a.translate(instanceList=(str(partname+'-2'), ), vector=(-ZG/2, 0.0, L))
        # 如果是立式
        elif item[0] == '\xc1\xa2\xca\xbd':
            a.rotate(instanceList=(str(partname+'-1'), ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=90.0)
            a.rotate(instanceList=(str(partname+'-2'), ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=90.0)
            a.translate(instanceList=(str(partname+'-1'), ), vector=(0.0, ZG/2, L))
            a = mdb.models['Model-1'].rootAssembly
            a.translate(instanceList=(str(partname+'-2'), ), vector=(0.0, -ZG/2, L))

    # *************************************    一、从三棍轧机的表格读取参数(一行一行来,建模轧辊，及装配)*******************************************
    # 获取三辊轧机表格行数
    TC_nums = len(TZgTable)
    print('There are '+str(TC_nums) + ' rows in the table2')

    # 三辊计数标记
    T_tag_nums = int(1)

    for item in TZgTable:
        partname = 'TZG'+str(T_tag_nums)
        T_tag_nums = T_tag_nums+1

        print(partname)

        # 判断各道次轧辊类型
        # 判断是否是弧三角形孔轧辊
        if item[1]=='\xbb\xa1\xc8\xfd\xbd\xc7\xbf\xd7':
            hu3_2023.HU3_2023(partname_k=partname, D_k=item[2], bata_k = item[7], ZGD = item[3], YS_k = item[5], S_k = item[4])
            
            
        # 判断是否是圆三角形孔轧辊
        elif item[1]=='\xd4\xb2\xc8\xfd\xbd\xc7\xbf\xd7':
            yuan2023_fun.yuankong(partname_k = partname, ZGD_k = item[3], YS_k = item[5], S_k = item[4], alf_k = item[6], D_k = item[2])

        # 判断是否是平三角形型孔轧辊
        elif item[1]=='\xc6\xbd\xc8\xfd\xbd\xc7\xbf\xd7':
            ping3_2023.PING3_2023(partname = partname, ZGD = item[3], D=item[2], S_k=item[4], YS=item[5])
        
        # 判断是否是KOCKS
        elif item[1] == 'KOCKS':
            kocks_2023.KOCKS_2023(partname_k=partname, DSI=item[2], PSI=item[8], ZGD=item[3], YS_k=item[5], W_k=item[4], R_k=item[9])

        else:
            print("weizhicanshu_table2")
        
        # 开始装配
        a = mdb.models['Model-1'].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
        
        # 导入零件,三个轧辊
        a = mdb.models['Model-1'].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        p = mdb.models['Model-1'].parts[partname]
        a.Instance(name=str(partname+'-1'), part=p, dependent=ON)
        a = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts[partname]
        a.Instance(name=str(partname+'-2'), part=p, dependent=ON)
        a = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts[partname]
        a.Instance(name=str(partname+'-3'), part=p, dependent=ON)

        a = mdb.models['Model-1'].rootAssembly
       
   
        # 轧辊在Z轴的位置
        L = L+float(item[10])
        # 轧辊半径
        TZGR = float(item[3])/2
        # 如果是正Y型
        if item[0] == '\xd5\xfdY':
            a.rotate(instanceList=(str(partname + '-1'), ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, -10.0), angle=90.0)
            a.translate(instanceList=(str(partname + '-1'), ), vector=(0.0, -TZGR, L))

            a.rotate(instanceList=(str(partname+'-2'), ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, -10.0), angle=-30.0)
            a.translate(instanceList=(str(partname+'-2'), ), vector=(TZGR*math.cos(30*du), TZGR/2 , L))

            a.rotate(instanceList=(str(partname+'-3'), ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, -10.0), angle=30.0)
            a.translate(instanceList=(str(partname+'-3'), ), vector=(-TZGR*math.cos(30*du), TZGR/2 , L))

        
        # 如果是倒Y型
        elif item[0] == '\xb5\xb9Y':
            a.rotate(instanceList=(str(partname + '-1'), ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, -10.0), angle=90.0)
            a.translate(instanceList=(str(partname + '-1'), ), vector=(0.0, TZGR, L))

            a.rotate(instanceList=(str(partname+'-2'), ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, -10.0), angle=30.0)
            a.translate(instanceList=(str(partname+'-2'), ), vector=(TZGR*math.cos(30*du), -TZGR/2 , L))

            a.rotate(instanceList=(str(partname+'-3'), ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, -10.0), angle=-30.0)
            a.translate(instanceList=(str(partname+'-3'), ), vector=(-TZGR*math.cos(30*du), -TZGR/2 , L))
            

        
    # # 切换到YZ视图
    # session.viewports['Viewport: 1'].view.setValues(session.views['Left'])

    # *************************************创建step、以及接触关系**************************************************************************
    # 创建分析步， 2023.2.20日
    # 创建分析步 Step-1， 仿真时间为timePeriod 10s ， 质量缩放系数ZLSF 为10000.0

    mdb.models['Model-1'].TempDisplacementDynamicsStep(name='Step-1',  previous='Initial', timePeriod=float(TimwWork), massScaling=((SEMI_AUTOMATIC, MODEL, AT_BEGINNING, float(ZLSF), 0.0, None, 0, 0, 0.0, 0.0, 0, None), ),  improvedDtMethod=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, constraints=ON, connectors=ON, engineeringFeatures=ON,  adaptiveMeshConstraints=OFF)

    # *******在接触模块创建接触关系**********
    mdb.models['Model-1'].ContactProperty('IntProp-1')
    # 设置切向行为、摩擦系数frictCoeff:0.3、
    mdb.models['Model-1'].interactionProperties['IntProp-1'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
        table=((float(frictCoeff), ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    # 设置发向行为
    mdb.models['Model-1'].interactionProperties['IntProp-1'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)
    # 设置热传导率
    mdb.models['Model-1'].interactionProperties['IntProp-1'].ThermalConductance(
        definition=TABULAR, clearanceDependency=ON, pressureDependency=OFF, 
        temperatureDependencyC=OFF, massFlowRateDependencyC=OFF, dependenciesC=0, 
        clearanceDepTable=((15.0, 0.0), (0.0, 10.0)))
    #: The interaction property "IntProp-1" has been created.


    #  *******#############################################二、配置轧件和两棍轧辊的接触关系#####################################**********

    # 套筒的外表面和一号轧辊的外表面
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['TaoTong-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#f ]', ), )
    region1=a.Surface(side1Faces=side1Faces1, name='WorkFace')

    # for循环建立每个轧辊和轧件的表面接触关系
    # 计数标记
    flag_nums = int(1)
    for i in range(C_nums):
        # 一次创建一个道次，相同两个轧辊和轧件的关系
        # 创建标签如ZG1-1、ZG1-2
        ZG_partname1='ZG'+str(flag_nums)+'-1'
        ZG_partname2='ZG'+str(flag_nums)+'-2'
        # 轧辊表面命名,如WR1-1、WR1-2
        ZG_face1 = 'WR'+str(flag_nums)+'-1'
        ZG_face2 = 'WR'+str(flag_nums)+'-2'
        # 接触关系命名。 ZG1-1_Work
        JC1 = ZG_partname1 + 'Work'
        JC2 = ZG_partname2 + 'Work'
        
        flag_nums = flag_nums+1

        # 创建ZG1-1零件的表面与轧件工作面的接触关系
        a = mdb.models['Model-1'].rootAssembly
        s1 = a.instances[ZG_partname1].faces
        side1Faces1 = s1.getSequenceFromMask(mask=('[#1ff ]', ), )
        region2=a.Surface(side1Faces=side1Faces1, name=ZG_face1)
        mdb.models['Model-1'].SurfaceToSurfaceContactExp(name = JC1, 
            createStepName='Initial', master = region1, slave = region2, 
            mechanicalConstraint=KINEMATIC, sliding=FINITE, 
            interactionProperty='IntProp-1', initialClearance=OMIT, datumAxis=None, 
            clearanceRegion=None)
        #: The interaction "Int-1" has been created.

        a = mdb.models['Model-1'].rootAssembly
        region1=a.surfaces['WorkFace']
        a = mdb.models['Model-1'].rootAssembly
        s1 = a.instances[ZG_partname2].faces
        side1Faces1 = s1.getSequenceFromMask(mask=('[#1ff ]', ), )
        region2=a.Surface(side1Faces=side1Faces1, name=ZG_face2)
        mdb.models['Model-1'].SurfaceToSurfaceContactExp(name =JC2, 
            createStepName='Initial', master = region1, slave = region2, 
            mechanicalConstraint=KINEMATIC, sliding=FINITE, 
            interactionProperty='IntProp-1', initialClearance=OMIT, datumAxis=None, 
            clearanceRegion=None)
        #: The interaction "Int-2" has been created.

    # ****************************##########二、配置轧件和三棍轧辊的接触关系#####################################*********
    # for循环建立每个轧辊和轧件的表面接触关系
    # 计数标记
    flag_T_nums = int(1)
    for i in range(TC_nums):
        # 一次创建一个道次，相同三个轧辊和轧件的关系
        # 创建标签如TZG1-1、TZG1-2、TZG-3
        TZG_partname1='TZG'+str(flag_T_nums)+'-1'
        TZG_partname2='TZG'+str(flag_T_nums)+'-2'
        TZG_partname3='TZG'+str(flag_T_nums)+'-3'

        # 轧辊表面命名,如TWR1-1、TWR1-2、TWR1-3
        TZG_face1 = 'TWR'+str(flag_T_nums)+'-1'
        TZG_face2 = 'TWR'+str(flag_T_nums)+'-2'
        TZG_face3 = 'TWR'+str(flag_T_nums)+'-3'
        # 接触关系命名。 TZG1-1_Work
        TJC1 = TZG_partname1 + 'Work'
        TJC2 = TZG_partname2 + 'Work'
        TJC3 = TZG_partname3 + 'Work'
        
        flag_T_nums = flag_T_nums+1

        # 创建TZG1-1零件的表面与轧件工作面的接触关系
        a = mdb.models['Model-1'].rootAssembly
        s1 = a.instances[TZG_partname1].faces
        side1Faces1 = s1.getSequenceFromMask(mask=('[#1ff ]', ), )
        region2=a.Surface(side1Faces=side1Faces1, name=TZG_face1)

        mdb.models['Model-1'].SurfaceToSurfaceContactExp(name = TJC1, 
            createStepName='Initial', master = region1, slave = region2, 
            mechanicalConstraint=KINEMATIC, sliding=FINITE, 
            interactionProperty='IntProp-1', initialClearance=OMIT, datumAxis=None, 
            clearanceRegion=None)

        a = mdb.models['Model-1'].rootAssembly
        region1=a.surfaces['WorkFace']
        a = mdb.models['Model-1'].rootAssembly
        s1 = a.instances[TZG_partname2].faces
        side1Faces1 = s1.getSequenceFromMask(mask=('[#1ff ]', ), )
        region2=a.Surface(side1Faces=side1Faces1, name=TZG_face2)
        mdb.models['Model-1'].SurfaceToSurfaceContactExp(name =TJC2, 
            createStepName='Initial', master = region1, slave = region2, 
            mechanicalConstraint=KINEMATIC, sliding=FINITE, 
            interactionProperty='IntProp-1', initialClearance=OMIT, datumAxis=None, 
            clearanceRegion=None)
        
        a = mdb.models['Model-1'].rootAssembly
        region1=a.surfaces['WorkFace']
        a = mdb.models['Model-1'].rootAssembly
        s1 = a.instances[TZG_partname3].faces
        side1Faces1 = s1.getSequenceFromMask(mask=('[#1ff ]', ), )
        region2=a.Surface(side1Faces=side1Faces1, name=TZG_face3)
        mdb.models['Model-1'].SurfaceToSurfaceContactExp(name =TJC3, 
            createStepName='Initial', master = region1, slave = region2, 
            mechanicalConstraint=KINEMATIC, sliding=FINITE, 
            interactionProperty='IntProp-1', initialClearance=OMIT, datumAxis=None, 
            clearanceRegion=None)


    # ########设置轧件和空气的换热系数， 这里散热系数设置为:0.3; 环境的温度SN_Tmp：300 开尔文
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    a = mdb.models['Model-1'].rootAssembly
    region=a.surfaces['WorkFace']
    mdb.models['Model-1'].FilmCondition(name='Int-13', createStepName='Step-1', surface=region, definition=EMBEDDED_COEFF, filmCoeff=float(AirFilmCoff), filmCoeffAmplitude='', 
        sinkTemperature=float(SN_Tmp), sinkAmplitude='', sinkDistributionType=UNIFORM, sinkFieldName='')
    
    
    # ******************************************************Load模块*******************************************************************************
    #  套筒和芯棒绑定关系
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['XinBang-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    region1=a.Surface(side1Faces=side1Faces1, name='XINBANG_out')
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['TaoTong-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
    region2=a.Surface(side1Faces=side1Faces1, name='TaoTong_in')
    mdb.models['Model-1'].Tie(name='Xin_Tao_Cont', master=region1, slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

    # 切换为初始步
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')

    # for循环建立限制每个轧辊的自由度, 在Y轴上转，还是在X轴上转
    # 计数标记
    free_nums = int(1)
    
    for item in ZgTable:
        # 一次创建一个道次，相同两个轧辊和轧件的关系
        # 创建标签如ZG1-1、ZG1-2
        ZG_partname1='ZG'+str(free_nums)+'-1'
        ZG_partname2='ZG'+str(free_nums)+'-2'

        # 轧辊旋转点Set_ZG1-1,旋转中心
        ZG_Set1 ='Set-' + ZG_partname1
        ZG_Set2 ='Set-' + ZG_partname2

        # 转动关系命名,如ZHUAN_WR1-1、ZHUAN_WR1-2
        ZG_zhuan1 = 'ZHUAN_WR'+str(free_nums)+'-1'
        ZG_zhuan2 = 'ZHUAN_WR'+str(free_nums)+'-2'
        
        free_nums = free_nums+1
        #  需要再判断一次是横向还是纵向。 横向轧辊限制只留Y轴， 纵向轧辊只留X轴
        # 如果是卧式
        
        # 如果是立式
        if item[0] == '\xc1\xa2\xca\xbd':
            # print('\xc1\xa2\xca\xbd')
            a = mdb.models['Model-1'].rootAssembly
            r1 = a.instances[ZG_partname1].referencePoints
            refPoints1=(r1[2], )
            region = a.Set(referencePoints=refPoints1, name=ZG_Set1)
            mdb.models['Model-1'].DisplacementBC(name=ZG_zhuan1,  createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET,  ur2=SET,
                ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',   localCsys=None)

            a = mdb.models['Model-1'].rootAssembly
            r1 = a.instances[ZG_partname2].referencePoints
            refPoints1=(r1[2], )
            region = a.Set(referencePoints=refPoints1, name=ZG_Set2)
            mdb.models['Model-1'].DisplacementBC(name=ZG_zhuan2,  createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET,   ur2=SET, 
                ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',   localCsys=None)

        elif item[0] == '\xce\xd4\xca\xbd':
            # print('\xce\xd4\xca\xbd')
            a = mdb.models['Model-1'].rootAssembly
            r1 = a.instances[ZG_partname1].referencePoints
            refPoints1=(r1[2], )
            region = a.Set(referencePoints=refPoints1, name=ZG_Set1)
            mdb.models['Model-1'].DisplacementBC(name=ZG_zhuan1,  createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=UNSET, 
                ur3=SET, amplitude=UNSET, distributionType=UNIFORM,  fieldName='', localCsys=None)

            a = mdb.models['Model-1'].rootAssembly
            r1 = a.instances[ZG_partname2].referencePoints
            refPoints1=(r1[2], )
            region = a.Set(referencePoints=refPoints1, name=ZG_Set2)
            mdb.models['Model-1'].DisplacementBC(name=ZG_zhuan2,  createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=SET,  ur2=UNSET, 
                ur3=SET, amplitude=UNSET, distributionType=UNIFORM,   fieldName='', localCsys=None)
            
    
    T_free_nums = int(1)
    for item in TZgTable:
         # 一次创建一个道次，相同三个轧辊和轧件的关系
        # 创建标签如ZG1-1、ZG1-2
        TZG_partname1='TZG'+str(T_free_nums)+'-1'
        TZG_partname2='TZG'+str(T_free_nums)+'-2'
        TZG_partname3='TZG'+str(T_free_nums)+'-3'

        # 轧辊旋转点Set_ZG1-1,旋转中心
        TZG_Set1 ='TSet-' + TZG_partname1
        TZG_Set2 ='TSet-' + TZG_partname2
        TZG_Set3 ='TSet-' + TZG_partname3

        # 转动关系命名,如ZHUAN_WR1-1、ZHUAN_WR1-2
        TZG_zhuan1 = 'TZHUAN_WR'+str(T_free_nums)+'-1'
        TZG_zhuan2 = 'TZHUAN_WR'+str(T_free_nums)+'-2'
        TZG_zhuan3 = 'TZHUAN_WR'+str(T_free_nums)+'-3'
        
        T_free_nums = T_free_nums+1

        a = mdb.models['Model-1'].rootAssembly
        r1 = a.instances[TZG_partname1].referencePoints
        refPoints1=(r1[2], )
        region = a.Set(referencePoints=refPoints1, name=TZG_Set1)
        datum = mdb.models['Model-1'].rootAssembly.instances[TZG_partname1].datums[3]
        mdb.models['Model-1'].DisplacementBC(name=TZG_zhuan1,  createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, 
            ur1=SET,  ur2=UNSET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',   localCsys=datum)
        
        a = mdb.models['Model-1'].rootAssembly
        r1 = a.instances[TZG_partname2].referencePoints
        refPoints1=(r1[2], )
        region = a.Set(referencePoints=refPoints1, name=TZG_Set2)
        datum = mdb.models['Model-1'].rootAssembly.instances[TZG_partname2].datums[3]
        mdb.models['Model-1'].DisplacementBC(name=TZG_zhuan2,  createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, 
            ur1=SET,  ur2=UNSET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',   localCsys=datum)
        
        a = mdb.models['Model-1'].rootAssembly
        r1 = a.instances[TZG_partname3].referencePoints
        refPoints1=(r1[2], )
        region = a.Set(referencePoints=refPoints1, name=TZG_Set3)
        datum = mdb.models['Model-1'].rootAssembly.instances[TZG_partname3].datums[3]
        mdb.models['Model-1'].DisplacementBC(name=TZG_zhuan3,  createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, 
            ur1=SET,  ur2=UNSET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',   localCsys=datum)
                
    
    # *************************************设置初始转速 vel**************************************************************************
    # 速度可对应表格
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')

    vel_nums = int(1)
    for item in ZgTable:

        # 创建标签如ZG1-1、ZG1-2
        ZG_partname1='ZG'+str(vel_nums)+'-1'
        ZG_partname2='ZG'+str(vel_nums)+'-2'

        # 轧辊旋转点Set_ZG1-1,旋转中心
        ZG_Set1 ='Set-' + ZG_partname1
        ZG_Set2 ='Set-' + ZG_partname2

        # 转动关系命名,如ZHUAN_WR1-1、ZHUAN_WR1-2
        ZG_vel1 = 'VEL_WR'+str(vel_nums)+'-1'
        ZG_vel2 = 'VEL_WR'+str(vel_nums)+'-2'
        vel_nums = vel_nums+1

        Zg_vel_value = float(item[11])

        # 如果是卧式
        if item[0] == '\xce\xd4\xca\xbd':
            # print('\xce\xd4\xca\xbd')
            a = mdb.models['Model-1'].rootAssembly
            region = a.sets[ZG_Set1]
            mdb.models['Model-1'].VelocityBC(name=ZG_vel1, createStepName='Step-1', region=region, v1=UNSET, v2=UNSET, v3=UNSET, vr1=UNSET,
                vr2=Zg_vel_value, vr3=UNSET, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

            a = mdb.models['Model-1'].rootAssembly
            region = a.sets[ZG_Set2]
            mdb.models['Model-1'].VelocityBC(name=ZG_vel2, createStepName='Step-1', region=region, v1=UNSET, v2=UNSET, v3=UNSET, vr1=UNSET, 
                vr2=-Zg_vel_value, vr3=UNSET, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

        # 如果是立式
        elif item[0] == '\xc1\xa2\xca\xbd':
            # print('\xc1\xa2\xca\xbd')
            a = mdb.models['Model-1'].rootAssembly
            region = a.sets[ZG_Set1]
            mdb.models['Model-1'].VelocityBC(name=ZG_vel1, createStepName='Step-1', region=region, v1=UNSET, v2=UNSET, v3=UNSET, vr1=-Zg_vel_value,
                vr2=UNSET, vr3=UNSET, amplitude=UNSET, localCsys=None, distributionType=UNIFORM,   fieldName='')
            
            a = mdb.models['Model-1'].rootAssembly
            region = a.sets[ZG_Set2]
            mdb.models['Model-1'].VelocityBC(name=ZG_vel2, createStepName='Step-1', region=region, v1=UNSET, v2=UNSET, v3=UNSET, vr1=Zg_vel_value, 
                vr2=UNSET, vr3=UNSET, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

    ####################################三辊轧机部分###########################
    Tvel_nums = int(1)
    for item in TZgTable:
        # 创建标签如TZG1-1、TZG1-2
        TZG_partname1='TZG'+str(Tvel_nums)+'-1'
        TZG_partname2='TZG'+str(Tvel_nums)+'-2'
        TZG_partname3='TZG'+str(Tvel_nums)+'-3'

        # 轧辊旋转点Set_ZG1-1,旋转中心
        TZG_Set1 ='TSet-' + TZG_partname1
        TZG_Set2 ='TSet-' + TZG_partname2
        TZG_Set3 ='TSet-' + TZG_partname3

        # 转动关系命名,如ZHUAN_WR1-1、ZHUAN_WR1-2
        TZG_vel1 = 'TVEL_WR'+str(Tvel_nums)+'-1'
        TZG_vel2 = 'TVEL_WR'+str(Tvel_nums)+'-2'
        TZG_vel3 = 'TVEL_WR'+str(Tvel_nums)+'-3'

        Tvel_nums = Tvel_nums+1

        TZg_vel_value = float(item[11])

        # 如果是正Y
        if item[0] == '\xd5\xfdY':
            a = mdb.models['Model-1'].rootAssembly
            region = a.sets[TZG_Set1]
            datum = mdb.models['Model-1'].rootAssembly.instances[TZG_partname1].datums[3]
            mdb.models['Model-1'].VelocityBC(name=TZG_vel1, createStepName='Step-1', region=region, v1=UNSET, v2=UNSET, v3=UNSET, vr1=UNSET,
                vr2=TZg_vel_value, vr3=UNSET, amplitude=UNSET, localCsys=datum, distributionType=UNIFORM, fieldName='')

            a = mdb.models['Model-1'].rootAssembly
            region = a.sets[TZG_Set2]
            datum = mdb.models['Model-1'].rootAssembly.instances[TZG_partname2].datums[3]
            mdb.models['Model-1'].VelocityBC(name=TZG_vel2, createStepName='Step-1', region=region, v1=UNSET, v2=UNSET, v3=UNSET, vr1=UNSET, 
                vr2=TZg_vel_value, vr3=UNSET, amplitude=UNSET, localCsys=datum, distributionType=UNIFORM, fieldName='')
            
            a = mdb.models['Model-1'].rootAssembly
            region = a.sets[TZG_Set3]
            datum = mdb.models['Model-1'].rootAssembly.instances[TZG_partname3].datums[3]
            mdb.models['Model-1'].VelocityBC(name=TZG_vel3, createStepName='Step-1', region=region, v1=UNSET, v2=UNSET, v3=UNSET, vr1=UNSET, 
                vr2=-TZg_vel_value, vr3=UNSET, amplitude=UNSET, localCsys=datum, distributionType=UNIFORM, fieldName='')

        # 如果是倒Y
        elif item[0] == '\xb5\xb9Y':
            a = mdb.models['Model-1'].rootAssembly
            region = a.sets[TZG_Set1]
            datum = mdb.models['Model-1'].rootAssembly.instances[TZG_partname1].datums[3]
            mdb.models['Model-1'].VelocityBC(name=TZG_vel1, createStepName='Step-1', region=region, v1=UNSET, v2=UNSET, v3=UNSET, vr1=UNSET,
                vr2=-TZg_vel_value, vr3=UNSET, amplitude=UNSET, localCsys=datum, distributionType=UNIFORM, fieldName='')

            a = mdb.models['Model-1'].rootAssembly
            region = a.sets[TZG_Set2]
            datum = mdb.models['Model-1'].rootAssembly.instances[TZG_partname2].datums[3]
            mdb.models['Model-1'].VelocityBC(name=TZG_vel2, createStepName='Step-1', region=region, v1=UNSET, v2=UNSET, v3=UNSET, vr1=UNSET, 
                vr2=TZg_vel_value, vr3=UNSET, amplitude=UNSET, localCsys=datum, distributionType=UNIFORM, fieldName='')
            
            a = mdb.models['Model-1'].rootAssembly
            region = a.sets[TZG_Set3]
            datum = mdb.models['Model-1'].rootAssembly.instances[TZG_partname3].datums[3]
            mdb.models['Model-1'].VelocityBC(name=TZG_vel3, createStepName='Step-1', region=region, v1=UNSET, v2=UNSET, v3=UNSET, vr1=UNSET, 
                vr2=-TZg_vel_value, vr3=UNSET, amplitude=UNSET, localCsys=datum, distributionType=UNIFORM, fieldName='')



    # 保存
    # mdb.saveAs(pathName='D:/abaqus_2021_tmp/SecondDevelop/zhazhi6')
    
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')

    # 设定轧辊表面的温度
    # 0、1、2、3、4.......
    # for i in range(C_nums):
    zg_tmp_nums = int(1)
    for item in ZgTable:

        # 创建标签如ZG1-1、ZG1-2
        ZG_partname1='ZG'+str(zg_tmp_nums)+'-1'
        ZG_partname2='ZG'+str(zg_tmp_nums)+'-2'

        # 轧辊旋转点Set_ZG1-1,旋转中心
        ZG_Set1 ='Set-' + ZG_partname1
        ZG_Set2 ='Set-' + ZG_partname2

        # 转动关系命名,如ZHUAN_WR1-1、ZHUAN_WR1-2
        ZG_tmp1 = 'TMP_WR'+str(zg_tmp_nums)+'-1'
        ZG_tmp2 = 'TMP_WR'+str(zg_tmp_nums)+'-2'

        zg_tmp_nums = zg_tmp_nums+1

        # 获取表格中的温度、 开氏温度
        Zg_TMP_value = float(item[12])
        
        a = mdb.models['Model-1'].rootAssembly
        region = a.sets[ZG_Set1]
        mdb.models['Model-1'].TemperatureBC(name=ZG_tmp1, createStepName='Step-1', 
            region=region, fixed=OFF, distributionType=UNIFORM, fieldName='', 
            magnitude=Zg_TMP_value, amplitude=UNSET)
        a = mdb.models['Model-1'].rootAssembly
        region = a.sets[ZG_Set2]
        mdb.models['Model-1'].TemperatureBC(name=ZG_tmp2, createStepName='Step-1', 
            region=region, fixed=OFF, distributionType=UNIFORM, fieldName='', 
            magnitude=Zg_TMP_value, amplitude=UNSET)
    

    Tzg_tmp_nums = int(1)
    for item in TZgTable:
        # 创建标签如ZG1-1、ZG1-2
        TZG_partname1='TZG'+str(Tzg_tmp_nums)+'-1'
        TZG_partname2='TZG'+str(Tzg_tmp_nums)+'-2'
        TZG_partname3='TZG'+str(Tzg_tmp_nums)+'-3'

        # 轧辊旋转点Set_ZG1-1,旋转中心
        TZG_Set1 ='TSet-' + TZG_partname1
        TZG_Set2 ='TSet-' + TZG_partname2
        TZG_Set3 ='TSet-' + TZG_partname3

        # 转动关系命名,如ZHUAN_WR1-1、ZHUAN_WR1-2
        TZG_tmp1 = 'T_TMP_WR'+str(Tzg_tmp_nums)+'-1'
        TZG_tmp2 = 'T_TMP_WR'+str(Tzg_tmp_nums)+'-2'
        TZG_tmp3 = 'T_TMP_WR'+str(Tzg_tmp_nums)+'-3'

        Tzg_tmp_nums = Tzg_tmp_nums+1

        # 获取表格中的温度、 开氏温度
        TZg_TMP_value = float(item[12])
        
        a = mdb.models['Model-1'].rootAssembly
        region = a.sets[TZG_Set1]
        mdb.models['Model-1'].TemperatureBC(name=TZG_tmp1, createStepName='Step-1', 
            region=region, fixed=OFF, distributionType=UNIFORM, fieldName='', 
            magnitude=TZg_TMP_value, amplitude=UNSET)
        a = mdb.models['Model-1'].rootAssembly
        region = a.sets[TZG_Set2]
        mdb.models['Model-1'].TemperatureBC(name=TZG_tmp2, createStepName='Step-1', 
            region=region, fixed=OFF, distributionType=UNIFORM, fieldName='', 
            magnitude=TZg_TMP_value, amplitude=UNSET)
        a = mdb.models['Model-1'].rootAssembly
        region = a.sets[TZG_Set3]
        mdb.models['Model-1'].TemperatureBC(name=TZG_tmp3, createStepName='Step-1', 
            region=region, fixed=OFF, distributionType=UNIFORM, fieldName='', 
            magnitude=TZg_TMP_value, amplitude=UNSET)

    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')

    # 设定轧件、初速度velocity3
    a = mdb.models['Model-1'].rootAssembly
    c1 = a.instances['TaoTong-1'].cells
    cells1 = c1.getSequenceFromMask(mask=('[#1 ]', ), )
    f1 = a.instances['TaoTong-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#f ]', ), )
    e1 = a.instances['TaoTong-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#f ]', ), )
    v1 = a.instances['TaoTong-1'].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#f ]', ), )
    c2 = a.instances['XinBang-1'].cells
    cells2 = c2.getSequenceFromMask(mask=('[#1 ]', ), )
    f2 = a.instances['XinBang-1'].faces
    faces2 = f2.getSequenceFromMask(mask=('[#7 ]', ), )
    e2 = a.instances['XinBang-1'].edges
    edges2 = e2.getSequenceFromMask(mask=('[#3 ]', ), )
    v2 = a.instances['XinBang-1'].vertices
    verts2 = v2.getSequenceFromMask(mask=('[#3 ]', ), )
    region = a.Set(vertices=verts1+verts2, edges=edges1+edges2, faces=faces1+\
        faces2, cells=cells1+cells2, name='ZHAJIAN_region')
    
    # 设定轧件初速度velocity3  mm
    mdb.models['Model-1'].Velocity(name='chusudu', region=region, field='', distributionType=MAGNITUDE, velocity3=float(Vel), omega=0.0)
    
    # 设定轧件初始温度 开尔文温度
    a = mdb.models['Model-1'].rootAssembly
    region = a.sets['ZHAJIAN_region']
    mdb.models['Model-1'].Temperature(name='ZHAJIAN_TMP', createStepName='Initial', region=region, distributionType=UNIFORM, 
        crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(float(Tmp), ))
    

    # *************************************mesh模块**************************************************************************
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, bcs=OFF, predefinedFields=OFF, connectors=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=ON)
    # mesh种子分布间距

    # 画套筒网格
    p = mdb.models['Model-1'].parts['TaoTong']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['TaoTong']
    p.seedPart(size=float(MeshSize), deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['TaoTong']
    p.generateMesh()
    # 画芯棒网格
    p = mdb.models['Model-1'].parts['XinBang']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['XinBang']
    p.seedPart(size=float(MeshSize), deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['XinBang']
    p.generateMesh()

    elemType1 = mesh.ElemType(elemCode=C3D8RT, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=C3D6T, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4T, elemLibrary=EXPLICIT)
    p = mdb.models['Model-1'].parts['XinBang']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))

    elemType1 = mesh.ElemType(elemCode=C3D8RT, elemLibrary=EXPLICIT, kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT, distortionControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=C3D6T, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4T, elemLibrary=EXPLICIT)
    p = mdb.models['Model-1'].parts['XinBang']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))

    p = mdb.models['Model-1'].parts['TaoTong']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    elemType1 = mesh.ElemType(elemCode=C3D8RT, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=C3D6T, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4T, elemLibrary=EXPLICIT)
    p = mdb.models['Model-1'].parts['TaoTong']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2,  elemType3))

    # 微信温度网格、加减速积分
    p = mdb.models['Model-1'].parts['XinBang']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    elemType1 = mesh.ElemType(elemCode=C3D8RT, elemLibrary=EXPLICIT, kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT, distortionControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=C3D6T, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4T, elemLibrary=EXPLICIT)
    p = mdb.models['Model-1'].parts['XinBang']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8RT, elemLibrary=EXPLICIT,  kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT, distortionControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=C3D6T, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4T, elemLibrary=EXPLICIT)
    p = mdb.models['Model-1'].parts['XinBang']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))

    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=OFF)

    # 切换至个人视角
    session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)


    # mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    #     atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    #     memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
    #     nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
    #     contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
    #     resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=8, 
    #     activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=8)
    # mdb.jobs['Job-1'].submit(consistencyChecking=OFF, datacheckJob=True)
    # #: The job input file "Job-1.inp" has been submitted for analysis.
    # #: Job Job-1: Analysis Input File Processor completed successfully.
    # #: Job Job-1: Abaqus/Explicit Packager completed successfully.
    # mdb.save()
