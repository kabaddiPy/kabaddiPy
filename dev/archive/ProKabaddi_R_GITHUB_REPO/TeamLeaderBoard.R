#install.packages("rvest")
library(rvest)

#Creating necessary directory strings
wrkdir <- getwd()
helpfunc<-paste0(wrkdir,"/","helpers/helpers_TeamLeaderBoard.R")
datafilepath<-paste0(wrkdir,"/","data/TeamLeaderBoard.csv")
    
#load necessary helper functions
source(helpfunc)

#store urls & info in a list
kabaddi_info <- list(Season1 = "http://www.prokabaddi.com/season1-leaderboard", 
                     Season2 = "http://www.prokabaddi.com/leaderboard",
                     Season3 = "http://www.prokabaddi.com/season3-leaderboard",
                     Season4 = "http://www.prokabaddi.com/season4-leaderboard")


#Defintions of various metrics
Metrics_Info<-list(SuccRaids = 13,                #Succesful Raids
                   RaidPoints = 14,               #Raid Points
                   SuccTack = 15,                 #Successful Tackles     
                   SuccRaidsPerMatch = 16,        #Successful Raids Per Match
                   SuccRaidPer = 17,              #Successful Raid Percent
                   SuccTackPerMatch = 18,         #Successful Tackles Per Match
                   SuccTackPer = 19,              #Successful Tackle Percent
                   SuperTack  = 20)               #Super  Tackles

nameslist<-as.list(names(Metrics_Info))
names(nameslist)<-names(Metrics_Info)

InterData<-lapply(nameslist,GetMetricPlayerData,
                               y = Metrics_Info, 
                               urldata = kabaddi_info,
                               namesurldata = names(kabaddi_info))   

##Collate all seasons data into one data frame
InterData2<-lapply(InterData,function(x){do.call("rbind",x)})

#Removing unnecessary row.names columns
FinalData<-do.call("rbind",InterData2)
row.names(FinalData)<-NULL


#Writing to a .csv file
write.csv(FinalData,datafilepath,row.names=FALSE)
