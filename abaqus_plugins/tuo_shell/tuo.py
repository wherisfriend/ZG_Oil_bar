# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
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



# 孔测试
# 2023年2月19, 解析几何
# 孔型槽底宽度  b_k
# 孔型高度      H_k
# 辊缝          S_k
# 工作直径      D_k
# 延伸          YS_k
# 文件名        partname_k

b_value = str(float(190))       
H_k = str(float(127))         
D_k = str(float(680))   
S_k = str(float(13))    
     
YS_k = str(float(50.0))   
partname_k = str('hu5')     

def tuo2023(b_value, H_k, D_k, S_k, YS_k, partname_k, r_rate):
    
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=1200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.ConstructionLine(point1=(0.0, -600.0), point2=(0.0, 600.0))
    s1.FixedConstraint(entity=g[2])
    # 横构造线
    s1.ConstructionLine(point1=(-85.0, 0.0), point2=(55.0, 0.0))
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)

    s1.ConstructionLine(point1=(0.0, 80.0), point2=(0.0, -16.1079406738281))
    s1.VerticalConstraint(entity=g[4], addUndoState=False)

    s1.FixedConstraint(entity=g[3])
    s1.FixedConstraint(entity=g[2])
    
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='D', expression=D_k)
    s.Parameter(name='H', expression=H_k, previousParameter='D')
    s.Parameter(name='B', expression=b_value, previousParameter='H')
    s.Parameter(name='S', expression=S_k, previousParameter='B')
    s.Parameter(name='YS', expression=YS_k, previousParameter='S')

    L1 = float(D_k)/2

    s1.ConstructionLine(point1=(L1, 0.0), point2=(L1, -60.0))
    s1.VerticalConstraint(entity=g[5], addUndoState=False)
    s1.DistanceDimension(entity1=g[2], entity2=g[5], textPoint=(181.577301025391, 140.25634765625), value=L1)

    
    s.Parameter(name='R_k', path='dimensions[0]', expression='D/2',  previousParameter='YS')
    
    L2 = L1 - float(H_k)/2

    L3 = L1 - float(S_k)/2


    s1.Spot(point=(L2, 0.0))
    s1.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
    s1.Spot(point=(L3, 1.093*float(b_value)/2))
    s1.Spot(point=(L3, -1.093*float(b_value)/2))

    s1.SymmetryConstraint(entity1=v[1], entity2=v[2], symmetryAxis=g[3])
    s1.CoincidentConstraint(entity1=v[0], entity2=g[3])
    s1.VerticalDimension(vertex1=v[1], vertex2=v[2], textPoint=(292.301971435547, 0.0), value=1.093*float(b_value))

    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='B_k', path='dimensions[1]', expression='B*1.093', previousParameter='R_k')
    s1.DistanceDimension(entity1=v[1], entity2=g[2], textPoint=(13.0478363037109, 108.553230285645), value=260.0)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='R1', path='dimensions[2]', expression='R_k-S/2',  previousParameter='B_k')
    s1.DistanceDimension(entity1=v[0], entity2=g[2], textPoint=(2.46385192871094, 64.656623840332), value=200.0)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='R2', path='dimensions[3]', expression='R_k-H/2',  previousParameter='R1')

   # 圆弧坐标特殊处理
    arc_a = (float(D_k) - float(S_k))/2 
    arc_b = (float(b_value)*1.093)/2
    arc_c = (float(D_k) - float(H_k))/2 
 
    s1.Arc3Points(point1=(arc_a, arc_b), point2=(arc_a, -arc_b), point3=(arc_c, 0.0))
    # s1.Arc3Points(point1=(333.5, 94.5), point2=(333.5, -94.5), point3=(276.5, 0.0))

    s1.Line(point1=(405.0, 180.0), point2=(405.0, 115.0))
    s1.VerticalConstraint(entity=g[7], addUndoState=False)
    s1.Line(point1=(405.0, -125.0), point2=(405.0, -180.0))
    s1.VerticalConstraint(entity=g[8], addUndoState=False)
    s1.SymmetryConstraint(entity1=g[7], entity2=g[8], symmetryAxis=g[3])
    s1.CoincidentConstraint(entity1=v[7], entity2=v[1])
    # s1.DistanceDimension(entity1=v[6], entity2=g[3], textPoint=(438.849365234375, 15.8825750350952), value=149.5)
    # s=mdb.models['Model-1'].sketches['__profile__']
    # s.Parameter(name='B2', path='dimensions[4]', expression='B/2+YS',  previousParameter='R2')

    r_radis = float(H_k)
    r_radis = r_radis * float(r_rate)
    # print(L2)
    # print(L3)

    # s1.FilletByRadius(radius=r_radis, curve1=g[6], nearPoint1=(L2, 1), curve2=g[7], nearPoint2=(L3, 1.093*float(b_value)/2 + float(YS_k)/2))
    # s1.FilletByRadius(radius=r_radis, curve1=g[6], nearPoint1=(L2, -1), curve2=g[8], nearPoint2=(L3, -1.093*float(b_value)/2 - float(YS_k)/2))
    s1.FilletByRadius(radius=r_radis, curve1=g[7], nearPoint1=(L3, (float(YS_k)+float(b_value))/2), curve2=g[6], nearPoint2=(L2,  58.0))
    s1.FilletByRadius(radius=r_radis, curve1=g[6], nearPoint1=(L2, -58), curve2=g[8], nearPoint2=(L3, -(float(YS_k)+float(b_value))/2))

    s1.unsetPrimaryObject()


    p = mdb.models['Model-1'].Part(name=partname_k, dimensionality=THREE_D,  type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models['Model-1'].parts[partname_k]
    p.AnalyticRigidSurfRevolve(sketch=s1)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname_k]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

    # 补倒角
    # p = mdb.models['Model-1'].parts[partname_k]
    # s = p.features['3D Analytic rigid shell-1'].sketch
    # mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    # s1 = mdb.models['Model-1'].sketches['__edit__']
    # g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    # s1.setPrimaryObject(option=SUPERIMPOSE)
    # p.projectReferencesOntoSketch(sketch=s1, upToFeature=p.features['3D Analytic rigid shell-1'], filter=COPLANAR_EDGES)
    # s1.FilletByRadius(radius=r_radis, curve1=g[7], nearPoint1=(L3, (float(YS_k)+float(b_value))/2), curve2=g[6], nearPoint2=(L2,  58.0))
    # s1.FilletByRadius(radius=r_radis, curve1=g[6], nearPoint1=(L2, -58), curve2=g[8], nearPoint2=(L3, -(float(YS_k)+float(b_value))/2))

    # s1.unsetPrimaryObject()
    # p = mdb.models['Model-1'].parts[partname_k]
    # p.features['3D Analytic rigid shell-1'].setValues(sketch=s1)
    # del mdb.models['Model-1'].sketches['__edit__']
    # p = mdb.models['Model-1'].parts[partname_k]
    # p.regenerate()


# tuo2023(str('201'), str('149'), str('666'), str('13'), str('66'), str('yy'), str('0.175'))