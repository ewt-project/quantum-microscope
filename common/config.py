# Configuration

#------------------------------------------------------------------------------------------------------
# CONFIGURATION FILE
# Configurable variables are stored here.
# First section includes the variables that are available in the Blender UI panel to be controlled by the user. Should not be modified in this file.
# Second section includes variables for this program that may only be set in this file, including some Blender settings. May be modified in this file.
#------------------------------------------------------------------------------------------------------

import bpy

############################################ CONFIG VARIABLES CONTROLLED IN THE BLENDER UI #####################################################

# PHASE 1 CONTROLS:
if 'wave_centers' not in locals():
    wave_centers = 1                               # The number of neutrinos (wave centers) to display
if 'anti_wave_centers' not in locals():
    anti_wave_centers = 0                          # The number of antineutrinos to display
if 'wave_amplitude' not in locals():
    wave_amplitude = 5                             # The displacement distance of granules (amplitude)
if 'wave_speed' not in locals():
    wave_speed = 0.2                               # The wave speed of the wave through space
if 'show_neutrino_motion' not in locals():
    show_neutrino_motion = False                   # Show a neutrino in motion, moving to minimize wave amplitude
if 'show_granules' not in locals():
    show_granules = True                           # Show detailed granules if True, else show waves
if 'longitudinal_wave' not in locals():
    longitudinal_wave = True                       # Show a longitudinal wave
if 'transverse_wave' not in locals():
    transverse_wave = False                        # Show a transverse wave
if 'spacetime_length' not in locals():
    spacetime_length = 10                          # The length of the spacetime array that is shown and simulated
if 'dimensions' not in locals():
    dimensions = 2                                 # The number of dimensions of the spacetime universe that is shown and simulated

# PHASE 2 CONTROLS:
if 'neutrinos' not in locals():
    neutrinos = 1                                  # The total number of neutrinos

# PHASE 3 CONTROLS:
if 'electrons' not in locals():
    electrons = 1                                   # The total number of electrons; Notice that more than 4 electrons not stable
if 'positrons' not in locals():
    positrons = 1                                   # The total number of positrons
if 'particle_accelerator' not in locals():
    particle_accelerator = True                     # If true, a particle accelerator is added to simulation.  See config below for disabling.
if 'accelerator_force' not in locals():
    accelerator_force = 1000                        # Energy (force) of particle to collide with proton. See comments for expected results and forces to set.

# PHASE 4 CONTROLS:
if 'protons' not in locals():
    protons = 1                                     # The total number of protons (Note: Electrons already set above)
if 'neutrons' not in locals():
    neutrons = 1                                    # The total number of neutrons
if 'show_electron_cloud' not in locals():
    show_electron_cloud = False                     # If true, the electron cloud will be shown in the atom view

# PHASE 5 CONTROLS:
if 'hydrogen_atoms' not in locals():
    hydrogen_atoms = 1                              # The total number of hydrogen atoms

# SIMULATION CONFIGURATION
if 'spin' not in locals():
    spin = True                                     # If true, add spin to simulation. No spin if false.
if 'external_force' not in locals():
    external_force = True                           # If true, an external force is added to simulation.  See config below for disabling.
if 'ext_force_strength' not in locals():
    ext_force_strength = 100                        # Strength of a force that is applied to particles from external source. Reduces at inverse square. Keep around 100-500 for most phases except ph 5.
if 'show_calculations' not in locals():
    show_calculations = True                        # If true, the calculations for particle radius and energy are shown.
if 'show_forces' not in locals():
    show_forces = True                              # If true, forces that are visual in Blender will be shown
if 'num_frames' not in locals():
    num_frames = 1000                               # The total number of frames for the simulation to run


############################################ CONFIGS ADJUSTABLE HERE IN THE FILE ONLY #####################################################

# MATH CONFIGS
pi = 3.1416
fundamental_wavelength = 2.818e-17                  # The fundamental longitudinal wavelength * elec orbital g-factor applied (meters) from https://energywavetheory.com/equations
fundamental_wavelength_no_gfactor = 2.854e-17       # The fundamental longitudinal wavelength without electron orbital g-factor applied (meters) from https://energywavetheory.com/equations
fundamental_amplitude = 9.215e-19                   # The fundamental longitudinal amplitude with electron spin g-factor applied (meters) from https://energywavetheory.com/equations
fundamental_wavespeed = 2.998e+8                    # The fundamental wave speed, which is the speed of light (meters per second) from https://energywavetheory.com/equations
fundamental_density = 3.860e+22                     # The fundamental density (kg/m^3) from https://energywavetheory.com/equations
fundamental_energy = 2.389                          # The fundamental energy in electron-volts (eV) from https://energywavetheory.com/subatomic-particles/calculations-particles/
fine_structure = 7.2974e-3                          # The fine structure constant from CODATA values
electron_radius = 2.818e-15                         # The electron classical radius from CODATA values and also Phase 2
electron_energy = 8.187e-14                         # The electron energy from CODATA values
bohr_radius = 5.292e-11                             # The Bohr radius (hydrogen ground state) from CODATA values
elementary_charge = 1.602e-19                       # The elementary charge from CODATA values
coulomb_constant = 8.988e9                          # Coulomb's constant from CODATA values

# DISTANCES                                             # Distances are recalibrated as phases progress.  See phase specific settings which override.
neutrino_core_radius = 0.5                              # The neutrino core distance radius for the simulation, such that the diameter is 1.
electron_core_radius = neutrino_core_radius * 10        # The electron core distance radius, derived at 10 wave centers.
hydrogen_radius = 100                                   # The radius of hydrogen for the simulation
emitter_radius = 100                                    # Default size of sphere emitting particles. The default is often overridden depending on its use for particle emission.

# CHARGES
neutrino_charge = 2                                     # The neutrino core charge for the simulation.
electron_charge = neutrino_charge * 10                  # The electron core charge
particle_charge = neutrino_charge * neutrinos           # The core for any particle is a function of wave centers due to constructive interference.
flow = 10                                               # Slows down particle movement to settle faster (0-10; where 10 slows quickly)

# WAVES
neutrino_wavelength = neutrino_core_radius * 4          # Neutrino wavelength (fundamental wavelength)
num_waves = neutrinos                                   # Total number of standing waves
wavelength = neutrinos * neutrino_wavelength            # Particle wavelength of standing waves at particle core
core_strength = particle_charge * 2                     # Harmonic force strength of first sphere at core

# FORCES
particle_force = 1000                                   # Force positron to center. Required in Blender.
particle_strong_force = 1/fine_structure                # The Lennard Jones force used for the strong force. In Blender, not related to charge but a nod to the fine structure constant.
particle_nuclear_force = particle_strong_force * 1/4    # Nuclear force should be less than strong force due to greater distance to node
orbital_force = hydrogen_radius * electron_charge       # The orbital force that repels electrons in an atom

# STANDING WAVE GRID CONFIGURATION
grid_spacing = wavelength / 2                           # Spacing distance between each node (each node is at half wavelength)
grid_strength = neutrinos * 2                           # Charge strength of force at each grid point
grid_size = int((-(-(neutrinos*2) ** (1/3)//1)))        # Total number of standing wave nodes in a row of a grid based on number of wave centers

# SPIN CONFIGURATION
spin_frequency = 200                                    # The number of simulation frames to complete a rotation
spin_strength = 5                                       # The strength of the vortex spin of the proton

# EXTERNAL FORCE CONFIGURATION
ext_force_radius = 500                                  # Size of sphere applying external force.  Should be larger that the emitter to be "external".
ext_force_startframe = 1                                # Starting frame where force is turned on.  Set to 1 if the beginning.
ext_force_endframe = 20                                 # Ending frame where force is turned off.  Set to num_frames if the entire time, or number to end.

# PARTICLE ACCELERATOR CONFIGURATION
accelerator_startframe = 50                             # The frame number when the particle is released from the particle accelerator

# SIMULATION COLORS
neutrino_color = (0.5, 0.6, 0.8, 1)                     # Color of wave center (neutrino) in simulation in (R, G, B, A) values
antineutrino_color = (0.8, 0.3, 0.6, 1)                 # Color of opposite phase wave center (antineutrino) in simulation in (R, G, B, A) values
electron_color = (0.0, 0.0, 0.6, 1)                     # Color of electron particle in simulation in (R, G, B, A) values
positron_color = (0.8, 0.2, 0.3, 1)                     # Color of positron particle in simulation in (R, G, B, A) values
proton_color = (1, 0.0, 0.0, 1)                         # Color of proton particle displayed as Particle Shell when unhidden in (R, G, B, A) values
neutron_color = (0.0, 0.0, 0.0, 1)                      # Color of neutron particle displayed as Particle Shell when unhidden in (R, G, B, A) values accelerator_color = (0.0, 0.0, 0.05, 1)                 # Color of accelerator and its particle in (R, G, B, A) values
hydrogen_color = (1, 1, 1, 1)                           # Color of hydrogen atom displayed as Particle Shell when unhidden in (R, G, B, A) values
helium_color = (.83, 1, 1, 1)                           # Color of helium atom displayed as Particle Shell when unhidden in (R, G, B, A) values
accelerator_color = (0.0, 0.0, 0.05, 1)                 # Color of accelerator and its particle in (R, G, B, A) values

# PROJECT
project_text = "~EWT Project"                           # Hidden text in simulator that describes the project and phase

########################################################## BLENDER CONFIGS ################################################################

bpy.context.scene.use_gravity = False                   # Turn off gravity
bpy.context.scene.frame_end = num_frames                # Set the total number of frames for the simulation
for a in bpy.context.screen.areas:
    if a.type == 'VIEW_3D':
        for s in a.spaces:
            if s.type == 'VIEW_3D':
                s.clip_end = 20000                      # Set the zooming factor
