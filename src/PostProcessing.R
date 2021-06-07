
# windows wd
setwd("C:\\Users\\bg\\U of U\\Graduate Research\\DataAnalysisScripts\\Image-Analysis\\07112018")

# Linux wd
#setwd()

# Load files from directory

temp = list.files(pattern="*_processed.csv")
named.list <- lapply(temp, read.csv)

df <- data.frame()

for (i in 1:length(temp)) {
  
  fileString <- temp[i]
  
  temp.df <- named.list[i][[1]]
  
  valve <- readline(prompt=paste("Enter valve for", fileString, ":", sep=" "))
  flow <- readline(prompt=paste("Enter flow rate for", fileString, ":", sep=" "))
  
  temp.df$Valve <- rep(valve, nrow(temp.df))
  temp.df$flow.rate <- rep(flow, nrow(temp.df))
  
  df <- rbind(df, temp.df)
}

df$delta_time <- df$Delta_Index*0.25
df$Start_time <- df$Start_Index*0.25

df <- rbind(df, temp.df)
df <- subset(df, select = -X)
df <- subset(df, select = -Delta_Index)
df <- subset(df, select = -Start_Index)
# ask user to identify which valve
# output csv of all data