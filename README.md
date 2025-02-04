# Physics Body Simulator
A PyQt5 and PyOpenGL based simulator which simulates the interaction between bodies influenced by collision and gravity. It supports two body gravity, gravity planes, and boundary constraints. Additionally, it also includes graphing of particle properties using PyQtGraph.

![](/images/three_body_gif.gif)
![](/images/newton_gif.gif)

## Installation
Install from requirements.txt : 
```bash
pip install -r requirements.txt
```
Or install them manually : 
```bash
pip install PyQt5 PyOpenGL numpy pyqtgraph
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

## Pictures

![](/images/solar_system.png)
![](/images/billiards.png)
![](/images/three_body.png)
![](/images/two_body.png)


Any feedback is welcome!
