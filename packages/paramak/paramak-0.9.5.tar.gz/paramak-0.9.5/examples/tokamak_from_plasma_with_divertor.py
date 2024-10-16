
from example_util_functions import transport_particles_on_h5m_geometry
from paramak.utils import create_wire_workplane_from_points
import paramak
from cadquery import vis, Workplane

# makes a rectangle that overlaps the lower blanket under the plasma
# the intersection of this and the layers will form the lower divertor
points = [(300, -700), (300, 0), (400, 0), (400, -700)]
divertor_lower = Workplane('XZ', origin=(0,0,0)).polyline(points).close().revolve(180)


my_reactor = paramak.tokamak_from_plasma(
    radial_build=[
        (paramak.LayerType.GAP, 10),
        (paramak.LayerType.SOLID, 30),
        (paramak.LayerType.SOLID, 50),
        (paramak.LayerType.SOLID, 10),
        (paramak.LayerType.SOLID, 120),
        (paramak.LayerType.SOLID, 20),
        (paramak.LayerType.GAP, 60),
        (paramak.LayerType.PLASMA, 300),
        (paramak.LayerType.GAP, 60),
        (paramak.LayerType.SOLID, 20),
        (paramak.LayerType.SOLID, 120),
        (paramak.LayerType.SOLID, 10),
    ],
    elongation=2,
    triangularity=0.55,
    rotation_angle=180,
    extra_intersect_shapes=[divertor_lower]
)
my_reactor.save(f"tokamak_with_divertor.step")
print(f"Saved as tokamak_with_divertor.step")
# vis.show(my_reactor)

# from cad_to_dagmc import CadToDagmc
# my_model = CadToDagmc()
# material_tags = ["mat1"] * 6  # as inner and outer layers are one solid there are only 6 solids in model
# my_model.add_cadquery_object(cadquery_object=my_reactor, material_tags=material_tags)
# my_model.export_dagmc_h5m_file(min_mesh_size=3.0, max_mesh_size=20.0)

# h5m_filename = "dagmc.h5m"
# flux = transport_particles_on_h5m_geometry(
#     h5m_filename=h5m_filename,
#     material_tags=material_tags,
#     nuclides=["H1"] * len(material_tags),
#     cross_sections_xml="tests/cross_sections.xml",
# )
# assert flux > 0.0
