#install.packages("rvest")
library(rvest)

#Creating necessary directory strings
wrkdir <- getwd()
helpfunc<-paste0(wrkdir,"/","helpers/helpers_TeamStats.R")
datafilepath<-paste0(wrkdir,"/","data/TeamStats.csv")

#load necessary helper functions
source(helpfunc)

#store urls & info in a list
Team_Info<- list(BengalWarriors ="http://www.prokabaddi.com/teams/4-bengal-warriors-teamprofile",
            BengaluruBulls ="http://www.prokabaddi.com/teams/1-bengaluru-bulls-teamprofile",
            DabangDelhi ="http://www.prokabaddi.com/teams/2-dabang-delhi-teamprofile",
            JaipurPinkPanthers ="http://www.prokabaddi.com/teams/3-jaipur-pink-panthers-teamprofile",
            PatnaPirates = "http://www.prokabaddi.com/teams/6-patna-pirates-teamprofile",
            PuneriPaltan = "http://www.prokabaddi.com/teams/7-puneri-paltan-teamprofile",
            TeluguTitans ="http://www.prokabaddi.com/teams/8-telugu-titans-teamprofile",
            UMumba ="http://www.prokabaddi.com/teams/5-u-mumba-teamprofile")


#using lapply to extract stats of all teams
InterData<-lapply(names(Team_Info),GetTeamStats,Team_Info)

#Combining all teams' dataframes into single
FinalData<-do.call("rbind",InterData)

#Writing Data to a .csv file
write.csv(FinalData,datafilepath,row.names = FALSE)



