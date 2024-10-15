import pytest
import moapy.wgsd.wgsd_flow as wgsd_3dpm
from moapy.data_pre import Lcb, Lcoms, Lcom, Force, PMOptions, MemberForce, Moment, enUnitForce, enUnitMoment
from moapy.rc_pre import Material, Geometry

def test_3dpm_conc_rebar():
    material = Material()
    geom = Geometry()
    lcb = Lcb
    lcb.uls = Lcoms(lcoms=[Lcom(name="uls1", f=MemberForce(Fz=Force(value=100.0, unit=enUnitForce.N),
                                                           Mx=Moment(value=10.0, unit=enUnitMoment.Nmm),
                                                           My=Moment(value=50.0, unit=enUnitMoment.Nmm))),
                           Lcom(name="uls2", f=MemberForce(Fz=Force(value=100.0, unit=enUnitForce.N),
                                                           Mx=Moment(value=15.0, unit=enUnitMoment.Nmm),
                                                           My=Moment(value=50.0, unit=enUnitMoment.Nmm))),
                           Lcom(name="uls3", f=MemberForce(Fz=Force(value=100.0, unit=enUnitForce.N),
                                                           Mx=Moment(value=0.0, unit=enUnitMoment.Nmm),
                                                           My=Moment(value=0.0, unit=enUnitMoment.Nmm))),
                           Lcom(name="uls4", f=MemberForce(Fz=Force(value=-100.0, unit=enUnitForce.N),
                                                           Mx=Moment(value=0.0, unit=enUnitMoment.Nmm),
                                                           My=Moment(value=0.0, unit=enUnitMoment.Nmm)))])
    opt = PMOptions()
    res = wgsd_3dpm.calc_3dpm(material, geom, lcb, opt)
    assert pytest.approx(res.strength[0].name) == 'uls1'
    assert pytest.approx(res.strength[0].f.Mx.value) == 495152.21186695714
    assert pytest.approx(res.strength[0].f.My.value) == 2475761.0593347857
    assert pytest.approx(res.strength[0].f.Fz.value) == 4951522.118669571
    assert pytest.approx(res.strength[1].name) == 'uls2'
    assert pytest.approx(res.strength[1].f.Mx.value) == 742728.3178004358
    assert pytest.approx(res.strength[1].f.My.value) == 2475761.0593347857
    assert pytest.approx(res.strength[1].f.Fz.value) == 4951522.118669571
    assert pytest.approx(res.strength[2].name) == 'uls3'
    assert pytest.approx(res.strength[2].f.Mx.value) == 0.0
    assert pytest.approx(res.strength[2].f.My.value) == 0.0
    assert pytest.approx(res.strength[2].f.Fz.value) == 4951522.118669571
    assert pytest.approx(res.strength[3].name) == 'uls4'
    assert pytest.approx(res.strength[3].f.Mx.value) == 0.0
    assert pytest.approx(res.strength[3].f.My.value) == 0.0
    assert pytest.approx(res.strength[3].f.Fz.value) == -574000.0435605047

# res = test_3dpm_conc_tendon(1250)
# m_x_values = [item[0] for item in res]
# m_y_values = [item[1] for item in res]
# d_n_values = [item[2] for item in res]

# # Combine m_x and m_y into a single array of points
# points = np.column_stack((m_x_values, m_y_values, d_n_values))

# hull = ConvexHull(points)

# # Create the 3D plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plot the convex hull
# vertices = [points[simplex] for simplex in hull.simplices]
# poly3d = Poly3DCollection(vertices, color='cyan', alpha=0.8)
# ax.add_collection3d(poly3d)

# # 새로운 데이터 셋의 Convex Hull 플롯

# # Plot the original points
# ax.scatter(m_x_values, m_y_values, d_n_values, color='green', label='Dataset 2')

# # Set labels
# ax.set_xlabel('m_x')
# ax.set_ylabel('m_y')
# ax.set_zlabel('d_n')
# ax.set_title('3D PM Interacetion')

# # Show the plot
# plt.show()