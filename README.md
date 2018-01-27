# Agent-based Legislative Modeling
Simulations of legislatures with agent-based models in Python

## Description
Legislators within a majority and minority party are generated and mapped onto a one-dimensional euclidean space. A spatial voting model is assumed with legislators' ideal points (preferred policy outcomes) following a normal distribution at party means. A member will vote in favor a bill if the proposed policy point is within an "error" distance of their ideal point. A randomly selected legislator puts forth proposals at the point nearest to the median ideal within their acceptable range, and repeats this process until a bill is passed. Each time a vote is taken but the proposal does not pass, the "error" range of each member is increased as a fatigue factor. Majority party size, distance between party medians, and intraparty heterogeneity are altered to generate results across these variables and output to a .csv file. R is used to run linear regressions and create exploratory visualizations with `ggplot2`.

## Results
Note: in these simulations, the majority party is mapped to have ideal points greater than 0, while the minority party is mapped to have ideal points less than 0.

### Majority Party Size
When comparing the initial values of bills passed, there is a split at 0 (correlating to a ﬁnal value around the 0.25-0.3 point), with values less than this requiring a relatively large (greater than 40) number of votes to pass, while instances after this point typically require less than 20 votes to pass. This distinction is not particularly clear until the majority party size approaches values near 60, and as the majority party size grows past this point, the separation between these two groups become slightly more distinct. Statistically signiﬁcant results were found when running linear regressions only on the group with initial values greater than 0. Though this result may have been somewhat expected, it suggests as the size of the majority party grows, it becomes easier to pass bills that are closer to the majority party’s preference, while harder to pass bills of the minority party’s preference. A deciding split is at 0, the mean of the party medians.
 
![majpartysize](https://github.com/joseph-stigall/agent-based-legislatures/blob/master/visualizations/size.png "Majority Party Size")
![majpartysize2](https://github.com/joseph-stigall/agent-based-legislatures/blob/master/visualizations/size2.png "Majority Party Size 2")

### Distance Between Medians
The initial value threshold point of 0 (correlating to a ﬁnal value of around 0.28) is again relevant here in an interesting way. For the subset of bills with an initial value less than 0, distance between party median and number of votes needed to pass have a near-perfect positive linear relationship. Bills with a initial value greater than zero do not seem to have strong results; they have a statistically signiﬁcant negative relationship when running a regression, but a relatively low R2 value. In pratical application, this suggests that increased polarization between parties has strong negative consequences, but only for the minority party. Especially since these simulations were ran with only a 1 member diﬀerence between the two parties, this stark diﬀerence is notable. 

![medians](https://github.com/joseph-stigall/agent-based-legislatures/blob/master/visualizations/median.png "Distance Between Party Medians")
![medians2](https://github.com/joseph-stigall/agent-based-legislatures/blob/master/visualizations/medians2.png "Distance Between Party Medians 2")

### Intraparty Homogeneity
When the parties are high homogenous within themselves (st. dev < .05), the majority party has a clear advantage. However, as more variance is seen, this advantage exists less and less. 

![homogeneity](https://github.com/joseph-stigall/agent-based-legislatures/blob/master/visualizations/homogeneity.png "Intrparty Homogeneity")
