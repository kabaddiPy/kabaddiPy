###########Functions used for Scrape_PlayerLeaderboard.R#############

#Functions to Scrape Season Data from LeaderBoard

GetSeasonData<-function(x,y,iden,mname){
    
    tmp_id <- paste0("'",iden,"'")
    urlinfo<-read_html(y[[x]])
    
    #Extract Player Name
    Name<-urlinfo %>% 
        html_nodes(paste0("div.si-table-tr[data-shortid = ",tmp_id,"]",
                          "> div.si-table-td.tbl-player",
                          "> div.player-info > span.player-name"))%>%
        html_text()
    
    #Extract Player Values
    Value<-urlinfo %>% 
        html_nodes(paste0("div.si-table-tr[data-shortid = ",tmp_id,"]",
                          "> div.si-table-td.tbl-raids>span"))%>%
        html_text()%>%
        as.numeric()
   
    Metric = rep(mname,each =length(Name))
    SeasonId = rep(x,each = length(Name))
    
    tmpdataframe<-data.frame(SeasonId,Metric,Name,Value,
                             stringsAsFactors = FALSE)
    
    return(tmpdataframe)
}


#Function to iterate over various metrics

GetMetricPlayerData<-function(x,y,urldata,namesurldata){
    
    metricid<-y[[x]]
    metricname<-x
    
    z<-lapply(namesurldata,GetSeasonData,urldata,iden = metricid,
              mname = metricname)
    return(z)
}



############################################################################

