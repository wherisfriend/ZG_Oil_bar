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
import math

# 孔测试
# 2023年2月10,
# 孔型槽底宽度  b_k
# 孔型高度      H_k
# 辊缝          S_k
# 工作直径      D_k
# 延伸          YS_k
# 文件名        partname_k

 

# 解析刚体,2022.2.19改为解析刚体


def yuan2023(ZJ, D_k, S_k, YS_k, partname_k, r_radis):   
   
    session.viewports['Viewport: 1'].view.setValues(nearPlane=1523.47, 
        farPlane=2641.41, width=1251.22, height=558.819, viewOffsetX=0.417439,  viewOffsetY=0.708868)
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',   sheetSize=1200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -600.0), point2=(0.0, 600.0))
    s.FixedConstraint(entity=g[2])
    # 水平参考线
    s.ConstructionLine(point1=(-130.0, 0.0), point2=(185.0, 0.0))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.FixedConstraint(entity=g[3])
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='ZD', expression=D_k)
    s.Parameter(name='YS', expression=YS_k, previousParameter='ZD')
    s.Parameter(name='ZJ', expression=ZJ, previousParameter='YS')
    s.Parameter(name='S', expression=S_k, previousParameter='ZJ')
    s.Parameter(name='r_rate', expression=r_radis, previousParameter='S')
    # 垂直辅助线，轧辊半径
    f_ZG_R = float(D_k)/2
    s.ConstructionLine(point1=(f_ZG_R, 120.0), point2=(f_ZG_R, -75.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.DistanceDimension(entity1=g[2], entity2=g[4], textPoint=(184.98779296875, 184.981002807617), value=f_ZG_R)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='center', path='dimensions[0]', expression='ZD/2',  previousParameter='r_rate')
    # 辅助线,实际，减一半辊缝
    f_S_k = float(S_k)
    p1 = f_ZG_R - f_S_k/2
    s.ConstructionLine(point1=(p1, 150.0), point2=(p1, -40.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.DistanceDimension(entity1=g[2], entity2=g[5], textPoint=(236.166015625, 155.703414916992), value=p1)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='S_c', expression='center-S/2', previousParameter='center')
    # 打点
    s.Spot(point=((float(D_k)-float(ZJ))/2, 0.0))

    s.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=v[0], entity2=g[2], textPoint=(62.3734130859375,  88.0988616943359), value=(float(D_k)-float(ZJ))/2)

    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='L1', path='dimensions[2]', expression='(ZD-ZJ)/2',  previousParameter='S_c')

    s.Arc3Points(point1=(p1, 60.0), point2=((float(D_k)-float(ZJ))/2, 0.0), point3=(p1, -60.0))
    s.CoincidentConstraint(entity1=v[1], entity2=g[5], addUndoState=False)
    s.CoincidentConstraint(entity1=v[3], entity2=g[5], addUndoState=False)
    s.undo()

    s.Arc3Points(point1=(p1, 45.0), point2=(p1, -45.0), point3=((float(D_k)-float(ZJ))/2, 0.0))
    s.CoincidentConstraint(entity1=v[1], entity2=g[5], addUndoState=False)
    s.CoincidentConstraint(entity1=v[2], entity2=g[5], addUndoState=False)
    s.SymmetryConstraint(entity1=v[1], entity2=v[2], symmetryAxis=g[3])
    s.RadialDimension(curve=g[6], textPoint=(271.403442382813, 115.086578369141), radius=45.75)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='R', path='dimensions[3]', expression='ZJ/2', previousParameter='L1')

    hh = (float(ZJ)/2)*(float(ZJ)/2) - (float(S_k)/2)*(float(S_k)/2)

    hhsqut = math.sqrt(hh)
    # print(hhsqut)

    s.Line(point1=(p1, hhsqut), point2=(p1, hhsqut+float(YS_k)))
    s.VerticalConstraint(entity=g[7], addUndoState=False)
    # s.ParallelConstraint(entity1=g[5], entity2=g[7], addUndoState=False)
    # s.CoincidentConstraint(entity1=v[4], entity2=g[5], addUndoState=False)
    # s.CoincidentConstraint(entity1=v[5], entity2=g[5], addUndoState=False)

    s.Line(point1=(p1, -hhsqut), point2=(p1, -hhsqut-float(YS_k)))
    # print(-hhsqut-float(YS_k))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    # s.ParallelConstraint(entity1=g[5], entity2=g[8], addUndoState=False)
    # s.CoincidentConstraint(entity1=v[6], entity2=g[5], addUndoState=False)
    # s.CoincidentConstraint(entity1=v[7], entity2=g[5], addUndoState=False)

    # s.SymmetryConstraint(entity1=g[7], entity2=g[8], symmetryAxis=g[3])
    # s.CoincidentConstraint(entity1=v[4], entity2=v[1])
    # s.DistanceDimension(entity1=v[5], entity2=g[3], textPoint=(421.941741943359, 29.9881744384766), value=137.377014160156)

    # s=mdb.models['Model-1'].sketches['__profile__']
    # s.Parameter(name='H1', path='dimensions[4]', expression='R+YS', previousParameter='R')

    r_radis = float(r_radis)

    # s.SymmetryConstraint(entity1=v[7], entity2=v[5], symmetryAxis=g[3])
    s.FilletByRadius(radius=r_radis, curve1=g[6], nearPoint1=(f_ZG_R-float(ZJ)/2, 20), curve2=g[7], nearPoint2=(p1, hhsqut+float(YS_k)/2))
    s.FilletByRadius(radius=r_radis, curve1=g[6], nearPoint1=(f_ZG_R-float(ZJ)/2, -20), curve2=g[8], nearPoint2=(p1, -hhsqut-float(YS_k)/2))
   
    p = mdb.models['Model-1'].Part(name=partname_k, dimensionality=THREE_D,  type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models['Model-1'].parts[partname_k]
    p.AnalyticRigidSurfRevolve(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname_k]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

# yuan2023(str('164'),str('906'),str('14'),str('80'), str('zz'), str('1.75'))


