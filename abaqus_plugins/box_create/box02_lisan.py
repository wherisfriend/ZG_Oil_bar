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

# 箱型孔测试
# 2022年11月8,解析刚体
# 孔型槽底宽度  b_k
# 孔型高度      H_k
# 辊缝          S_k
# 工作直径      D_k
# 侧壁斜度（百分比）    y_k
# 延伸          yanshen_k
# 文件名        partname_k
# 圆角系数      r_rate

b_k = str(float(162))       
H_k = str(float(232.2))    
S_k = str(float(10))        
D_k = str(float(500))       
y_k = str(float(18))        
yanshen_k = str(float(80.0))   
partname_k = str('zhaoyag')
r_rate = 0.1
r_radis = float(b_k) * r_rate


# 离散刚体

def box(b_k, H_k, S_k, D_k, y_k, yanshen_k, partname_k, r_rate):
    r_radis = float(b_k) * r_rate
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=1000.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -500.0), point2=(0.0, 500.0))
    s.FixedConstraint(entity=g[2])
    s.ConstructionLine(point1=(-60.0, 0.0), point2=(45.0, 0.0))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s=mdb.models['Model-1'].sketches['__profile__']

    s.Parameter(name='H', expression=H_k)
    s.Parameter(name='W', expression=b_k, previousParameter='H')
    s.Parameter(name='y', expression=y_k, previousParameter='W')
    s.Parameter(name='S', expression=S_k, previousParameter='y')
    s.Parameter(name='r', expression=str(r_radis), previousParameter='S')
    s.Line(point1=(100.0, 80.0), point2=(100.0, 40.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.Line(point1=(100.0, 40.0), point2=(60.0, 20.0))
    s.Line(point1=(60.0, 20.0), point2=(60.0, -20.0))
    s.VerticalConstraint(entity=g[6], addUndoState=False)
    s.Line(point1=(60.0, -20.0), point2=(100.0, -40.0))
    s.Line(point1=(100.0, -40.0), point2=(100.0, -80.0))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.VerticalDimension(vertex1=v[2], vertex2=v[3], textPoint=(39.0944519042969, 
        -12.6425933837891), value=40.0)
    s.VerticalDimension(vertex1=v[1], vertex2=v[4], textPoint=(122.170196533203, 
        -19.7401733398438), value=80.0)
    s.HorizontalDimension(vertex1=v[2], vertex2=v[1], textPoint=(73.3020935058594, 
        51.6793518066406), value=40.0)
    s.VerticalDimension(vertex1=v[0], vertex2=v[1], textPoint=(123.058685302734, 
        56.1153411865234), value=40.0)
    s.SymmetryConstraint(entity1=g[5], entity2=g[7], symmetryAxis=g[3])
    s.SymmetryConstraint(entity1=g[4], entity2=g[8], symmetryAxis=g[3])
    s.DistanceDimension(entity1=g[6], entity2=g[2], textPoint=(0.444244384765625, 
        12.642578125), value=60.0)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='b_k', path='dimensions[0]', expression='W', 
        previousParameter='r')
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='h_k', path='dimensions[2]', expression='(H-S)/2', 
        previousParameter='b_k')
    s.Parameter(name='B_k', path='dimensions[1]', expression='(y/100)*2*h_k+b_k', 
        previousParameter='h_k')

    # s.parameters['B_k'].setValues(expression='(y/100)*2*h_k+b_k')

    s.Parameter(name='yanshen', path='dimensions[3]', expression=yanshen_k,  previousParameter='B_k')
    s.Parameter(name='D', expression=D_k, previousParameter='y')
    s.Parameter(name='R_k', path='dimensions[4]', expression='(D-H)/2',  previousParameter='yanshen')

    s.sketchOptions.setValues(constructionGeometry=ON)
    s.assignCenterline(line=g[2])
    p = mdb.models['Model-1'].Part(name=partname_k, dimensionality=THREE_D,   type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts[partname_k]
    p.BaseShellRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname_k]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)

    del mdb.models['Model-1'].sketches['__profile__']

    p = mdb.models['Model-1'].parts[partname_k]
    e = p.edges
    p.Round(radius=r_radis, edgeList=(e[4], ))

    p = mdb.models['Model-1'].parts[partname_k]
    e1 = p.edges
    p.Round(radius=r_radis, edgeList=(e1[5], ))
    p = mdb.models['Model-1'].parts[partname_k]
    e = p.edges
    p.Round(radius=r_radis, edgeList=(e[8], ))
    p = mdb.models['Model-1'].parts[partname_k]
    e1 = p.edges
    p.Round(radius=r_radis, edgeList=(e1[11], ))

    # 抽壳
    c1 = p.cells
    p.RemoveCells(cellList = c1[0:1])
    #: 
    #: One shell per selected cell has been created from the cell's faces.
