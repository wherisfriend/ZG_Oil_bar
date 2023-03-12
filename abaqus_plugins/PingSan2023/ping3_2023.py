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


   
dd_k = str(float(300))    
S_k = str(float(2))        
D_k = str(float(650))            
yanshen_k = str(float(40.0))   
partname = str('pbox2')         

def PING3_2023(partname, ZGD, D, S_k, YS):

    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=800.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -400.0), point2=(0.0, 400.0))
    s.FixedConstraint(entity=g[2])
    s.ConstructionLine(point1=(-90.0, 0.0), point2=(85.0, 0.0))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.FixedConstraint(entity=g[3])

    ZGD_f = float(ZGD)


    s.ConstructionLine(point1=(ZGD_f/2, 95.0), point2=(ZGD_f/2, -145.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.DistanceDimension(entity1=g[4], entity2=g[2], textPoint=(62.4816207885742, 116.073249816895), value=ZGD_f/2)

    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='ZGD', expression=ZGD)
    s.Parameter(name='D', expression=D, previousParameter='ZGD')
    s.Parameter(name='YS', expression=YS, previousParameter='D')
    s.Parameter(name='S', expression=S_k, previousParameter='YS')
    s.Parameter(name='ZGR', path='dimensions[0]', expression='ZGD/2', previousParameter='S')
    

    s.ConstructionLine(point1=(150.0, 0.0), point2=(175.0, -40.0))
    s.ConstructionLine(point1=(150.0, 0.0), point2=(175.0, 25.0))
    s.AngularDimension(line1=g[5], line2=g[3], textPoint=(186.616271972656,  12.3437786102295), value=122.005383208083)
    s.AngularDimension(line1=g[6], line2=g[3], textPoint=(208.554321289063, -17.9512805938721), value=120.0)
    s.delete(objectList=(d[1], ))
    s.AngularDimension(line1=g[5], line2=g[3], textPoint=(191.283935546875,  23.9957103729248), value=120.0)
    s.delete(objectList=(g[5], ))
    s.delete(objectList=(g[6], ))


    s.Spot(point=(ZGD_f/2, 0.0))
    s.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
    s.Spot(point=(ZGD_f/2, 0.0))
    s.FixedConstraint(entity=v[0])

    s.ConstructionLine(point1=(ZGD_f/2, 0.0), point2=(ZGD_f/2 + 1, -2))
    s.CoincidentConstraint(entity1=v[0], entity2=g[7], addUndoState=False)

    s.ConstructionLine(point1=(ZGD_f/2, 0.0), point2=(ZGD_f/2 + 1, 2))
    s.CoincidentConstraint(entity1=v[0], entity2=g[8], addUndoState=False)

    s.AngularDimension(line1=g[7], line2=g[3], textPoint=(184.749206542969, 10.0133800506592), value=120.0)
    s.AngularDimension(line1=g[8], line2=g[3], textPoint=(185.215972900391, -10.4940357208252), value=120.0)

    pot_x = ZGD_f/2 - float(D)/2

    s.ConstructionLine(point1=(pot_x, 0.0), point2=(pot_x, -80.0))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.DistanceDimension(entity1=g[2], entity2=g[9], textPoint=(54.5213317871094, 39.3762817382813), value=pot_x)

    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='L1', path='dimensions[6]', expression='ZGR-D/2',  previousParameter='ZGR')

    # d*2*sin(60)-2*gunfeng

    H1 = 2*float(D)*(math.sin((math.pi)/3)) - 2*float(S_k)

    s.Line(point1=(pot_x, H1/2), point2=(pot_x, -H1/2))

    s.VerticalConstraint(entity=g[10], addUndoState=False)
    s.ParallelConstraint(entity1=g[9], entity2=g[10], addUndoState=False)
    s.CoincidentConstraint(entity1=v[2], entity2=g[9], addUndoState=False)
    s.CoincidentConstraint(entity1=v[3], entity2=g[9], addUndoState=False)
    s.SymmetryConstraint(entity1=v[2], entity2=v[3], symmetryAxis=g[3])
    s.VerticalDimension(vertex1=v[2], vertex2=v[3], textPoint=(78.7931823730469, -20.7477436065674), value=H1)

    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='H1', path='dimensions[7]', expression='D*2*sin(60)-2*S',  previousParameter='L1')

    ppp = math.sin(((math.pi)/3))

    s.Line(point1=(pot_x, H1/2), point2=(pot_x-float(YS)/2, H1/2 + ppp*float(YS)))

    s.Line(point1=(pot_x, -H1/2), point2=(pot_x-float(YS)/2, -H1/2 - ppp*float(YS)))
  
    # s.AngularDimension(line1=g[11], line2=g[3], textPoint=(95.5824279785156,  18.9698276519775), value=60)
   
    # s.ObliqueDimension(vertex1=v[4], vertex2=v[2], textPoint=(125.0, 76.2775573730469), value=float(YS))

    # s.Parameter(name='YS_a', path='dimensions[9]', expression='YS',  previousParameter='H1')
    s.SymmetryConstraint(entity1=g[11], entity2=g[12], symmetryAxis=g[3])
    p = mdb.models['Model-1'].Part(name=partname, dimensionality=THREE_D,  type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models['Model-1'].parts[partname]
    p.AnalyticRigidSurfRevolve(sketch=s)
    # s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

    p.ReferencePoint(point=(0, 0.0, 0.0))

    #创建坐标系，YZG1圆轧辊
    #创建坐标系，YZG1圆轧辊
    r = p.referencePoints
    p.DatumCsysByThreePoints(origin=r[2], name='Oener_Datum_csys-1', 
    coordSysType=CARTESIAN, point1=(1.0, 0.0, 0.0), point2=(3.0, 3.0, 0.0))


