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

# alf取值为40°~30°
# 轧辊直径 Dh_k
# 扩张圆角
# 弧长半径R:
# gunfeng_k辊缝宽度
# yanshen_k延伸长度

# 此处有一个bug：顺时针、逆时针画圆弧(已解决)
# COUNTERCLOCKWISE、CLOSEWISE
   
# s.ArcByCenterEnds(center=(pox1, 0.0), point1=(pox1-40, 15.0), point2=(pox1-40, -15.0),  direction=CLOCKWISE)



def yuankong(partname_k, ZGD_k, YS_k, S_k, alf_k, D_k):
   
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=800.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -400.0), point2=(0.0, 400.0))
    s.FixedConstraint(entity=g[2])
    s.ConstructionLine(point1=(-45.0, 0.0), point2=(120.0, 0.0))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.FixedConstraint(entity=g[3])
   
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='alf', expression=alf_k)
    s.Parameter(name='ZGD', expression=ZGD_k, previousParameter='alf')
    s.Parameter(name='D', expression=D_k, previousParameter='ZGD')
    s.Parameter(name='YS', expression=YS_k, previousParameter='D')
    s.Parameter(name='S_k', expression=S_k, previousParameter='YS')

    pox1 = float(ZGD_k)/2
    s.Spot(point=(pox1, 0.0))
    s.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=v[0], entity2=g[2], textPoint=(25.6949920654297, 91.5448608398438), value=pox1)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='ZGR', path='dimensions[0]', expression='ZGD/2',  previousParameter='S_k')
    
    s.ConstructionLine(point1=(pox1, 0.0), point2=(pox1, -65.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)

    s.CoincidentConstraint(entity1=v[0], entity2=g[4], addUndoState=False)
    s.ConstructionLine(point1=(pox1, 0.0), point2=(pox1+25, -35.0))
    s.CoincidentConstraint(entity1=v[0], entity2=g[5], addUndoState=False)
    s.ConstructionLine(point1=(pox1, 0.0), point2=(pox1+25, 35.0))
    s.CoincidentConstraint(entity1=v[0], entity2=g[6], addUndoState=False)

    s.AngularDimension(line1=g[5], line2=g[3], textPoint=(283.912902832031, 19.0416679382324), value=120.0)
    s.AngularDimension(line1=g[6], line2=g[3], textPoint=(285.201843261719, -10.9892311096191), value=120.0)
    
    s.ConstructionLine(point1=(pox1, 0.0), point2=(pox1+80, -55.0))
    s.CoincidentConstraint(entity1=v[0], entity2=g[7], addUndoState=False)
    s.ConstructionLine(point1=(pox1, 0.0), point2=(pox1+80, 55.0))
    s.CoincidentConstraint(entity1=v[0], entity2=g[8], addUndoState=False)
    s.AngularDimension(line1=g[7], line2=g[5], textPoint=(201.420639038086,  56.7948112487793), value=float(alf_k))
    s.AngularDimension(line1=g[8], line2=g[6], textPoint=(193.257369995117,  -62.0417900085449), value=float(alf_k))

    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Jia1', path='dimensions[3]', expression='alf',  previousParameter='ZGR')
    s.Parameter(name='Jia2', path='dimensions[4]', expression='alf',  previousParameter='Jia1')


    pox2 = pox1-(float(S_k)/2)/(math.sin((math.pi)/3))
    s.Spot(point=(pox2, 0.0))

    s.CoincidentConstraint(entity1=v[1], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=v[1], entity2=g[2], textPoint=(12.9567565917969, -13.8148384094238), value=pox2)

    s.Parameter(name='L2', path='dimensions[5]', expression='ZGR-(S_k/2)/(sin(60))',  previousParameter='Jia2')


    s.ConstructionLine(point1=(pox2, 0.0), point2=(pox2+7, -15.0))
    s.CoincidentConstraint(entity1=v[1], entity2=g[9], addUndoState=False)
    s.ConstructionLine(point1=(pox2, 0.0), point2=(pox2+7,  15))
    s.CoincidentConstraint(entity1=v[1], entity2=g[10], addUndoState=False)

    s.ParallelConstraint(entity1=g[9], entity2=g[5])
    s.ParallelConstraint(entity1=g[10], entity2=g[6])

    # COUNTERCLOCKWISE
   
    s.ArcByCenterEnds(center=(pox1, 0.0), point1=(pox1-40, 15.0), point2=(pox1-40, -15.0),  direction=CLOCKWISE)
    s.CoincidentConstraint(entity1=v[2], entity2=g[7], addUndoState=False)
    s.CoincidentConstraint(entity1=v[3], entity2=g[8], addUndoState=False)
    
    s.RadialDimension(curve=g[11], textPoint=(191.5087890625, 9.61495208740234),   radius=float(D_k)/2)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='RR', path='dimensions[6]', expression='D/2', previousParameter='L2')

    jiadu = 60 - float(alf_k)

    jiaodu_r = (math.pi)*jiadu/180
    jiadu_x = (float(D_k)/2)*math.cos(jiaodu_r)
    jiadu_y = (float(D_k)/2)*math.sin(jiaodu_r)

    # print(jiadu_x)
    # print(jiadu_y)

    rrr = float(D_k)/2

    xianchang = (rrr)/(math.cos((math.pi)*(float(alf_k))/180))

    ppp1_x = xianchang*math.cos((math.pi)/3)
    ppp1_y = xianchang*math.sin((math.pi)/3)

    # 相切
    # 点1坐标
    p_1_x = pox1- jiadu_x
    p_1_y = jiadu_y
    # 点2坐标
    p_2_x = pox1-ppp1_x
    p_2_y =ppp1_y
    # 斜率
    k_k = (p_2_y-p_1_y)/(p_2_x-p_1_x)
    # 斜边长度
    k_L = (float(S_k)/2)/math.sin((math.pi)*(90-float(alf_k))/180)

    jiajia_m = math.atan(k_k)

    p_3_x = p_2_x - k_L*math.cos(jiajia_m)
    p_3_y = p_2_y - k_L*math.sin(jiajia_m)
    

    s.Line(point1=(p_1_x, p_1_y), point2=(p_3_x, p_3_y))


    # s.TangentConstraint(entity1=g[11], entity2=g[12], addUndoState=False)
    # s.CoincidentConstraint(entity1=v[5], entity2=g[10], addUndoState=False)
   
    s.Line(point1=(p_1_x, -p_1_y), point2=(p_3_x, -p_3_y))
    # s.TangentConstraint(entity1=g[11], entity2=g[13], addUndoState=False)
    # s.CoincidentConstraint(entity1=v[6], entity2=g[9], addUndoState=False)

    p_4_x = p_3_x - float(YS_k)/2
    p_4_y = p_3_y + float(YS_k)*math.sin((math.pi)/3)
   
    s.Line(point1=(p_3_x, p_3_y), point2=(p_4_x, p_4_y))
    # s.CoincidentConstraint(entity1=v[7], entity2=g[9], addUndoState=False)

    s.Line(point1=(p_3_x, -p_3_y), point2=(p_4_x, -p_4_y))
    # s.CoincidentConstraint(entity1=v[8], entity2=g[10], addUndoState=False)
    # s.SymmetryConstraint(entity1=g[12], entity2=g[13], symmetryAxis=g[3])
    # s.SymmetryConstraint(entity1=v[8], entity2=v[7], symmetryAxis=g[3])
    # s.ObliqueDimension(vertex1=v[8], vertex2=v[5], textPoint=(221.318832397461, 79.8554916381836), value=29.4635952962876)
    # s.undo()
    # s.ObliqueDimension(vertex1=v[8], vertex2=v[5], textPoint=(221.539947509766, 78.5307693481445), value=29.4635952962876)

    # s.undo()

    # s.delete(objectList=(c[37], ))

    # s.ObliqueDimension(vertex1=v[6], vertex2=v[7], textPoint=(199.221069335938,  -50.0505332946777), value=29.4635952955965)
    # s=mdb.models['Model-1'].sketches['__profile__']
    # s.Parameter(name='YSL', path='dimensions[7]', expression='YS',  previousParameter='RR')
   
    # s.SymmetryConstraint(entity1=v[7], entity2=v[8], symmetryAxis=g[3])
   
    # s.ObliqueDimension(vertex1=v[8], vertex2=v[5], textPoint=(218.816009521484,   77.6159362792969), value=29.4635952962876)
    s=mdb.models['Model-1'].sketches['__profile__']
    # s.Parameter(name='YSL2', path='dimensions[8]', expression='YS',   previousParameter='YSL')
  
    p = mdb.models['Model-1'].Part(name=partname_k, dimensionality=THREE_D,  type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models['Model-1'].parts[partname_k]
    p.AnalyticRigidSurfRevolve(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname_k]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']



    p.ReferencePoint(point=(0, 0.0, 0.0))

    # #创建坐标系，YZG1圆轧辊
    # r = p.referencePoints
    # p.DatumCsysByThreePoints(origin=r[2], name='YZG1', coordSysType=CARTESIAN, 
    # point1=(0.0, 0.0, 0.0), point2=(5.0, 0.0, -1.0))



dd_k = str(float(400))    
S_k = str(float(2))        
D_k = str(float(600))            
yanshen_k = str(float(50.0))   
partname = str('pbox2')     

# yuankong(partname,D_k,yanshen_k,S_k,str('40'),dd_k)