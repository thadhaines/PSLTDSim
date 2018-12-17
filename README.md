# LTD_sim
Using Ironpython, communicate with PSLF to simulate longterm dynamics.
## Current Progress:
Code creates python mirror of PSLF generators, loads, and busses.
Various functions have been written to check accuracy of mirror and 
output to terminal.
### Results:
For smaller test cases with only 1 Slack generator, the mirror seems to be 
accurate, however, for the full WECC (with 84 Slack generators), the global
system lack has yet to be identified programmatically.
