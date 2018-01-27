# Agent-based Legislative Modeling
Simulations of legislatures with agent-based models in Python

## Description
Legislators within a majority and minority party are generated and mapped onto a one-dimensional euclidean space. A spatial voting model is assumed with legislators' ideal points (preferred policy outcomes) following a normal distribution at party means. A member will vote in favor a bill if the proposed policy point is within an "error" distance of their ideal point. A randomly selected legislator puts forth proposals at the point nearest to the median ideal within their acceptable range, and repeats this process until a bill is passed. Each time a vote is taken but the proposal does not pass, the "error" range of each member is increased as a fatigue factor. Majority party size, distance between party medians, and intraparty heterogeneity are altered to generate results across these variables and output to a .csv file. 

## Notes
To reduce computational time, this script use multi-core processing to run the simulation across different variables. Be sure to change the commented number in the `parallelize` function to match the number of processor cores the computer has in order to correctly start the multiprocessing pool.
