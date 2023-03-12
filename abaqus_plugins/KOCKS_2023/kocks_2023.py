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
  
     

def KOCKS_2023(partname_k, DSI, PSI, ZGD, YS_k, W_k, R_k):
    du = math.pi/180

    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=800.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -400.0), point2=(0.0, 400.0))
    s.FixedConstraint(entity=g[2])
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='ZGD', expression=ZGD)
    s.Parameter(name='DSA', expression=DSI, previousParameter='ZGD')
    s.Parameter(name='PSI', expression=PSI, previousParameter='DSA')
    s.Parameter(name='W', expression=W_k, previousParameter='PSI')
    s.Parameter(name='R', expression=R_k, previousParameter='W')

    s.ConstructionLine(point1=(0.0, 0.0), point2=(140.0, 0.0))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.FixedConstraint(entity=g[3])

    v_zgr = float(ZGD)/2
   
    s.Spot(point=(v_zgr, 0.0))
    s.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=v[0], entity2=g[2], textPoint=(7.68038940429688, 74.5050659179688), value=v_zgr)

    v1_x = v_zgr - float(DSI)/2
    s.Spot(point=(v1_x, 0.0))
    s.CoincidentConstraint(entity1=v[1], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=v[1], entity2=g[2], textPoint=(7.27816772460938, 39.9649314880371), value=v1_x)
    s.Parameter(name='ZGR', path='dimensions[0]', expression='ZGD/2',  previousParameter='R')
    s.Parameter(name='L1', path='dimensions[1]', expression='ZGR-DSA/2', previousParameter='ZGR')

    s.ConstructionLine(point1=(v_zgr, 0.0), point2=(v_zgr+10, -20.0*math.sin(60*du)))
    s.CoincidentConstraint(entity1=v[0], entity2=g[4], addUndoState=False)
    s.ConstructionLine(point1=(v_zgr, 0.0), point2=(v_zgr+10, 20.0*math.sin(60*du)))
    s.CoincidentConstraint(entity1=v[0], entity2=g[5], addUndoState=False)

    s.AngularDimension(line1=g[4], line2=g[3], textPoint=(v_zgr+80, 26.7111778259277), value=120.0)
    s.AngularDimension(line1=g[5], line2=g[3], textPoint=(v_zgr+80, -11.4436073303223), value=120.0)

    v2_x = v_zgr - (float(W_k)/2)/math.sin(60*du)
    s.Spot(point=(v2_x, 0.0))
    s.CoincidentConstraint(entity1=v[2], entity2=g[3], addUndoState=False)

    s.DistanceDimension(entity1=g[2], entity2=v[2], textPoint=(125.861190795898, -15.2846164703369), value=v2_x)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='L2', path='dimensions[4]', expression='ZGR-(W/2)/sin(60)',  previousParameter='L1')

    s.ConstructionLine(point1=(v2_x, 0.0), point2=(v2_x+10,  -20.0*math.sin(60*du)))
    s.CoincidentConstraint(entity1=v[2], entity2=g[6], addUndoState=False)
    s.ConstructionLine(point1=(v2_x, 0.0), point2=(v2_x+10, 20.0*math.sin(60*du)))
    s.CoincidentConstraint(entity1=v[2], entity2=g[7], addUndoState=False)

    s.ParallelConstraint(entity1=g[5], entity2=g[7])
    s.ParallelConstraint(entity1=g[4], entity2=g[6])

    s.ConstructionLine(point1=(v_zgr, 0.0), point2=(v_zgr-50*math.cos(du*float(PSI)),  50*math.sin(du*float(PSI))))
    s.CoincidentConstraint(entity1=v[0], entity2=g[8], addUndoState=False)

    s.ConstructionLine(point1=(v_zgr, 0.0), point2=(v_zgr-50*math.cos(du*float(PSI)),  -50*math.sin(du*float(PSI))))
    s.CoincidentConstraint(entity1=v[0], entity2=g[9], addUndoState=False)

    s.AngularDimension(line1=g[8], line2=g[3], textPoint=(v_zgr-50,  1.8504638671875), value=float(PSI))
    s.Parameter(name='jiao1', path='dimensions[5]', expression='PSI',   previousParameter='L2')
    s.AngularDimension(line1=g[3], line2=g[9], textPoint=(v_zgr-50, -3.89169883728027), value=float(PSI))
    s.Parameter(name='jiao2', path='dimensions[6]', expression='PSI',   previousParameter='jiao1')

    v3_x = v1_x+float(R_k)
    s.Spot(point=(v3_x, 0.0))
    s.CoincidentConstraint(entity1=v[3], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=v[3], entity2=g[2], textPoint=(37.4504089355469,  -31.8077430725098), value=v3_x)
    s.Parameter(name='L3', path='dimensions[7]', expression='L1+R', previousParameter='jiao2')

    # print(v2_x)

    a_v = 1 + math.tan(du*float(PSI))*math.tan(du*float(PSI))
    b_v = -(2*v3_x+2*v_zgr*(math.tan(du*float(PSI))*math.tan(du*float(PSI))))
    c_v = v3_x*v3_x - float(R_k)*float(R_k)+(math.tan(du*float(PSI))*math.tan(du*float(PSI)))*v_zgr*v_zgr

    # print(a_v)
    # print(b_v)
    # print(c_v)


    no1_x = (-b_v - math.sqrt(b_v*b_v - 4*a_v*c_v))/(2*a_v)

    no1_y = -(no1_x-v_zgr) * math.tan(du*float(PSI))

    # print(no1_x)
    # print(no1_y)


    s.ArcByCenterEnds(center=(v3_x, 0.0), point1=(no1_x,  no1_y), point2=(no1_x,  -no1_y),  direction=COUNTERCLOCKWISE)
    s.CoincidentConstraint(entity1=v[4], entity2=g[8], addUndoState=False)
    s.CoincidentConstraint(entity1=v[5], entity2=g[9], addUndoState=False)
    s.RadialDimension(curve=g[10], textPoint=(128.801132202148, 4.51539516448975),  radius=float(R_k))

    s.Parameter(name='R_v', path='dimensions[8]', expression='R',   previousParameter='L3')

    k_v = (v3_x-no1_x)/no1_y

    no2_x = (math.sqrt(3)*v2_x + no1_x*k_v - no1_y)/(k_v+math.sqrt(3))
    no2_y = -math.sqrt(3)*(no2_x-v2_x)




    s.Line(point1=(no1_x, no1_y), point2=(no2_x, no2_y))
    # s.TangentConstraint(entity1=g[10], entity2=g[11], addUndoState=False)
    # s.CoincidentConstraint(entity1=v[7], entity2=g[6], addUndoState=False)

    s.Line(point1=(no1_x, -no1_y), point2=(no2_x, -no2_y))
    # s.TangentConstraint(entity1=g[10], entity2=g[12], addUndoState=False)
    # s.CoincidentConstraint(entity1=v[8], entity2=g[7], addUndoState=False)


    s.Line(point1=(no2_x,no2_y), point2=(no2_x - float(YS_k)*math.cos(du*60), no2_y+float(YS_k)*math.sin(du*60)))
    # s.CoincidentConstraint(entity1=v[9], entity2=g[7], addUndoState=False)
    s.Line(point1=(no2_x,-no2_y), point2=(no2_x - float(YS_k)*math.cos(du*60), -no2_y-float(YS_k)*math.sin(du*60)))
    # s.CoincidentConstraint(entity1=v[10], entity2=g[6], addUndoState=False)

    p = mdb.models['Model-1'].Part(name=partname_k, dimensionality=THREE_D, type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models['Model-1'].parts[partname_k]
    p.AnalyticRigidSurfRevolve(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname_k]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

    p.ReferencePoint(point=(0, 0.0, 0.0))

    # #创建坐标系，YZG1圆轧辊
    #创建坐标系，YZG1圆轧辊
    r = p.referencePoints
    p.DatumCsysByThreePoints(origin=r[2], name='Oener_Datum_csys-1', 
    coordSysType=CARTESIAN, point1=(1.0, 0.0, 0.0), point2=(3.0, 3.0, 0.0))


  
S_k = str(float(2))        
ZGD_k = str(float(400))   
dd_k = str(float(30))            
yanshen_k = str(float(40.0))   
bata_k = str(float(25.0))   
partname = str('pbox55')    

# KOCKS_2023(partname_k=partname, DSI=dd_k, PSI=bata_k, ZGD=ZGD_k, YS_k=yanshen_k, W_k=S_k, R_k = '18')