
# Probability Calculator 

Hat class:
Takes a variable number of arguments each representing the number of balls of a color.
Draw method which removes random balls from the hat. 

experiment():
Takes a hat object, expected_balls object indicating the group of balls to attempt to draw from the hat, num_balls_drawn indicating the number of balls to draw each experiment, num_experiments indicating the number of experiements to perform. 
Returns an approximante probability of drawing the expected group of balls from the hat based on a number of experiments.

Example
```
hat = Hat(black=6, red=4, green=3)
probability = experiment(
    hat=hat,
    expected_balls={"red":2,"green":1},
    num_balls_drawn=5,
    num_experiments=2000
)

<!-- Returns -->
0.356
```

For the purpose of reviewing python to follow cse 312. 




