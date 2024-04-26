# boid
Boid demo with interactive sliders

Based on the [boid](https://people.ece.cornell.edu/land/courses/ece4760/labs/s2021/Boids/Boids.html#:~:text=Boids%20is%20an%20artificial%20life,very%20simple%20set%20of%20rules.) algorithm.

This version uses Pygame, and has sliders that can be used to change some of the important values for the boid algorithm.

To use this repo, download the files, then open your terminal.

You will need Python3 and pygame installed. To install pygame, you can use `pip install pygame`.

`cd` into the boids folder, then use `python3 boids.py` to run the file.

We have several components to this code.

1. Boid class
   1. Have an `x` and `y` position that are updated each frame by their `velocity_x` and `velocity_y`. Initially, these velocities are set to a random number less than the `max velocity`.
   2. `move` method that prevents the boids from going to the edge of the screen (minus a padding). When `move` is called, the boid will add its velocity to its `(x,y)` position.
   3. `align` method looks at the boids near the current boid (boids that are within the `NEIGHBOR_RADIUS` distance) and calculates their average velocity (`avg_v_x` and `avg_v_y`). We then slightly adjust the current boid's velocity by multiplying the difference vector (`avg_v_x` - `v_x`) by some coefficient `ALIGN_COEFF`. In simpler terms: if we take any vector for the center `c` that is comprised of a boid vector `a` + some difference vector `b`, then center `c` - boid `a` will produce a vector that points to the center `c` and away from boid `a`.
   4. `cohesion` method: finds the average of the positions of the boids close to the current boid (within `NEIGHBOR_RADIUS`) and then adjust current boid's velocity by difference between position of boid and position of center (multiplied by a `COHESION_COEFF`)
   5. `separation` method: if other boids are in in your `AVOID_RADIUS` (which often smaller than the `NEIGHBOR_RADIUS`), then find a `move` amount that is pointing away from the other boids. Multiply this `move` amount by a coefficient.
   6. `attract` method: for any reward on the map, if a boid is within its `ATTRACT_RADIUS`, then alter velocity to move toward the reward by a `REWARD_COEFF`.
   7. `check_vel` method: boids can keep getting faster and faster by increasing their velocities, especially in the presence of other boids. This method limits the velocity of each boid by use of a ratio `MAX_VELOCITY / sqrt(v_x^2 + v_y^2)` so that their velocity doesn't exceed the `MAX_VELOCITY`.
   8. `update` method will call the above methods:
      1. Align
      2. Cohesion
      3. Separation
      4. Attract
      5. Check Velocity
      6. Move
2. Reward class
   1. A reward has an `x`, `y`, and `radius` used to draw it on the screen. The `radius` is the attraction radius that will bring boids toward it.
3. Slider class
   1. A slider is used to alter the different coefficients listed above, to dynamically alter the simulation while its running.
   2. Sliders have a `x`, `y`, `w`, `h`, `min_val`, `max_val`, `start_val`, and `label`. These are used to plot the slider on the canvas (or surface), and to allow the user to choose a value within a range of values to alter the coefficients.
4. Main function
   1. Can handle: `quit` events, pressing `space` to pause the simulation, and slider input.
   2. Basic process:
      1. Draw the `reward`
      2. Update all `boids`
      3. Draw all `boids`
      4. Draw all `sliders`
      5. Update counter for number of steps iterated
      6. Tick the clock
      7. Restart the loop