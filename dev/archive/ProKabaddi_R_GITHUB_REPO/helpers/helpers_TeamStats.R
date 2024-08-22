###########Functions used for TeamStats.R#############

GetTeamStats<-function(x,y){
    
    #extract the url of the Team Page
    tmp_url<-y[[x]]
    
    #Read the html into a variable
    TeamStats_Page<-read_html(tmp_url)
    
    #Team Name
    Team<-x
    
    #Pull OVerAll Metrics
    TotalMatches<-GetMetricsVal(".stats-total .stats-num", urlinfo = TeamStats_Page)
    Wins<-GetMetricsVal(".stats-wins .stats-num", urlinfo = TeamStats_Page)   
    Losses<-GetMetricsVal(".stats-losses .stats-num", urlinfo = TeamStats_Page)
    Draw<-GetMetricsVal(".stats-draw .stats-num", urlinfo = TeamStats_Page)
    
    #Pull Raid Metrics
    TotalRaids<-GetMetricsVal(".stats-row2 .si-table-tr:nth-child(1) .stats-num span",
                              urlinfo = TeamStats_Page)
    SuccRaids<-GetMetricsVal(".stats-row2 .active .stats-num span",
                             urlinfo = TeamStats_Page)
    UnSuccRaids<-GetMetricsVal(".stats-row2 .active+ .si-table-tr .stats-num span",
                               urlinfo = TeamStats_Page)
    
    EmptyRaids<-GetMetricsVal(".active~ .si-table-tr+ .si-table-tr .stats-num span",
                              urlinfo = TeamStats_Page)    
    
    TmpString1<-TeamStats_Page%>%
                html_nodes(".raid-graph .graph-value")%>%
                html_text()
    
    SuccRaidRate<-as.numeric(substr(TmpString1,1,nchar(TmpString1)-1))/100
    
    #Pull Tackle Metrics
    
    SuperTackles<-GetMetricsVal(".stats-row3 .si-table-tr:nth-child(1) .stats-num span",
                                urlinfo = TeamStats_Page)
    SuccTackles<-GetMetricsVal(".stats-row3 .active .stats-num span",
                               urlinfo = TeamStats_Page)
    UnSuccTackles<-GetMetricsVal(".stats-row3 .active+ .si-table-tr .stats-num span",
                                 urlinfo = TeamStats_Page)
    
    TmpString2<-TeamStats_Page%>%
                html_nodes(".tackle-graph .graph-value")%>%
                html_text()
       
    SuccTackleRate<-as.numeric(substr(TmpString2,1,nchar(TmpString2)-1))/100    
    
    #Pull Cards Metrics
    GreenCards<-GetMetricsVal(".stats-greencard .stats-num",
                              urlinfo = TeamStats_Page)
    RedCards<-GetMetricsVal(".stats-redcard .stats-num",
                              urlinfo = TeamStats_Page)
    YellowCards<-GetMetricsVal(".stats-yellowcard .stats-num",
                              urlinfo = TeamStats_Page)
    
    TmpData<-data.frame(Team,TotalMatches,Wins,Losses,Draw,
                            TotalRaids,SuccRaids,UnSuccRaids,EmptyRaids,SuccRaidRate,
                            SuperTackles,SuccTackles,UnSuccTackles,SuccTackleRate,
                            GreenCards,RedCards,YellowCards, stringsAsFactors = FALSE)
                      
    
    return(TmpData)
    
}

####function to pull metrics at  node element###############
GetMetricsVal<-function(x,urlinfo){
    
    TmpVal<-urlinfo%>%
            html_nodes(x)%>%
            html_text()%>%
            as.numeric()

    
}