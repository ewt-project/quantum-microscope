# Reset

#------------------------------------------------------------------------------------------------------
# RESET SIMULATION
# Reset the simulation by clearing everything and start fresh
#------------------------------------------------------------------------------------------------------

import bpy

def clear_simulation():
    context = bpy.context
    scene = context.scene

    # Ensure that Blender is in Object mode before starting
    if context.active_object:
        if context.active_object.mode == 'EDIT':
            bpy.ops.object.editmode_toggle()

    # Unhide collections and delete items in collections.
    for c in bpy.data.collections:
        c.hide_viewport = False
        obs = [o for o in c.objects if o.users == 1]
        while obs:
            bpy.data.objects.remove(obs.pop())

    # Unhide all other objects to be deleted.
    for o in bpy.data.objects:
        o.hide_set(False)
        o.hide_viewport = False

    # Select the remaining objects to be deleted
    for o in bpy.context.scene.objects:
        o.select_set(True)

    # Delete all objects
    bpy.ops.object.delete()

    # Unlink all the child collections
    for c in scene.collection.children:
        scene.collection.children.unlink(c)

    # Running this after removes the orphan collection
    for c in bpy.data.collections:
        if not c.users:
            bpy.data.collections.remove(c)

    # Delete all materials
    for m in bpy.data.materials:             
        bpy.data.materials.remove(m)

    # Delete all particle systems
    for p in bpy.data.particles:
        bpy.data.particles.remove(p)
