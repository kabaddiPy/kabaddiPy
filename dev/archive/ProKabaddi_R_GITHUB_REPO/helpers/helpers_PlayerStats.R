###########Functions used for TeamStats.R#############

#########Function to extract player URLS#####################

GetPlayerurls<-function(x,y){
    
    #extract the url of the Team Page
    tmp_url<-y[[x]]
    
    #Read the html into a variable
    TeamStats_Page<-read_html(tmp_url)
    
    #Team Name
    Team<-x
    
    #Getting player urls from the page
    TmpUrls<-TeamStats_Page%>%
             html_nodes(".box-content a")%>%
             html_attr("href")
    
    FinalUrls<-unique(TmpUrls)
    
    #Using lapply over extracted list of Urls to extract each player info
    
    PlayerData<-lapply(FinalUrls,GetPlayerData,Team)
    return(PlayerData)
       
}

#########Function to collate Individual Player Data#########

GetPlayerData<-function(x,y){
    
    #Adding required text to make it a http url
    ExactUrl = paste0("http://www.prokabaddi.com",x)
    
    #Reading player profile Page
    UrlPage<-read_html(ExactUrl)
    
    
    #Pull Player Name
    Player<-UrlPage %>%
            html_nodes(".squad-name span")%>%
            html_text()
    
    #Pull Player Type
    PlayerType<-UrlPage %>%
                html_nodes(".squad-title")%>%
                html_text()
    
    #Pull OVerAll Metrics
    TotalMatches<-GetPlayerMetricsVal(".stats-matchesplayed .stats-num", urlinfo = UrlPage)
    TotalPoints<-GetPlayerMetricsVal(".stats-totalpoints .stats-num", urlinfo = UrlPage)   
    TotalRaidPoints<-GetPlayerMetricsVal(".stats-raidpoints .stats-num", urlinfo = UrlPage)
    TotalDefencePoints<-GetPlayerMetricsVal(".stats-defencepoints .stats-num", urlinfo = UrlPage)
    
    TotalRaids<-GetPlayerMetricsVal(".stats-row2-col1 .stats-raid .stats-num", urlinfo = UrlPage)
    SuccRaids<-GetPlayerMetricsVal(".stats-row2-col1 .stats-successraids .stats-num", 
                                   urlinfo = UrlPage)
    UnSuccRaids<-GetPlayerMetricsVal(".stats-row2-col1 .stats-unsuccessraids .stats-num",
                                     urlinfo = UrlPage)
    EmptyRaids<-GetPlayerMetricsVal(".stats-emptyraids .stats-num", urlinfo = UrlPage)

    Tackles<-GetPlayerMetricsVal(".stats-row2-col2 .stats-raid .stats-num", urlinfo = UrlPage)
    SuccTackles<-GetPlayerMetricsVal(".stats-row2-col2 .stats-successraids .stats-num",
                                     urlinfo = UrlPage)
    UnSuccTackles<-GetPlayerMetricsVal(".stats-row2-col2 .stats-unsuccessraids .stats-num",
                                       urlinfo = UrlPage)    
    
    #Pull Cards Info
    GreenCards<-GetPlayerMetricsVal(".stats-greencard .stats-num", urlinfo = UrlPage)
    RedCards<-GetPlayerMetricsVal(".stats-redcard .stats-num", urlinfo = UrlPage)
    YellowCards<-GetPlayerMetricsVal(".stats-yellowcard .stats-num", urlinfo = UrlPage)
    
    PlayerUrl<-x
    Team<-y
    
    TmpData<-data.frame(Team,Player,PlayerType,PlayerUrl,
                        TotalMatches,TotalPoints,TotalRaidPoints,TotalDefencePoints,
                        TotalRaids,SuccRaids,UnSuccRaids,EmptyRaids,
                        Tackles,SuccTackles,UnSuccTackles,
                        GreenCards,RedCards,YellowCards, stringsAsFactors = FALSE)
    
    
    return(TmpData)
    
}

#### Function to extract Player Individual Metrics####################
GetPlayerMetricsVal<-function(x,urlinfo){
    
    TmpVal<-urlinfo%>%
        html_nodes(x)%>%
        html_text()%>%
        as.numeric()
    
    
}

