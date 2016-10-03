# PyPio
Various scripts automating use of PioSolver, a postflop Nash Equilibrium solver for NLHE.

# piochoose
runs a bunch of specified scripts for a number of steps, chooses best and discards rest, proceeds to run the chosen one deep.

typical use case: we want to compare several versions of a tree - for example different sizing options or inclusion/exclusion of a strategic option - and keep the one which is best from the viewpoint of the player whose strategic options we are considering.

as EV converges much faster than the full strategy, it makes no sense to run full calculation for each version of the tree. piochoose helps automate this process to facilitate learning and ensure effective use of CPU time.

Requires: PioSolver pro/edge
