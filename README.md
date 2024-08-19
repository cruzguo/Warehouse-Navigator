**Project Structure**
The project consists of three parts, each with its own set of challenges:

**Part A**: Basic Delivery
Objective: Implement an algorithm to pick up and deliver all boxes in the given order using a grid-based warehouse.

**Inputs:**

**warehouse_viewer:** A grid representation of the warehouse with walls (#), traversable spaces (.), boxes (0-9a-zA-Z), and a drop zone (@).
**dropzone_location:** Coordinates of the drop zone.
**todo:** List of boxes to be delivered in order.
**box_locations:** Dictionary mapping box characters to their locations.
Rules:

Robot can move in 8 directions and perform actions like picking up and putting down boxes.
Costs are associated with movements and actions (e.g., moving, lifting, dropping).
Your algorithm should minimize the total cost while accessing as few cells as possible.
Return: A list of moves in the format:

'move {d}'
'lift {x}'
'down {d}'
**Part B:** Single Box Delivery with Cost
Objective: Deliver a single box considering additional floor costs and without knowing the robot's starting location.

**Inputs:**

**warehouse:** Grid layout of the warehouse.
warehouse_cost: Grid of floor costs.
**todo:** Single box to deliver.
**Rules:**

Similar to Part A but includes floor costs and no surrounding walls.
Output two policies: one for picking up the box and another for delivering it.
**Return:** Two lists of lists representing the policies for:

To Box Policy
Deliver Box Policy
**Part C:** Stochastic Movements
**Objective:** Handle stochastic movements where the robot's intended direction may vary due to probabilistic outcomes.

**Inputs:**

Same as Part B, with an additional stochastic_probabilities parameter.
**Rules:**

Implement policies for picking up and delivering the box with stochastic movement probabilities.
Costs depend on the actual movement performed.
Return: Two lists of lists representing policies for:

To Box Policy
Deliver Box Policy
Setup
**Environment Test:**

Run python warehouse.py to check your setup.
Run python testing_suite_PartA.py (or B, C) to test your solution.
**Development:**

Use the provided testing suite to run specific test cases and debug your code.
**Visualization:**

Toggle visualization in visualizer.py for debugging and understanding the warehouse layout.
