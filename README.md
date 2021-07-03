
## Overview

This is a simple "life" simulation done via PyOpenGL to experiment with and implement 3D models, lighting, textures, and basic shaders. This project needed to be completed from scratch in ~9 days so there may be some remaining issues with efficiency or collision bugs.

There are two views for this project, and while both allow for first-person control of the camera, they focus on different things and have differing controls. The free view is how it starts, and allows for full view and control of the simulation (F3 to spawn creatures), and is also best for exploring the environment. The inspect view focuses on a single creature and has a controllable light.

Things of note to see:
-	Spawn/death animations done with a combination of shaders and translation/rotation.
-	From-scratch random terrain generation, with two passes for calculating normals and then averaging them for Gouraud shading.
-	Lamp model with light source (bulb goes off when inspect mode light is used).
-	Crawler models themselves, which are patterned/colored according to their DNA via shaders, and have several 3D details.



## Controls

**Esc**: quit

**w/a/s/d**: camera movement

**arrow keys**: camera look movement


**f**: toggle view mode (free view/crawler inspect view)


**F1**: toggle creature movement

**F2**: toggle light auto-movement


### In free view:

**F3**: spawn in a new egg in a random position

**j/J**: increase/decrease spawn size of crawlers

**k**: kill all living crawlers


### In inspect view:

**\+** or **-** : increase or decrease light distance

**]** or **\[** : increase or decrease light height

**\>** or **<** : move light sideways in either direction


**j**: activate spawn animation

**k**: activate burn animation








## Description of Crawler “Life”

The crawlers begin as eggs, spawned randomly about the area within the boundaries. However, if two crawlers would overlap, the random location is resampled until an open space is found. If there's not enough open space after 100 resamples, they will simply stop spawning. Then after a pre-set time until hatching, the crawlers will "hatch" and spawn in as adults. The spawn effect is done via fragment shader. They begin facing a random direction, and their sex and number of legs is determined by a crude "DNA" consisting of two integer values in [0,9]. Females and males are currently identical except that females have a loop structure on top of their heads. They all move standard though, going forward unless encountering a wall or another crawler, when they turn on a preset value. 

If they encounter another crawler, there is collision detection (on the bodies only, not the legs) to
handle one of three outcomes, unless the collision was between an unhatched crawler or a "dying" crawler.  If they are of opposite sex, they will mate and produce a new egg which will later hatch. That egg consists  of a random ordering of one piece of each parent's DNA (chosen at random). Currently, each crawler can only mate once. If the colliding crawlers are the same sex and have  the same DNA sum, they just turn around and  walk away from each other. If they have differing DNA sums, the one with the greater sum survives and the  other dies. They can also die from old age, a preset value.

When the crawlers die, they "burn up" in an effect done via fragment shader. I achieved this effect by selecting a color (of three burn colors) based on the results of Perlin noise, seeded by the fragment's location in model space and a time variable. There is a primary color (50%) a secondary (40%), and a tertiary (10%). Since the noise is partially seeded by time, there is a "shimmering" or "burning" effect on the border of the "burn." The burn hole itself (discarded fragments) and the border are simply  drawn via a sphere, with a radius determined by time, in model space.


