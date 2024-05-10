bl_info = {
    "name": "Quantum Microscope",
    "description": "Simulating particles and the formation of matter using classical physics.",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Physics",
}

# Initialization file for Blender add-on

#------------------------------------------------------------------------------------------------------
# CONFIGURATION
# Imports, configs and reset of the simulation
#------------------------------------------------------------------------------------------------------

import bpy
import sys
import os
import importlib

# Default phase
phase = 1

# Development toggle (run as script or as add-on; set to True when building an add-on)
add_on_mode = True

#------------------------------------------------------------------------------------------------------
# UI VARIABLES
# User adjusted settings in the Blender panel
#------------------------------------------------------------------------------------------------------

def view_enum_changed(self, context):
    scene = context.scene
    if scene.view_enum == "W":
        scene.longitudinal_wave = False
        scene.transverse_wave = True
    else:
        scene.longitudinal_wave = True
        scene.transverse_wave = True

def show_motion_changed(self, context):
    scene = context.scene
    if scene.show_neutrino_motion:
        scene.wave_centers = 1
        scene.anti_wave_centers = 0

def proton_changed(self, context):
    scene = context.scene
    scene.electrons_atoms = scene.protons
    if scene.protons == 1:
        scene.neutrons = 0
    else:
        scene.neutrons = scene.protons

def external_force_changed(self, context):
    scene = context.scene
    if scene.external_force:
        scene.ext_force_strength = 100
        scene.wave_speed = 0.1
        scene.wave_amplitude = 2
    else:
        scene.ext_force_strength = 0
        scene.wave_speed = 0
        scene.wave_amplitude = 0

def particle_accelerator_changed(self, context):
    scene = context.scene
    if scene.particle_accelerator:
        scene.accelerator_force = 1000
    else:
        scene.accelerator_force = 0

def ext_force_enum_changed(self, context):
    scene = context.scene
    if scene.ext_force_enum == 'OP2':
        scene.ext_force_strength_molecules = 100000
    elif scene.ext_force_enum == 'OP3':
        scene.ext_force_strength_molecules = 1000000
    elif scene.ext_force_enum == 'OP4':
        scene.ext_force_strength_molecules = 10000000
    else:
        scene.ext_force_strength_molecules = 100

bpy.types.Scene.wave_centers = bpy.props.IntProperty(
    name = "Neutrinos",
    default = 1, min = 0, max = 2,
    description = "The number of neutrinos to simulate")

bpy.types.Scene.anti_wave_centers = bpy.props.IntProperty(
    name = "Antineutrinos",
    default = 0, min = 0, max = 2,
    description = "The number of antineutrinos to simulate")

bpy.types.Scene.neutrinos = bpy.props.IntProperty(
    name = "Neutrinos",
    default = 10, min = 0, max = 200,
    description = "The number of neutrinos to simulate")

bpy.types.Scene.electrons_nucleons = bpy.props.IntProperty(
    name = "Electrons",
    default = 4, min = 0, max = 20,
    description = "The number of electrons to simulate for nucleons")

bpy.types.Scene.positrons = bpy.props.IntProperty(
    name = "Positrons",
    default = 1, min = 0, max = 20,
    description = "The number of positrons to simulate")

bpy.types.Scene.electrons_atoms = bpy.props.IntProperty(
    name = "Electrons",
    default = 1, min = 0, max = 20,
    description = "The number of electrons to simulate for atoms")

bpy.types.Scene.protons = bpy.props.IntProperty(
    name = "Protons",
    default = 1, min = 0, max = 20,
    description = "The number of protons to simulate",
    update = proton_changed)

bpy.types.Scene.neutrons = bpy.props.IntProperty(
    name = "Neutrons",
    default = 0, min = 0, max = 20,
    description = "The number of neutrons to simulate")

bpy.types.Scene.hydrogen_atoms = bpy.props.IntProperty(
    name = "Hydrogen Atoms",
    default = 10, min = 1, soft_max = 200,
    description = "The number of hydrogen atoms to simulate")

bpy.types.Scene.show_electron_cloud = bpy.props.BoolProperty(
    name ="Show Cloud",
    default = False,
    description = "Multiple positions of the electron are simulated to illustrate the probability cloud")

bpy.types.Scene.show_calculations = bpy.props.BoolProperty(
    name ="Show Calculations",
    default = True,
    description = "Show calculations in the simulator")

bpy.types.Scene.show_forces = bpy.props.BoolProperty(
    name ="Show Forces",
    default = True,
    description = "Show forces in the simulator")

bpy.types.Scene.show_neutrino_motion = bpy.props.BoolProperty(
    name ="Neutrino Motion",
    default = False,
    description = "Show motion of a neutrino to minimize wave amplitude",
    update = show_motion_changed)

bpy.types.Scene.spin = bpy.props.BoolProperty(
    name ="Spin",
    default = True,
    description = "Spin particles or nuclei")

bpy.types.Scene.external_force = bpy.props.BoolProperty(
    name ="Add Force",
    default = True,
    description = "This applies an external force towards the center",
    update = external_force_changed)

bpy.types.Scene.ext_force_strength = bpy.props.IntProperty(
    name = "Strength",
    default = 100, min = 0, soft_max = 1000,
    description = "The strength of the external force")

bpy.types.Scene.ext_force_strength_molecules = bpy.props.IntProperty(
    name = "Strength",
    default = 100, min = 0, max = 10000000,
    description = "The strength of the external force")

bpy.types.Scene.particle_accelerator = bpy.props.BoolProperty(
    name ="Add Particle Accelerator",
    default = False,
    description = "This adds an accelerator firing a particle towards the center",
    update = particle_accelerator_changed)

bpy.types.Scene.accelerator_force = bpy.props.IntProperty(
    name = "Strength",
    default = 100, min = 0, soft_max = 100000,
    description = "The strength of the force of the particle from the accelerator")

bpy.types.Scene.spacetime_length = bpy.props.IntProperty(
    name = "Grid Length",
    default = 20, min = 0, soft_max = 50, step = 2,
    description = "The length of the spacetime array in one dimension")

bpy.types.Scene.wave_amplitude = bpy.props.IntProperty(
    name = "Wave Amplitude",
    default = 2, min = 0, soft_max = 50,
    description = "The displacement distance (wave amplitude) of granules")

bpy.types.Scene.wave_speed = bpy.props.FloatProperty(
    name = "Wave Speed",
    default = 0.1, min = 0, soft_max = 1,
    description = "The speed that the wave propagates through space")

bpy.types.Scene.longitudinal_wave = bpy.props.BoolProperty(
    name ="Longitudinal",
    default = True,
    description = "Show a longitudinal wave - amplitude in same direction as wave propagation")

bpy.types.Scene.transverse_wave = bpy.props.BoolProperty(
    name ="Transverse",
    default = False,
    description = "Show a transverse wave - amplitude perpendicular to wave propagation")

bpy.types.Scene.num_frames = bpy.props.IntProperty(
    name = "Total Frames",
    default = 1000, min = 1, soft_max = 10000,
    description = "The total number of frames to run the simulation")

bpy.types.Scene.auto_play = bpy.props.BoolProperty(
    name = "Auto Play",
    default = True,
    description = "This automatically plays the simulation on button press")

bpy.types.Scene.ext_force_enum = bpy.props.EnumProperty(
    name = "Condition",
    description="Applies exponentially increasing levels of force on particles",
    default = 'OP1',
    items=[ ('OP1', "Normal", ""),
                ('OP2', "Nuclear", ""),
                ('OP3', "Collider", ""),
                ('OP4', "Supernova", "") ],
    update = ext_force_enum_changed)

bpy.types.Scene.dimensions_enum = bpy.props.EnumProperty(
    name = "Dimensions",
    description="The number of dimensions for the spacetime array",
    default = '2',
    items=[ ('1', "1D", ""),
                ('2', "2D", ""),
                ('3', "3D", "") ])

bpy.types.Scene.view_enum = bpy.props.EnumProperty(
    name = "View",
    description="The view type displaying individual granules or collective waves",
    default = 'G',
    items=[ ('G', "Granule", ""),
                ('W', "Wave", "") ],
    update = view_enum_changed)


#------------------------------------------------------------------------------------------------------
# UI PANEL
# Layout of UI options and button operators to choose the simulator (by phase number)
#------------------------------------------------------------------------------------------------------

class EWTPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Qscope"


class EWT_PT_1(EWTPanel, bpy.types.Panel):
    bl_idname = "EWT_PT_1"
    bl_label = "Spacetime"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        row = layout.row()
        row.prop(scene, "wave_centers")
        row = layout.row()
        row.prop(scene, "anti_wave_centers")
        row = layout.row()
        row.prop(scene, "view_enum",  expand = True)
        row = layout.row()
        row.prop(scene, "show_neutrino_motion")


class EWT_PT_1_1(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_1"
    bl_label = "External Force"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column()
        col.prop(scene, "wave_amplitude")

        col = layout.column()
        col.prop(scene, "wave_speed")

        col = layout.column()
        col.prop(scene, "external_force")


class EWT_PT_1_2(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_1"
    bl_label = "Configuration"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row()
        row.prop(scene, "dimensions_enum", expand = True)
        row = layout.row()
        row.prop(scene, "spacetime_length")

        row = layout.row()
        row.prop(scene, "longitudinal_wave")
        row.prop(scene, "transverse_wave")


class EWT_PT_1_Run(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_1"
    bl_label = "Simulator"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False
        row = layout.row()
        row.scale_y = 2.0
        row.operator("ewt.phase", text="Run Spacetime", icon='RENDER_ANIMATION').phase = 1


class EWT_PT_2(EWTPanel, bpy.types.Panel):
    bl_label = "Particles"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row()
        row.prop(scene, "neutrinos")


class EWT_PT_2_1(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_2"
    bl_label = "External Force"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column()
        col.prop(scene, "ext_force_strength")

        col = layout.column()
        col.prop(scene, "external_force")


class EWT_PT_2_Run(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_2"
    bl_label = "Simulator"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False
        row = layout.row()
        row.scale_y = 2.0
        row.operator("ewt.phase", text="Run Particles", icon='RENDER_ANIMATION').phase = 2


class EWT_PT_3(EWTPanel, bpy.types.Panel):
    bl_label = "Nucleons"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row()
        row.prop(scene, "electrons_nucleons")
        row = layout.row()
        row.prop(scene, "positrons")


class EWT_PT_3_1(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_3"
    bl_label = "External Force"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column()
        col.prop(scene, "ext_force_strength")

        col = layout.column()
        col.prop(scene, "external_force")


class EWT_PT_3_2(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_3"
    bl_label = "Particle Accelerator"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column()
        col.prop(scene, "accelerator_force")

        col = layout.column()
        col.prop(scene, "particle_accelerator")


class EWT_PT_3_Run(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_3"
    bl_label = "Simulator"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False
        row = layout.row()
        row.scale_y = 2.0
        row.operator("ewt.phase", text="Run Nucleons", icon='RENDER_ANIMATION').phase = 3


class EWT_PT_4(EWTPanel, bpy.types.Panel):
    bl_label = "Atoms"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row()
        row.prop(scene, "protons")
        row = layout.row()
        row.prop(scene, "neutrons")
        row = layout.row()
        row.prop(scene, "electrons_atoms")
        row = layout.row()
        row.prop(scene, "show_electron_cloud")


class EWT_PT_4_Run(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_4"
    bl_label = "Simulator"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False
        row = layout.row()
        row.scale_y = 2.0
        row.operator("ewt.phase", text="Run Atoms", icon='RENDER_ANIMATION').phase = 4


class EWT_PT_5(EWTPanel, bpy.types.Panel):
    bl_label = "Molecules"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row()
        row.prop(scene, "hydrogen_atoms")


class EWT_PT_5_1(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_5"
    bl_label = "External Force"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column()
        col.prop(scene, "ext_force_enum", expand = True)

        col = layout.column()
        col.prop(scene, "ext_force_strength_molecules")

        col = layout.column()
        col.prop(scene, "external_force")


class EWT_PT_5_Run(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_5"
    bl_label = "Simulator"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False
        row = layout.row()
        row.scale_y = 2.0
        row.operator("ewt.phase", text="Run Molecules", icon='RENDER_ANIMATION').phase = 5


class EWT_PT_Settings(EWTPanel, bpy.types.Panel):
    bl_label = "Quantum Microscope"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.label(text="Settings:")
        row = layout.row()
        row.prop(scene, "auto_play")
        row = layout.row()
        row.prop(scene, "spin")
        row = layout.row()
        row.prop(scene, "show_forces")
        row = layout.row()
        row.prop(scene, "show_calculations")
        row = layout.row()
        row.prop(scene, "num_frames")
        row = layout.row()


class EWT_PT_Settings_1(EWTPanel, bpy.types.Panel):
    bl_parent_id = "EWT_PT_Settings"
    bl_label = "About"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.label(text="Learn more at:")
        row = layout.row()
        row.operator("wm.url_open", text="EWT Web Site").url = "http://www.energywavetheory.com"


#------------------------------------------------------------------------------------------------------
# MAIN FUNCTION
# After simulator button press in UI is executed
#------------------------------------------------------------------------------------------------------

def main(operator, context, phase):

    # Clear the simulation
    from common import reset
    importlib.reload(reset)
    reset.clear_simulation()

    # Import configs
    from common import config
    importlib.reload(config)

    # Set common config variables to the UI inputs
    config.show_neutrino_motion = context.scene.show_neutrino_motion
    config.wave_amplitude = context.scene.wave_amplitude
    config.wave_speed = context.scene.wave_speed
    config.spin = context.scene.spin
    config.external_force = context.scene.external_force
    config.ext_force_strength = context.scene.ext_force_strength
    config.show_calculations = context.scene.show_calculations
    config.show_forces = context.scene.show_forces
    config.num_frames = context.scene.num_frames
    config.longitudinal_wave = context.scene.longitudinal_wave
    config.transverse_wave = context.scene.transverse_wave
    config.spacetime_length = context.scene.spacetime_length
    config.dimensions = int(context.scene.dimensions_enum)

    if context.scene.view_enum == "G":
        config.show_granules = True
    else:
        config.show_granules = False

    # Execute the correct module based on phase
    if phase == 1:
        from phase1 import spacetime
        importlib.reload(spacetime)
        spacetime.main(wave_centers = context.scene.wave_centers,
        anti_wave_centers = context.scene.anti_wave_centers)

    if phase == 2:
        from phase2 import particles
        importlib.reload(particles)
        particles.main(neutrinos = context.scene.neutrinos)

    if phase == 3:
        from phase3 import nucleons
        importlib.reload(nucleons)
        nucleons.main(electrons = context.scene.electrons_nucleons,
            positrons = context.scene.positrons,
            particle_accelerator = context.scene.particle_accelerator,
            accelerator_force = context.scene.accelerator_force)

    if phase == 4:
        from phase4 import atoms
        importlib.reload(atoms)
        atoms.main(protons = context.scene.protons,
            neutrons = context.scene.neutrons,
            electrons = context.scene.electrons_atoms,
            show_electron_cloud = context.scene.show_electron_cloud)

    if phase == 5:
        config.ext_force_strength = context.scene.ext_force_strength_molecules
        from phase5 import molecules
        importlib.reload(molecules)
        molecules.main(hydrogen_atoms = context.scene.hydrogen_atoms)

    # Automatically start playing
    if context.scene.auto_play == True:
        if not bpy.context.screen.is_animation_playing:
            bpy.ops.screen.animation_play()

    # Finished.  Set the view and clear cache.
    bpy.ops.view3d.view_axis(type = 'TOP')    # Set the correct view, frame number and deselect items
    bpy.ops.view3d.view_orbit(type='ORBITDOWN')
    bpy.ops.view3d.view_orbit(type='ORBITRIGHT')
    bpy.ops.view3d.view_all(center=True)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.frame_set(1)
    bpy.ops.ptcache.free_bake_all()  #Blender has an issue with cache that affects particle systems. Workaround is to delete all bakes and then toggle gravity to clear the cache correctly.
    bpy.context.scene.use_gravity = True
    bpy.context.scene.use_gravity = False


#------------------------------------------------------------------------------------------------------
# OPERATOR CLASS DEFINITION
# Execute function when simulator button selected
#------------------------------------------------------------------------------------------------------

class EWTPhase(bpy.types.Operator):
    bl_idname = "ewt.phase"
    bl_label = "EWT Phase"
    bl_description = "Run Simulator"

    phase : bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        # Two paths are used for add-on scripts and for development mode (set at top of file in add_on_mode)
        script_file = os.path.realpath(__file__)
        file = os.path.dirname(__file__)

        if add_on_mode:
            dir = os.path.dirname(script_file)
        else:
            dir = os.path.dirname(bpy.data.filepath)

        if not dir in sys.path:
            sys.path.append(dir)

        if add_on_mode:
            sys.path.append(os.path.join(os.path.realpath(__file__), '..', 'common'))
        else:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

        from common import config
        importlib.reload(config)

        main(self, context, self.phase)

        return {'FINISHED'}


#------------------------------------------------------------------------------------------------------
# REGISTRATIONS
# Registering class files
#------------------------------------------------------------------------------------------------------

def register():
    bpy.utils.register_class(EWTPhase)
    bpy.utils.register_class(EWT_PT_1)
    bpy.utils.register_class(EWT_PT_1_1)
    bpy.utils.register_class(EWT_PT_1_2)
    bpy.utils.register_class(EWT_PT_1_Run)
    bpy.utils.register_class(EWT_PT_2)
    bpy.utils.register_class(EWT_PT_2_1)
    bpy.utils.register_class(EWT_PT_2_Run)
    bpy.utils.register_class(EWT_PT_3)
    bpy.utils.register_class(EWT_PT_3_1)
    bpy.utils.register_class(EWT_PT_3_2)
    bpy.utils.register_class(EWT_PT_3_Run)
    bpy.utils.register_class(EWT_PT_4)
    bpy.utils.register_class(EWT_PT_4_Run)
    bpy.utils.register_class(EWT_PT_5)
    bpy.utils.register_class(EWT_PT_5_1)
    bpy.utils.register_class(EWT_PT_5_Run)
    bpy.utils.register_class(EWT_PT_Settings)
    bpy.utils.register_class(EWT_PT_Settings_1)

def unregister():
    bpy.utils.unregister_class(EWTPhase)
    bpy.utils.unregister_class(EWT_PT_1)
    bpy.utils.unregister_class(EWT_PT_1_1)
    bpy.utils.unregister_class(EWT_PT_1_2)
    bpy.utils.unregister_class(EWT_PT_1_Run)
    bpy.utils.unregister_class(EWT_PT_2)
    bpy.utils.unregister_class(EWT_PT_2_1)
    bpy.utils.unregister_class(EWT_PT_2_Run)
    bpy.utils.unregister_class(EWT_PT_3)
    bpy.utils.unregister_class(EWT_PT_3_1)
    bpy.utils.unregister_class(EWT_PT_3_2)
    bpy.utils.unregister_class(EWT_PT_3_Run)
    bpy.utils.unregister_class(EWT_PT_4)
    bpy.utils.unregister_class(EWT_PT_4_Run)
    bpy.utils.unregister_class(EWT_PT_5)
    bpy.utils.unregister_class(EWT_PT_5_1)
    bpy.utils.unregister_class(EWT_PT_5_Run)
    bpy.utils.unregister_class(EWT_PT_Settings)
    bpy.utils.unregister_class(EWT_PT_Settings_1)

if __name__ == "__main__":
    register()
