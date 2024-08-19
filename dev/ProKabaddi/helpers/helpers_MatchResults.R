###########Functions used in MatchResults.R#############
GetResults<-function(x,y){
    
    #extract the url of the Team Page
    tmp_url<-y[[x]]
    
    #Read the html into a variable
    Results_Page<-read_html(tmp_url)
    
    #Season Name
    SeasonId<-x
    
    #Extract Participating Teams
    
    Team1<-Results_Page %>% 
        html_nodes("div.si-table-tr.prematch.schData")%>%
        html_attr("data-teama")    
    
    Team2<-Results_Page %>% 
        html_nodes("div.si-table-tr.prematch.schData")%>%
        html_attr("data-teamb")    
    
    
    #Extract Date, Time and Venue
    
    MatchDate<-Results_Page %>% 
        html_nodes("div.si-table-td.tblfxdate>div.datetime>span.date")%>%
        html_text()%>%
        as.Date("%B %d %Y")    
    
    MatchTime<-Results_Page %>% 
        html_nodes("div.si-table-td.tblfxdate>div.datetime>span.time")%>%
        html_text()
    
    MatchVenue<-Results_Page %>% 
        html_nodes("div.si-table-td.tblfxdate>div.venue>span")%>%
        html_text()    
    
    
    #Extract MatchNo and Scores Information
    
    MatchId<-Results_Page %>% 
        html_nodes("div.si-table-td.tblfxinfo>h3")%>%
        html_text()    
    
    Team1Score<-Results_Page %>% 
        html_nodes("div.si-table-td.tblfxinfo>div.team-detail-box
                       >div.team.team-a>span.team-scores")%>%
        html_text()%>%
        as.numeric()
    
    Team2Score<-Results_Page %>% 
        html_nodes("div.si-table-td.tblfxinfo>div.team-detail-box
                       >div.team.team-b>span.team-scores")%>%
        html_text()%>%
        as.numeric()
    
    if(SeasonId == "Season3")
        MatchResult<- rep("Not Completed", times = length(Team1))
        
    else
        
        MatchResult<-Results_Page %>% 
            html_nodes("div.si-table-td.tblfxstatus>div.postmatch-box>p")%>%
            html_text()
  
   
    
    #Combine all the vectors to make a temporary dataframe
    
    tmpdataframe<-data.frame(SeasonId,MatchId,Team1,Team2,Team1Score,Team2Score,
                             MatchResult,MatchVenue, MatchDate, MatchTime,
                             stringsAsFactors = FALSE)
    
    return(tmpdataframe)
    
}