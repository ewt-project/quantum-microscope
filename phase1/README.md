# Spacetime

### About
Spacetime is an option in the Quantum Microscope simulator to model the fabric of the universe itself, and the creation of the fundamental particle and its forces. It illustrates a spacetime "universe" of granules, which are displaced from equilibrium and returning, creating waves. It illustrates the creation of waves and their interference, including reflections off dense "wave centers" that create the neutrino particle from standing waves.


## Running the Simulation
This is a simulation option of the Quantum Microscope add-on to Blender.  For instructions on installing and running the add-on refer to the [ReadMe.md](/ReadMe.md) file in the root directory of the project. Once it is running, within the Quantum Microscope UI, select the **Spacetime** panel. Under Simulator, choose Run Spacetime.

### UI Options

| UI Option | Description |
| ------ | ------ |
| Neutrinos / Antineutrinos | The number of fundamental particles that will be shown in the simulation |
| View (Granule or Wave) | Granules and their motion create waves within spacetime.  However, due to the complexity viewing granules, a second option is provided to view a collection of granules in "Wave View" |
| Neutrino Motion | A single neutrino is shown in motion using the fundamental reason for force and motion - to minimize wave amplitude |
| Wave Amplitude | The granule displacement distance (amplitude) from equilibrium |
| Wave Speed | The speed of the wave in the simulator measured by Blender frames |
| Add Force | The ability to turn on or off the external force that generates waves |
| Dimensions | Viewing spacetime in 1D, 2D or 3D options |
| Grid Length | The number of wavelengths in the spacetime grid (a larger number affects performance) |
| Wave Types | Longitudinal and transverse waves options may be shown in the simulation |

### Suggested Tests

1. In the Configuration tab of the Spacetime panel, various dimensions can be set in addition to wave types (longitudinal and transverse).  Choose the 1D view and select Run to see the difference between Longitudinal and Transverse waves (2D and 3D views also have this option but it is more difficult to see the difference in wave types).  Note that in EWT, the longitudinal wave is the electric force.  
2. In Granule view, choose 1 neutrino and select Run.  A standing wave will form at the center once the wave reaches the center.  In Blender, under Scene Collection in top right, Neutrino Shell can be hidden or unhidden.  Unhide the shell to see the sphere of the particle that surrounds standing waves, becoming what we see as the neutrino.
3. In Granule view, select Neutrino Motion and then Run to see the motion of a particle  as it moves to minimize wave amplitude.  Then turn off "Add Force" to stop the waves and note that the neutrino's motion stops.
4. In Wave view, choose 1 neutrino. A standing wave is easier to visualize at the center in this view.  The entire Spacetime grid can be hidden under Scene Collection, showing only the standing wave pattern at the center where the neutrino forms.
5. Choose 2 or more neutrinos and select Run to watch as wave interference patterns form.  Wave view is best for this mode to see the interference patterns.  


## Contributing
Developers are welcome to contribute to the simulation to improve its functionality and accuracy, including the goal of using only simple, classical physics.  The following improvements and corrections have been identified:

 Due to the way granules form waves by using Blender's wave modifier, granules cannot be controlled by the physics of other objects.  This leads to issues that need to be corrected or improved such as:

 1) Granules are not reflecting off objects (i.e. wave centers) to create standing waves.  Standing waves are formed manually and should be changed to be a reflection from a mesh object.  This needs to be corrected for standing waves to be modeled correctly in phases two and beyond.
 2) Granule energy cannot currently be calculated by the simulator.  Standing wave energy should be calculated as the sum total of granules and their displacement motion from equilibrium within a volume.
 3) Similar to #2, granule forces cannot be calculated. Traveling wave energy should be calculated based on granules and their motion (displacement from equilibrium).  The collective force of granules in traveling waves can be proven to be the force property of particles known as charge.
 4) Blender's wave modifier does not use an inverse square law.  Instead it sets falloff as a distance.  This needs to be changed to be accurate physics (falling at the inverse square of distance in three-dimensional view).
 5) Blender's wave modifier does not appear to be using exact constructive and destructive wave interference and should be modified to be more accurate.
 6) The neutrino motion scenario is animated to illustrate the sole rule of motion, to minimize wave amplitude (energy).  Because granules are not currently being controlled by or controlling other objects, it is simulated based on wave amplitude and speed.  This should be corrected when granules affect other objects, such that the traveling wave energy of granules is what forces the neutrino into motion.  
