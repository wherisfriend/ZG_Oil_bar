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
from caeModules import *
from driverUtils import executeOnCaeStartup

def bar(D, Thick, L, materialXin, materialTao,modelName, modelName2):
    session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=204.830078125,  height=200.41667175293)
    session.viewports['Viewport: 1'].makeCurrent()
    session.viewports['Viewport: 1'].maximize()
    executeOnCaeStartup()
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=ON)
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='D', expression=D)
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(-10.0, -15.0))
    s.RadialDimension(curve=g[2], textPoint=(-35.0961532592773, 12.0215454101563), radius=18.0277563773199)
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(-20.0, 17.5))
    s.RadialDimension(curve=g[3], textPoint=(-36.5177688598633, 19.740177154541),  radius=26.5753645318366)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='R1', path='dimensions[1]', expression='D/2',  previousParameter='D')
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Thick', expression=Thick, previousParameter='D')
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='R2', path='dimensions[0]', expression='R1-Thick',  previousParameter='R1')
    p = mdb.models['Model-1'].Part(name='TaoTong', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['TaoTong']

    # L 是float

    p.BaseSolidExtrude(sketch=s, depth=float(L))
    s.unsetPrimaryObject()

    p = mdb.models['Model-1'].parts['TaoTong']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='D', expression=D)
    s.Parameter(name='Thick', expression=Thick, previousParameter='D')
    s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(-5.0, -5.0))
    s1.RadialDimension(curve=g[2], textPoint=(-9.50705718994141, 10.335865020752),   radius=7.07106781186548)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='R', path='dimensions[0]', expression='D/2-Thick',  previousParameter='Thick')
    p = mdb.models['Model-1'].Part(name='XinBang', dimensionality=THREE_D,  type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['XinBang']

    # 拉伸长度
    p.BaseSolidExtrude(sketch=s1, depth=float(L))
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['XinBang']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,  engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues( referenceRepresentation=OFF)
        

    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-XinBang',  material=materialXin, thickness=None)
    p = mdb.models['Model-1'].parts['XinBang']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(cells=cells, name='Set-1')
    p = mdb.models['Model-1'].parts['XinBang']
    p.SectionAssignment(region=region, sectionName='Section-XinBang', offset=0.0,  offsetType=MIDDLE_SURFACE, offsetField='',  thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-TaoTong',  material=materialTao, thickness=None)
    p = mdb.models['Model-1'].parts['TaoTong']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['TaoTong']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(cells=cells, name='Set-1')
    p = mdb.models['Model-1'].parts['TaoTong']
    p.SectionAssignment(region=region, sectionName='Section-TaoTong', offset=0.0,  offsetType=MIDDLE_SURFACE, offsetField='',  thicknessAssignment=FROM_SECTION)
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['TaoTong']
    a.Instance(name='TaoTong-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['XinBang']
    a.Instance(name='XinBang-1', part=p, dependent=ON)

    a = mdb.models['Model-1'].rootAssembly
    a.rotate(instanceList=('TaoTong-1', 'XinBang-1'), axisPoint=(0.0, 1.0, 0.0), 
    axisDirection=(0.0, -1.0, 0.0), angle=180.0)


# 从材料库导入材料
# from material import createMaterialFromDataString
    # createMaterialFromDataString('Model-1', 'SI_m111111_AISI304', '6-10', 
    #     """{'specificHeat': {'temperatureDependency': OFF, 'table': ((500.0,),), 'dependencies': 0, 'law': CONSTANTVOLUME}, 'materialIdentifier': '', 'description': '\xb2\xc4\xc1\xcf\xbf\xe2\xc0\xb4\xd4\xb4: https://xcbjx.taobao.com/\n\xbb\xb6\xd3\xad\xbc\xd3\xc8\xebqq\xc8\xba : Abaqus \xbb\xb6\xc0\xd6\xb9\xb2\xbd\xf8\xc6\xbd\xcc\xa8 431603427\nAISI 304[N_m_kg]\n\xb2\xe2\xca\xd4\xc0\xe0\xd0\xcd\xa3\xba\n\xcb\xb5\xc3\xf7\xa3\xba\n\xd0\xc5\xcf\xa2\xa3\xba\n\xce\xaa\xc2\xfa\xd7\xe3\xc6\xf3\xd2\xb5\xbb\xf2\xb8\xf6\xc8\xcb\xb6\xa8\xd6\xc6\xbb\xaf\xd0\xe8\xc7\xf3\xa3\xac\xce\xd2\xc3\xc7\xcc\xe1\xb9\xa9\xb2\xc4\xc1\xcf\xbf\xe2\xb6\xa8\xd6\xc6\xb7\xfe\xce\xf1\xa3\xac\xd2\xb2\xbd\xab\xcd\xc6\xb3\xf6\xb8\xfc\xb6\xe0\xc0\xa9\xb3\xe4\xa1\xa2\xd7\xa8\xd2\xb5\xb5\xc4\xb2\xc4\xc1\xcf\xbf\xe2\xa3\xac\xce\xaaABAQUS\xb7\xc2\xd5\xe6\xd0\xa7\xc2\xca\xcc\xe1\xb8\xdf\xb6\xf8\xc5\xac\xc1\xa6\xa1\xa3', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((190000000000.0, 0.29),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((8000.0,),), 'dependencies': 0}, 'name': 'SI_m111111_AISI304', 'plastic': {'temperatureDependency': OFF, 'strainRangeDependency': OFF, 'rate': OFF, 'dependencies': 0, 'hardening': ISOTROPIC, 'dataType': HALF_CYCLE, 'table': ((206807000.0, 0.0),), 'numBackstresses': 1}, 'expansion': {'temperatureDependency': OFF, 'userSubroutine': OFF, 'zero': 0.0, 'dependencies': 0, 'table': ((1.8e-05,),), 'type': ISOTROPIC}, 'conductivity': {'temperatureDependency': OFF, 'table': ((16.0,),), 'dependencies': 0, 'type': ISOTROPIC}}""")
    # #: Material 'SI_m111111_AISI304' has been copied to the current model.
    # from material import createMaterialFromDataString
    # createMaterialFromDataString('Model-1', 'SI_m111111_AISI304', '6-10', 
    #     """{'specificHeat': {'temperatureDependency': OFF, 'table': ((500.0,),), 'dependencies': 0, 'law': CONSTANTVOLUME}, 'materialIdentifier': '', 'description': '\xb2\xc4\xc1\xcf\xbf\xe2\xc0\xb4\xd4\xb4: https://xcbjx.taobao.com/\n\xbb\xb6\xd3\xad\xbc\xd3\xc8\xebqq\xc8\xba : Abaqus \xbb\xb6\xc0\xd6\xb9\xb2\xbd\xf8\xc6\xbd\xcc\xa8 431603427\nAISI 304[N_m_kg]\n\xb2\xe2\xca\xd4\xc0\xe0\xd0\xcd\xa3\xba\n\xcb\xb5\xc3\xf7\xa3\xba\n\xd0\xc5\xcf\xa2\xa3\xba\n\xce\xaa\xc2\xfa\xd7\xe3\xc6\xf3\xd2\xb5\xbb\xf2\xb8\xf6\xc8\xcb\xb6\xa8\xd6\xc6\xbb\xaf\xd0\xe8\xc7\xf3\xa3\xac\xce\xd2\xc3\xc7\xcc\xe1\xb9\xa9\xb2\xc4\xc1\xcf\xbf\xe2\xb6\xa8\xd6\xc6\xb7\xfe\xce\xf1\xa3\xac\xd2\xb2\xbd\xab\xcd\xc6\xb3\xf6\xb8\xfc\xb6\xe0\xc0\xa9\xb3\xe4\xa1\xa2\xd7\xa8\xd2\xb5\xb5\xc4\xb2\xc4\xc1\xcf\xbf\xe2\xa3\xac\xce\xaaABAQUS\xb7\xc2\xd5\xe6\xd0\xa7\xc2\xca\xcc\xe1\xb8\xdf\xb6\xf8\xc5\xac\xc1\xa6\xa1\xa3', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((190000000000.0, 0.29),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((8000.0,),), 'dependencies': 0}, 'name': 'SI_m111111_AISI304', 'plastic': {'temperatureDependency': OFF, 'strainRangeDependency': OFF, 'rate': OFF, 'dependencies': 0, 'hardening': ISOTROPIC, 'dataType': HALF_CYCLE, 'table': ((206807000.0, 0.0),), 'numBackstresses': 1}, 'expansion': {'temperatureDependency': OFF, 'userSubroutine': OFF, 'zero': 0.0, 'dependencies': 0, 'table': ((1.8e-05,),), 'type': ISOTROPIC}, 'conductivity': {'temperatureDependency': OFF, 'table': ((16.0,),), 'dependencies': 0, 'type': ISOTROPIC}}""")
    # #: Material 'SI_m111111_AISI304' has been copied to the current model.
    # from material import createMaterialFromDataString
    # createMaterialFromDataString('Model-1', 'SI_m111111_AISI1045Steel_colddrawn', 
    #     '6-10', 
    #     """{'specificHeat': {'temperatureDependency': OFF, 'table': ((486.0,),), 'dependencies': 0, 'law': CONSTANTVOLUME}, 'materialIdentifier': '', 'description': '\xb2\xc4\xc1\xcf\xbf\xe2\xc0\xb4\xd4\xb4: https://xcbjx.taobao.com/\n\xbb\xb6\xd3\xad\xbc\xd3\xc8\xebqq\xc8\xba : Abaqus \xbb\xb6\xc0\xd6\xb9\xb2\xbd\xf8\xc6\xbd\xcc\xa8 431603427\nAISI 1045 Steel, cold drawn[N_m_kg]\n\xb2\xe2\xca\xd4\xc0\xe0\xd0\xcd\xa3\xba\n\xcb\xb5\xc3\xf7\xa3\xba\n\xd0\xc5\xcf\xa2\xa3\xba\n\xce\xaa\xc2\xfa\xd7\xe3\xc6\xf3\xd2\xb5\xbb\xf2\xb8\xf6\xc8\xcb\xb6\xa8\xd6\xc6\xbb\xaf\xd0\xe8\xc7\xf3\xa3\xac\xce\xd2\xc3\xc7\xcc\xe1\xb9\xa9\xb2\xc4\xc1\xcf\xbf\xe2\xb6\xa8\xd6\xc6\xb7\xfe\xce\xf1\xa3\xac\xd2\xb2\xbd\xab\xcd\xc6\xb3\xf6\xb8\xfc\xb6\xe0\xc0\xa9\xb3\xe4\xa1\xa2\xd7\xa8\xd2\xb5\xb5\xc4\xb2\xc4\xc1\xcf\xbf\xe2\xa3\xac\xce\xaaABAQUS\xb7\xc2\xd5\xe6\xd0\xa7\xc2\xca\xcc\xe1\xb8\xdf\xb6\xf8\xc5\xac\xc1\xa6\xa1\xa3', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((205000000000.0, 0.29),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((7850.0,),), 'dependencies': 0}, 'name': 'SI_m111111_AISI1045Steel_colddrawn', 'plastic': {'temperatureDependency': OFF, 'strainRangeDependency': OFF, 'rate': OFF, 'dependencies': 0, 'hardening': ISOTROPIC, 'dataType': HALF_CYCLE, 'table': ((530000000.0, 0.0),), 'numBackstresses': 1}, 'expansion': {'temperatureDependency': OFF, 'userSubroutine': OFF, 'zero': 0.0, 'dependencies': 0, 'table': ((1.15e-05,),), 'type': ISOTROPIC}, 'conductivity': {'temperatureDependency': OFF, 'table': ((49.8,),), 'dependencies': 0, 'type': ISOTROPIC}}""")
    # #: Material 'SI_m111111_AISI1045Steel_colddrawn' has been copied to the current model.
    # from material import createMaterialFromDataString
    # createMaterialFromDataString('Model-1', 'SI_m111111_AISI1020', '6-10', 
    #     """{'specificHeat': {'temperatureDependency': OFF, 'table': ((420.0,),), 'dependencies': 0, 'law': CONSTANTVOLUME}, 'materialIdentifier': '', 'description': '\xb2\xc4\xc1\xcf\xbf\xe2\xc0\xb4\xd4\xb4: https://xcbjx.taobao.com/\n\xbb\xb6\xd3\xad\xbc\xd3\xc8\xebqq\xc8\xba : Abaqus \xbb\xb6\xc0\xd6\xb9\xb2\xbd\xf8\xc6\xbd\xcc\xa8 431603427\nAISI 1020[N_m_kg]\n\xb2\xe2\xca\xd4\xc0\xe0\xd0\xcd\xa3\xba\n\xcb\xb5\xc3\xf7\xa3\xba\n\xd0\xc5\xcf\xa2\xa3\xba\n\xce\xaa\xc2\xfa\xd7\xe3\xc6\xf3\xd2\xb5\xbb\xf2\xb8\xf6\xc8\xcb\xb6\xa8\xd6\xc6\xbb\xaf\xd0\xe8\xc7\xf3\xa3\xac\xce\xd2\xc3\xc7\xcc\xe1\xb9\xa9\xb2\xc4\xc1\xcf\xbf\xe2\xb6\xa8\xd6\xc6\xb7\xfe\xce\xf1\xa3\xac\xd2\xb2\xbd\xab\xcd\xc6\xb3\xf6\xb8\xfc\xb6\xe0\xc0\xa9\xb3\xe4\xa1\xa2\xd7\xa8\xd2\xb5\xb5\xc4\xb2\xc4\xc1\xcf\xbf\xe2\xa3\xac\xce\xaaABAQUS\xb7\xc2\xd5\xe6\xd0\xa7\xc2\xca\xcc\xe1\xb8\xdf\xb6\xf8\xc5\xac\xc1\xa6\xa1\xa3', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((200000000000.0, 0.29),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((7900.0,),), 'dependencies': 0}, 'name': 'SI_m111111_AISI1020', 'plastic': {'temperatureDependency': OFF, 'strainRangeDependency': OFF, 'rate': OFF, 'dependencies': 0, 'hardening': ISOTROPIC, 'dataType': HALF_CYCLE, 'table': ((351571000.0, 0.0),), 'numBackstresses': 1}, 'expansion': {'temperatureDependency': OFF, 'userSubroutine': OFF, 'zero': 0.0, 'dependencies': 0, 'table': ((1.5e-05,),), 'type': ISOTROPIC}, 'conductivity': {'temperatureDependency': OFF, 'table': ((47.0,),), 'dependencies': 0, 'type': ISOTROPIC}}""")
    # #: Material 'SI_m111111_AISI1020' has been copied to the current model.
    # from material import createMaterialFromDataString
    # createMaterialFromDataString('Model-1', 'SI_m111111_AISI1020Steel_ColdRolled', 
    #     '6-10', 
    #     """{'specificHeat': {'temperatureDependency': OFF, 'table': ((486.0,),), 'dependencies': 0, 'law': CONSTANTVOLUME}, 'materialIdentifier': '', 'description': '\xb2\xc4\xc1\xcf\xbf\xe2\xc0\xb4\xd4\xb4: https://xcbjx.taobao.com/\n\xbb\xb6\xd3\xad\xbc\xd3\xc8\xebqq\xc8\xba : Abaqus \xbb\xb6\xc0\xd6\xb9\xb2\xbd\xf8\xc6\xbd\xcc\xa8 431603427\nAISI 1020 Steel, Cold Rolled[N_m_kg]\n\xb2\xe2\xca\xd4\xc0\xe0\xd0\xcd\xa3\xba\n\xcb\xb5\xc3\xf7\xa3\xba\n\xd0\xc5\xcf\xa2\xa3\xba\n\xce\xaa\xc2\xfa\xd7\xe3\xc6\xf3\xd2\xb5\xbb\xf2\xb8\xf6\xc8\xcb\xb6\xa8\xd6\xc6\xbb\xaf\xd0\xe8\xc7\xf3\xa3\xac\xce\xd2\xc3\xc7\xcc\xe1\xb9\xa9\xb2\xc4\xc1\xcf\xbf\xe2\xb6\xa8\xd6\xc6\xb7\xfe\xce\xf1\xa3\xac\xd2\xb2\xbd\xab\xcd\xc6\xb3\xf6\xb8\xfc\xb6\xe0\xc0\xa9\xb3\xe4\xa1\xa2\xd7\xa8\xd2\xb5\xb5\xc4\xb2\xc4\xc1\xcf\xbf\xe2\xa3\xac\xce\xaaABAQUS\xb7\xc2\xd5\xe6\xd0\xa7\xc2\xca\xcc\xe1\xb8\xdf\xb6\xf8\xc5\xac\xc1\xa6\xa1\xa3', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((205000000000.0, 0.29),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((7870.0,),), 'dependencies': 0}, 'name': 'SI_m111111_AISI1020Steel_ColdRolled', 'plastic': {'temperatureDependency': OFF, 'strainRangeDependency': OFF, 'rate': OFF, 'dependencies': 0, 'hardening': ISOTROPIC, 'dataType': HALF_CYCLE, 'table': ((350000000.0, 0.0),), 'numBackstresses': 1}, 'expansion': {'temperatureDependency': OFF, 'userSubroutine': OFF, 'zero': 0.0, 'dependencies': 0, 'table': ((1.17e-05,),), 'type': ISOTROPIC}, 'conductivity': {'temperatureDependency': OFF, 'table': ((51.9,),), 'dependencies': 0, 'type': ISOTROPIC}}""")
    # #: Material 'SI_m111111_AISI1020Steel_ColdRolled' has been copied to the current model.