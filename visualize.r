###########################################################
# Accompanying exploratory visualizations in ggplot2
#
# Joseph Stigall
###########################################################

library(ggplot2)
library(stargazer)

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
    # passes through ggplot objects and display in a grid
    
    require(grid)
    # Make a list from the ... arguments and plotlist
    plots <- c(list(...), plotlist)
    numPlots = length(plots)
    # If layout is NULL, then use 'cols' to determine layout
    if (is.null(layout)) {
        # Make the panel
        # ncol: Number of columns of plots
        # nrow: Number of rows needed, calculated from # of cols
        layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                         ncol = cols, nrow = ceiling(numPlots/cols))
    }
    if (numPlots==1) {
        print(plots[[1]])  
    } else {
        # Set up the page
        grid.newpage()
        pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
        
        # Make each plot, in the correct location
        for (i in 1:numPlots) {
            # Get the i,j matrix positions of the regions that contain this subplot
            matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
            print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row, 
                                          layout.pos.col = matchidx$col))
        }
    }
}

###########################################
#Majority Party Size
###########################################

#Read and Clean Data
party_size <- read.csv("simulation_output/output_party_size.csv", colClasses= 
                         c("numeric","numeric","numeric", "numeric", "numeric", "numeric",
                           "numeric","numeric","numeric","numeric"))
party_size <- party_size[,c(2,3,4,5,6)]

#Generate Main Plot
ps_main <- qplot(Majority.Party.Size, Number.of.Votes, data= party_size, color= Initial.Value)+ 
  labs(title="Comparison between Majority Party Size and Number of Votes",
  x = "Majority Party Size",y="Number of Votes", color = "Vote Initial Value") +
  ylim(0,70)

#Linear Regression Models
ps_1.lm <- lm(Number.of.Votes~ Majority.Party.Size, data=subset(party_size,Initial.Value <=0))
ps_2.lm <- lm(Number.of.Votes~ Majority.Party.Size, data=subset(party_size,Initial.Value >0))
summary(ps_1.lm)
summary(ps_2.lm)

#Secondary Plots
ps_1 <- qplot(Majority.Party.Size, Number.of.Votes, data= subset(party_size, Initial.Value <=0 )) +
  labs(title="Initial Value <= 0", x = "Majority Party Size",y="Number of Votes") +
  ylim(0,70) + stat_smooth(method= "lm")

ps_2 <- qplot(Majority.Party.Size, Number.of.Votes, data= subset(party_size, Initial.Value >0)) +
  labs(title="Initial Value > 0 ", x = "Majority Party Size",y="Number of Votes") +
  ylim(0,70) + stat_smooth(method= "lm")

#Show Plots
ps_main
multiplot(ps_1,ps_2)

###########################################
#Party Distance
###########################################

#Read and Clean Data
party_distance <- read.csv("simulation_output/output_party_distance.csv", colClasses= 
                             c("numeric","numeric","numeric", "numeric", "numeric", "numeric",
                               "numeric","numeric","numeric","numeric"))
party_distance <- party_distance[,c(2,3,4,5,7)]

#Generate Main Plot
pd_main <- qplot(Distance.between.Medians, Number.of.Votes, data= party_distance, color= Initial.Value)+ 
  labs(title="Comparison between Median Distance and Number of Votes", 
  x = "Distance Between Medians",y="Number of Votes", color = "Vote Initial Value Interval") +
  ylim(0,100)

#Linear Regression Models
pd_1.lm <- lm(Number.of.Votes ~ Distance.between.Medians, data= subset(party_distance, Initial.Value <=0))
pd_2.lm <- lm(Number.of.Votes ~ Distance.between.Medians, data= subset(party_distance, Initial.Value >0))
summary(ps_1.lm)
summary(ps_2.lm)

#Secondary Plots
pd_1 <- qplot(Distance.between.Medians, Number.of.Votes, data= subset(party_distance, Initial.Value <= 0)) +
  labs(title="Initial Value <= 0", x = "Distance Between Medians",y="Number of Votes") +
  ylim(0,100) + stat_smooth(method="lm")

pd_2 <- qplot(Distance.between.Medians, Number.of.Votes, data= subset(party_distance, Initial.Value > 0)) +
  labs(title="Inital Value > 0", x = "Distance Between Medians", y="Number of Votes") +
  ylim(0,100) + stat_smooth(method="lm")

#Show Plots
pd_main
multiplot(pd_1,pd_2)

###########################################
#Intraparty Homogeneity
###########################################

#Read and Clean Data
party_homogeneity <- read.csv("simulation_output/output_intraparty.csv", colClasses= 
                             c("numeric","numeric","numeric", "numeric", "numeric", "numeric",
                               "numeric","numeric","numeric","numeric"))
party_homogeneity <- party_homogeneity[,c(2,3,4,5,8)]
names(party_homogeneity)[names(party_homogeneity)=="Majority.St..Dev."] <- "Homogeneity"

#Generate and show main plot
ph_main <- qplot(Homogeneity, Number.of.Votes, data= party_homogeneity , color= Initial.Value)+ 
  labs(title="Comparison between Intraparty Homogeneity and Number of Votes ", 
  x = "Intraparty Homogeneity(St. Dev)",y="Number of Votes", color = "Vote Initial Value Interval")+
  ylim(0,70)

ph_main
