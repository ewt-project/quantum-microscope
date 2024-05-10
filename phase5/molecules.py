# Phase 5 - Molecules

# COMMENTS:
# This simulation assumes atoms are constructed properly from phase 4.  Atoms may be forced by energy, to within proximity of other atoms, to share electrons - forming molecules.
# The simplest molecule is formed from two hydrogen atoms - molecular hydrogen (H2).
# TODO: Molecules beyond hydrogen can be created after the completion of phase 4 and the correct arrangement of atoms.
# TODO: The emitters use a standard force and collection groups, not charges.  This should be replaced with true forces between all particles when Phase 4 is completed.
# TODO: Nuclear production creates helium but can also be expanded to include other atoms in the future.
# TODO: The explosion section for nuclear fusion, accelerators and supernovae are simulated due to complexity of breaking down particles. This should be changed in the future.
# For more details, visit www.energywavetheory.com

#------------------------------------------------------------------------------------------------------
# STANDARD CONFIGURATION
# Imports, configs and reset of the simulation
#------------------------------------------------------------------------------------------------------

import bpy
import sys
import os
import importlib
import math
import random

# Import Config Variables & Common Functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from common import config
importlib.reload(config)
from common import functions
importlib.reload(functions)
from common import data
importlib.reload(data)


#------------------------------------------------------------------------------------------------------
# Main function for molecules
# hydrogen_atoms: the count of hydrogen atoms for the simulation
#------------------------------------------------------------------------------------------------------

def main(hydrogen_atoms):

    #------------------------------------------------------------------------------------------------------
    # CONFIGS - USER VARIABLES SET IN THE UI
    # Variables from the Blender Panel
    #------------------------------------------------------------------------------------------------------

    config.hydrogen_atoms = hydrogen_atoms


    #------------------------------------------------------------------------------------------------------
    # PHASE CONFIGURATION
    # Modifications specific to this phase
    #------------------------------------------------------------------------------------------------------

    config.ext_force_radius = 1000 + (100 * config.hydrogen_atoms / 10)   # Making it dynamic based on the number of hydrogen atoms.  Should be sufficiently large to get a number of molecules in view.
    config.emitter_radius = config.hydrogen_radius * 3    # Need sufficient space between atoms to combine to molecules
    config.show_forces = False     # Disable showing proton forces as the focus is molecules
    config.flow = 10               # Slow down the effect of electrons finding electron holes
    phase_scale_factor = 1/40      # Scale downsize of particles for this phase

    # Simulates an explosion of particles depending on energy as atoms convert back to fundamental components
    explosion = False
    ext_force_strength_threshold = 100000                               # The threshold in the external force strength value before it becomes an explosion
    repulsive_force_strength = 0                                        # Unless the force is enough for an explosion, there will be no repulsive force (explosion)
    if config.ext_force_strength >= ext_force_strength_threshold:
        config.ext_force_startframe = 25                                # The external force start frame is overridden.  Enough time to allow atoms to be seen before moving to center.
        config.ext_force_endframe = config.ext_force_startframe + 25    # Atoms are held in the center for +X frames before being repelled (exploded)
        attractive_force_strength = 100000                              # Attractive strength does not use ext_force_strength for explosion because then particles can't be seen at the center.
        repulsive_force_strength = 10000                                # Force strength should be small enough to view particles being emitted from center
        explosion = True
    else:
        attractive_force_strength = config.ext_force_strength


    ############################################ PROGRAM #####################################################

    text = config.project_text + ": Phase 5 - Molecules"
    functions.add_text(name=text, text=text, location=(-1000, 1000, 0), radius=50)
    bpy.data.objects[text].hide_set(True)


    #------------------------------------------------------------------------------------------------------
    # CALCULATIONS
    # Calculations used in this phase use EWT equations and explanations - refer to www.energywavetheory.com.
    #------------------------------------------------------------------------------------------------------

    # Based on the number of hydrogen atoms in the configuration, it consists of the following smaller particles. TODO: Other atoms need to be added other than hydrogen.
    electrons = config.hydrogen_atoms * 5       # Based on 4 electrons in vertices of proton and one electron in orbital - https://energywavetheory.com/explanations/whats-in-a-proton/
    positrons = config.hydrogen_atoms           # Based on a positron in the center of the proton - https://energywavetheory.com/explanations/whats-in-a-proton/
    neutrinos = config.hydrogen_atoms * 60      # Based on the above number of electrons and positrons (6 total) and 10 neutrinos per electron. https://energywavetheory.com/subatomic-particles/electron/
    helium_atoms = math.floor(config.hydrogen_atoms / 4)    # Based on two H atoms creating neutrons; result is 4 nucleons and 2 electrons - https://energywavetheory.com/subatomic-particles/neutron/


    #------------------------------------------------------------------------------------------------------
    # ATOMS
    # Add an atom object - to be used by atom emitter.
    # TODO: Only hydrogen (H) currently supported. Future atoms need to be supported.
    #------------------------------------------------------------------------------------------------------

    # Currently supporting hydrogen (H) atoms, building molecular hydrogen (H2).
    atom = "H"
    molecule = "H2"

    # The default text that appears if show_calculations is set (text overridden in explosion scenario).  This is based on H to H2 conversion. TODO: Other atoms need to be added.
    calc_text = "Natural Forces" + "\n\n" + "Begin: " + str(config.hydrogen_atoms) + " Hydrogen Atoms"  + "\n" + "End: "
    calc_text = calc_text + str(math.floor(config.hydrogen_atoms/2)) + " H2 Molecules and " + str(config.hydrogen_atoms % 2) + " H Atoms"

    # Add a hydrogen atom and move it from view (it will be used by the emitter).
    functions.add_atom(name=atom, color=config.hydrogen_color, atom_type=atom, scale_factor=phase_scale_factor)
    o = bpy.data.objects[atom]


    #------------------------------------------------------------------------------------------------------
    # ATOM EMITTER
    # Add a number of atoms based on the configuration settings.
    # TODO: This emitter uses two different forces not charges to keep atoms at distance.  This is incorrect.
    # TODO: This emitter also uses collection groups to keep molecules separated, which is also incorrect.
    # TODO: Both issues above likely require the same fix - Blender changes to create electron holes such that only one electron can fill the hole.
    #------------------------------------------------------------------------------------------------------

    i = 1

    # This emitter is specific to molecular hydrogen.  Take the number of hydrogen atoms, divide by 2 to create molecule collections. Odd numbers will be handled by one emitter.
    while i <= math.ceil(config.hydrogen_atoms / 2):

        # Add a collection for each molecule to organize
        collection_name = 'Molecule - ' + molecule + ' - ' + str(i)
        molecule_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(molecule_collection)

        # Generate a random location for the emitter
        range = config.ext_force_radius-1
        if i == 1:                         # Special case for the first molecule which is placed at the center, then others are randomly placed.
            random_location = (0,0,0)
        else:
            random_location = (random.randint(-range,range),random.randint(-range,range),random.randint(-range,range))

        if i != 1:                         # Special case for first hydrogen atom which is already created at the center. If so, ignore creating an emitter.
            # Add first emitter with attractive atom. TODO: There should only be one emitter and no collection groups required. TODO: This is only hydrogen.
            pset = functions.add_emitter(name="Emitter - Atom 1" + ' - ' + str(i), color = config.hydrogen_color, object_name=atom, radius = config.emitter_radius, count = 1)
            pset.particle_size = 1
            pset.force_field_1.type = 'FORCE'
            pset.force_field_1.strength = -config.particle_force
            pset.force_field_1.flow = config.flow
            pset.damping = 1
            pset.effector_weights.collection = bpy.data.collections[collection_name]
            o = bpy.data.objects["Emitter - Atom 1" + ' - ' + str(i)]
            o.particle_systems[0].seed = random.randint(1,100)
            o.location = random_location
            functions.link_collection(collection=molecule_collection)

        # Add second emitter with repulsive atoms to keep the atoms separated at distance, sharing electrons. Only if even number of atoms.
        if not ((i == math.ceil(config.hydrogen_atoms / 2)) and ((config.hydrogen_atoms % 2) == 1)):
            pset = functions.add_emitter(name="Emitter - Atom 2" + ' - ' + str(i), color = config.hydrogen_color, object_name=atom, radius = config.emitter_radius, count = 1)
            pset.particle_size = 1
            pset.force_field_1.type = 'FORCE'
            pset.force_field_1.strength = config.particle_force * 10
            pset.force_field_1.flow = config.flow
            pset.damping = 1
            pset.effector_weights.collection = bpy.data.collections[collection_name]
            pset.force_field_1.use_max_distance = True
            pset.force_field_1.distance_max = config.hydrogen_radius * 2.75    # This value likely needs to be dynamic for atoms beyond hydrogen.
            o = bpy.data.objects["Emitter - Atom 2" + ' - ' + str(i)]
            o.particle_systems[0].seed = random.randint(1,100)
            o.location = random_location
            functions.link_collection(collection=molecule_collection)

        # An explosive force is used instead of external force, which accomplishes the same thing but then reverses force.  TODO: When effector groups removed, this should be moved out of collections.
        if config.external_force:
            functions.add_explosive_force(name="External Force" + ' - ' + str(i),
                attractive_strength=attractive_force_strength,
                repulsive_strength=repulsive_force_strength,
                startframe=config.ext_force_startframe,
                endframe=config.ext_force_endframe)
            functions.link_collection(collection=molecule_collection)
        i += 1


    #------------------------------------------------------------------------------------------------------
    # EXPLOSION
    # If set to True, an explosion is created that breaks atoms into their components depending on external force strength
    # This conversion of atoms to smaller particles is animated and does not use real physics.
    # It simulates the energy in stars for the nuclear process to create higher order atoms (only helium currently supported). TODO: support beyond He fusion.
    # It simulates the energy in particle accelerators to strip atoms to nucleons and begin the separation process for nucleon decay.
    # It simulates the energy of supernovae that breaks down matter and emits most of its energy as neutrinos.  Each is based on increasing energy levels.
    # TODO: When previous phases are completed this section should be rewritten to use the real logic of particle and atom creation and decay and not be animated.
    #------------------------------------------------------------------------------------------------------

    if explosion:

        # The initial atoms created above will be hidden after the explosion.  Set the keyframes using animation.
        for o in bpy.data.objects:
            functions.hide_at_keyframe(name = o.name, init_hide=False, start_frame=1, end_frame=config.ext_force_endframe)

        # Add the explosive force in the main collection to affect the particles that are formed in the process
        functions.add_explosive_force(name="External Force",
            attractive_strength=attractive_force_strength,
            repulsive_strength=repulsive_force_strength,
            startframe=config.ext_force_startframe,
            endframe=config.ext_force_endframe)

        # NUCLEAR. With a large force, the nuclei of atoms merge together to form new atomic elements.  In stars, helium is created in abundance from hydrogen. TODO: Add more atoms.
        if config.ext_force_strength >= ext_force_strength_threshold and config.ext_force_strength < ext_force_strength_threshold*10:
            pset = functions.add_emitter(name="Helium Emitter", color = config.helium_color, radius=10, count=helium_atoms, scale_factor=150)
            pset.mass = 500  # Making helium heavier to slow it down relative to other particles when being emitted
            functions.hide_at_keyframe(name="Helium Emitter", init_hide=True, start_frame=1, end_frame=config.ext_force_endframe)
            pset = functions.add_emitter(name="Hydrogen Emitter", color = config.hydrogen_color, radius=10, count=config.hydrogen_atoms % 4, scale_factor=100) # Remainder is H atoms.
            pset.mass = 200
            functions.hide_at_keyframe(name="Hydrogen Emitter", init_hide=True, start_frame=1, end_frame=config.ext_force_endframe)
            calc_text = "Nuclear Fusion" + "\n\n" + "Begin: " + str(config.hydrogen_atoms) + " Hydrogen Atoms"  + "\n" + "End: " + str(helium_atoms) + " Helium Atoms and " + str(config.hydrogen_atoms % 4) + " Hydrogen Atoms"

        # ACCELERATORS. With a very large force, atomic nuclei separate and protons begin to separate to quarks. With sufficient energy in the future, these quarks should be separated to electrons/positrons.
        elif config.ext_force_strength >= ext_force_strength_threshold*10 and config.ext_force_strength < ext_force_strength_threshold*100:
            pset = functions.add_emitter(name="Electron Emitter", color = config.electron_color, radius=10, count=electrons, scale_factor=40)
            functions.hide_at_keyframe(name="Electron Emitter", init_hide=True, start_frame=1, end_frame=config.ext_force_endframe)
            pset = functions.add_emitter(name="Positron Emitter", color = config.positron_color, radius=10, count=positrons, scale_factor=40)
            o = bpy.data.objects["Positron Emitter"]
            o.particle_systems[0].seed = random.randint(1,100)  # Make the seeding different from electrons so they follow a different path
            functions.hide_at_keyframe(name = "Positron Emitter", init_hide=True, start_frame=1, end_frame=config.ext_force_endframe)
            calc_text = "Accelerator Explosion" + "\n\n" + "Begin: " + str(config.hydrogen_atoms) + " Hydrogen Atoms"  + "\n" + "End: " + str(electrons) + " Electrons and " + str(positrons) + " Positrons"

        # SUPERNOVA. With a very, very large force, all atoms break down to the fundamental particle (neutrinos).  99% of energy emitted from supernovas are neutrinos.
        elif config.ext_force_strength >= ext_force_strength_threshold*100:
            pset = functions.add_emitter(name="Neutrino Emitter", color = config.neutrino_color, radius = 10, scale_factor=10, count = neutrinos)
            functions.hide_at_keyframe(name="Neutrino Emitter", init_hide=True, start_frame=1, end_frame=config.ext_force_endframe)
            calc_text = "Supernova Explosion" + "\n\n" + "Begin: " + str(config.hydrogen_atoms) + " Hydrogen Atoms"  + "\n" + "End: " + str(neutrinos) + " Neutrinos"


    #------------------------------------------------------------------------------------------------------
    # SHOW CALCULATIONS
    # If set to True, the calculations are shown
    #------------------------------------------------------------------------------------------------------

    if config.show_calculations:

        # Display the beginning and ending atom and particle counts
        functions.add_text(name="Molecule Count", text=calc_text, location=(300, -300, 0), radius=50)

        # Display during the duration of the external force so that it is apparent when it is turned off.
        functions.add_text(name="External Force Indicator", text="External Force: ON", location=(300, -100, 0), radius=50)
        functions.hide_at_keyframe(name = "External Force Indicator", init_hide=False, start_frame=1, end_frame=config.ext_force_endframe)
