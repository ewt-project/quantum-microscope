# Phase 1 - Spacetime

# COMMENTS:
# This phase illustrates a spacetime "universe" of granules, which are displaced from equilibrium and returning, creating waves.
# It illustrates the creation of waves and their interference, including reflections off dense "wave centers" that create the neutrino particle from standing waves.
# Due to the difficuly in visualizing three-dimensional waves from individual components, there are various views constructed:
#  - Show Granules (vs Waves): This illustrates the underlying granules or their collective motion as waves (equivalent to seeing water molecules or water waves in an ocean)
#  - Show Motion: When a single neutrino is displaced in spacetime, it can be shown in motion.  Or stable at the center of spacetime.  The latter shows its standing wave configuration.
#  - Dimensions (1D, 2D, 3D): Although spacetime is three-dimensional, visualizations for 1D and 2D make it easier to see the formation of waves and their interactions
#  - Wave Types: Longitudinal and transverse waves options may be shown in the simulation
#  - Other options are available in the UI and settings to configure the spacetime grid size and properties, including wave speed, wave amplitude, wavelength and density of granules
# TODO: Due to the way granules form waves using Blender's wave modifier, granules cannot be controlled with physics of other objects.  This leads to major improvements needed with:
# TODO: 1) Granules are not reflecting off objects to create standing waves.  Standing waves are formed manually and should be changed to be a reflection from a mesh object.
# TODO: 2) Granule energy cannot be calculated.  Standing wave energy should be calculated as the sum total of granules and their motion, as displaced from equilibrium using amplitude properties.
# TODO: 3) Granule forces cannot be caculated.  Traveling wave energy should be calculated based on granules and their motion, again using amplitude.  This can be tied to the property known as charge.
# TODO: 4) Blender's wave modifier does not use an inverse square law and sets falloff as a distance.  This needs to be changed to be accurate physics (inverse square for three-dimensional)
# TODO: 5) Blender's wave modifier does not appear to be using exact constructive and destructive wave interference and should be modified to be more accurate.
# For more details, visit www.energywavetheory.com

#------------------------------------------------------------------------------------------------------
# STANDARD CONFIGURATION
# Imports, configs and reset of the simulation
#------------------------------------------------------------------------------------------------------

import bpy
import sys
import os
import random
import importlib


# Import Config Variables & Common Functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from common import config
importlib.reload(config)
from common import functions
importlib.reload(functions)


#------------------------------------------------------------------------------------------------------
# Main function for atoms
# wave_centers: the count of wave centers for the simulation that reflect standing waves to become neutrinos
# anti_wave_centers: the count of wave centers for antineutrinos that are on opposite nodes (they will be placed at odd integers in the grid as opposed to even)
#------------------------------------------------------------------------------------------------------

def main(wave_centers, anti_wave_centers):

    #------------------------------------------------------------------------------------------------------
    # CONFIGS - USER VARIABLES SET IN THE UI
    # Variables from the Blender Panel
    #------------------------------------------------------------------------------------------------------

    config.wave_centers = wave_centers
    config.anti_wave_centers = anti_wave_centers

    #------------------------------------------------------------------------------------------------------
    # PHASE CONFIGURATION
    # Modifications specfic to this phase
    #------------------------------------------------------------------------------------------------------

    # Granule properties
    granule_wavelength = 2   # The default wavelength size such that neutrinos are at even nodes and antineutrinos are at odd nodes
    granule_array_count = round(config.spacetime_length / 2)   # The total length of the simulation is divided in half for two separate arrays
    granule_size = 0.2       # Granule radius - displayed as a sphere
    granule_force = 1        # Granule force is the default force strength used in Blender

    # Array properties
    array_size = granule_wavelength * granule_array_count     # A grid is created of granule "wavelengths", using half the total length as the array_size because it is duplicated for opposite direction in x, y and z.
    position = (array_size - granule_wavelength/2)            # Position of outer array used for calculation of forces and array creation

    # Properties that change based on dimension.
    if config.dimensions == 3:
        range = [ (-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1), (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1) ] # Starting points and resizing for granule array, wave center emitter and container.
        number_cuts = 2    # Controls the subdivision of array cube for wave.  A larger number is better for wave production, but for performance reasons, it is managed by dimensions.
        granule_count = int((2 * granule_array_count) ** 3 / 8)      # Reduce granules and cuts by dimension for performance reasons.
        config.flow = 1     # Flow is different by dimension due to the way granule density is managed for performance.
        transform_value = (array_size, array_size, array_size)    # Resizing cube properties based on dimensions.
    elif config.dimensions == 2:
        range = [ (-1, -1, 0), (-1, 1, 0), (1, -1, 0), (1, 1, 0) ]
        number_cuts = 3
        granule_count = int((8 * granule_array_count) ** 2 / 2)
        config.flow = 10
        transform_value = (array_size, array_size, granule_wavelength)
    else:
        range = [ (-1, 0, 0), (1, 0, 0) ]
        number_cuts = 4
        granule_count = (24 * granule_array_count)
        config.flow = 0.1
        transform_value = (array_size, granule_wavelength, granule_wavelength)


    ############################################ PROGRAM #####################################################

    text = config.project_text + ": Phase 1 - Spacetime"
    functions.add_text(name=text, text=text, location=(-1000, 1000, 0), radius=50)
    bpy.data.objects[text].hide_set(True)


    #------------------------------------------------------------------------------------------------------
    # COLLECTIONS
    # Collections are used to organize the objects in Blender
    #------------------------------------------------------------------------------------------------------

    context = bpy.context
    scene = context.scene
    granules_collection = bpy.data.collections.new('Granules')
    bpy.context.scene.collection.children.link(granules_collection)
    neutrinos_collection = bpy.data.collections.new('Neutrinos')
    bpy.context.scene.collection.children.link(neutrinos_collection)
    default_collection = context.scene.collection


    #------------------------------------------------------------------------------------------------------
    # CALCULATIONS
    # Calculations used in this phase use EWT equations for neutrinos - see https://energywavetheory.com/subatomic-particles/neutrino/
    #------------------------------------------------------------------------------------------------------

    # Neutrino standing wavelength is the fundamental wavelength.
    calc_radius = config.fundamental_wavelength

    # Neutrino energy should be calculated by collective energy of standing wave granules.  It is calculated based on EWT equations for now.  TODO: use granule physics to calculate total energy.
    calc_energy_joules = ( (4/3) * config.pi * config.fundamental_density * (config.fundamental_amplitude ** 6) * config.fundamental_wavespeed ** 2 ) / (config.fundamental_wavelength_no_gfactor ** 3)

    # Neutrino energy is first calculated in joues.  To convert to electron-volts (eV), the following conversion is used: 6.242e+18 J to eV.
    calc_energy = calc_energy_joules * 6.242e+18

    # Determine the time it takes for the wave to reach the center, measured in number of keyframes in Blender.  TODO: This would be automatically displaced when a wave center can reflect granules to create standing waves.
    if config.wave_speed > 0:
        frame_to_center = int( ( (2 * granule_array_count - granule_wavelength) / (config.wave_speed) ) * (config.dimensions ** (1/2)) )
    else:
        frame_to_center = 1

    # Determine the total number of neutrinos.  The simulator has different scenarios for showing neutrinos at the center or randomly placed to show wave interference patterns.
    total_neutrinos = config.wave_centers + config.anti_wave_centers


    #------------------------------------------------------------------------------------------------------
    # FUNCTIONS
    # Shared wave properties for the wave modifier
    #------------------------------------------------------------------------------------------------------

    # Add standard wave modifiers based on settings for longitudinal or transverse waves.  This manages the configuration options for Blender's wave modifier.
    def wave_mods(mod):
        m = mod

        if config.longitudinal_wave == True:      # For longitudinal waves, the mesh object deforms.
            m.use_normal = True
            m.use_normal_x = True
        else:
            m.use_normal = False

        if config.transverse_wave == True:         # For a transverse wave, the amplitude is perpendicular to the direction of wave propagation so z direction is used.
            m.use_normal_z = True
        else:
            m.use_normal_z = False

        if config.dimensions == 1:                 # For a 1D wave, y is disbaled to show x direction.
            m.use_normal_y = False

        m.height = config.wave_amplitude           # Height of wave is the wave amplitude.
        m.speed = config.wave_speed                # The wave speed is based on speed per frame of the wave ripple using Blender's wave modifier: https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/wave.html
        m.width = granule_wavelength / 2           # Blender's wave modifier width is not a true wavelength.  Two widths to a wavelength.
        m.narrowness = granule_wavelength          # Narrowness is a Blender wave modifier property.  For a good sine wave it should be twice the width.

        if config.transverse_wave == False and config.longitudinal_wave == False:
            m.height = 0                           # If no option to view either a longitudinal or transverse wave, amplitude is set to zero so no waves appear


    # Add waves from the corner positions
    def add_waves(mod_name, neutrino_location=False, x=0, y=0):

        # If the neutrino's location is not set as known x, y properties the wave is generated from the corners.  Otherwise, from the neutrino(s).
        if not neutrino_location:

            # The corner positions are determined and iterated through to create a wave at each corner
            for multiplier in range:

                x = multiplier[0] * position
                y = multiplier[1] * position
                z = multiplier[2] * position

                # Create a wave using Blender's wave modifier
                name = mod_name + " " + str(multiplier)

                # A special case to show standing waves
                if mod_name == "Neutrino - Standing Wave":
                    m = o.modifiers.new(name, type='WAVE')
                else:
                    m = s.modifiers.new(name, type='WAVE')
                m.start_position_x = x
                m.start_position_y = y
                wave_mods(m)
                m.falloff_radius = array_size * 2    # Falloff should be inverse square not a set distance.  TODO: Need to modify Blender wave modifier for inverse square law for falloff.

        else:

            # Set the position of the wave to match the neutrino's position as passed in the x, y properties
            name = mod_name + " " + str(x) + ", " + str(y)
            m = s.modifiers.new(name, type='WAVE')
            m.start_position_x = x
            m.start_position_y = y
            wave_mods(m)
            m.falloff_radius = array_size * 2
            m.start_position_object = o     # Linking wave placement with the neutrino to be able to move the object and have wave change with it.


    # Add granules into the mesh object as a particle system.  Returns the particle settings to be overriden outside of function.
    def add_granules(name):
        o = bpy.data.objects[name]
        o.show_instancer_for_viewport = False
        m = o.modifiers.new(name, type='PARTICLE_SYSTEM')
        ps = m.particle_system
        pset = ps.settings
        pset.display_size = granule_size
        pset.frame_end = 1
        pset.lifetime = config.num_frames
        pset.normal_factor = 0
        pset.physics_type = 'NO'
        pset.use_modifier_stack = True
        pset.emit_from = 'VOLUME'
        pset.use_emit_random = True
        pset.distribution = 'RAND'
        return pset


    # Determine a random position in spacetime for the neutrino to be placed.
    def create_random_location(antimatter=False):

        # This function generates even or odd numbers depending on matter (even) or antimatter (odd) so that placement is half wavelength nodes apart for antimatter
        if antimatter:
            start_range = 1
        else:
            start_range = 2
        step_range = granule_wavelength

        # Generates a random x, y and z value for neutrinos (even numbers) and antineutrinos (odd numbers)
        x_rand = random.randrange(-array_size+start_range, array_size-1, step_range)
        y_rand = random.randrange(-array_size+start_range, array_size-1, step_range)
        z_rand = random.randrange(-array_size+start_range, array_size-1, step_range)

        # Due to the way Blender moves waves up in z axis, the neutrino needs to move up the z axis for only the wave view (doesn't apply to granules)
        if config.show_granules == True:
            z_locate = 0
        else:
            z_locate = config.wave_amplitude

        # Depending on the dimensions simulated, y or z axis may be zero for location to keep it in the plane or the line.
        if config.dimensions == 3:
            random_location = (x_rand, y_rand, z_rand)
        elif config.dimensions == 2:
            random_location = (x_rand, y_rand, z_locate)
        else:
            random_location = (x_rand, 0, z_locate)
            y_rand = 0

        # Add waves into the simulation originating from the neutrino particles.  Only x and y passed as Blender's wave modifier doesn't support a z.
        add_waves(mod_name = "Neutrino", neutrino_location=True, x=x_rand, y=y_rand)

        return random_location


    #------------------------------------------------------------------------------------------------------
    # SPACETIME CONTAINER
    # Add a "universe" for granules and their wave centers.  The container confines them to move within this user-defined space.
    # The spacetime container is also used to show wave motion, as an aggregate of granule motion when "Wave" view is selected.
    #------------------------------------------------------------------------------------------------------

    bpy.ops.mesh.primitive_cube_add(size=granule_wavelength, enter_editmode=True, location=(0, 0, 0))
    bpy.context.active_object.name = "Spacetime"
    s = bpy.data.objects["Spacetime"]
    bpy.ops.transform.resize(value=transform_value)
    bpy.ops.mesh.subdivide(number_cuts = (array_size * 2) ** 2)    # The number of cuts is used for wave modifiers.  Since spacetime cube is set by user, this is proportional
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.shade_smooth()
    bpy.ops.object.modifier_add(type='COLLISION')                  # Spacetime is set as a collision object in Blender to keep particles within the "universe"
    bpy.ops.rigidbody.object_add()
    s.rigid_body.type = 'PASSIVE'

    # There are two views.  One in which GRANULES are shown (and the spacetime cube is hidden), and another view where WAVES are illustrated instead of granules
    if config.show_granules == True and total_neutrinos < 2:
        s.hide_set(True)        # If Granule view, then hide the spacetime container to see granules.  If more than 2 neutrinos shown, spacetime is hidden a different way in the particle emitter

    else:
        if total_neutrinos < 2:
            add_waves(mod_name = "Wave")  # If Wave view, waves are shown instead.  Waves are added at corners for zero or one neutrino.  For multiple neutrinos, it is handled a different way in emitter


    #------------------------------------------------------------------------------------------------------
    # GRANULE ARRAY
    # Configuration of granules using an array modifier
    #------------------------------------------------------------------------------------------------------

    # Granule array is used to illustrate waves in scenarios with zero or one neutrinos.  Otherwise, spacetime volume is filled with granules because of complexity of multiple particles.
    if total_neutrinos < 2:

        # Determine the corner positions to create an array of granules where waves are directed toward the center.
        for multiplier in range:

            x = multiplier[0] * position
            y = multiplier[1] * position
            z = multiplier[2] * position

            # Set the first granule cube, which is one wavelength.
            name = "Granule Array " + str(multiplier)
            bpy.ops.mesh.primitive_cube_add(size=granule_wavelength, enter_editmode=True, location=(x, y, z))
            bpy.context.active_object.name = name
            o = bpy.data.objects[name]
            functions.link_collection(collection=granules_collection)
            bpy.ops.mesh.subdivide(number_cuts = number_cuts)
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.shade_smooth()

            # Create an array of granule wavelengths in the x or -x direction
            bpy.ops.object.modifier_add(type='ARRAY')
            o.modifiers["Array"].name = name + "x"
            o.modifiers[name + "x"].count = granule_array_count
            o.modifiers[name + "x"].relative_offset_displace[0] = -multiplier[0]

            # Expand the array in the y direction if 2D or 3D set
            if config.dimensions == 2 or config.dimensions == 3:
                bpy.ops.object.modifier_add(type='ARRAY')
                o.modifiers["Array"].name = name + "y"
                o.modifiers[name + "y"].count = granule_array_count
                o.modifiers[name + "y"].relative_offset_displace[1] = -multiplier[1]
                o.modifiers[name + "y"].relative_offset_displace[0] = 0

            # Expand the array in the z direction if 3D set
            if config.dimensions == 3:
                bpy.ops.object.modifier_add(type='ARRAY')
                o.modifiers["Array"].name = name + "z"
                o.modifiers[name + "z"].count = granule_array_count
                o.modifiers[name + "z"].relative_offset_displace[2] = -multiplier[2]
                o.modifiers[name + "z"].relative_offset_displace[0] = 0

            # Create a wave using Blender's wave modifier.
            m = o.modifiers.new(str(multiplier), type='WAVE')
            wave_mods(mod=m)

            # Create the granule particle system.
            pset = add_granules(name = name)

            if config.show_granules == True:
                pset.count = granule_count
            else:
                pset.count = 0    # If show_granules is not selected, then wave motion is shown and no granules are used in the particle emitter

            # Granules use the wave modifier and physics cannot be used.  Subtituting all granules for a collective force at the origination point. TODO: Real physics should be used for granules and this should be removed.
            name = "Granule Force " + str(multiplier)
            bpy.ops.object.effector_add(type='FORCE', enter_editmode=False, location=(x, y, z))
            bpy.context.active_object.name = name
            functions.link_collection(collection=granules_collection)
            o = bpy.data.objects[name]
            o.field.strength = -(granule_force * granule_count * config.wave_speed * config.wave_amplitude ** 2) ** (1/config.dimensions)   # Force proportional to count and amplitude since it uses a collective force of all granules
            o.field.flow = config.flow
            o.hide_set(True)


    #------------------------------------------------------------------------------------------------------
    # NEUTRINOS
    # Adds wave centers to the spacetime array and the standing wave structures that forms the neutrino particle.
    #------------------------------------------------------------------------------------------------------

    # If no neutrinos or no waves from external forces, it doesn't do anything.  If one neutrino, it places it at the center to show standing waves.  If more than one, they are placed randomly in spacetime.
    if total_neutrinos == 0:

        config.show_calculations = False      # There are no neutrinos to simulate.  Only wave motion.  Disable calculations.

    # One neutrino
    elif total_neutrinos == 1:

        # There are various scenarios based on showing granules, waves or motion.  Begin by creating the neutrino shell used for all scenarios.
        bpy.ops.mesh.primitive_uv_sphere_add(radius=granule_wavelength, enter_editmode=False, location=(0, 0, 0))
        functions.link_collection(collection=neutrinos_collection)
        bpy.context.active_object.name = "Neutrino Shell"
        o = bpy.data.objects["Neutrino Shell"]
        bpy.ops.object.shade_smooth()
        functions.add_color(name="Neutrino Shell", color=config.neutrino_color, transparent=True)
        o.hide_set(True)

        # If Show Motion is set in the UI, the neutrino is placed in spacetime and forced towards the center by an external force; else placed at center.
        if config.show_neutrino_motion == True:

            # If show_neutrino_motion is true, use a particle emitter to generate a neutrino that will react to forces as it moves through the spacetime array.
            bpy.ops.mesh.primitive_cube_add(size=granule_wavelength, enter_editmode=False, location=(0, 0, 0))
            functions.link_collection(collection=neutrinos_collection)
            bpy.context.active_object.name = "Neutrino"
            o = bpy.data.objects["Neutrino"]
            bpy.ops.transform.resize(value=transform_value)
            o.show_instancer_for_viewport = False

            # Add a neutrino using a particle emitter
            pset = add_granules(name = "Neutrino")
            o.particle_systems[0].seed = random.randint(1,100)           # Random position of neutrino by using particle seeding

            # Override or add particle settings in the particle system
            pset.count = config.wave_centers
            pset.particle_size = 1
            pset.render_type = 'OBJECT'
            pset.instance_object = bpy.data.objects["Neutrino Shell"]
            pset.physics_type = 'NEWTON'

        # No motion scenario.  Static placement of neutrino.
        else:

            # A single neutrino will be displayed in the center of the spacetime array. Neutrino shell is set to be a collision object.
            bpy.ops.object.modifier_add(type='COLLISION')
            bpy.ops.rigidbody.object_add()
            o.rigid_body.type = 'PASSIVE'

            # Show a single neutrino - granule view
            if config.show_granules == True:

                # Show the standing wave, creating the particle.  Due to current inability of granule physics with the wave modifier, this needs to be simulated when the wave reaches the center.
                # TODO: This entire section should be replaced with a true standing wave that occurs naturally.
                bpy.ops.mesh.primitive_uv_sphere_add(radius=granule_size * 2, enter_editmode=False, location=(0, 0, 0))
                functions.link_collection(collection=neutrinos_collection)
                bpy.ops.object.shade_smooth()
                name = "Neutrino - Wave Center"
                bpy.context.active_object.name = name
                o = bpy.data.objects[name]
                functions.add_color(name=name, color=config.neutrino_color, transparent=True)

                # Add a wave center using a particle emitter.  It has force field properties and his hidden until the waves reach the center.
                pset = add_granules(name = name)
                pset.emit_from = 'FACE'
                pset.count = 14 * config.dimensions
                pset.physics_type = 'NEWTON'
                pset.force_field_1.type = 'FORCE'
                pset.force_field_1.strength = granule_force
                pset.force_field_1.flow = 1
                pset.force_field_1.use_max_distance = True
                pset.force_field_1.distance_max = granule_wavelength
                pset.use_self_effect = True
                pset.display_color = 'VELOCITY'
                functions.hide_at_keyframe(name = name, init_hide=True, start_frame=1, end_frame=frame_to_center)

            # Show a single neutrino - wave view
            else:
                # Show a standing wave pattern at the center in wave format instead of granule format to match the rest of the simulation.
                bpy.ops.mesh.primitive_plane_add(size=granule_wavelength * 2, enter_editmode=True, location=(0, 0, -config.wave_amplitude /2 ))
                functions.link_collection(collection=neutrinos_collection)
                name = "Neutrino - Standing Wave"
                bpy.context.active_object.name = name
                o = bpy.data.objects[name]
                bpy.ops.mesh.subdivide(number_cuts = 50)
                bpy.ops.object.mode_set(mode="OBJECT")
                bpy.ops.object.shade_smooth()
                add_waves(mod_name = name)
                functions.hide_at_keyframe(name = name, init_hide=True, start_frame=1, end_frame=frame_to_center)

    # Scenarios for two or more neutrinos
    else:

        # For multiple neutrinos, don't show the calculations.
        config.show_calculations = False

        # For all scenarios where there are two or more neutrinos, position neutrinos at random points in spacetime and show wave interference patterns.
        neutrino = 1
        while neutrino <= config.wave_centers:

            name = "Neutrino " + str(neutrino)
            functions.add_neutrino(name = name, color=config.neutrino_color, radius=granule_wavelength)
            functions.link_collection(collection=neutrinos_collection)
            o = bpy.data.objects[name]
            random_location = create_random_location(antimatter = False)
            o.location = random_location
            neutrino += 1

        # Same as above for antineutrinos but with a difference in placement (odd nodes instead of even nodes) and using the antineutrino's color to differentiate.
        antineutrino = 1
        while antineutrino <= config.anti_wave_centers:

            name = "Antineutrino " + str(antineutrino)
            functions.add_neutrino(name = name, color=config.antineutrino_color, radius=granule_wavelength)
            functions.link_collection(collection=neutrinos_collection)
            o = bpy.data.objects[name]
            random_location = create_random_location(antimatter = True)
            o.location = random_location
            antineutrino += 1

        # If show granules, add the granules into spacetime to oscillate as waves from neutrinos
        if config.show_granules:
            s.show_instancer_for_viewport = False
            pset = add_granules(name = "Spacetime")
            pset.count = granule_count * (2 ** config.dimensions)

    # This modifier helps to make the waves looks better (smoother) in the simulation
    m = s.modifiers.new("Smoother", type='CORRECTIVE_SMOOTH')


    #------------------------------------------------------------------------------------------------------
    # SHOW CALCULATIONS
    # If set to True, the calculations for the neutrino's energy and radius are shown
    #------------------------------------------------------------------------------------------------------

    if config.show_calculations and not config.show_neutrino_motion and config.external_force:

        # If it is a single neutrino, the calculated energy and radius from EWT equations are displayed
        calc_text = "Neutrino \n" + "Energy: " + str(round(calc_energy, 3)) + " (eV)" + "\n" + "Radius: " + f"{calc_radius:.3e}" + " (m)"
        functions.add_text(name="Calculations", text=calc_text, location=(array_size + 2, -2, 0), radius=2)

        # Display only after neutrino has formed
        functions.hide_at_keyframe(name = "Calculations", init_hide=True, start_frame=1, end_frame=frame_to_center)
