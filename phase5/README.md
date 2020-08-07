# Molecules

### About
Molecules is an option in the Quantum Microscope simulator to model molecules and their formation from atoms. It illustrates the combination of hydrogen atoms to form molecular hydrogen. It also illustrates an external force crushing atoms together, demonstrating how they can combine to form new atoms (nuclear process), or demonstrating with enough energy how they can reverse the creation process and break down to its components (particles and neutrinos).


## Running the Simulation
This is a simulation option of the Quantum Microscope add-on to Blender.  For instructions on installing and running the add-on refer to the [ReadMe.md](/ReadMe.md) file in the root directory of the project. Once it is running, within the Quantum Microscope UI, select the **Molecules** panel. Under Simulator, choose Run Molecules.

### UI Options

| UI Option | Description |
| ------ | ------ |
| Hydrogen Atoms | The number of hydrogen atoms that will be shown in the simulation |
| External Force Condition | The conditions changing the strength of the external force: Normal (creates molecules), Nuclear (creates new atoms), Collider (breaks down to particles), Supernova (breaks down to neutrinos) |
| External Force Strength | The strength of the external force should automatically change when the above condition is set, but may be adjusted |
| Add Force | Turns on or off the external force |

### Suggested Tests

1. Choose 10 hydrogen atoms and select Run.  Each hydrogen atom should eventually bind with another hydrogen atom by sharing electrons, forming a molecule known as molecular hydrogen.  
2. Choose various numbers of hydrogen atoms and select Run at Normal conditions.  More molecules should form.  If an odd number of hydrogen atoms selected, there should always be one hydrogen atom that does not form a molecule.
3. Using the configuration from #1 (10 hydrogen atoms), change the External Force Condition to be Nuclear and select Run.  Note that two helium atoms are created (from 8 hydrogen atoms), with two hydrogen atoms leftover that cannot create helium.  It takes four hydrogen atoms to create helium.  
4. Using the configuration from #1, change the External Force Condition to be Collider and select Run. Note that this greater energy causes nucleons to break down and split into their components, and a particle "plasma" is produced.  
5. Using the configuration from #1, change the External Force Condition to be Supernova and Select Run.  Note that this tremendous energy causes the atoms, and its particles, to break down and split into its fundamental components - neutrinos.  This is seen in supernova explosions when 99% of energy is emitted as neutrinos.  


## Contributing
Developers are welcome to contribute to the simulation to improve its functionality and accuracy, including the goal of using only simple, classical physics.  The following improvements and corrections have been identified:

1) Currently, only hydrogen molecules are modeled.  Beyond hydrogen requires the completion of phase 4 and the correct arrangement of atomic nuclei.  Complex atoms should be eventually modeled in the simulator, such as oxygen binding with hydrogen to form a water molecule.
2) The atom emitters use a collection group, such that only two atoms in the same group affect each other and can bind.  This should be replaced with true forces between all atoms when Phase 4 is completed.
3) The nuclear production currently creates helium from hydrogen atoms.  In the future, other atoms should be created in the nuclear process.
4) The External Force Conditions for nuclear fusion, colliders and supernovae are simulated due to complexity of breaking down particles. This should be changed in the future to be true physics and not animated.
