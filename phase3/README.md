# Nucleons

### About
Nucleons is an option in the Quantum Microscope simulator to model composite particles and their creation from standalone particles such as electrons and positrons. It illustrates the combination of electrons and positrons to form nucleons, similar to the previous phase of neutrinos forming standalone particles and similar to the upcoming phase of protons forming atomic nuclei. It illustrates electrons being forced together, overcoming their repulsive charge forces, until reaching standing wave nodes in which they may be stable and be misunderstood to be high-energy "quarks".


## Running the Simulation
This is a simulation option of the Quantum Microscope add-on to Blender.  For instructions on installing and running the add-on refer to the [ReadMe.md](/ReadMe.md) file in the root directory of the project. Once it is running, within the Quantum Microscope UI, select the **Nucleons** panel. Under Simulator, choose Run Nucleons.

### UI Options

| UI Option | Description |
| ------ | ------ |
| Electrons / Positrons | The number of electrons and positrons that will be shown in the simulation |
| External Force Strength | The wave properties from the Spacetime phase have been replaced with a generic force, representing the spherical wave motion of granules towards the center of the simulator.  An increase in strength increases the motion of particles towards the center.
| Add Force | The ability to turn on or off the external force that generates waves.  |
| Particle Accelerator Strength | The force of a separate particle that will be emitted from a particle accelerator, directed towards the nucleon.  This simulates a particle collision such as those seen in particle colliders, with the ability to modify the force/energy of the incoming particle.
| Add Particle Accelerator | The particle accelerator is only shown when this option is selected |

### Suggested Tests

1. Choose 4 electrons and 1 positron and select Run.  With an external force set at a moderate strength, the particles should be forced together to within standing wave nodes and form a new particle.  Once together, the Particle Shell option may be unhidden (under Scene Collection in top right) to show the proton.  This is the pentaquark structure of the proton (four quarks and an antiquark).
2. Using the same configuration as #1, turn off the external force and choose Run.  Without a force to move the particles together, they remain with the property of charge (traveling waves) and will repel if at short distances to affect each other.
3. Turn on the external force again and try various combinations of electrons and positrons.  Note that 1 electron and 1 positron form a meson.  3 electrons form a baryon.  A combination of four of the particles (including two of each) form a tetraquark.
4. Choose 5 electrons and 1 positron and select Run.  With an external force set at a moderate strength, the particles should be forced together and form a neutron.  Note that the positron in the center combines with an electron, annihilating so that it has destructive waves and is a neutral charge.  
5. Using the configuration from #4, turn on the Particle Accelerator.  This will emit a particle (e.g. a neutrino) towards the neutron.  The neutron should eject the center electron, becoming a proton. Note that this is the beta decay process.
6. Using the configuration from #1, turn on the Particle Accelerator.  This will emit a particle (e.g. a proton) towards the proton.  The strength of the particle accelerator may be adjusted to see what happens to the proton.  At lower energies, the positron barely moves, colliding with an electron which would be destructive waves for two particles (leaving three to be detected).  Turn up the strength of the particle accelerator until all five particles separate, such as the pentaquark discovery of the proton.  It should snap back together to form a proton unless the accelerator strength is very high such that all bonds break and the particles are separated.


## Contributing
Developers are welcome to contribute to the simulation to improve its functionality and accuracy, including the goal of using only simple, classical physics.  The following improvements and corrections have been identified:

1. Blender's Lennard Jones force is a close proximity for the strong force, but not exact.  It is used as the force once particles are within standing wave range.  This force should ultimately be replaced by a single electric force that recognizes standing wave nodes and allows particles to reside at the nodes without being repelled or attracted.
2. The scale_factor is used to compensate for the Lennard Jones force to make particles smaller and then resized in the emitter because Lennard Jones is dependent on size. If the Lennard Jones force continues to be used, this can be adjusted to not be a workaround for particle sizes (although it is not critical as it is currently working).
3. The positron does not have the same properties as the electron (disables the Lennard Jones force) as it is held in place in the center of the electron by electric forces.  This will likely be fixed when #1 is corrected above.
4. Similar to #3, a fifth electron is used in the neutron creation, but is has separate properties than the other electrons (not using Lennard Jones force) to model the electric (weak) force keeping it in the center.  All electrons should be similar in properties and not modeled separately.  This will also likely be fixed when #1 is corrected above.
5. Spin is animated for the proton in Blender. It should use physics and be a natural motion of particles moving to nodes. This is likely inherited when spin is fixed in the earlier phase for particles.  
