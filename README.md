# COVID Simulation

## Installation

You need the following prerequisits to install and run the simulation:

* python3 >= 3.7
* pip3

In order to use the render mode, you need an OpenGL compatible graphic card (with GLSL version >= 130).

To install all other dependencies (python packages), please run the install_dependencies.sh script (works on Linux and Windows).

## Usage

### Running the simulation

<pre>
    python3 -m main [--model model_name] [--no-render]
</pre>

#### --model

One can choose a model vie the model parameter.
There are currently two models available:
The "realistic" model, which tries to simulate COVID according to currently available data, and the "test" model, which models a more agressive disease, in order to speed things up in the simulation.

#### --no-render

One can activate no-render mode. Here, the simualtion will run in the background, w/o any visuals.

### Displaying stats

One can display stats from the simulation using the stats.py file. Note that the simulation must have run at least once!

<pre>
    python3 -m stats -c category
</pre>

#### Category "activity"

This will display all activities done by any person in the simulation

#### Category "bobby"

Bobby is one of the persons living in the simulation. displaying his stats will show, what he does during the days.

#### Category "bobby_needs"

This will display the bobby's needs during the simulation
