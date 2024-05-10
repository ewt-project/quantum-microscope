# Atoms

### About
Atoms is an option in the Quantum Microscope simulator to model atoms and their nuclei creation and their capture of electrons in orbitals. It illustrates the combination of nucleons to form an atomic nucleus, similar to the previous phases of neutrinos forming standalone particles and similar to electrons and positrons forming nucleons. It illustrates electrons being attracted by the positively charged protons in the nucleus, but repelled by dipole magnetic forces within the proton (a composite particle).  The attractive and repulsive forces keep electrons in orbitals.


## Running the Simulation
This is a simulation option of the Quantum Microscope add-on to Blender.  For instructions on installing and running the add-on refer to the [ReadMe.md](/ReadMe.md) file in the root directory of the project. Once it is running, within the Quantum Microscope UI, select the **Atoms** panel. Under Simulator, choose Run Atoms.

### UI Options

| UI Option | Description |
| ------ | ------ |
| Protons | The number of protons will be shown in the simulation, determining the type of atom |
| Neutrons | The number of neutrons automatically adjusts to the number of protons, but may be changed to be the correct number of neutrons in an atom |
| Electrons | The number of electrons automatically adjusts to the number of protons, but may be changed to be ionized versions of atoms.  It should not be greater than the number of atoms. |
| Show Cloud | When this option is selected, many electrons are generated without affecting each other, such that the probability cloud nature of orbitals can be visualized.  In this view electrons do not affect other electrons, but they do interact with forces from the nucleus. |

### Suggested Tests

1. Choose 1 proton (and it should default to 1 electron) and select Run.  This is hydrogen.  Hydrogen has a special simulation to show the repelling forces within the pentaquark structure of the proton.  At alignment of the positron and electron in the proton, a repelling force appears.  At all other times, the positron in the center attracts the electron.  This causes movement towards and away from the proton creating an orbital.  The calculation of the sum of forces becomes the most probable distance (Bohr radius) and the energy level of the orbital.
2. Using the configuration from #1, turn on the Show Cloud button.  Many electrons are displayed, each only interacting with the nucleus.  This shows the probability nature of electrons as they will all be affected differently.
3. Turn off Show Cloud and adjust to 2 protons and select Run.  This is helium.  The atomic nucleus begins to form with multiple protons and neutrons.  The formation is not exact (see TODO item).  Since hydrogen has proven the attraction and repulsion, for scaling and performance, the nucleus center now aggregates the collective attraction and repulsion of all protons.  
4. Choose 3 protons and select Run.  This is lithium.  Note that the 2s orbital appears.  The ionization energy (E) only appears for the electron that will be ionized, using calculations from EWT.
5. Choose 5 protons and select Run.  This is boron.  Note that the 2p orbital appears.  Next, turn on Show Cloud.  The electron clouds for all three orbitals will be shown.  Under Scene Collection (top right of Blender), go to 1s Emitter and 2s Emitter and hide both from view.  This will leave only the 2p Emitter showing the 2p cloud.   Notice that it has the dumbbell shape like the 2p orbital should have.  You may need to pan and rotate to see it at the right angle.  
6. From configuration #5 (without Show Cloud on), change the number of electrons to be lower (e.g. 3 electrons or 2 electrons).  This is ionized versions of boron.  All atoms in the simulation up to calcium (20 protons) can be shown with ionized versions.
7. Try various configurations of protons up to 20 (calcium).  Note that energy levels are only calculated for atoms with 12 electrons or fewer.  This is due to the complexity of calculating constructive wave interference (a TODO item for the simulation to improve).


## Contributing
Developers are welcome to contribute to the simulation to improve its functionality and accuracy, including the goal of using only simple, classical physics.  The following improvements and corrections have been identified:

The core issue to be resolved is the structure of the nucleus.  Once resolved, many of these TODO items may be automatically fixed.
1) Nucleons should arrange at standing wave nodes, similar to particles.  Currently, there is no logic to separate neutrons and protons.  This development is dependent on Phase 2 and Phase 3, correcting standing waves and nodes and the creation of nucleons.
2) The repelling force uses a Blender "Wind" force to simulate the axial, magnetic force.  This is because the magnetic force in Blender does not work correctly for static objects.  This can be corrected by changing how the magnetic force works in Blender.
3) The orbital distances for all atoms (up to calcium) can be calculated in real-time using simultaneous equations. Currently, it uses pre-calculated values from MathCad, attached in a data file.  This requires tracking the position of each electron in orbitals as each one affects other electrons to create the orbital distances.  
4) Orbitals are isolated to Blender effector groups, interacting with the nucleus and electrons within that orbital, but not with the forces of electrons from other orbitals.  This is not correct as all electrons should affect other electrons.  The position of electrons is dependent on the nucleus arrangement for various orbital and this likely cannot be resolved until #1 is solved first. 
5) The electron ionization energies may be improved when electron positions are simulated and a more accurate method of wave interference is established (after solving #3).  As electron configuration increases to 12 electrons in an atom, the accuracy of the pre-calculated values from MathCad diminishes such that some calculated energy values exceed 10% of measured energy values for atoms with more than 12 electrons (which is why they have been excluded).
6) The atom's nucleus only supports up to calcium (Z=20) because of the above issues with accuracy, and also because the nucleus is unstable at large numbers of Z.  Future versions of the simulation should be able to model all atoms, up to Z=118.
7) The neutron count of atoms is not managed correctly, due to issue #1.  Currently the number of neutrons defaults to be the same number of protons, but may be changed by the user.  The number of neutrons for stable atoms is often different from the number of protons, and should be corrected to default to the right number of neutrons when the nucleon arrangement is solved in #1.
8) Currently, the p orbital shape is managed by a manual axial force.  This should instead be based on the alignment of protons in the nucleus, but due to #1, the nucleus is currently not modeled correctly.  The shapes of orbitals should depend on alignment of spin and the magnetic forces when the nucleus forms correctly.
