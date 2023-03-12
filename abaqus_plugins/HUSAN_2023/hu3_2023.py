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
import math

# 直径超过600，圆弧会不匹配
   
     

def HU3_2023(partname_k, D_k, bata_k, ZGD, YS_k, S_k):

    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=800.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -400.0), point2=(0.0, 400.0))
    s.FixedConstraint(entity=g[2])
    s.ConstructionLine(point1=(-60.0, 0.0), point2=(10.0, 0.0))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.FixedConstraint(entity=g[3])

    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='D', expression=D_k)
    s.Parameter(name='bata', expression=bata_k, previousParameter='D')
    s.Parameter(name='ZGD', expression=ZGD, previousParameter='bata')
    s.Parameter(name='YS', expression=YS_k, previousParameter='ZGD')
    s.Parameter(name='S_k', expression=S_k, previousParameter='YS')
    s.Parameter(name='G', expression='2*sin(60)/3+tan(bata/4)',  previousParameter='S_k')
    s.Parameter(name='aa', expression='D/G', previousParameter='G')
    s.Parameter(name='R', expression='(aa/2)/(sin(bata/2))',  previousParameter='aa')

    # 轧辊半径
    p1_x = float(ZGD)/2

    s.Spot(point=(p1_x, 0.0))
    s.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=v[0], entity2=g[2], textPoint=(50.4989929199219, 55.2729415893555), value=p1_x)
    
    # 构造线
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='ZGR', path='dimensions[0]', expression='ZGD/2',  previousParameter='R')

    s.ConstructionLine(point1=(p1_x, 0.0), point2=(p1_x-10, 20*math.sin((math.pi)/3)))
    s.CoincidentConstraint(entity1=v[0], entity2=g[4], addUndoState=False)
    s.ConstructionLine(point1=(p1_x, 0.0), point2=(p1_x-10, -20*math.sin((math.pi)/3)))
    s.CoincidentConstraint(entity1=v[0], entity2=g[5], addUndoState=False)

    s.AngularDimension(line1=g[4], line2=g[3], textPoint=(p1_x+100, 26.7832260131836), value=120.0)
    s.AngularDimension(line1=g[5], line2=g[3], textPoint=(p1_x+100,  -29.13857173919678), value=120.0)

    # 辊缝参考点
    p2_x = p1_x - (float(S_k)/2)/(math.sin((math.pi)/3))

    s.Spot(point=(p2_x, 0.0))
    s.CoincidentConstraint(entity1=v[1], entity2=g[3], addUndoState=False)

    s.ConstructionLine(point1=(p2_x, 0.0), point2=(p2_x-10, 20*math.sin((math.pi)/3)))
    s.CoincidentConstraint(entity1=v[1], entity2=g[6], addUndoState=False)
    
    s.DistanceDimension(entity1=v[1], entity2=g[2], textPoint=(15.0133819580078, 42.0963401794434), value=p2_x)
    s.Parameter(name='L1', path='dimensions[3]', expression='ZGR-(S_k/2)/sin(60)',   previousParameter='ZGR')
    s.ParallelConstraint(entity1=g[4], entity2=g[6])

    s.ConstructionLine(point1=(p2_x, 0.0), point2=(p2_x-10, -20*math.sin((math.pi)/3)))
    s.CoincidentConstraint(entity1=v[1], entity2=g[7], addUndoState=False)
    s.ParallelConstraint(entity1=g[7], entity2=g[5])

    # 内接圆
    p3_x = p1_x - float(D_k)/2
    
    # print(p3_x)
    s.Spot(point=(p3_x, 0.0))
    s.CoincidentConstraint(entity1=v[2], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=v[2], entity2=g[2], textPoint=(26.3270416259766, 109.095062255859), value=p3_x)
    s.Parameter(name='L2', path='dimensions[4]', expression='ZGR-D/2',  previousParameter='L1')
    
    # 大圆弧圆心
    G =2*math.sin((math.pi)/3)/3 + math.tan((float(bata_k)/4)*(math.pi)/180)
    aa_k = float(D_k)/G
    Big_R = (aa_k/2)/(math.sin((float(bata_k)/2)*(math.pi)/180))
    p4_x = p3_x + Big_R
    s.Spot(point=(p4_x, 0.0))
    s.CoincidentConstraint(entity1=v[3], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=v[3], entity2=g[2], textPoint=(91.2624359130859,  79.8441314697266), value=p4_x)
    s.Parameter(name='L3', path='dimensions[5]', expression='L2+R',  previousParameter='L2')
   
    # 求x、求根
    a_c = float(4)
    b_c = -(6*p2_x+2*p4_x)
    c_c = 3*p2_x*p2_x + p4_x*p4_x-Big_R*Big_R


    X_x = (-b_c - math.sqrt(b_c*b_c - 4*a_c*c_c))/(2*a_c)
    Y_y = math.sqrt(3)*(X_x - p2_x)

    # print(X_x)
    # print(Y_y)


    s.ArcByCenterEnds(center=(p4_x, 0.0), point1=(p3_x, 0.0), point2=(X_x, Y_y), direction=COUNTERCLOCKWISE)
    s.CoincidentConstraint(entity1=v[5], entity2=g[7], addUndoState=False)

    s.ArcByCenterEnds(center=(p4_x, 0.0), point1=(p3_x, 0.0), point2=(X_x, -Y_y), direction=CLOCKWISE)
    s.CoincidentConstraint(entity1=v[8], entity2=g[6], addUndoState=False)
   


    s.Line(point1=(X_x, Y_y), point2=(X_x-float(YS_k)/2, Y_y-float(YS_k)*(math.sqrt(3))/2))
    s.CoincidentConstraint(entity1=v[10], entity2=g[7], addUndoState=False)
   
    s.Line(point1=(X_x, -Y_y), point2=(X_x-float(YS_k)/2, -Y_y+float(YS_k)*(math.sqrt(3))/2))
    s.CoincidentConstraint(entity1=v[11], entity2=g[6], addUndoState=False)
    
    # s.ObliqueDimension(vertex1=v[10], vertex2=v[5], textPoint=(188.516860961914,  30.994556427002), value=float(YS_k))
    # s.Parameter(name='YS_K', path='dimensions[6]', expression='Y4S',  previousParameter='L3')
    # s.SymmetryConstraint(entity1=v[10], entity2=v[11], symmetryAxis=g[3])
    # s.ObliqueDimension(vertex1=v[8], vertex2=v[11], textPoint=(182.844848632813,  -29.6974334716797), value=float(YS_k))

    # s.Parameter(name='YS_K2', path='dimensions[7]', expression='YS',  previousParameter='YS_K')
    p = mdb.models['Model-1'].Part(name=partname_k, dimensionality=THREE_D,  type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models['Model-1'].parts[partname_k]
    p.AnalyticRigidSurfRevolve(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname_k]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

    p.ReferencePoint(point=(0, 0.0, 0.0))

    #创建坐标系，YZG1圆轧辊
    r = p.referencePoints
    p.DatumCsysByThreePoints(origin=r[2], name='Oener_Datum_csys-1', 
    coordSysType=CARTESIAN, point1=(1.0, 0.0, 0.0), point2=(3.0, 3.0, 0.0))


dd_k = str(float(300))    
S_k = str(float(2))        
ZGD_k = str(float(650))   
dd_k = str(float(50))            
yanshen_k = str(float(40.0))   
bata_k = str(float(40.0))   
partname = str('pbox2')    

# HU3_2023(partname,dd_k,bata_k,ZGD_k,yanshen_k,S_k)