# Phase 3 - Nucleons

# COMMENTS:
# Nucleons and composite particles, like the proton, are created from stable particles in geometric arrangements that keep particles together. See: https://energywavetheory.com/explanations/whats-in-a-proton/
# A high external force is applied to electrons, which normally repel each other, to get the particles within close proximity of their standing wave structures.
# Once within this standing wave radius, the electron's charge changes to a Lennard Jones force to simulate the strong force interaction holding electrons at standing wave nodes.
# The positron continues to have a charge and is held in the proton's structure by weak forces, not the strong force.
# The electron's standing waves collapse to the first wavelength (core) which is used in the structure to compute the proton's radius.  See: https://energywavetheory.com/physics-constants/proton-radius
# A particle accelerator is added to simulate what is seen in accelerator experiments. At low values, the positron overlaps with an electron (i.e. three quarks detected). At high values, all separate (i.e. pentaquark).
# TODO: In Blender, the Lennard Jones force is a close proximity for the strong force, but not exact.  It needs to be supported by standing wave forces.  A second electron force is used for the weak force.
# TODO: The scale_factor is used to compensate for the Lennard Jones force to make particles smaller and then resized in the emitter because Lennard Jones is dependent on size.
# TODO: Spin is animated for the proton in Blender. It should use physics and be a natural motion of particles moving to nodes.
# For more details, visit www.energywavetheory.com

#------------------------------------------------------------------------------------------------------
# STANDARD CONFIGURATION
# Imports, configs and reset of the simulation
#------------------------------------------------------------------------------------------------------

import bpy
import sys
import os
import importlib

# Import Config Variables & Common Functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from common import config
importlib.reload(config)
from common import functions
importlib.reload(functions)


#------------------------------------------------------------------------------------------------------
# Main function for nucleons
# electrons: the count of electrons for the simulation
# positrons: the count of positrons for the simulation
# particle_accelerator (optional): if True, a particle accelerator is added shooting a particle towards the center
# accelerator_force (optional): the strength of the force of the particle emitted by the particle accelerator
#------------------------------------------------------------------------------------------------------

def main(electrons, positrons, particle_accelerator=False, accelerator_force=100):

    #------------------------------------------------------------------------------------------------------
    # CONFIGS - USER VARIABLES SET IN THE UI
    # Variables from the Blender Panel
    #------------------------------------------------------------------------------------------------------

    config.electrons = electrons
    config.positrons = positrons
    config.particle_accelerator = particle_accelerator
    config.accelerator_force = accelerator_force

    #------------------------------------------------------------------------------------------------------
    # PHASE CONFIGURATION
    # Modifications specific to this phase
    #------------------------------------------------------------------------------------------------------

    # Set everything to the electron since it is the stable particle for composite particles.  Electron configs.
    config.neutrinos = 10
    config.num_waves = 10
    config.wavelength = 10 * config.neutrino_core_radius * 4

    # Emitter size
    config.emitter_radius = config.ext_force_radius

    # Disable spin and calculation of particles if no external force pushes particles together
    if not config.external_force:
        config.spin = False
        config.show_calculations = False

    # Shrink the emitter to immediately create a proton so an accelerator can target the proton with particles for collisions
    if config.particle_accelerator:
        config.external_force = True
        config.ext_force_endframe = 15
        config.emitter_radius = config.electron_core_radius * 4
        config.spin = False
        config.show_calculations = False

    # The particle shell color will be the proton's color unless it is a neutron
    shell_color = config.proton_color


    ############################################ PROGRAM #####################################################

    text = config.project_text + ": Phase 3 - Nucleons"
    functions.add_text(name=text, text=text, location=(-1000, 1000, 0), radius=50)
    bpy.data.objects[text].hide_set(True)


    #------------------------------------------------------------------------------------------------------
    # CALCULATIONS
    # Calculations used in this phase using EWT equations - refer to www.energywavetheory.com.
    #------------------------------------------------------------------------------------------------------

    show_radius = False
    neutron = False

    calc_radius_simulation = (config.wavelength * 5) * ((3/8) ** (1/2))    # The simulation is a fundamental wavelength of 2 meters.  To scale, divide by 2.  Then scale by fundamental wavelength.  See https://energywavetheory.com/physics-constants/proton-radius
    calc_radius = calc_radius_simulation / 2 * config.fundamental_wavelength_no_gfactor
    calc_radius_text = "Radius: " + f"{calc_radius:.3e}" + " (m)"
    attractive_force = config.electron_energy * config.electron_radius      # Coulomb force of positron from Electric Force equation at https://energywavetheory.com/equations/classical-constants/
    attractive_force_text = "Attractive: " + f"{attractive_force:.3e}" + " (J*m) - decreasing at 1/r^2"
    repelling_force = config.electron_energy * (config.electron_radius ** 2) / (config.fine_structure ** 2)    # Repelling force from Orbital Force equation at https://energywavetheory.com/equations/classical-constants/
    repelling_force_text = "Repelling: " + f"{repelling_force:.3e}" + " (J*m^2) - decreasing at 1/r^3"

    # Determine the type of composite particle based on electron and positron count
    if ((config.electrons == 1) and (config.positrons == 1)):
        particle_type = "Meson"
    elif ((config.electrons == 3) and (config.positrons == 0)):
        particle_type = "Baryon"
    elif ((config.electrons == 4) and (config.positrons == 0)) or ((config.electrons == 2) and (config.positrons == 2)):
        particle_type = "Tetraquark"
    elif ((config.electrons == 4) and (config.positrons == 1)):
        particle_type = "Proton (pentaquark)" + "\n" + calc_radius_text + "\n" + attractive_force_text + "\n" + repelling_force_text
        show_radius = True
    elif ((config.electrons == 4) and (config.positrons == 1)):
        particle_type = "Proton (pentaquark)" + "\n" + calc_radius_text + "\n" + attractive_force_text + "\n" + repelling_force_text
        show_radius = True
    elif ((config.electrons == 5) and (config.positrons == 1)):
        particle_type = "Neutron" + "\n" + calc_radius_text
        show_radius = True
        neutron = True
        config.electrons = 4
    else:
        particle_type = ""


    #------------------------------------------------------------------------------------------------------
    # ELECTRON AND POSITRON OBJECTS
    # These particles are created automatically, assumed to have been proven in the previous phase
    # The electron and positron are hidden from view because they are used by the particle emitters.
    #------------------------------------------------------------------------------------------------------

    # Add electron object (it will be used at the vertices of the proton - first wavelength is the core of the electron only)
    functions.add_electron(name="Electron",
        color=config.electron_color,
        scale_factor = 1/(config.electron_core_radius * 4) / 2,     # Scaling factor to compensate for Blender Lennard Jones radius rule for strong force
        core_only=True)                                             # A standalone electron is standing waves, but as a composite particle its waves collapse to only one wavelength - core
    o = bpy.data.objects["Electron"]
    o.location = (1000,1000,1000)   # Move it out of view and hide it
    o.hide_set(True)

    # Add positron object (it will be used at the center of the proton - first wavelength core only)
    functions.add_electron(name="Positron",
        color=config.positron_color,
        scale_factor = 1/(config.electron_core_radius * 4),
        core_only=True,
        antimatter=True)
    o = bpy.data.objects["Positron"]
    o.location = (1000,1000,1000)   # Move it out of view and hide it
    o.hide_set(True)

    # Add a free electron object that will be attracted to the positron at the center of the proton (first wavelength core only)
    if neutron:
        functions.add_electron(name="Electron - Free",
            color=config.electron_color,
            scale_factor = 1/(config.electron_core_radius * 4),
            core_only=True)
        o = bpy.data.objects["Electron - Free"]
        o.location = (1000,1000,1000)   # Move it out of view and hide it
        o.hide_set(True)


    #------------------------------------------------------------------------------------------------------
    # ELECTRON PARTICLE EMITTER
    # This emitter generates electrons that will be subject to the strong force when forced to close ranges
    # It uses keyframe animation to switch from electric charge to the strong force (Lennard Jones)
    # TODO: The strong force should be a natural property within standing waves and not use animation.
    #------------------------------------------------------------------------------------------------------

    # Add the spherical emitter and link to the electron object as the particle being emitted
    pset = functions.add_emitter(name="Emitter - Electron",
        color = config.electron_color,
        radius = config.emitter_radius,
        count = config.electrons,
        self_effect = True,
        object_name="Electron")
    pset.particle_size = (config.electron_core_radius * 4) * 2    # Blender Lennard Jones force needs to be x2 for particle separation
    pset.display_size = (config.electron_core_radius * 4)
    pset.force_field_1.flow = 0
    pset.force_field_2.type = 'FORCE'
    pset.force_field_2.flow = config.flow

    # Set the initial electron settings of charge property when at distance
    p = bpy.data.particles[-1]
    p.force_field_1.type = 'CHARGE'
    p.force_field_1.strength = config.electron_charge
    p.force_field_1.falloff_power = 2
    p.force_field_1.use_max_distance = False
    p.force_field_1.distance_max = 0
    p.force_field_2.strength = 0
    p.keyframe_insert(data_path='force_field_1.type', frame=1)
    p.keyframe_insert(data_path='force_field_1.strength', frame=1)
    p.keyframe_insert(data_path='force_field_1.falloff_power', frame=1)
    p.keyframe_insert(data_path='force_field_1.use_max_distance', frame=1)
    p.keyframe_insert(data_path='force_field_1.distance_max', frame=1)
    p.keyframe_insert(data_path='force_field_2.strength', frame=1)

    # Apply the strong force if an external force pushes electrons together to close range
    if config.external_force:
        p.force_field_1.type = 'LENNARDJ'     # Now set the values at the keyframe for the strong forces; turn on 10 frames before external force stops
        p.force_field_1.strength = config.particle_strong_force
        p.force_field_1.falloff_power = 0
        p.force_field_1.use_max_distance = True
        p.force_field_1.distance_max = config.electron_core_radius * 40   # The strong force max distance should be standing waves of electrons
        p.force_field_2.strength = -config.particle_force
        p.keyframe_insert(data_path='force_field_1.type', frame=config.ext_force_endframe - 10)
        p.keyframe_insert(data_path='force_field_1.strength', frame=config.ext_force_endframe - 10)
        p.keyframe_insert(data_path='force_field_1.falloff_power', frame=config.ext_force_endframe - 10)
        p.keyframe_insert(data_path='force_field_1.use_max_distance', frame=config.ext_force_endframe - 10)
        p.keyframe_insert(data_path='force_field_1.distance_max', frame=config.ext_force_endframe - 10)
        p.keyframe_insert(data_path='force_field_2.strength', frame=config.ext_force_endframe - 10)
        old_type = bpy.context.area.type      # Make the switch a constant on/off for the transition of forces. Blender default is gradual changes.
        bpy.context.area.type = 'GRAPH_EDITOR'
        bpy.ops.graph.interpolation_type(type='CONSTANT')
        bpy.context.area.type = old_type


    #------------------------------------------------------------------------------------------------------
    # POSITRON PARTICLE EMITTER
    # This emitter generates positrons that will be attracted by electrons.
    # Unlike the electron, this positron is not modeled for the strong force.
    #------------------------------------------------------------------------------------------------------

    pset = functions.add_emitter(name="Emitter - Positron",
        color = config.positron_color,
        radius = config.emitter_radius/4,
        count = config.positrons,
        self_effect = True,
        object_name="Positron")
    pset.particle_size = (config.electron_core_radius * 4)
    pset.display_size = (config.electron_core_radius * 4)
    pset.effector_weights.lennardjones = 0   # The strong force should only apply to the electrons at vertices and not the positron in the middle held by weak forces
    pset.effector_weights.harmonic = 0   # Excluding the external (harmonic) force as it should only apply to push electrons to vertices, then positron attracted to center.
    pset.force_field_1.type = 'CHARGE'
    pset.force_field_1.strength = config.electron_charge
    pset.force_field_1.falloff_power = 2
    pset.force_field_1.flow = 0


    #------------------------------------------------------------------------------------------------------
    # FREE ELECTRON PARTICLE EMITTER
    # This emitter generates a free electron that will not be bound by the strong force. Only used for neutron.
    #------------------------------------------------------------------------------------------------------

    if neutron:
        pset = functions.add_emitter(name="Emitter - Electron - Free",
            color = config.electron_color,
            radius = config.emitter_radius/2,
            count = config.positrons,
            self_effect = True,
            object_name="Electron - Free")
        pset.particle_size = (config.electron_core_radius * 4)
        pset.display_size = (config.electron_core_radius * 4)
        pset.effector_weights.lennardjones = 0   # The strong force should only apply to the electrons at vertices and not the positron in the middle held by weak forces
        pset.effector_weights.harmonic = 0   # Excluding the external (harmonic) force as it should only apply to push electrons to vertices, then positron attracted to center.
        pset.force_field_1.type = 'CHARGE'   # Standard electric charge force for the free electron.
        pset.force_field_1.strength = -config.electron_charge
        pset.force_field_1.falloff_power = 2
        pset.force_field_1.flow = 0
        shell_color = config.neutron_color

    #------------------------------------------------------------------------------------------------------
    # PROTON SPIN
    # If spin is set to True, the particles at the center of the simulation will spin using a Vortex force.
    # TODO: This spin is not the true spin of the proton and it should be automatic as particles move to nodes.
    #------------------------------------------------------------------------------------------------------

    if config.spin:
        functions.add_vortex(name="Axis", strength=config.spin_strength, frequency=config.spin_frequency)


    #------------------------------------------------------------------------------------------------------
    # PROTON SHELL
    # The proton is a composite particle consisting of smaller particles.
    # This "shell" can be shown to represent a proton object with transparency to view its parts
    #------------------------------------------------------------------------------------------------------

    bpy.ops.mesh.primitive_uv_sphere_add(radius=calc_radius_simulation, enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.name = "Particle Shell"
    bpy.ops.object.shade_smooth()
    o = bpy.data.objects["Particle Shell"]
    o.hide_set(True)
    functions.add_color(name="Particle Shell", color=shell_color, transparent=True)


    #------------------------------------------------------------------------------------------------------
    # PARTICLE ACCELERATOR
    # If set to true, a particle accelerator is added to the simulation which shoots a particle at a target nucleon.
    # This simulates various forces colliding with composite particles (e.g. proton) that describe its
    # components with the strong and weak interactions. It can also be used to simulate beta decay.
    #------------------------------------------------------------------------------------------------------

    if config.particle_accelerator:

        # The speed is fixed for easier viewing, so this makes the particle display size appear larger as force increases to give it a visual
        if config.accelerator_force <= 1000:
            display_radius = (config.electron_core_radius * 4) * 0.5
        elif config.accelerator_force > 1000 and config.accelerator_force <= 10000:
            display_radius = (config.electron_core_radius * 4) * 1.5
        else:
            display_radius = (config.electron_core_radius * 4) * 2

        # Location and size of the particle accelerator
        x_location = -(config.electron_core_radius * 4) * 40
        x_depth = 500

        # Add the particle accelerator (as a cylinder shooting a particle towards the target composite particle)
        bpy.ops.mesh.primitive_cylinder_add(radius=config.electron_core_radius * 12, depth=x_depth, enter_editmode=False, location=(x_location, 0, 0))
        bpy.context.active_object.name = "Particle Accelerator"
        o = bpy.data.objects["Particle Accelerator"]
        o.rotation_euler[1] = 1.5708
        bpy.ops.object.shade_smooth()
        m = o.modifiers.new("Accelerator Particle System", type='PARTICLE_SYSTEM')
        ps = m.particle_system
        pset = ps.settings
        pset.count = 1
        pset.frame_start = config.accelerator_startframe
        pset.frame_end = config.accelerator_startframe
        pset.emit_from = "VOLUME"
        pset.lifetime = config.num_frames
        pset.normal_factor = 0
        pset.particle_size = (config.electron_core_radius * 4)
        pset.display_size = display_radius
        pset.use_self_effect = False
        pset.effector_weights.all = 0     # Due to its speed, the colliding particle should not be affected by forces (it was slowed down to view in sim)
        pset.force_field_1.type = 'FORCE'
        pset.force_field_1.strength = config.accelerator_force
        pset.force_field_1.use_max_distance = True
        pset.force_field_1.distance_max = 40   # Do not affect proton until a diameter of the electron to make simulation easier to see
        pset.force_field_2.type = 'CHARGE'
        pset.force_field_2.strength = config.electron_charge
        pset.force_field_2.use_max_distance = True
        pset.force_field_2.distance_max = 40   # Do not affect proton until a diameter of the electron to make simulation easier to see
        pset.object_align_factor[2] = 200      # Speed of accelerated particle - 200 m/s is max that seems to be set in Blender for z-axis.
        functions.add_color(name="Particle Accelerator", color=config.accelerator_color)
        functions.add_text(name="Particle Accelerator - Text", text="Particle Accelerator", location=(x_location - x_depth/2, 100, 0), radius=50)


    #------------------------------------------------------------------------------------------------------
    # EXTERNAL FORCE
    # If set to True, an external force is applied to particles (e.g. electrons) to force them together.
    # This force simulates the energy required to force particles to within standing waves for the strong force.
    # The force can be turned on and off, by setting the start and end frames that the force is applied.
    #------------------------------------------------------------------------------------------------------

    if config.external_force:
        functions.add_external_force(name="External Force",
            radius = config.ext_force_radius,
            location = (0, 0, 0),
            strength = config.ext_force_strength,
            startframe = config.ext_force_startframe,
            endframe = config.ext_force_endframe)


    #------------------------------------------------------------------------------------------------------
    # SHOW CALCULATIONS
    # If set to True, the calculations are shown for the proton's radius
    #------------------------------------------------------------------------------------------------------

    if config.show_calculations:

        # If it is a neutron, set correctly back to 5 electrons for the display
        if neutron:
            config.electrons = 5

        # Display the proton's radius
        if show_radius:
            bpy.ops.mesh.primitive_circle_add(radius=calc_radius_simulation, enter_editmode=False, location=(0, 0, 0))
            bpy.context.active_object.name = "Proton Radius"
        functions.add_text(name="Calculations", text=str(particle_type), location=(100, 100, 0), radius=10)

        # Hide everything except for the particle emitter and particle
        for o in bpy.data.objects:
            if (o.name.find ('Emitter') == -1) and o.name.find ('Electron') == -1 and o.name.find ('Positron') == -1:
                o.hide_viewport = True
                o.keyframe_insert(data_path='hide_viewport', frame=0)

        # Unhide everything when the external force ends + 50 frames
        for o in bpy.data.objects:
            o.hide_viewport = False
            o.keyframe_insert(data_path='hide_viewport', frame=config.ext_force_endframe + 50)

        # Display the total count of electrons and positrons used in the composite particle
        text = "Electrons: " + str(config.electrons) + "\n" + "Positrons: " + str(config.positrons)
        functions.add_text(name="Particle Count", text=text, location=(-100, 100, 0), radius=10)

        # Display during the duration of the external force so that it is apparent when it is turned off.
        functions.add_text(name="External Force Indicator", text="External Force: ON", location=(100, -100, 0), radius=10)
        functions.hide_at_keyframe(name = "External Force Indicator", init_hide=False, start_frame=1, end_frame=config.ext_force_endframe)
