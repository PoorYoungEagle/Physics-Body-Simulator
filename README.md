# Physics Body Simulator
A PyQt5 and PyOpenGL based simulator which simulates the interaction between bodies influenced by collision and gravity. It supports two body gravity, gravity planes, and boundary constraints. Additionally, it also includes graphing of particle properties using PyQtGraph.

![](/images/three_body_gif.gif)
![](/images/newton_gif.gif)

## Motivation
As a way to start learning Python, this project idea specifically came to mind while watching a [Veritasium video](https://youtu.be/6akmv1bsz1M?si=2NwH1JOH_uGeQnhm) that explored a scenario involving an empty, static universe with nothing in it except a single spherically symmetric physical body. 
I loved the concept of it as it introduces a world governed by a small set of simple rules, yet capable of producing counterintuitive behaviour. This sparked my interest in programming a simulator to view gravitational and dynamic interactions through code aswell as creating feedback using graphs.

## Installation
Install from requirements.txt : 
```bash
pip install -r requirements.txt
```
Or install them manually : 
```bash
pip install PyQt5 PyOpenGL numpy pyqtgraph pyrr
```

## Running the Simulator
Run the main script : 
```bash
python main.py
```

## Controls
Movement Controls:  
* ```W``` - Move forward (into the screen)  
* ```S``` - Move backward (away from the screen)  
* ```A``` - Move left  
* ```D``` - Move right  
* ```Space``` - Move upward  
* ```Ctrl``` - Move downward  

Camera Controls:  
* ```Left Click + Drag``` - Adjust camera angle

Simulation Controls:  
* ```Q``` - Start the simulation  
* ```E``` - Stop the simulation  
* ```R``` - Reset the simulation 
* ```F``` - Toggle Fullscreen Mode

## Simulation Features
* Simulates gravitational interactions between bodies
* Supports gravity planes and boundary constraints
* Includes a random particle/body generator
* Interactive camera controls for adjusting the view
* Supports customizable visual and world settings

## Graphing Features
* Displays real time particle properties for selected particles
* Supports both 2D and 3D graphing systems
* Customizable graph design

## Limitations

- The gravitational solver uses direct pairwise force calculations, causing O(N^2) time complexity. The performance of the simulator degrades significantly if more than 50 bodies are interacting with each other.
- The current algorithm uses Newtonian force model. No spatial acceleration structures such as Barnes-Hut algorithm or any form of spatial grids system were implemented for this project, limiting the number of bodies present in the simulation.
- The gravitational plane uses a rough idea of the Rodrigues' rotation formula which may cause some irregularities in the amount of force being applied to a body in contact with the plane.
- As the time step in this simulation is fixed for simplicity, it causes numerical drifts and energy instability over long simulation runs.
- Keep in mind that the simulator prioritizes real-time visualization, interactivity and graphical feedback over high-precision physical accuracy.

## License
This project falls under the MIT license.

## Pictures

![](/images/solar_system.png)
![](/images/billiards.png)
![](/images/three_body.png)
![](/images/two_body.png)


Any feedback is welcome!
