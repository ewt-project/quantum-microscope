# Functions

#------------------------------------------------------------------------------------------------------
# COMMON FUNCTIONS
# Functions that are used across phases are placed in this module.
#------------------------------------------------------------------------------------------------------

import bpy
import sys
import os
import importlib

# Import Config Variables & Data
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from common import config
importlib.reload(config)
from common import data
importlib.reload(data)


############################################ COMMON FUNCTIONS #####################################################

#------------------------------------------------------------------------------------------------------
# Spins an object creating a 1/2 spin by rotating a tetrahedron twice as fast as one axis relative to another
# name: object name that is passed into this function to spin
# frequency: the number of keyframes until a full rotation is completed
# TODO: This spin is animated using Blender keyframes and should use physics when standing waves form.
#------------------------------------------------------------------------------------------------------

def spin_object(name, frequency, spin_up=True):
    step_num = 0
    frame_num = 0
    if config.spin:                                                # Spin only if the config is set to true
        while frame_num <= config.num_frames:
            if spin_up:
                rotation = -(config.pi * step_num)
            else:
                rotation = (config.pi * step_num)
            bpy.context.scene.frame_set(frame_num)
            o = bpy.data.objects[name]                             # Spin the object passed by reference name
            o.rotation_euler[0] = rotation
            o.rotation_euler[1] = rotation * 2    # Spins twice as fast on one axis for 1/2 spin rotation
            bpy.ops.anim.keyframe_insert_menu(type='Rotation')
            step_num += 1
            frame_num += config.spin_frequency


#------------------------------------------------------------------------------------------------------
# Adds color to an object using Blender materials.
# name: object name that is passed into this function to create material
# color: the desired color in (R,G,B,A) values
# transparent (optional): when set, the material is transparent in a Blender view to see inside particles.
#------------------------------------------------------------------------------------------------------

def add_color(name, color, transparent=False):
    o = bpy.data.objects[name]
    shell_material = bpy.data.materials.new(name + "Material")
    o.active_material = shell_material
    shell_material.diffuse_color = color
    if transparent:
        shell_material.blend_method = 'HASHED'
        shell_material.use_nodes = True
        shell_material.use_backface_culling = True
        nodes = shell_material.node_tree.nodes
        links = shell_material.node_tree.links
        for n in nodes:
            nodes.remove(n)
        output = nodes.new( type = 'ShaderNodeOutputMaterial' )
        diffuse = nodes.new( type = 'ShaderNodeBsdfTransparent' )
        link = links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
        bpy.data.materials[shell_material.name].node_tree.nodes["Transparent BSDF"].inputs[0].default_value = color


#------------------------------------------------------------------------------------------------------
# Adds an external force in the simulation towards the center to push particles together with energy.
# name: the desired name of the external force
# radius: the desired radius of a sphere that applies the force
# location: the centerpoint of the sphere location in (x,y,z) coordinates
# type (optional): the type of force. default is harmonic.
# strength (optional): the strength of the force.
# startframe (optional): the point at which the force is turned on using a Blender frame number.
# endframe (optional): the point at which the force is turned off using a Blender frame number.
#------------------------------------------------------------------------------------------------------

def add_external_force(name, radius, location, type='HARMONIC', strength=1, startframe=1, endframe=1):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, enter_editmode=False, location=location)
    bpy.context.active_object.name = name
    b = bpy.data.objects[name]
    b.hide_set(True)
    bpy.ops.object.effector_add(type=type, enter_editmode=False, location=location)
    bpy.context.active_object.name = name + " Field"
    a = bpy.data.objects[name + " Field"]
    bpy.ops.object.select_all(action='DESELECT') # deselect all objects
    a.select_set(True)
    b.select_set(True)
    bpy.context.view_layer.objects.active = b
    bpy.ops.object.parent_set(type='VERTEX', keep_transform=True)
    b.instance_type = 'VERTS'
    b.show_instancer_for_viewport = False
    b.show_instancer_for_render = False

    # The external force can be configured to begin and end at certain keyframes like a force being turned on and off
    if startframe > 1:
        a.field.strength = 0
        a.keyframe_insert(data_path='field.strength', frame=1)
    a.field.strength = strength
    a.keyframe_insert(data_path='field.strength', frame=startframe)
    a.field.strength = 0
    a.keyframe_insert(data_path='field.strength', frame=endframe)
    old_type = bpy.context.area.type
    bpy.context.area.type = 'GRAPH_EDITOR'
    bpy.ops.graph.interpolation_type(type='CONSTANT')
    bpy.context.area.type = old_type


#------------------------------------------------------------------------------------------------------
# Adds an explosive force that pulls particles to the center and then explodes outwards.
# This is very similar to the external force, but uses a force in the center to attract and repel at specific times
# name: the desired name of the explosive force
# location (optional): the centerpoint of the sphere location in (x,y,z) coordinates. Defaults to center location.
# type (optional): the type of force. default is standard force.
# attractive_strength (optional): the strength of the attractive force - similar to the external_force_strength pushing to center.
# repulsive_strength (optional): the strength of the repulsive force - should be adjustable so that the explosion can be seen in simulation.
# startframe (optional): the point at which the force is turned on using a Blender frame number.
# endframe (optional): the point at which the force is turned off using a Blender frame number.
#------------------------------------------------------------------------------------------------------

def add_explosive_force(name, location=(0,0,0), type='FORCE', attractive_strength=1, repulsive_strength=1, startframe=1, endframe=1):

    # Add a force
    bpy.ops.object.effector_add(type=type, enter_editmode=False, location=location)
    bpy.context.active_object.name = name
    a = bpy.data.objects[name]
    a.field.flow = config.flow


    # The explosive force is configured to first be attractive at the start frame and repulsive at the end frame.
    if startframe > 1:
        a.field.strength = 0
        a.keyframe_insert(data_path='field.strength', frame=1)
    a.field.strength = -attractive_strength
    a.keyframe_insert(data_path='field.strength', frame=startframe)
    a.field.strength = repulsive_strength
    a.keyframe_insert(data_path='field.strength', frame=endframe)
    old_type = bpy.context.area.type
    bpy.context.area.type = 'GRAPH_EDITOR'
    bpy.ops.graph.interpolation_type(type='CONSTANT')
    bpy.context.area.type = old_type


#------------------------------------------------------------------------------------------------------
# Adds an neutrino or antineutrinio to the simulation as a mesh object
# name: the desired name of the particle
# color: the desired color of the particle (it will also use transparency)
# radius: the desired radius of the particle
#------------------------------------------------------------------------------------------------------

def add_neutrino(name, color, radius):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.name = name
    bpy.ops.object.shade_smooth()
    add_color(name=name, color=color, transparent=True)


#------------------------------------------------------------------------------------------------------
# Adds an electron or positron to the simulation
# name: the desired name of the particle
# color: the desired color of the particle (it will also use transparency)
# scale_factor (optional): electron simulation settings are used by default but can be scaled by a factor
# core_only (optional): only an electron core (one wavelength) is shown when True.  Used for composite particles.
# antimatter (optional): when set to True, the positron is created instead of electron and rotated.
#------------------------------------------------------------------------------------------------------

def add_electron(name, color, scale_factor=1, core_only=False, antimatter=False):

    # Config variables that are constant to the electron
    if scale_factor != 1:
        config.wavelength = (config.neutrinos * 2) * scale_factor
    config.grid_size = 3  # Fix to electron size at 3
    config.grid_spacing = (config.wavelength / 2)

    # Calculations for the particle using the scale factor
    if core_only:
        config.num_waves = 1
    else:
        config.num_waves = config.neutrinos

    # Add the shell and then the core
    bpy.ops.mesh.primitive_uv_sphere_add(radius=(config.wavelength * config.num_waves), enter_editmode=False, location=(config.grid_spacing,config.grid_spacing,config.grid_spacing))
    bpy.context.active_object.name = name
    bpy.ops.object.shade_smooth()

    x = 0   # Create the electron particle with a tetrahedron core
    y = 0
    z = 0
    nodeNum = 1
    while x < config.grid_size:
        while y < config.grid_size:
            while z < config.grid_size:
                if ((x+y+z) % 2) == 0:
                    if not (nodeNum == 2 or nodeNum == 4 or nodeNum == 10 or nodeNum == 14):  # Exclude certain points to make it a tetrahedron
                        bpy.ops.mesh.primitive_uv_sphere_add(radius=config.grid_spacing/4, enter_editmode=False, location=(x*config.grid_spacing, y*config.grid_spacing, z*config.grid_spacing))
                        bpy.ops.object.shade_smooth()
                        bpy.context.active_object.name = name
                nodeNum += 0.5
                z += 1
            z = 0
            y += 1
        y = 0
        x += 1
        bpy.ops.object.select_pattern(pattern=name + "*")
        bpy.ops.object.join()
        bpy.context.active_object.name = name  # Makes sure name of object result of join is correct
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        o = bpy.data.objects[name]
        if antimatter:
            o.rotation_euler = (config.pi/2, 0, 0)
        add_color(name=name, color=color, transparent=True)


#------------------------------------------------------------------------------------------------------
# Adds a standard emitter of particles.  Many settings change by emitter so only common settings here
# name: the desired name of the proton
# color: the desired color of the particle (it will also use transparency)
# radius: the radius of the emitter.
# count: the number of particles emitted
# scale_factor (optional): proton simulation settings are used by default but can be scaled by a factor
# self_effect (optional): if true, particles will effect other particles from this emitter
# object_name (optional): the object to render if set; positron and electron auto set in this function
# particle_type (optional): certain particles have default settings such as electron, positron, proton and neutron
# core_only (optional): for use with electrons and positrons. if true, only show core of these particles
# RETURNS pset - particles settings that can be adjusted and customized outside of the function
#------------------------------------------------------------------------------------------------------

def add_emitter(name, color, radius, count, scale_factor=1, self_effect=True, object_name="", particle_type="", core_only=False):

    # Creating objects and charges for certain particles (electron, positron and proton)
    if particle_type == "electron":
        charge = -config.electron_charge
        scale_factor = 1
        if bpy.data.objects.get("Electron") is None:
            add_electron(name="Electron", color = color, scale_factor = scale_factor, core_only = core_only)
        object_name = "Electron"
        bpy.data.objects['Electron'].location = (1000,1000,1000)     # move out of view and hide
        bpy.data.objects['Electron'].hide_set(True)

    if particle_type == "positron":
        charge = config.electron_charge
        scale_factor = 1
        if bpy.data.objects.get("Positron") is None:
            add_electron(name="Positron", color = color, scale_factor = scale_factor, core_only = core_only)
        object_name = "Positron"
        bpy.data.objects['Positron'].location = (1000,1000,1000)     # move out of view and hide
        bpy.data.objects['Positron'].hide_set(True)

    if particle_type == "proton":
        charge = config.electron_charge

    # Standard across any emitter
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.name = name
    o = bpy.data.objects[name]
    o.show_instancer_for_viewport = False
    m = o.modifiers.new(name, type='PARTICLE_SYSTEM')
    ps = m.particle_system
    pset = ps.settings
    pset.count = count
    pset.frame_end = 1
    pset.lifetime = config.num_frames
    pset.normal_factor = 0
    pset.particle_size = scale_factor
    pset.display_size = scale_factor

    # If an object is passed, use the object to display instead of standard halo
    if object_name != "":
        pset.render_type = 'OBJECT'
        pset.instance_object = bpy.data.objects[object_name]

    # If set, particles self-effect each other.
    if self_effect:
        pset.use_self_effect = True

    # Standard forces for the electron, positron and proton particles.
    if particle_type == "electron" or particle_type == "positron" or particle_type == "proton":
        pset.force_field_1.type = 'CHARGE'
        pset.force_field_1.strength = charge
        pset.force_field_1.falloff_power = 2

    # Additional forces for the proton for the strong and nuclear forces
    if particle_type == "proton":
        pset.force_field_2.type = 'LENNARDJ'
        pset.force_field_2.strength = config.particle_nuclear_force
        pset.force_field_2.flow = 1
        pset.force_field_2.use_max_distance = True
        pset.force_field_2.distance_max = 10

    # Standard forces for the neutron
    if particle_type == "neutron":
        pset.force_field_1.type = 'LENNARDJ'
        pset.force_field_1.strength = config.particle_nuclear_force
        pset.force_field_1.flow = 1
        pset.force_field_1.use_max_distance = True
        pset.force_field_1.distance_max = 10
        o.particle_systems[0].seed= 1

    # Add the color to the particle
    add_color(name=name, color=color)

    return pset


#------------------------------------------------------------------------------------------------------
# Adds a proton or antiproton to the simulation
# name: the desired name of the proton
# vertex_color: the desired color of the vertex particles (it will also use transparency)
# center_color: the desired color of the center particle (it will also use transparency)
# scale_factor (optional): proton simulation settings are used by default but can be scaled by a factor
# spin_up (optional): spin direction of particle, either spin up or down if true or false
# antimatter (optional): when set to True, the antiproton is created instead of the proton
# neutron (optional): when set to True, a neutron is created instead of a proton
# repulsion (optional): when set to True, the proton's repelling orbital force is turned on. Turned off for neutron or other select cases.
#------------------------------------------------------------------------------------------------------

def add_nucleon(name, vertex_color, center_color, scale_factor=1, spin_up=True, neutron=False, repulsion=True):

    # Add the electron and positron objects to form the proton
    add_electron(name=name + " - Vertex 1", color = vertex_color, scale_factor = scale_factor, core_only = True)
    o = bpy.data.objects[name + " - Vertex 1"]
    o.location = (config.wavelength ,config.wavelength , config.wavelength)
    add_electron(name=name + " - Vertex 2", color = vertex_color, scale_factor = scale_factor, core_only = True)
    o = bpy.data.objects[name + " - Vertex 2"]
    o.location = (-config.wavelength ,-config.wavelength ,config.wavelength )
    add_electron(name=name + " - Vertex 3", color = vertex_color, scale_factor = scale_factor, core_only = True)
    o = bpy.data.objects[name + " - Vertex 3"]
    o.location = (-config.wavelength ,config.wavelength ,-config.wavelength )
    add_electron(name=name + " - Vertex 4", color = vertex_color, scale_factor = scale_factor, core_only = True)
    o = bpy.data.objects[name + " - Vertex 4"]
    o.location = (config.wavelength ,-config.wavelength ,-config.wavelength )
    add_electron(name=name + " - Positron", color = center_color, scale_factor = scale_factor, core_only = True, antimatter = True)
    o = bpy.data.objects[name + " - Positron"]
    o.location = (0,0,0)
    o.hide_set(True)

    # The positron in the center of the proton uses a particle emitter to use Blender's charge capability
    pset = add_emitter(name=name + " - Emitter",
        particle_type = "positron",
        color = center_color,
        radius = 0.1,
        count = 1,
        self_effect = False,
        object_name = name + " - Positron",
        core_only = True)
    pset.mass = 1836    # proton - electron mass ratio since electron is set to 1
    pset.effector_weights.all = 0   # TODO: positron not held in place by strong forces, so it can be affected in Blender by the electron.
    pset.force_field_2.type = 'LENNARDJ'     # The nuclear force when two or more nucleons are in proximity
    pset.force_field_2.strength = config.particle_strong_force

    # The center electron of a neutron uses a particle emitter to use Blender's charge capability and is destructive with the positron
    if neutron:
        pset = add_emitter(name=name + " - Emitter 2",
        particle_type = "electron",
        color = vertex_color,
        radius = 0.1,
        count = 1,
        self_effect = False,
        object_name = name + " - Vertex 1",
        core_only = True)
        pset.mass = 1    # neutron - neutron adds roughly one electron mass to the proton (set above)
        pset.effector_weights.all = 0   # TODO: center electron not held in place by strong forces, so it can be affected in Blender by the electron.
        pset.force_field_2.type = 'LENNARDJ'     # The nuclear force when two or more nucleons are in proximity
        pset.force_field_2.strength = config.particle_strong_force
        repulsion = False

    # Add the nucleon shell for appearance of a single particle
    calc_radius_simulation = (config.wavelength * 5) * ((3/8) ** (1/2))    # The simulation is a fundamental wavelength of 2 meters.  To scale, divide by 2.  Then scale by fundamental wavelength.
    bpy.ops.mesh.primitive_uv_sphere_add(radius=calc_radius_simulation, enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.name = name + " - Shell"
    bpy.ops.object.shade_smooth()
    if neutron:
        add_color(name=name + " - Shell", color=config.neutron_color, transparent=True)
    else:
        add_color(name=name + " - Shell", color=config.proton_color, transparent=True)

    # Add the axial repelling forces if is a proton; if neutron there are no repelling forces because center has positron and electron. Refer to https://energywavetheory.com/atoms/.
    if repulsion:
        f=1
        while f <= 4:
            # TODO: Repelling force uses Blender's wind force as the closest thing to an axial magnetic force.  This needs to be changed within Blender to be more accurate.
            bpy.ops.object.effector_add(type='WIND', enter_editmode=False, location=(0, 0, 0))
            bpy.ops.transform.resize(value=(1, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.context.active_object.name = name + " - Repelling Force " + str(f)
            o = bpy.data.objects[name + " - Repelling Force " + str(f)]
            o.field.strength = config.orbital_force
            o.field.shape = 'LINE'
            o.field.falloff_type = 'CONE'
            o.field.falloff_power = 3
            o.field.z_direction = 'POSITIVE'

            # Rotate the forces to be between the positron and each electron; this aligns the force like a dipole magnet from the center to vertices of the tetrahedron
            if f == 1:
                o.rotation_euler = (2.26893,0,-2.35619)
            elif f == 2:
                o.rotation_euler = (2.26893,0,0.785398)
            elif f == 3:
                o.rotation_euler = (0.959931,-0.261799,-0.610865)
            else:
                o.rotation_euler = (0.959931,-0.261799,2.53073)
            if not config.show_forces:
                o.hide_set(True)
            f += 1

    # Add a plain axis to spin for the forces
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius = .01, location=(0, 0, 0))
    bpy.context.active_object.name = name

    # Parent everything to the axis the object. Make sure that the AXIS is the last one created (above) to work properly.
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern=name + "*")
    bpy.ops.object.parent_set(type='OBJECT')

    # Add spin
    spin_object(name = name, frequency = config.spin_frequency, spin_up = spin_up)


#------------------------------------------------------------------------------------------------------
# Adds an atom to the simulation
# name: the desired name of the atom
# color: the desired color of the atom
# atom_type: the type of atom, using the atom's symbol such as H, He, Li, etc.
# scale_factor (optional): The scaling of the atom for visual display
# TODO: Only hydrogen currently supported. Other atoms may be supported after completion of atom and nucleus structure in phase 4
#------------------------------------------------------------------------------------------------------

def add_atom(name, color, atom_type, scale_factor=1):

    # Only hydrogen supported, so default everything to H for now.  TODO: This should be removed when more atoms are supported.
    if atom_type != "H":
        atom_type == "H"

    # Lookup in the data table how many protons and electrons for the atom based on its symbol (the count of electrons and protons are equal for neutral atoms)
    count = data.atoms.index(atom_type)     # The data.atoms array is designed so that the index position of the atom symbol is the electron (and proton) count

    # Electron distance. Loop through the neutral atom array for the element and assign x to the largest number, as long as it is not zero (no orbital)
    i = 1
    while i <= len(data.neutral_atom):
        if data.neutral_atom[i-1][count] != 0:
            x = data.neutral_atom[i-1][count]   # If not 0, assign x to the next orbital as the outermost shell
        i += 1

    # The distance to the valence shell is a ratio of the Bohr radius (hydrogen radius and the ratio from above)
    valence_distance = x * config.hydrogen_radius

    # Add valence electrons and protons. Proton structure was proven in Phase 3, so for efficiency of creating objects a positron is used as a single object for atoms.
    add_nucleon(name=name + " - Proton", vertex_color=config.electron_color, center_color=config.positron_color, scale_factor = scale_factor*4, repulsion=False)  # Resize proton to make it more visible for simulation
    a = bpy.data.objects[name + " - Proton"]
    add_electron(name=name + " - Electron", color=config.electron_color, scale_factor = scale_factor)
    b = bpy.data.objects[name + " - Electron"]
    b.location = (valence_distance,0,0)

    # Add the atom shell. It uses Blender's metaball for appearance of atoms combining to form molecules.
    bpy.ops.object.metaball_add(type='BALL', enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.name = name
    c = bpy.data.objects[name]
    c.scale = (valence_distance * 1.4, valence_distance * 1.4, valence_distance * 1.4)  # Overcome the data threshold plus additional space for electron
    c.data.resolution = 0.1
    c.data.threshold = 1.2
    add_color(name=name, color=color, transparent=True)

    # Parent the nucleus, valence electron, electron hole and shell to be an atoms
    bpy.ops.object.select_all(action='DESELECT')
    a.select_set(True)
    b.select_set(True)
    c.select_set(True)
    bpy.context.view_layer.objects.active = c
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)


#------------------------------------------------------------------------------------------------------
# Adds a vortex spin in the center to simulate a spinning nucleon or atomic nucleus
# name: the desired name of the axis
# location (optional): where the text box appears in x, y, z coordinates. By default it is in the center.
# strength (optional): the strength of the vortex spin. By default it uses the config setting.
# frequency (optional): the frequency for one complete rotation. By default it uses the config setting.
# TODO: see spin_object for details as this is a workaround until particles naturally spin for standing node alignment
#------------------------------------------------------------------------------------------------------

def add_vortex(name, location=(0,0,0), strength=config.spin_strength, frequency=config.spin_frequency):

    # Add a Force Vortex to spin an empty plain axis
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    bpy.context.active_object.name = name
    b = bpy.data.objects[name]
    bpy.ops.object.effector_add(type='VORTEX', enter_editmode=False, location=location)
    bpy.context.active_object.name = name + " Spin Force"
    a = bpy.data.objects[name + " Spin Force"]
    a.field.strength = strength
    bpy.ops.object.select_all(action='DESELECT') # deselect all objects
    a.select_set(True)
    b.select_set(True)
    bpy.context.view_layer.objects.active = b
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    # Spin the Vortex
    spin_object(name = name, frequency = frequency)


#------------------------------------------------------------------------------------------------------
# Adds a text field given text and a location. A simple enhancement of the Blender text_add function
# name: the desired name of the text box
# text: the text to appear in the text box
# location: where the text box appears in x, y, z coordinates
# radius (optional): the size of the text
#------------------------------------------------------------------------------------------------------

def add_text(name, text, location, radius=10):
    bpy.ops.object.text_add(radius=radius, enter_editmode=False, align='WORLD', location=location, rotation=(0, 0, 0))
    bpy.context.active_object.name = name
    bpy.context.scene.objects[name].data.body = text


#------------------------------------------------------------------------------------------------------
# Hides or unhides objects at specific keyframes
# name: the desired name of the object to hide/unhide
# init_hide (optional): hidden at start frame if True, unhidden if False; then flips to opposite at end frame
# start_frame (optional): the frame number to start the hide/unhide
# start_frame (optional): the frame number to end the hide/unhide and flip to be the opposite
#------------------------------------------------------------------------------------------------------

def hide_at_keyframe(name, init_hide=False, start_frame=1, end_frame=1):
        ob = bpy.data.objects[name]
        ob.hide_viewport = init_hide
        ob.keyframe_insert(data_path="hide_viewport", frame=start_frame)
        ob.hide_viewport = not init_hide
        ob.keyframe_insert(data_path="hide_viewport", frame=end_frame)


#------------------------------------------------------------------------------------------------------
# Links the most recent (active) object to a collection.
# collection: the name of the collection to link to
#------------------------------------------------------------------------------------------------------

def link_collection(collection):
    obj = bpy.context.active_object
    default_collection = bpy.context.scene.collection
    collection.objects.link(obj)
    default_collection.objects.unlink(obj)
