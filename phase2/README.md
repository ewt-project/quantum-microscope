# Particles

### About
Particles is an option in the Quantum Microscope simulator to model standalone particles and their creation from a fundamental particle - the neutrino. It illustrates the combination of neutrinos to form a particle, analogous to protons forming to create atoms. It illustrates the creation of standing waves, calculating standing wave energy as the particle's energy and the radius to the boundary of standing waves as the particle's radius.


## Running the Simulation
This is a simulation option of the Quantum Microscope add-on to Blender.  For instructions on installing and running the add-on refer to the [ReadMe.md](/ReadMe.md) file in the root directory of the project. Once it is running, within the Quantum Microscope UI, select the **Particles** panel. Under Simulator, choose Run Particles.

### UI Options

| UI Option | Description |
| ------ | ------ |
| Neutrinos | The number of neutrinos that will be shown in the simulation |
| External Force Strength | The wave properties from the Spacetime phase have been replaced with a generic force, representing the spherical wave motion of granules towards the center of the simulator.  An increase in strength increases the motion of particles towards the center.
| Add Force | The ability to turn on or off the external force that generates waves.  |

### Suggested Tests

1. Choose 1 neutrino and select Run. The result is similar to the Spacetime simulation creating a single neutrino.
2. Select 2 or more neutrinos and Run.  New particles are created with a formation of neutrinos at the center, reflecting standing waves that increase in amplitude and wavelength.  This greatly affects the energy of particles such that all known particles fit within a combination of 118 neutrinos.  
3. Select 10 neutrinos and Run.  Note the stable geometry that forms for the particle, matching the electron's properties.  
4. Turn off the external force and Run.  Note that the neutrinos are not forced together to form a new particle.  
5. Turn on the external force and adjust various properties.  Note that high forces are also unstable and new particles may not form.  
6. Under Scene Collection in the top right of Blender, unhide the Particle Shell option to see the boundary of standing waves and the view of a particle.  


## Contributing
Developers are welcome to contribute to the simulation to improve its functionality and accuracy, including the goal of using only simple, classical physics.  The following improvements and corrections have been identified:

1. Due to the inability to reflect waves and naturally create a standing wave from phase 1, a standing wave grid is manually added as a workaround to create standing wave nodes. Standing waves should occur naturally when a dense unit cell of spacetime (referred to as a wave center in EWT) reflects waves. This should be inherited from phase 1 when it is completed. Then, neutrino particles should automatically move to nodes.
2. A particle force has been added as a workaround for the rule that only one wave center may reside in a specific location/node.  This is a workaround specifically for Blender's particle systems and may be written a different way to ensure that particles may not overlap and occupy the same space.
3. Particle spin is currently animated using Blender keyframes and needs to use real physics.  This should likely be an inherited fix when standing waves form automatically.
4. Waves should eventually be shown beyond the particle's standing wave boundary as traveling waves, extending the spherical longitudinal waves for the electric force and transverse waves due to spin at the poles of the particle for the magnetic force.  The latter cannot be accomplished until after particle spin is simulated with correct physics. 
5. Based on changes above for true standing waves, certain geometries of particles should be stable and others unstable. A "time to decay" may be tracked for unstable particles and measured against known results of particle decay times. This cannot be completed until standing waves are correctly modeled.
