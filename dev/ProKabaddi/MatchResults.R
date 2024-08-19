#loading library rvest
library(rvest)

#Creating necessary directory strings
wrkdir <- getwd()
helpfunc<-paste0(wrkdir,"/","helpers/helpers_MatchResults.R")
datafilepath<-paste0(wrkdir,"/","data/MatchResults.csv")

#load necessary helper functions
source(helpfunc)

#store urls & info in a list
Season_Info<- list(Season1 = "http://www.prokabaddi.com/season1-results",
                   Season2 =  "http://www.prokabaddi.com/season2-results",
                   Season3 = "http://www.prokabaddi.com/schedules-fixtures",
                   Season4 = "http://www.prokabaddi.com/season4-results")


#lapply over the list of URLs
InterData<-lapply(names(Season_Info),GetResults,Season_Info)

#Collating all the seasons Data
FinalData<-do.call("rbind",InterData)

#Writing to a .csv file
write.csv(FinalData,datafilepath,row.names = FALSE)





