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
# 2022年11月6,改变直径后，会有圆角方向颠倒
# 孔型槽底宽度  b_k
# 孔型高度      H_k
# 辊缝          S_k
# 工作直径      D_k
# 侧壁斜度（百分比）    y_k
# 延伸          yanshen_k
# 文件名        partname_k

b_value = str(float(183.9))       
H_k = str(float(127))    
S_k = str(float(10))        
D_k = str(float(650))       
y_k = str(float(18))        
yanshen_k = str(float(100.0))   
partname_k = str('box2')         

def tuoyuan_shell(b_value, H_k, D_k, yanshen_k, partname_k, r_rate):

    r_radis = float(H_k) * r_rate

    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=1200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -600.0), point2=(0.0, 600.0))
    s.FixedConstraint(entity=g[2])
    s.ConstructionLine(point1=(-195.0, 0.0), point2=(100.0, 0.0))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.FixedConstraint(entity=g[3])
    s.Line(point1=(220.0, 100.0), point2=(220.0, 60.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.Line(point1=(220.0, -60.0), point2=(220.0, -100.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='b', expression=b_value)
    s.Parameter(name='h', expression=H_k, previousParameter='b')
    s.Parameter(name='b_k', expression='1.093*b', previousParameter='h')
    s.Spot(point=(140.0, 0.0))
    s.CoincidentConstraint(entity1=v[4], entity2=g[3], addUndoState=False)
    s.DistanceDimension(entity1=g[2], entity2=v[4], textPoint=(103.955688476563, -58.8212890625), value=140.0)

    s.Parameter(name='D', expression=D_k, previousParameter='b_k')
    s.Parameter(name='R_k', path='dimensions[0]', expression='D/2',  previousParameter='D')
    s.Arc3Points(point1=(220.0, 60.0), point2=(220.0, -60.0), point3=(150.0, 0.0))
    s.RadialDimension(curve=g[6], textPoint=(204.179626464844, 30.6083831787109), radius=60.7142857142857)

    s.Parameter(name='S', expression='0.25*h', previousParameter='D')
    s.Parameter(name='Rhu', path='dimensions[1]',   expression='((h-S)*(h-S)+b_k*b_k)/(4*(h-S))', previousParameter='R_k')
    s.DistanceDimension(entity1=g[5], entity2=g[2], textPoint=(22.3904418945313,  -147.186294555664), value=300.0)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='L2', path='dimensions[2]', expression='(D+h-S)/2',  previousParameter='Rhu')
    s.CoincidentConstraint(entity1=v[2], entity2=g[5])
    s.CoincidentConstraint(entity1=v[1], entity2=g[4])
    s.SymmetryConstraint(entity1=g[4], entity2=g[5], symmetryAxis=g[3])

    s.delete(objectList=(g[4], ))
    s.Line(point1=(200.0, 170.0), point2=(200.0, 120.0))
    s.VerticalConstraint(entity=g[7], addUndoState=False)

    s.delete(objectList=(g[5], ))
    s.Line(point1=(200.0, -185.0), point2=(200.0, -120.0))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.CoincidentConstraint(entity1=v[7], entity2=v[1])
    s.CoincidentConstraint(entity1=v[2], entity2=v[9])
    s.SymmetryConstraint(entity1=g[7], entity2=g[8], symmetryAxis=g[3])
    s.DistanceDimension(entity1=g[7], entity2=g[2], textPoint=(22.5473022460938, 
        137.02326965332), value=197.625)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='L2', path='dimensions[3]', expression='(D+h-S)/2',  previousParameter='Rhu')
    s.VerticalDimension(vertex1=v[6], vertex2=v[1], textPoint=(241.505798339844,  120.805801391602), value=65.0)

    s.Parameter(name='yanshen', path='dimensions[4]', expression= yanshen_k,  previousParameter='L2')
    s.Parameter(name='r_rate', expression='0.175*h', previousParameter='yanshen')
    s.Parameter(name='R_rate', expression='0.25*h', previousParameter='r_rate')
    s.ConstructionLine(point1=(240.0, 205.0), point2=(240.0, -160.0))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.DistanceDimension(entity1=g[9], entity2=g[7], textPoint=(205.413696289063, 218.110549926758), value=42.375)
    s.CoincidentConstraint(entity1=v[4], entity2=g[6])
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='gunfneg', path='dimensions[5]', expression='S/2', previousParameter='R_rate')
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
    session.viewports['Viewport: 1'].view.setValues(width=1217.2, height=543.624, 
        viewOffsetX=0.455414, viewOffsetY=9.1982)
    p = mdb.models['Model-1'].parts[partname_k]
    e1 = p.edges
    p.Round(radius=r_radis, edgeList=(e1[1], e1[4]))




# tuoyuan_shell(b_value, H_k, D_k, yanshen_k, partname_k, r_rate=0.18)


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
D_k = str(float(680))   
S_k = str(float(13))    
     
YS_k = str(float(50.0))   
partname_k = str('hu5')     

def tuo2023(b_value, H_k, D_k, S_k, YS_k, partname_k, r_rate):
    r_radis = float(H_k) * r_rate
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=1200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.ConstructionLine(point1=(0.0, -600.0), point2=(0.0, 600.0))
    s1.FixedConstraint(entity=g[2])
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
    s1.ConstructionLine(point1=(355.0, 0.0), point2=(355.0, -60.0))
    s1.VerticalConstraint(entity=g[5], addUndoState=False)
    s1.DistanceDimension(entity1=g[2], entity2=g[5], textPoint=(181.577301025391, 140.25634765625), value=355.0)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='R_k', path='dimensions[0]', expression='D/2',  previousParameter='YS')
    s1.Spot(point=(200.0, 0.0))
    s1.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
    s1.Spot(point=(260.0, 80.0))
    s1.Spot(point=(260.0, -60.0))
    s1.SymmetryConstraint(entity1=v[1], entity2=v[2], symmetryAxis=g[3])
    s1.CoincidentConstraint(entity1=v[0], entity2=g[3])
    s1.VerticalDimension(vertex1=v[1], vertex2=v[2], textPoint=(292.301971435547, 0.0), value=120.0)

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
    s1.DistanceDimension(entity1=v[6], entity2=g[3], textPoint=(438.849365234375, 15.8825750350952), value=149.5)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='B2', path='dimensions[4]', expression='B/2+YS',  previousParameter='R2')




    s1.sketchOptions.setValues(constructionGeometry=ON)
    s1.assignCenterline(line=g[2])
    p = mdb.models['Model-1'].Part(name=partname_k, dimensionality=THREE_D,  type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-1'].parts[partname_k]
    p.BaseShellRevolve(sketch=s1, angle=360.0, flipRevolveDirection=OFF)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname_k]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts[partname_k]
    e1 = p.edges
    p.Round(radius=r_radis, edgeList=(e1[1], e1[4]))
