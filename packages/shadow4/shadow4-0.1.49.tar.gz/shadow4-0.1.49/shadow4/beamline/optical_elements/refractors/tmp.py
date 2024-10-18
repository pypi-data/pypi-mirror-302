from shadow4.beamline.s4_beamline import S4Beamline

beamline = S4Beamline()

# electron beam
from shadow4.sources.s4_electron_beam import S4ElectronBeam

electron_beam = S4ElectronBeam(energy_in_GeV=6, energy_spread=0.00145, current=0.2)
electron_beam.set_sigmas_all(sigma_x=1.29e-05, sigma_y=8.7e-06, sigma_xp=2.5e-06, sigma_yp=3.6e-06)

# magnetic structure
from shadow4.sources.undulator.s4_undulator import S4Undulator

source = S4Undulator(
    K_vertical=1.191085,  # syned Undulator parameter
    period_length=0.025,  # syned Undulator parameter
    number_of_periods=94.0,  # syned Undulator parameter
    emin=7999.998647331844,  # Photon energy scan from energy (in eV)
    emax=7999.998647331844,  # Photon energy scan to energy (in eV)
    ng_e=1,  # Photon energy scan number of points
    maxangle=1.6810267595895065e-05,  # Maximum radiation semiaperture in RADIANS
    ng_t=100,  # Number of points in angle theta
    ng_p=11,  # Number of points in angle phi
    ng_j=20,  # Number of points in electron trajectory (per period) for internal calculation only
    code_undul_phot='srw',  # internal, pysru, srw
    flag_emittance=1,  # when sampling rays: Use emittance (0=No, 1=Yes)
    flag_size=2,  # when sampling rays: 0=point,1=Gaussian,2=FT(Divergences)
    distance=30.0,  # distance to far field plane
    srw_range=0.2,  # for SRW backpropagation, the range factor
    srw_resolution=50,  # for SRW backpropagation, the resolution factor
    srw_semianalytical=0,  # for SRW backpropagation, use semianalytical treatement of phase
    magnification=0.05,  # for internal/wofry backpropagation, the magnification factor
    flag_backprop_recalculate_source=0,
    # for internal or pysru/wofry backpropagation: source reused (0) or recalculated (1)
    flag_backprop_weight=0,  # for internal or pysru/wofry backpropagation: apply Gaussian weight to amplitudes
    weight_ratio=0.5,  # for flag_backprop_recalculate_source=1, the ratio value sigma/window halfwidth
    flag_energy_spread=0,  # for monochromatod sources, apply (1) or not (0) electron energy spread correction
)

# light source
from shadow4.sources.undulator.s4_undulator_light_source import S4UndulatorLightSource

light_source = S4UndulatorLightSource(name='undulator', electron_beam=electron_beam, magnetic_structure=source,
                                      nrays=5000, seed=5676561)
beam = light_source.get_beam()

beamline.set_light_source(light_source)

# optical element number XX
from syned.beamline.shape import Rectangle

boundary_shape = Rectangle(x_left=-5e-05, x_right=5e-05, y_bottom=-5e-05, y_top=5e-05)

from shadow4.beamline.optical_elements.absorbers.s4_screen import S4Screen

optical_element = S4Screen(name='Generic Beam Screen/Slit/Stopper/Attenuator', boundary_shape=boundary_shape,
                           i_abs=0,  # 0=No, 1=prerefl file_abs, 2=xraylib, 3=dabax
                           i_stop=0, thick=0, file_abs='<specify file name>', material='Au', density=19.3)

from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=51.824, q=0, angle_radial=0, angle_azimuthal=0, angle_radial_out=3.141592654)
from shadow4.beamline.optical_elements.absorbers.s4_screen import S4ScreenElement

beamline_element = S4ScreenElement(optical_element=optical_element, coordinates=coordinates, input_beam=beam)

beam, footprint = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# optical element number XX
boundary_shape = None
from shadow4.beamline.optical_elements.refractors.s4_crl import S4CRL

optical_element = S4CRL(name='Compound Refractive Lens',
                        n_lens=0,
                        piling_thickness=0.0025,  # syned stuff
                        boundary_shape=boundary_shape,  # syned stuff, replaces "diameter" in the shadow3 append_lens
                        material='Be',  # the material for ri_calculation_mode > 1
                        density=1.484,  # the density for ri_calculation_mode > 1
                        thickness=2.9999999999999997e-05,
                        # syned stuff, lens thickness [m] (distance between the two interfaces at the center of the lenses)
                        surface_shape=2,  # now: 0=plane, 1=sphere, 2=parabola, 3=conic coefficients
                        # (in shadow3: 1=sphere 4=paraboloid, 5=plane)
                        convex_to_the_beam=0,
                        # for surface_shape: convexity of the first interface exposed to the beam 0=No, 1=Yes
                        cylinder_angle=0,  # for surface_shape: 0=not cylindricaL, 1=meridional 2=sagittal
                        ri_calculation_mode=0,  # source of refraction indices and absorption coefficients
                        # 0=User, 1=prerefl file, 2=xraylib, 3=dabax
                        prerefl_file='<none>',
                        # for ri_calculation_mode=0: file name (from prerefl) to get the refraction index.
                        refraction_index=1,  # for ri_calculation_mode=1: n (real)
                        attenuation_coefficient=0,  # for ri_calculation_mode=1: mu in cm^-1 (real)
                        dabax=None,  # the pointer to dabax library
                        radius=0.0001,
                        # for surface_shape=(1,2): lens radius [m] (for spherical, or radius at the tip for paraboloid)
                        conic_coefficients1=None,
                        # for surface_shape = 3: the conic coefficients of the single lens interface 1
                        conic_coefficients2=None,
                        # for surface_shape = 3: the conic coefficients of the single lens interface 2
                        )

import numpy
from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=1, q=1, angle_radial=0, angle_azimuthal=0, angle_radial_out=3.141592654)
movements = None
from shadow4.beamline.optical_elements.refractors.s4_crl import S4CRLElement

beamline_element = S4CRLElement(optical_element=optical_element, coordinates=coordinates, movements=movements,
                                input_beam=beam)

beam, mirr = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# test plot
if True:
    from srxraylib.plot.gol import plot_scatter

    plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)',
                 plot_histograms=0)
    plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')