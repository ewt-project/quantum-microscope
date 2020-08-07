# Quantum Microcope

Quantum Microscope is an open source add-on to Blender, simulating subatomic particles and the formation of matter using classical physics. It provides a microscopic look at molecules, atoms, atomic nuclei, particles and spacetime, using the theoretical model from Energy Wave Theory (EWT).

## Getting Started

These instructions enable the add-on to be run on a local machine and provide access to the source files to contribute to the ongoing development of the project.

### Prerequisites

* [Blender 2.8+](https://www.blender.org/)
* Python IDE (optional)


### Installing the Blender Add-On

1. Download the Quantum Microscope Add-On zip file at http://www.energywavetheory.com/project/qscope
2. Open the Blender app (ensure that it is v2.8 or later)
3. In Blender, under the **Edit** menu select **Preferences**
4. Select **Add-Ons**
5. Select **Install** and navigate to the EWT_Qscope.zip file downloaded in step 1.
6. Select the **checkbox** next to "Quantum Microscope" to enable the add-on


## Running the Simulation

### Starting a Simulation

There are multiple simulations in the Quantum Microscope add-on.  Once the add-on is successfully installed, the following steps may be taken to run a simulation:

1) Open the Blender app, ensuring it is defaulted to the **Layout** workspace
2) Open the Sidebar by selecting View->Sidebar.  Alternatively, you may press the **"N"** key.
3) The Sidebar should appear on the right of the Layout workspace.  Select the **Qscope** tab.
4) Select the **Run** "X" button under the Simulator panel to run each type of simulation (X)

### Changing the Simulation Type

The simulation has multiple types, representing a greater zoom factor, from the smallest particles to molecules. Each type assumes the physics of a previous phase (type) which is re-used for scalability.  For example, the physics of a standing wave is proven in Phase 1 Spacetime for efficiency in Phase 2 Particles.  

Each simulation has its own panel with various UI options to control the simulation. After changing UI controls, the simulation is started by selecting the "Run X" button, where X is the simulation type.  The UI options and suggested steps to run in each simulation type is addressed in its own ReadMe file:

| Simulation Type | README |
| ------ | ------ |
| Spacetime (e.g. neutrino) | [/phase1/ReadMe.md](/phase1/ReadMe.md)  |
| Particles (e.g. electron) | [/phase2/ReadMe.md](/phase2/ReadMe.md)  |
| Nucleons (e.g. protons) | [/phase3/ReadMe.md](/phase3/ReadMe.md)   |
| Atoms (e.g. hydrogen) | [/phase4/ReadMe.md](/phase4/ReadMe.md)   |
| Molecules (e.g. molecular hydrogen) | [/phase5/ReadMe.md](/phase5/ReadMe.md)   |


### Changing Additional Configuration Variables

The simulator has additional configuration options not exposed in the UI. These additional config options require editing a text file.  Using a text editor, open the common/config.py file and make any necessary changes.  


## Built With

* [Blender](https://www.blender.org/) - 3D creation suite
* [Python](https://www.python.org/) - Programming language within Blender


## Contributing

Simulating with 100% *real* physics requires changes to the scripts or Blender's physics engine. Developers may wish to contribute and enhance the simulation.  Each simulation type has its own ReadMe file (see table above), detailing what needs to be improved or corrected. There are also TODOs marked in the Python scripts. Refer to the [EWT Project](https://www.energywavetheory.com/project) for general information about the project and the initial requirements for the simulator.

The project code may be downloaded from GitHub at:
```
git clone https://github.com/ewt-project/quantum-microscope
```

## Authors

* **Jeff Yee** - *Initial work*


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Heinz-Dieter Hauger
* Lori Gardi
* Kuldeep Singh
* Chris Seely
* Terrence Howard
* Ted Bogner
