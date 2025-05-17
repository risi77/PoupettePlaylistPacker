"""  
Poupette Playlist Packer  
Copyright (c) 2025 risi  
Licensed under the MIT License  
"""  
  
Welcome to  

# POUPETTE PLAYLIST PACKER

(la Poupette is my dog, she's the one preparing your playlists behind the scenes!)  

## Description

This script allows you to get a snipe playlist of all your scores below a "target" in your country leaderboard!  
Playlist is pooped out in the folder the executable is in, just move it to your playlists folder!  

## Setup

fill out config.json like so, and lauch PoupettePlaylistPacker.exe :  
  
{  
    
  "PLAYER_ID": "76561198964267559",         <- your scoresaber ID  
    
  "MAX_MAPS": -1,                           <- leave at -1 for full scan (how many ranked and unranked maps get scanned)  
    
  "COUNTRYRANK_MAJORSORT": true,            <- do you want your playlist to be sorted by ascending country rank (true), or let the other sort do it's job (false)?  
    
  "SORT": "recent",                         <- do you want your playlist to be sorted by recent ("recent") plays or top ("top") plays. If "COUNTRYRANK_MAJORSORT" is set to true, this will have practically no effects.  
    
  "TARGET": 1                               <- what rank would ou like to achieve on all maps? (1 or greater)  
    
  "CHECK_SCORESABER": true                  <- do you want to call scoresaber's api (true) or make playlists based on previous data (false). The program has to be run at least once with true, and running it
  with false is faster but might produce out of date results  
    
  "CHECK_NEW_MAPS": true,                   <- do you want to check your profile for scores on new maps (true) or only refresh your ranks on already known maps (false). The program has to be run at least once with true, and running it with false is faster but might produce out of date results  
    
  "I_PROMISE_IM_NOT_DDOSING": 0.2           <- how many seconds should you wait after each request? I wouldn't recommend lowering it  
    
  "last_refresh": "0"                       <- don't mess with it, it's simply a handy saved value for future uses.  
    
}  
  
Put a ‘cover.png’ image in the same folder if you think you have a good cover...  
...you really can't compete though

## random stuff and Poupette ASCII art

Very messy code, half french half english, it's my first actual piece of software and first executable  
Very much inspired by Hatopopvr's MyBSList  
Omg I managed to fail at the only important part of this script: getting country rank; now it shouldn't be modulo 12

                ++#*%#-                                  
           +=+*#*+%@%%*#*====+--:---+%*%=                
         =+*#%%#%%@%%+%%++*#+=*=-=+=##%*%%%+             
         %%@#%=%@@%%*+**#%#*++#+*%#+%%%%+%%%#+-          
          =@%%%%%%%#+*####%*+*%***#*+#%%%#%%%%#%         
           +**+===*##**#*#%+*#%%*+===###%%%%%@%          
           +=--**##+#####%%+*#%#**####*+###%%%           
          -=-=%%#%*#%%%%%%%###%%%%#%#%%#*+#**#           
          -++=%%%***%%%%%%#####%%#*++*###*+#*            
          -%*=+#**%*%%###########%#*+*%%##=%*            
          =#*==*##+=+=+*++++#############**%#            
          *#*==##*====-=========+##*####*##%%            
          =*+**+=:-----===**++++==**#######%*            
          =%**+#---===+++######***++*####**%             
           =#=+-==++*##%%%######*##*++#+#*#+             
            +++-:=*##%%%*%%%*######**+#+#**              
             =-==#%%#*#*%%###*######*+=#*                
             ---=*%%%%%%%%%%%#######**+##                
            #%===##%%#%%%%%#%%##*#*#**+*                 
            --=**##%%%%%#%%##########***#                
            ===*#%%%%%%%%%%%##*########+*                
            =%=###%%%%****#****######****                
             +*%#%%%*****##******#####*#*%               
              ##%%*******##*********#######                
                                 ****##      
                             