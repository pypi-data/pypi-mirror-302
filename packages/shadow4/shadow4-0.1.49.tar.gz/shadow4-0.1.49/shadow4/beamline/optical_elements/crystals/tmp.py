from shadow4.beamline.s4_beamline import S4Beamline

beamline = S4Beamline()

#
#
#
from shadow4.sources.source_geometrical.source_geometrical import SourceGeometrical
light_source = SourceGeometrical(name='SourceGeometrical', nrays=25000, seed=5676561)
light_source.set_spatial_type_gaussian(sigma_h=0.0,sigma_v=0.000382)
light_source.set_depth_distribution_off()
light_source.set_angular_distribution_gaussian(sigdix=0.000000,sigdiz=0.000000)
light_source.set_energy_distribution_gaussian(center=6457.520486, sigma=0.274800, unit='eV')
light_source.set_polarization(polarization_degree=1.000000, phase_diff=0.000000, coherent_beam=0)
beam = light_source.get_beam()


# print(">>> source Ep", beam.get_columns([16,17,18]))

beamline.set_light_source(light_source)

# optical element number XX
from shadow4.beamline.optical_elements.crystals.s4_plane_crystal import S4PlaneCrystal
optical_element = S4PlaneCrystal(name='Plane Crystal',
    boundary_shape=None, material='Si',
    miller_index_h=4, miller_index_k=0, miller_index_l=0,
    f_bragg_a=False, asymmetry_angle=0.0,
    is_thick=1, thickness=0.001,
    f_central=1, f_phot_cent=0, phot_cent=6457.52048581758,
    file_refl='/home/srio/Oasys/Si(400)_6450_6470.dat',
    f_ext=0,
    material_constants_library_flag=2, # 0=xraylib,1=dabax,2=preprocessor v1,3=preprocessor v2
    )
from syned.beamline.element_coordinates import ElementCoordinates
coordinates = ElementCoordinates(p=974, q=0.005657, angle_radial=0.785398164, angle_azimuthal=0, angle_radial_out=0.785398164)
movements = None
from shadow4.beamline.optical_elements.crystals.s4_plane_crystal import S4PlaneCrystalElement
beamline_element = S4PlaneCrystalElement(optical_element=optical_element,coordinates=coordinates, movements=movements, input_beam=beam)

beam, mirr = beamline_element.trace_beam()
print("Beam intensity after xtal 1", beam.intensity(nolost=1))

beamline.append_beamline_element(beamline_element)

# optical element number XX
from shadow4.beamline.optical_elements.crystals.s4_plane_crystal import S4PlaneCrystal
optical_element = S4PlaneCrystal(name='Plane Crystal',
    boundary_shape=None, material='Si',
    miller_index_h=4, miller_index_k=0, miller_index_l=0,
    f_bragg_a=False, asymmetry_angle=0.0,
    is_thick=1, thickness=0.001,
    f_central=1, f_phot_cent=0, phot_cent=6457.52048581758,
    file_refl='/home/srio/Oasys/Si(400)_6450_6470.dat',
    f_ext=0,
    material_constants_library_flag=2, # 0=xraylib,1=dabax,2=preprocessor v1,3=preprocessor v2
    method_efields_management=1,
    )
from syned.beamline.element_coordinates import ElementCoordinates
coordinates = ElementCoordinates(p=1, q=0.005657, angle_radial=0.7853981634, angle_azimuthal=1.570796327, angle_radial_out=0.7853981634)
movements = None
from shadow4.beamline.optical_elements.crystals.s4_plane_crystal import S4PlaneCrystalElement
beamline_element = S4PlaneCrystalElement(optical_element=optical_element,coordinates=coordinates, movements=movements, input_beam=beam)

beam, mirr = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)


print("Beam intensity after xtal 2", beam.intensity(nolost=1))
# test plot
if 0:
   from srxraylib.plot.gol import plot_scatter
   plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)', plot_histograms=0)
   plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')