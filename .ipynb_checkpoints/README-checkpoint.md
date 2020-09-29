# standup_graphs
A fun project aiming to create better mixed standup gorups - still very much a work in progress!


Previous standup groups were random but had a number of issues; they didn't promote good inter-team mixing, and they had to be manually checked over to ensure good grouping.

The new method has three main ideas behind it: 
1) Line managers can never be in the same group as their direct report
2) One and only one line manager needs to be in each group
3) Groups should prioritise mixing people together by taking prior groupings into account


The method works by using a graph to represent every mentor, with weighted edges corresponding to the number of previous interactions. To form a standup group we pick a node and then choose the 4 connected nodes with lowest weight.

Overview of the files:
* standups: loads the graph and generates new standups
* graph_setup: set up the inital graph and add historic standups to it
* standup_graphs.py: custom library of standup functions
* experimental_branch: testing ground for new features/big fixes
* graph_scratch: dummy model used for inital model development