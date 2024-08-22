#install.packages("rvest")
library(rvest)

#Creating necessary directory strings
wrkdir <- getwd()
helpfunc<-paste0(wrkdir,"/","helpers/helpers_PlayerStats.R")
datafilepath<-paste0(wrkdir,"/","data/PlayerStats.csv")

#load necessary helper functions
source(helpfunc)

#Start timer
start.time <- Sys.time()


#store urls & info in a list
Team_Info<- list(BengalWarriors ="http://www.prokabaddi.com/teams/4-bengal-warriors-teamprofile",
                 BengaluruBulls ="http://www.prokabaddi.com/teams/1-bengaluru-bulls-teamprofile",
                 DabangDelhi ="http://www.prokabaddi.com/teams/2-dabang-delhi-teamprofile",
                 JaipurPinkPanthers ="http://www.prokabaddi.com/teams/3-jaipur-pink-panthers-teamprofile",
                 PatnaPirates = "http://www.prokabaddi.com/teams/6-patna-pirates-teamprofile",
                 PuneriPaltan = "http://www.prokabaddi.com/teams/7-puneri-paltan-teamprofile",
                 TeluguTitans ="http://www.prokabaddi.com/teams/8-telugu-titans-teamprofile",
                 UMumba ="http://www.prokabaddi.com/teams/5-u-mumba-teamprofile")

#Using lapply to extract data of all player in all teams
InterData<-lapply(names(Team_Info),GetPlayerurls,Team_Info)

#Collating all one team players into One data frame
InterData2<-lapply(InterData,function(x){do.call("rbind",x)})

#Collating all teams data into one data frame
FinalData<-do.call("rbind",InterData2)


#Writing Data to a .csv file
write.csv(FinalData,datafilepath,row.names = FALSE)

end.time <- Sys.time()
time.taken <- end.time - start.time
print(time.taken)

