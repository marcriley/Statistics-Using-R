# Assignment: ASSIGNMENT Scores
# Name: Riley, Marc
# Date: 2021-04-9


install.packages("ggplot2")
install.packages("pastecs")
install.packages("psych")
library(pastecs)
library(ggplot2)
library(psych)

## Set the working directory to the root of your DSC 520 directory
setwd("C:/Users/Daffy/OneDrive/Documents/DSC520")

## Load the `data/r4ds/heights.csv` to
scores_df <- read.csv("scores.csv")

#What are the observational units in this study?
str(scores_df)
#Scores, section, and count are the observational units

#Identify the variables mentioned in the narrative paragraph and determine which are categorical and quantitative?
#Count and score are quantitative section is categorical.

#Create one variable to hold a subset of your data set that contains only the Regular Section and one variable for the Sports Section.
SP=subset(scores_df,Section=="Sports")
head(SP)

RE=subset(scores_df,Section=="Regular")
head(RE)

#Use the Plot function to plot each Sections scores and the number of students achieving that score. Use additional Plot Arguments to label the graph and give each axis an appropriate label. Once you have produced your Plots answer the following questions:
Score1=SP[,2]
Score2=RE[,2]
par(mfrow=c(2,1))
plot(Score1, xlab="# students", ylab="Score", main="Sports")
plot(Score2, xlab="# of students", ylab="Score", main="Regular")
describe(SP)
describe(RE)