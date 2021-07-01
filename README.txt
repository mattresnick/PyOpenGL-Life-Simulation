
--- Description, So Far ---

So far for the project there is a single species, called a "crawler." There's no environment yet,
so their boundaries are just marked by the white lines. As in the last HW, there's a single light
source that can be controlled in the same way if desired. There's also the same first person camera.

The crawlers begin as eggs, spawned randomly about the area within the boundaries. However, if two
crawlers would overlap, the random location is resampled until an open space is found. If there's not
enough open space after 100 resamples, they will simply stop spawning. Then after a pre-set time until
hatching, the crawlers will "hatch" and spawn in as adults. The spawn effect is done via fragment shader.
They begin facing a random direction, and their sex and number of legs is determined by a crude "DNA"
consisting of two integer values in [0,9]. Females and males are currently identical except that females
have a loop structure on top of their heads. They all move standard though, going forward unless encountering
a wall or another crawler, when they turn on a preset value. 

If they encounter another crawler, there is collision detection (on the bodies only, not the legs) to
handle one of three outcomes, unless the collision was between an unhatched crawler or a "dying" crawler. 
If they are of opposite sex, they will mate and produce a new egg which will later hatch. That egg consists 
of a random ordering of one piece of each parent's DNA (chosen at random). Currently, each crawler can only
mate once. If the colliding crawlers are the same sex and have  the same DNA sum, they just turn around and 
walk away from each other. If they have differing DNA sums, the one with the greater sum survives and the 
other dies. They can also die from old age, a preset value.

When the crawlers die, they "burn up" in an effect done via fragment shader. I achieved this effect by
selecting a color (of three burn colors) based on the results of Perlin noise, seeded by the fragment's
location in model space and a time variable. There is a primary color (50%) a secondary (40%), and a
tertiary (10%). Since the noise is partially seeded by time, there is a "shimmering" or "burning"
effect on the border of the "burn." The burn hole itself (discarded fragments) and the border are simply 
drawn via a sphere, with a radius determined by time, in model space. 


Controls
--------
Esc key: quit
w/a/s/d: camera movement
arrow keys: camera look movement

g key: spawn a new crawler

F1 key: toggle creature movement
F2 key: toggle light auto-movement

1 or ! : increase or decrease ambient value
2 or @ : increase or decrease diffuse value

+ or - : increase or decrease light distance
] or [ : increase or decrease light height
> or < : move light sideways in either direction






--- What's Left ---

Naturally, I still need the environment itself. How much I end up adding to it is dependent on the amount
of time I ultimately have, but I'd like to at least add some basic textured terrain, a container for the
terrain, and a container for the rest of the aquarium/environment. I may make some changes to the light
and its behavior.

I also intend on adding a shader-based skin to the crawlers so that the coloration and pattern of their
skin is dependent on their DNA values. If possible I'd also like to add some animation to their legs so
they sort of look like they're walking and not just sliding around.

I've also been struggling with the efficiency/framerate of the scene, especially as more crawlers get added
so I'd like to generally improve that as well.



--- References ---

Much of the vertex shader code, especially Phong lighting, is from your Example 27.

Noise function based on (among others):
https://thebookofshaders.com/10/

Shader logging code based on:
http://www.hivestream.de/opengl-logging-and-debugging.html
