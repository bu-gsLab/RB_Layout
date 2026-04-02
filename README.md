Steps to run
1. Install Astral's uv
2. Run `uv sync`
3. Run main script
```
uv run main.py --radius 1100 --tol 50 --prune --visualize --row 2
```
Arguments
- `--radius` is the keepout radius (mm)
- `--tol` is the tolerance for the horizontal distance between the modules and keepout arc (mm). It will give you all results in this tolerance (if any), along with the 10 best results under tolerance. Best = more module PCBs.
- `--prune` is a boolean flag for removing duplicate results. Duplicate here means two rows with the same end modules and the inner ones are just permutated (e.g. M3 M3 M6 M7 = M3 M6 M3 M7).
- `--visualize` is a boolean flag for launching a pygame window for seeing the results visually. Scroll through the results using left and right arrow keys. Results will be printed to console regardless.
- `--row` is the index of the row you wish to optimize (between 0 and 25). If the entire top/bottom side of the PB/RB lies outside the keepout radius, it will throw a value error (happens frequently for top and bottom rows).

The visualizer might be a little buggy, especially the keepout circle that get's overlaid. The numbers should be trustworthy though.

All the relevant dimensions are stored in the `dimensions.yaml` file. This file contains all the dimensions of the boards, along DEE layout measurements. Everything pulls from this file.