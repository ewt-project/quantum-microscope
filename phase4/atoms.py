# Phase 4 - Atoms

# COMMENTS:
# This phase combines nucelons (protons and neutrons) merging together to form the core of an atom, then attracting electrons in orbitals.
# Electrons are contained in orbitals due to attractive and repelling forces decreasing by the inverse square and cube respectively.
# This simulation is not to scale in terms of particle size relative to distance between particles (so that atoms can be viewed).
# An electron cloud option has been added which simulates electrons in various positions in the atom to show its probability cloud.
# Orbitals are isolated to Blender effector groups so that attractive and repulsive forces can be simulated (required because nucleus is not forming correctly)
# Ionization energy is calculated using Coulomb's Law for energy by determining the constructive wave interference on an electron from all particles, and its distance
# TODO: The core issue to be resolved is the structure of the nucleus.  Once resolved, many of these TODO items are automatically fixed.
# TODO: Nucleons should arrange at standing wave nodes, similar to particles.  Thus, this development is dependent on Phase 2.
# TODO: The repelling force uses a Blender "Wind" force to simulate the axial, magnetic force.  This needs to be improved.
# TODO: The orbital distances for all atoms (up to calcium) can be calculated if simulataneous equation solving is possible in Blender/Python
# TODO: Effector groups should be replaced with the true physics of each and every electron affecting each other - in all orbitals.
# TODO: The electron ionization energies may be improved when electron positions are simulated and a more accurate method of wave interference is established.
# TODO: The nucleus only supports up to calcium (Z=20) because of above, and also because the nucleus is unstable at large numbers of Z
# TODO: The shapes of orbitals will depend on alignment of spin and the magnetic forces when the nucleus forms correctly.
# For more details, visit www.energywavetheory.com/atoms

#------------------------------------------------------------------------------------------------------
# STANDARD CONFIGURATION
# Imports, configs and reset of the simulation
#------------------------------------------------------------------------------------------------------

import bpy
import sys
import os
import importlib
import math

# Import Config Variables & Common Functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from common import config
importlib.reload(config)
from common import functions
importlib.reload(functions)
from common import data
importlib.reload(data)


#------------------------------------------------------------------------------------------------------
# Main function for atoms
# protons: the count of protons for the simulation
# neutrons: the count of neutrons for the simulation
# electrons: the count of electrons for the simulation
# show_electron_cloud (optional): if True, electrons are simulated at different positions to illustrate their probability cloud
#------------------------------------------------------------------------------------------------------

def main(protons, neutrons, electrons, show_electron_cloud=False):

    #------------------------------------------------------------------------------------------------------
    # CONFIGS - USER VARIABLES SET IN THE UI
    # Variables from the Blender Panel
    #------------------------------------------------------------------------------------------------------

    config.protons = protons
    config.neutrons = neutrons
    config.electrons = electrons
    config.show_electron_cloud = show_electron_cloud

    #------------------------------------------------------------------------------------------------------
    # PHASE CONFIGURATION
    # Modifications specfic to this phase
    #------------------------------------------------------------------------------------------------------

    # Set everything to the electron for this phase to create protons (see phase 3)
    config.neutrinos = 10
    config.num_waves = 10

    # Scaling for visibility.  Electron core diameter is now 1m and a full electron is 10m. Proton radius should be around 1.54m at this size.
    phase_scale_factor = 1 / 40
    config.electron_core_radius = config.electron_core_radius * phase_scale_factor
    config.wavelength = config.electron_core_radius * 4

    # Nucleus
    proton_radius = config.wavelength * config.num_waves / 3.25       # Scale the proton radius based on electron size
    config.spin_frequency = 20                                        # Faster frequency to affect orbitals
    config.spin_strength = 1
    config.flow = 10

    # Orbital force exceptions for hydrogen and helium.
    if config.protons == 1:
        config.orbital_force = config.orbital_force * 0.15            # Hydrogen simulation uses an axial force and is simulated differently to illustrate probability
    if config.protons == 2:
        config.orbital_force = config.orbital_force * 0.75            # Beginning with helium, orbital force is simulated as spherical... helium needs a modification

    # Disable calculations when showing the electron cloud
    if config.show_electron_cloud:
        config.show_calculations = False


    ############################################ PROGRAM #####################################################

    text = config.project_text + ": Phase 4 - Atoms"
    functions.add_text(name=text, text=text, location=(-1000, 1000, 0), radius=50)
    bpy.data.objects[text].hide_set(True)


    #------------------------------------------------------------------------------------------------------
    # COLLECTIONS
    # Collections are used to organize objects in Blender.
    # The default collection and nucleus are set here.  Orbital collections are dynamic and set in the next section.
    #------------------------------------------------------------------------------------------------------

    context = bpy.context
    scene = context.scene
    nucleus_collection = bpy.data.collections.new('Nucleus')
    bpy.context.scene.collection.children.link(nucleus_collection)
    default_collection = context.scene.collection


    #------------------------------------------------------------------------------------------------------
    # CALCULATIONS OF ORBITALS AND ELECTRON EMITTER
    # Calculations used in this section for orbital distances are a ratio of the Bohr radius, requiring
    # solving simulataneous equations.  Mathcad was used, not Blender.  The table is here: https://energywavetheory.com/atoms/calculations-atoms/
    # Energy calculations are shown for the ionized electron. It uses amplitude factors from https://energywavetheory.com/atoms/calculations-amplitude-factors/
    # This emitter generates free electrons that will be subject to an attractive force and repelling force of the nucleus to remain in an orbital.
    # TODO: If Blender/Python can support simultaneous equation solvers, the equations can be imported here. Instead, they use a data file.
    # TODO: Nucleus forces on electrons in orbitals is placed here as temporary workaround until nucleus forces are completed.
    # TODO: Each electron needs to affect other electrons to determine placement of electrons.  Distances should be nearly accurate, but not placement.
    #------------------------------------------------------------------------------------------------------

    # Check to make sure the current atom array in the data file supports the atomic configuration (num of protons)
    if config.protons >= len(data.atoms):
        # reset protons to hydrogen if not supported by simulation
        config.protons = 1

    # Determine what type of atom (ionized, neutral or not a suported atom)
    if config.electrons == config.protons:           # Neutral atom
        atom_name = data.atoms[config.protons]
        orbital_ratio = data.neutral_atom
        amplitude_ratio = data.amp_neutral
    elif config.electrons < config.protons:          # Ionized atom
        ions = config.protons - config.electrons
        atom_name = data.atoms[config.protons] + str(ions) + "+"
        orbital_ratio, amplitude_ratio, atom_name = data.get_orbital_array(config.electrons, atom_name)
    else:                                            # Unsupported atom (there are more electrons than protons)
        orbital_ratio = data.neutral_atom
        amplitude_ratio = data.amp_neutral
        atom_name = "Atom not supported"

    # Loop through each orbital, calculating the distance and adding an electron emitter.
    orbital_text = ""
    energy_text = ""
    e = config.electrons

    i=1
    while i <= len(orbital_ratio):
        orbital = orbital_ratio[i-1][config.protons] * config.hydrogen_radius       # The calculated distance scaled for the simulation
        orbital_calc = orbital_ratio[i-1][config.protons] * config.bohr_radius      # The calculated orbital distance relative to the Bohr radius
        orbital_name = orbital_ratio[i-1][0]
        orbital_text = orbital_name + ": " + f"{orbital_calc:.2e}" + " (m)"
        energy_constants = (1/2) * config.coulomb_constant * config.elementary_charge ** 2      # Orbital energy is based on Coulomb's law - these are constant applied to next line.
        if orbital_calc != 0:
            energy_calc = energy_constants * amplitude_ratio[i-1][config.protons] / orbital_calc    # Energy constants multiplied by constructive wave interference / divide radius
            if energy_calc != 0:
                energy_text = ";  E: ~" + f"{energy_calc:.2e}" + " (J)"

        # Ensure that the right number of electrons are emitted for each shell following the electron sequence for shells: s, p, d, f
        shell_max = data.electron_sequence[i-1]
        if e > shell_max:
            valence_count = electron_count = shell_max
            e = e - shell_max
        elif e == shell_max:
            valence_count = electron_count = shell_max
            e = e - shell_max
            orbital_text = orbital_text + energy_text                                # Only show energy of orbital electron that is ionized
        else:
            valence_count = electron_count = e
            orbital_text = orbital_text + energy_text                                # Only show energy of orbital electron that is ionized
            e = 0

        # Orbitals - Show the calculation and generate electrons at each orbital
        if orbital != 0:

            # Add a collection for the orbital to organize
            orbital_collection = bpy.data.collections.new('Orbital - ' + orbital_name)
            bpy.context.scene.collection.children.link(orbital_collection)

            # Add a visual circle displaying the orbital if show_calculations is True
            if config.show_calculations:
                bpy.ops.mesh.primitive_circle_add(radius=orbital, enter_editmode=False, location=(0, 0, 0))
                bpy.context.active_object.name = orbital_name + " - Orbital"
                functions.link_collection(collection=orbital_collection)
                functions.add_text(name=orbital_name, text=orbital_text, location=(orbital, i*5, 0), radius=5 )
                functions.link_collection(collection=orbital_collection)

            # If displaying an electron cloud, disable electrons affecting themselves and set count higher to simulate the electron's probable positions.
            if config.show_electron_cloud:
                self_effect = False
                electron_count = config.num_frames / 10 * (int(orbital_name[:1])**2)        # Start with a smaller number of electrons near the core and increase with each shell for visibilty
                if config.protons == 1:                                                     # ...except hydrogen
                    electron_count = config.num_frames
            else:
                self_effect = True

            # Add the electron particle emitter at each orbital
            pset = functions.add_emitter(name=orbital_name + " - Emitter",
                particle_type = "electron",
                color = config.electron_color,
                radius = orbital,
                count = electron_count,
                self_effect = True,
                core_only = False)
            pset.force_field_1.flow = config.flow
            pset.emit_from = 'FACE'
            pset.use_emit_random = False

            # Rotate the p emitter. TODO: electrons from s shell should repel electrons in p shell instead of manual rotation; see note about use of effector groups
            if (orbital_name == "2p" or orbital_name == "3p"):
                o = bpy.data.objects[orbital_name + " - Emitter"]
                o.rotation_euler[2] = config.pi /2

            # If showing an electron cloud, ensure that the electrons in the same orbitals do not effect each other
            if config.show_electron_cloud:
                pset.use_self_effect = False
            functions.link_collection(collection=orbital_collection)

            # Atoms greater than hydrogen use collection effector groups to assist with isolating forces.
            if config.protons > 1:
                pset.effector_weights.collection = bpy.data.collections["Orbital - " + orbital_name]    # Create a collection for each shell.

                # Add the attractive force.  Each orbital is assigned a different effector group as a workaround. TODO: This section and next should be replaced when nucleus structure is completed.
                bpy.ops.object.effector_add(type='CHARGE', enter_editmode=False, location=(0, 0, 0))
                bpy.context.active_object.name = orbital_name + " - Force - Attractive"
                o = bpy.data.objects[orbital_name + " - Force - Attractive"]
                o.field.strength = config.protons * config.electron_charge        # The attractive force of protons in the nucleus. Number of protons times proton charge.
                o.field.falloff_power = 2                                         # This attractive electric force reduces at square of distance.
                functions.link_collection(collection=orbital_collection)

                # Add the repulsive force.  This is added here because protons (and spin) need to align for quantum jumps, which is under construction.  See: https://energywavetheory.com/atoms/quantum-leaps/
                repelling_force = config.orbital_force * orbital_ratio[i-1][config.protons] * config.protons       # Uses the data file for repelling force since already calculated.
                bpy.ops.object.effector_add(type='CHARGE', enter_editmode=False, location=(0, 0, 0))
                bpy.context.active_object.name = orbital_name + " - Force - Repelling"
                o = bpy.data.objects[orbital_name + " - Force - Repelling"]
                o.field.strength = -repelling_force    # TODO: this is simulated and needs to be occur naturally with proton alignment in nucleus
                o.field.falloff_power = 3              # The repelling force is an inverse cube decreasing force
                functions.link_collection(collection=orbital_collection)

                # Add the repulsive spin alignment causing electrons to jump at alignment. P orbital.  See: https://energywavetheory.com/atoms/orbital-shapes/.  TODO, this needs to be replaced when nucleus forms automatically.
                if (orbital_name == "2p" or orbital_name == "3p") and config.show_electron_cloud:
                    j = 1
                    if e == 0:
                        num_forces = math.ceil(valence_count/2)                                                # Valence electron shell.  Create an axial force for valence electrons up to 3 depending on valence count.
                    else:
                        num_forces = 3                                                                          # Defaults to three for p subshell if not valence electron shell
                    while j <= num_forces:                                                                      # Create axial forces when protons align to push electrons further
                        bpy.ops.object.effector_add(type='CHARGE', enter_editmode=False, location=(0, 0, 0))
                        bpy.context.active_object.name = orbital_name + " - Force - Axial - " + str(j)
                        o = bpy.data.objects[orbital_name + " - Force - Axial - " + str(j)]
                        o.rotation_euler[j-1] = config.pi / 2                                  # Rotate for the x, y and z planes
                        o.field.shape = 'LINE'
                        o.field.strength = 1
                        o.field.falloff_power = 3
                        o.field.falloff_type = 'TUBE'
                        functions.link_collection(collection=orbital_collection)
                        j += 1
        i += 1


    #------------------------------------------------------------------------------------------------------
    # NUCLEUS - PROTONS AND NEUTRONS
    # Adds protons and neutrons (nucleons) to the core of the atom
    # The emitter generates protons and neutrons in the nucleus for efficiency for atoms greater than hydrogen
    # If spin is set to True, the nucleus will spin using a Vortex force.
    # TODO: Nucleons require placement at standing wave nodes. Similar issue to particles that needs to be
    # TODO: solved in Blender for the formation of the atomic nucleus at the right sequence.
    # TODO: Should inherit from changes in Phase 2 here.  Then, spin should align and create orbital shapes.
    # TODO: The nucleus uses the LennardJones force in Blender which is a good approximation of the nuclear
    # TODO: force but it does not arrange at standing wave nodes. When Phase 2 is corrected it should appear here too.
    # TODO: This spin is not the true spin of the proton and should be changed once the real method is known.
    # TODO: Refer to https://energywavetheory.com/atoms/orbital-shapes/ for more information.
    #------------------------------------------------------------------------------------------------------

    # Nucleus
    functions.add_text(name=str(atom_name), text=str(atom_name), location=(config.protons/10 + 10, -5, 0), radius=5 )
    functions.link_collection(collection=nucleus_collection)

    # Hydrogen displays a detailed proton with quarks to illustrate repulsion and probability. Add a complete proton.
    if config.protons == 1:
        functions.add_nucleon(name = "Proton",            # A complete proton with quarks is shown for hydrogen, but just a halo for simplicity of simulation for all other atoms
            vertex_color = config.electron_color,
            center_color = config.positron_color,
            spin_up = True)
        o = bpy.data.objects["Proton"]
        o.location = (0,0,0)             # Hydrogen - center the proton

    # Reserved for future use.  Add a complete neutron by uncommenting the line below and placing it similar to above.  TODO: Scaling issue with center electron - needs to be core radius.
    # functions.add_nucleon(name = "Neutron", vertex_color = config.electron_color, center_color = config.positron_color, spin_up = True, neutron = True)

    # Atoms from helium and larger use an emitter for efficiency. These protons and neutrons do not show the internal quarks.
    if config.protons > 1:

        # Proton emitter
        pset = functions.add_emitter(name="Emitter - Proton",
            particle_type = "proton",
            color = config.proton_color,
            radius = config.protons/10 + 10,
            count = config.protons,
            self_effect = True,
            scale_factor = 1)
        pset.effector_weights.charge = 0   # TODO: positron not held in place by strong forces, so it can be affected in Blender by the electron.
        pset.particle_size = proton_radius
        pset.display_size = proton_radius
        functions.link_collection(collection=nucleus_collection)

        # Neutron emitter
        pset = functions.add_emitter(name="Emitter - Neutron",
            particle_type = "neutron",
            color = config.neutron_color,
            radius = config.neutrons/10 + 10,
            count = config.neutrons,
            self_effect = True,
            scale_factor = 1)
        pset.effector_weights.charge = 0   # TODO: positron not held in place by strong forces, so it can be affected in Blender by the electron.
        pset.particle_size = proton_radius
        pset.display_size = proton_radius
        functions.link_collection(collection=nucleus_collection)

        # Spin the entire nucleus of the atom (if set)
        if config.spin:
            functions.add_vortex(name="Axis", strength=config.spin_strength, frequency=config.spin_frequency)
            a = bpy.data.objects["Axis Spin Force"]
            b = bpy.data.objects["Axis"]
            nucleus_collection.objects.link(a)
            nucleus_collection.objects.link(b)
            default_collection.objects.unlink(a)
            default_collection.objects.unlink(b)
