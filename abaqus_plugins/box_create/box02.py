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


# 解析刚体

def box(b_k, H_k, S_k, D_k, y_k, yanshen_k, partname_k, r_rate):
    r_radis = float(b_k) * r_rate
    r_value = str(r_radis)
    # print(r_radis)
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=1200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.ConstructionLine(point1=(0.0, -600.0), point2=(0.0, 600.0))
    s1.FixedConstraint(entity=g[2])
    s1.ConstructionLine(point1=(-230.0, 0.0), point2=(85.0, 0.0))
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    s1.FixedConstraint(entity=g[3])
   
    
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='H', expression=H_k)
    s.Parameter(name='W', expression=b_k, previousParameter='H')
    s.Parameter(name='y', expression=y_k, previousParameter='W')
    s.Parameter(name='D', expression=D_k, previousParameter='y')
    s.Parameter(name='S', expression=S_k, previousParameter='D')
    s.Parameter(name='r', expression=r_value, previousParameter='S')
    s.Parameter(name='yanshen', expression=yanshen_k, previousParameter='r')

    f_D_k = float(D_k)
    f_S_k = float(S_k)
    f_H_k = float(H_k)
    f_y_k = float(y_k)
    f_b_k = float(b_k)
    f_yanshen_k = float(yanshen_k)
    f_Bk = (f_y_k/100)*2*((f_H_k-f_S_k)/2)+f_b_k
    p1_h = f_yanshen_k + f_Bk/2

    p1_r = (f_D_k-f_S_k)/2
    p2_r = (f_D_k-f_H_k)/2

    s1.Line(point1=(p1_r, p1_h), point2=(p1_r, f_Bk/2))
    s1.VerticalConstraint(entity=g[4], addUndoState=False)
    s1.Line(point1=(p1_r, f_Bk/2), point2=(p2_r, f_b_k/2))
    s1.Line(point1=(p2_r, f_b_k/2), point2=(p2_r, -f_b_k/2))
    s1.VerticalConstraint(entity=g[6], addUndoState=False)
    s1.Line(point1=(p2_r, -f_b_k/2), point2=(p1_r, -f_Bk/2))
    s1.Line(point1=(p1_r, -f_Bk/2), point2=(p1_r, -p1_h))
    s1.VerticalConstraint(entity=g[8], addUndoState=False)
    s1.SymmetryConstraint(entity1=v[2], entity2=v[3], symmetryAxis=g[3])
    s1.SymmetryConstraint(entity1=v[4], entity2=v[1], symmetryAxis=g[3])
    s1.SymmetryConstraint(entity1=v[0], entity2=v[5], symmetryAxis=g[3])

    s1.VerticalDimension(vertex1=v[2], vertex2=v[3], textPoint=(195.926361083984,   -51.6382217407227), value=210.0)
   
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='b_k', path='dimensions[0]', expression='W', previousParameter='yanshen')
    s1.VerticalDimension(vertex1=v[1], vertex2=v[4], textPoint=(376.573455810547, -86.9733200073242), value=280.0)
    s1.HorizontalDimension(vertex1=v[2], vertex2=v[1], textPoint=(277.9521484375, 240.878829956055), value=40.0)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='h_k', path='dimensions[2]', expression='(H-S)/2', previousParameter='b_k')
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='B_k', path='dimensions[1]', expression='(y/100)*2*h_k+b_k',  previousParameter='h_k')
    s1.DistanceDimension(entity1=v[0], entity2=g[3], textPoint=(492.083740234375,  59.1305160522461), value=190.0)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='YK', path='dimensions[3]', expression='yanshen+B_k/2',  previousParameter='B_k')
    s1.DistanceDimension(entity1=g[6], entity2=g[2], textPoint=(45.5498504638672,  82.1269760131836), value=224.0)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='R_k', path='dimensions[4]', expression='(D-H)/2',   previousParameter='YK')

    s1.FilletByRadius(radius=r_radis, curve1=g[6], nearPoint1=(p2_r, 0), curve2=g[5], nearPoint2=((p1_r+p2_r)/2, (f_Bk+f_b_k)/4))
    s1.FilletByRadius(radius=r_radis, curve1=g[5], nearPoint1=((p1_r+p2_r)/2, (f_Bk+f_b_k)/4), curve2=g[4], nearPoint2=(p1_r, f_Bk/2+f_yanshen_k/2))
    s1.FilletByRadius(radius=r_radis, curve1=g[6], nearPoint1=(p2_r, 0), curve2=g[7], nearPoint2=((p1_r+p2_r)/2, -(f_Bk+f_b_k)/4))
    s1.FilletByRadius(radius=r_radis, curve1=g[7], nearPoint1=((p1_r+p2_r)/2, -(f_Bk+f_b_k)/4), curve2=g[8], nearPoint2=(p1_r, -f_Bk/2-f_yanshen_k/2))
    p = mdb.models['Model-1'].Part(name=partname_k, dimensionality=THREE_D, type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models['Model-1'].parts[partname_k]
    p.AnalyticRigidSurfRevolve(sketch=s1)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname_k]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
