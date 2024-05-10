# Phase 2 - Particles

# COMMENTS:
# Wave centers (neutrinos) merge together to create particles, even if temporarily.
# A configurable number of wave centers is set and an external force is applied to create the conditions for merging (whether natural or manufactured - e.g. particle colliders)
# The particle's charge is constructive wave interference - refer to https://energywavetheory.com/subatomic-particles/
# The particle's wavelength and number of standing waves determines its size (radius) and is also based on constructive wave interference
# TODO: A standing wave grid is added for Blender as a workaround to create standing wave nodes since wave centers are not reflecting waves. Standing waves should occur naturally.
# TODO: A particle force is added for Blender as a workaround for the rule that only one wave center may reside in a specific location/node.
# TODO: Based on changes above for true standing waves, certain geometries of particles should be stable and others unstable. The time to decay should be tracked for unstable particles.
# TODO: Particle spin needs to use real physics.  It is currently animated using Blender keyframe animation.
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


#------------------------------------------------------------------------------------------------------
# Main function for particles
# neutrinos: the count of wave centers (neutrinos) for the simulation
#------------------------------------------------------------------------------------------------------

def main(neutrinos):

    #------------------------------------------------------------------------------------------------------
    # CONFIGS - USER VARIABLES SET IN THE UI
    # Variables from the Blender Panel
    #------------------------------------------------------------------------------------------------------

    config.neutrinos = neutrinos


    #------------------------------------------------------------------------------------------------------
    # PHASE CONFIGURATION
    # Modifications specific to this phase.  Must be set after user variables because of dependency.
    #------------------------------------------------------------------------------------------------------

    # WAVES - MODIFIED WITH WAVE CENTER CHANGES
    config.num_waves = config.neutrinos
    config.particle_display_radius = config.neutrino_core_radius * config.neutrinos
    config.particle_charge = config.neutrino_charge * config.neutrinos
    config.core_strength = config.particle_charge * 2
    particle_core_wavelength = config.neutrinos * config.neutrino_wavelength

    # STANDING WAVE GRID CONFIGURATION - MODIFIED WITH WAVE CENTER CHANGES
    config.grid_spacing = particle_core_wavelength / 2
    config.grid_strength = config.neutrinos * 2
    config.grid_size = int((-(-(config.neutrinos*2) ** (1/3)//1)))

    # EXTERNAL FORCE
    if not config.external_force:        # Disable spin and calculating particles if no external force exists to push particles together
        config.spin = False
        config.show_calculations = False

    # VISIBILITY
    config.flow = 7                      # Slow down flow for visibility
    config.emitter_radius = config.ext_force_radius / 2
    config.particle_force = config.particle_charge * 5  # TODO: Standing waves should form naturally and not need this force


    ############################################ PROGRAM #####################################################

    text = config.project_text + ": Phase 2 - Particles"
    functions.add_text(name=text, text=text, location=(-1000, 1000, 0), radius=50)
    bpy.data.objects[text].hide_set(True)


    #------------------------------------------------------------------------------------------------------
    # COLLECTIONS
    # Collections are used to organize the objects in Blender in categories to turn on/off visibility
    #------------------------------------------------------------------------------------------------------

    context = bpy.context
    scene = context.scene
    wavelength_collection = bpy.data.collections.new('Wavelength')
    bpy.context.scene.collection.children.link(wavelength_collection)
    standingwaves_collection = bpy.data.collections.new('Standing Waves')
    bpy.context.scene.collection.children.link(standingwaves_collection)
    nodes_collection = bpy.data.collections.new('Nodes')
    bpy.context.scene.collection.children.link(nodes_collection)
    default_collection = context.scene.collection


    #------------------------------------------------------------------------------------------------------
    # STANDING WAVE NODES
    # Standing wave nodes are the point of no displacement and a stable position for waves to converge.
    # This phenomenon should be proven in the previous phase and duplicated here in this phase.
    # TODO: Due to Blender's physics engine limitations, nodes are created manually.
    # TODO: In the future, the standing wave nodes should form naturally from reflections off wave centers.
    #------------------------------------------------------------------------------------------------------

    x = 0   # Standing wave node grid starting point - positive forces
    y = 0
    z = 0
    nodeNum = 0
    while x < config.grid_size:
        while y < config.grid_size:
            while z < config.grid_size:
                bpy.ops.object.effector_add(type='CHARGE', enter_editmode=False, location=(x*config.grid_spacing, y*config.grid_spacing, z*config.grid_spacing))
                if ((x+y+z) % 2) == 0:
                    bpy.context.active_object.name = "Node - Positive (" + str(nodeNum) + ")"
                    o = bpy.data.objects["Node - Positive (" + str(nodeNum) + ")"]
                    o.field.strength = config.grid_strength
                else:
                    bpy.context.active_object.name = "Node - Negative (" + str(nodeNum) + ")"
                    o = bpy.data.objects["Node - Negative (" + str(nodeNum) + ")"]
                    o.field.strength = -config.grid_strength
                o.field.flow = config.flow
                o.field.falloff_power = 2
                functions.link_collection(collection=nodes_collection)
                nodeNum += 1
                z += 1
            z = 0
            y += 1
        y = 0
        x += 1

    # Move the standing wave node grid to the origin
    offset = -((config.grid_size-1) / 2 * config.grid_spacing)
    bpy.ops.object.select_pattern(pattern="Node*")
    bpy.ops.transform.translate(value=(offset, offset, offset))

    # Add a plain axis to the center of the node grid and join the objects together
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    bpy.context.active_object.name = "Node - Axis"
    p = bpy.context.active_object
    functions.link_collection(collection=nodes_collection)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern="Node*")
    p.select_set(True)
    bpy.context.view_layer.objects.active = p
    bpy.ops.object.parent_set(type='OBJECT')


    #------------------------------------------------------------------------------------------------------
    # PARTICLE SPIN
    # If spin is set to True, the particles at the center of the simulation will spin by spinning the grid.
    # TODO: This spin is animated and should be replaced by true forces when standing waves form naturally.
    #------------------------------------------------------------------------------------------------------

    if config.spin:
        functions.spin_object(name = "Node - Axis", frequency = config.spin_frequency)

    if not config.show_forces:
        p.hide_set(True)


    #------------------------------------------------------------------------------------------------------
    # PARTICLE STANDING WAVES
    # In addition to standing wave nodes, a particle should form standing waves from in-waves and out-waves
    # until reaching a boundary (particle radius) that standing waves transition to traveling waves.
    # Standing waves are proportional to the number of wave centers as constructive interference: wavelength and number.
    # TODO: These waves are added manually as a limitation of Blender's physics. Should be automatic in future.
    #------------------------------------------------------------------------------------------------------

    i = 1
    sphere_strength = config.core_strength
    sphere_radius = particle_core_wavelength + (2 * particle_core_wavelength) - (2 * i * config.neutrino_wavelength)     # Distance to wavelength. Standing wavelength decreases proportional to shell number
    sphere_midwave = particle_core_wavelength + ( ( (2 * particle_core_wavelength) - (2 * i * config.neutrino_wavelength) ) / 2)   # Midpoint of wavelength for forces
    sphere_name = "Standing Wave Core"
    harmonic_name = "Standing Wave Harmonic Core"

    # Create spherical, standing waves at a given wavelength distance and number of wavelengths.  This becomes the particle volume.
    while i <= config.num_waves:
        if i > 1:
            sphere_strength = config.core_strength / (i ** 2)  #inverse square strength of wave
            sphere_radius = sphere_radius + (2 * particle_core_wavelength) - (2 * i * config.neutrino_wavelength)
            sphere_midwave = sphere_midwave + ( ( (2 * particle_core_wavelength) - (2 * i * config.neutrino_wavelength) ) )
            sphere_name = "Standing Wave Sphere " + str(i)
            harmonic_name = "Standing Wave Harmonic " + str(i)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=sphere_midwave, enter_editmode=False, location=(0, 0, 0))
        bpy.context.active_object.name = sphere_name
        b = bpy.data.objects[sphere_name]
        bpy.ops.object.effector_add(type='HARMONIC', enter_editmode=False, location=(0, 0, 0))
        bpy.context.active_object.name = harmonic_name
        a = bpy.data.objects[harmonic_name]
        a.field.strength = sphere_strength
        a.field.harmonic_damping = 0
        if not config.show_forces:
            a.hide_set(True)
        bpy.ops.object.select_all(action='DESELECT')
        a.select_set(True)
        b.select_set(True)
        bpy.context.view_layer.objects.active = b
        bpy.ops.object.parent_set(type='VERTEX', keep_transform=True)
        b.instance_type = 'VERTS'
        b.show_instancer_for_viewport = False
        b.show_instancer_for_render = False
        standingwaves_collection.objects.link(a)
        standingwaves_collection.objects.link(b)
        default_collection.objects.unlink(a)
        default_collection.objects.unlink(b)
        bpy.ops.mesh.primitive_circle_add(radius=sphere_radius, enter_editmode=False, location=(0, 0, 0))
        wavelength_name = "Wavelength " + str(i)
        bpy.context.active_object.name = wavelength_name
        functions.link_collection(collection=wavelength_collection)
        i += 1


    #------------------------------------------------------------------------------------------------------
    # PARTICLE SHELL
    # A particle shell is used to visualize a particle - as the volume of standing waves
    # The radius of the shell is the boundary of standing waves where they transition to traveling waves
    # This shell can be made transparent in some Blender views to see its underlying components
    #------------------------------------------------------------------------------------------------------

    bpy.ops.mesh.primitive_uv_sphere_add(radius=(config.num_waves * particle_core_wavelength), enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.name = "Particle Shell"
    o = bpy.data.objects["Particle Shell"]
    bpy.ops.object.shade_smooth()
    functions.add_color(name="Particle Shell", color=config.electron_color, transparent=True)
    o.hide_set(True)


    #------------------------------------------------------------------------------------------------------
    # NEUTRINO EMITTER
    # This emitter generates wave centers (neutrinos) that will be forced together to create particles.
    #------------------------------------------------------------------------------------------------------

    pset = functions.add_emitter(name="Emitter",
        color = config.neutrino_color,
        radius = config.emitter_radius,
        count = config.neutrinos,
        self_effect = True)
    pset.particle_size = config.particle_display_radius
    pset.display_size = config.particle_display_radius
    pset.force_field_1.type = 'CHARGE'
    pset.force_field_1.strength = -config.particle_charge
    pset.force_field_1.falloff_power = 2
    pset.force_field_1.flow = config.flow
    pset.force_field_2.type = 'FORCE'
    pset.force_field_2.strength = config.particle_force
    pset.force_field_2.use_max_distance = False
    o = bpy.data.objects["Emitter"]
    o.particle_systems[0].seed = random.randint(1,100)


    #------------------------------------------------------------------------------------------------------
    # EXTERNAL FORCE
    # If set to True, an external force is applied to wave centers to force them together.
    # This force simulates the energy required to force wave centers to create particles.
    #------------------------------------------------------------------------------------------------------

    if config.external_force:
        functions.add_external_force(name="External Force",
            radius = config.ext_force_radius,
            location = (0, 0, 0),
            strength = config.ext_force_strength,
            startframe = config.ext_force_startframe,
            endframe = config.ext_force_endframe)

        # Hide everything except for the particle emitter
        for o in bpy.data.objects:
            if o.name != 'Emitter':
                o.hide_viewport = True
                o.keyframe_insert(data_path='hide_viewport', frame=0)

        # Unhide everything when the external force ends and standing waves form
        for o in bpy.data.objects:
            o.hide_viewport = False
            o.keyframe_insert(data_path='hide_viewport', frame=config.ext_force_endframe)


    #------------------------------------------------------------------------------------------------------
    # SHOW CALCULATIONS
    # If set to True, the calculations of particle energy and radius are shown
    #------------------------------------------------------------------------------------------------------

    if config.show_calculations:

        # The simulation is a fundamental wavelength of 2 meters.  To scale, divide by 2.  Then scale by fundamental wavelength.  Proportional to number of wavelengths and wavelength.
        calc_radius = "Radius: " + f"{(config.fundamental_wavelength * config.num_waves * particle_core_wavelength / 2):.3e}" + " (m)"

        # The simulation doesn't automatically calc energy.  A fundamental energy value is used and the EWT equation from https://energywavetheory.com/subatomic-particles/equation/
        shell_multiplier = 0
        n = 1
        while n <= config.neutrinos:
            shell_multiplier = shell_multiplier + (n**3 - ((n-1)**3)) / n**4
            n +=1
        calc_energy = "Energy: " + str(round(config.fundamental_energy * (config.neutrinos ** 5) * shell_multiplier)) + " (eV)"

        # Calculation is the same, but formatting for eV vs MeV
        if config.neutrinos < 6:
            calc_energy = "Energy: " + str(round(config.fundamental_energy * (config.neutrinos ** 5) * shell_multiplier, 3)) + " (eV)"
        elif config.neutrinos < 40:
            calc_energy = "Energy: " + str(round(config.fundamental_energy * (config.neutrinos ** 5) * shell_multiplier / 1000000, 3)) + " (MeV)"
        else:
            calc_energy = "Energy: " + str(round(config.fundamental_energy * (config.neutrinos ** 5) * shell_multiplier / 1000000000, 3)) + " (GeV)"
        functions.add_text(name="Calculations", text=calc_energy + "\n" + calc_radius, location=(config.num_waves * particle_core_wavelength + 10, 20, 0), radius=10)

        # Display the K value for the particle.  K is a variable count of neutrinos at the core of a particle, analogous to Z as the variable count of protons at the core of an atom.
        if config.neutrinos == 1:
            particle_name_text = "Neutrino: " + "K=" + str(config.neutrinos)
        elif config.neutrinos == 10:
            particle_name_text = "Electron: " + "K=" + str(config.neutrinos)
        else:
            particle_name_text = "K=" + str(config.neutrinos)
        functions.add_text(name="Wave Center Count", text=particle_name_text, location=(config.num_waves * particle_core_wavelength + 10, 30, 0), radius=10)

        # Display during the duration of the external force so that it is apparent when it is turned off.
        functions.add_text(name="External Force Indicator", text="External Force: ON", location=(config.num_waves * particle_core_wavelength + 10, -30, 0), radius=10)
        functions.hide_at_keyframe(name = "External Force Indicator", init_hide=False, start_frame=1, end_frame=config.ext_force_endframe)
