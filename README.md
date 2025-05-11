"""
Poupette Playlist Packer
Copyright (c) 2025 risi
Licensed under the MIT License
"""

Welcome to

######################################################################################################################################################
#   ____   __   _  _  ____  ____  ____  ____  ____        ____  __     __   _  _  __     __   ____  ____        ____   __    ___  __ _  ____  ____   #
#  (  _ \ /  \ / )( \(  _ \(  __)(_  _)(_  _)(  __)      (  _ \(  )   / _\ ( \/ )(  )   (  ) / ___)(_  _)      (  _ \ / _\  / __)(  / )(  __)(  _ \  #
#   ) __/(  O )) \/ ( ) __/ ) _)   )(    )(   ) _)        ) __// (_/\/    \ )  / / (_/\  )(  \___ \  )(         ) __//    \( (__  )  (  ) _)  )   /  #
#  (__)   \__/ \____/(__)  (____) (__)  (__) (____)      (__)  \____/\_/\_/(__/  \____/ (__) (____/ (__)       (__)  \_/\_/ \___)(__\_)(____)(__\_)  #
#                                                                                                                                                    #
######################################################################################################################################################

(la Poupette is my dog, it's the one preparing your playlists behind the scenes!)

This script allows you to get a snipe playlist of all your scores below a "target" in your country leaderboard!
Playlist is pooped out in the folder the executable is in, just move it to your playlists folder!

fill out config.json like so, and lauch PoupettePlaylistPacker.exe :

{
  "PLAYER_ID": "76561198964267559",         <- your scoresaber ID
  "MAX_MAPS": -1,                           <- leave at -1 for full scan (how many ranked or unranked maps get scanned)
  "SORT": "recent",                         <- do you want your playlist to be ranked by recent ("recent") plays or top ("top") plays
  "TARGET": 1                               <- what rank would ou like to achieve on all maps? (1 or greater)
  "I_PROMISE_IM_NOT_DDOSING": 0.3           <- how many seconds should you wait after each request? I wouldn't recommend lowering it
  "CHECK_SCORESABER": True                  <- do you want to call scoresaber's api (true) or make playlists based on previous data (false). The program has to be run at least once with true, and running it with false is faster but might produce out of date results
  "last_refresh": "0"                       <- don't mess with it, it's simply a handy saved value for future uses.
}

Put a ‘cover.png’ image in the same folder if you think you have a good cover...
...you really can't compete though


Very messy code, half french half english, it's my first actual piece of software and first executable
Very much inspired by Hatopopvr's MyBSList

                ++#*%#-                                  
           +=+*#*+%@%%*#*====+--:---+%*%=                
         =+*#%%#%%@%%+%%++*#+=*=-=+=##%*%%%+             
         #%@#%=%@@%%*+**#%#*++#+*%#+%%%%+%%%#+-          
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
                                 %%%###      
                             
I guess:

MIT License

Copyright (c) 2025 risi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.