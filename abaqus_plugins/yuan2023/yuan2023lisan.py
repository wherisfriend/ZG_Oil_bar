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

# 孔测试
# 2023年2月10,
# 孔型槽底宽度  b_k
# 孔型高度      H_k
# 辊缝          S_k
# 工作直径      D_k
# 延伸          YS_k
# 文件名        partname_k

b_value = str(float(190))       
H_k = str(float(127))         
D_k = str(float(400))   
S_k = str(float(13))    

R_k = str(float(78))  
     
YS_k = str(float(50.0))   
partname_k = str('hu5')     

radis = str(float(1.75))   




def yuan2023(ZJ, D_k, S_k, YS_k, partname_k, r_radis):

    r_radis = float(r_radis)
   
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=1200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -600.0), point2=(0.0, 600.0))
    s.FixedConstraint(entity=g[2])
    s.ConstructionLine(point1=(-155.0, 0.0), point2=(-30.0, 0.0))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.ConstructionLine(point1=(0.0, 60.0), point2=(0.0, 9.54547119140625))
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.FixedConstraint(entity=g[3])
    s.FixedConstraint(entity=g[2])
   
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='S', expression=S_k)
    s.Parameter(name='ZD', expression=D_k, previousParameter='S')
    s.Parameter(name='YS', expression=YS_k, previousParameter='ZD')
    s.Parameter(name='ZJ', expression=ZJ, previousParameter='YS')
    s.ConstructionLine(point1=(330.0, 0.0), point2=(330.0, -90.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.DistanceDimension(entity1=g[2], entity2=g[5], textPoint=(222.576232910156,  192.587905883789), value=330.0)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='ZR', path='dimensions[0]', expression='ZD/2',  previousParameter='ZJ')
    s.ConstructionLine(point1=(285.0, 0.0), point2=(285.0, -75.0))
    s.VerticalConstraint(entity=g[6], addUndoState=False)
    s.DistanceDimension(entity1=g[2], entity2=g[6], textPoint=(230.690856933594,  162.204727172852), value=285.0)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='L2', path='dimensions[1]', expression='ZR-S/2', previousParameter='ZR')
    s.Spot(point=(260.0, 0.0))
    s.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=v[0], entity2=g[2], textPoint=(10.2426300048828, 
        118.317886352539), value=260.0)

    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='L1', path='dimensions[2]', expression='ZR-ZJ/2', 
        previousParameter='L2')
   
    s.Arc3Points(point1=(336.0, 40.7478179931641), point2=(336.0, 
        -38.5598754882813), point3=(301.0, 0.0))
    s.CoincidentConstraint(entity1=v[1], entity2=g[6], addUndoState=False)
    s.CoincidentConstraint(entity1=v[2], entity2=g[6], addUndoState=False)

    s.RadialDimension(curve=g[7], textPoint=(251.547058105469, 34.2527923583984), 
        radius=39.9611311387988)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='BJ', path='dimensions[3]', expression='ZJ/2', 
        previousParameter='L1')
    s.SymmetryConstraint(entity1=v[1], entity2=v[2], symmetryAxis=g[3])
    s.ConstructionLine(point1=(315.0, 100.0), point2=(315.0, 60.0))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.delete(objectList=(g[8], ))
    s.Line(point1=(325.0, 105.0), point2=(325.0, 60.0))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.Line(point1=(320.0, -55.0), point2=(320.0, -110.0))
    s.VerticalConstraint(entity=g[10], addUndoState=False)
    s.SymmetryConstraint(entity1=g[9], entity2=g[10], symmetryAxis=g[3])
    s.CoincidentConstraint(entity1=v[4], entity2=g[6])
    s.CoincidentConstraint(entity1=v[5], entity2=v[1])
    s.DistanceDimension(entity1=v[4], entity2=g[3], textPoint=(379.382232666016, 
        26.6158638000488), value=105.0)

    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='H1', path='dimensions[4]', expression='BJ+YS', 
        previousParameter='BJ')

    s.sketchOptions.setValues(constructionGeometry=ON)
    s.assignCenterline(line=g[2])
    p = mdb.models['Model-1'].Part(name=partname_k, dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-1'].parts[partname_k]
    p.BaseShellRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname_k]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts[partname_k]
    e = p.edges
    p.Round(radius=r_radis, edgeList=(e[1], e[4]))

# tuo2023(b_value, H_k, D_k, S_k, YS_k, partname_k)

# yuan2023(R_k,D_k,S_k,YS_k,partname_k,radis)