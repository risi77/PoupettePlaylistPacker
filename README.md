"""  
Poupette Playlist Packer  
Copyright (c) 2025 risi  
Licensed under the MIT License  
"""  
  
Welcome to  

# POUPETTE PLAYLIST PACKER

(la Poupette is my dog, she's the one preparing your playlists behind the scenes!)  

## Description

This script allows you to generate complex playlists from your scoresaber ranked scores!  

## Setup

fill out config.json like so :  
  
{  
    
  "PLAYER_ID": "76561198964267559",         <- your scoresaber ID  
    
  "I_PROMISE_IM_NOT_DDOSING": 0.2           <- how many seconds should the program wait after each request? I wouldn't recommend tinkering with it  
     
}
  
then take a look at my "EXAMPLE_PlaylistsSpecs.txt", and familiarize yourself with the spec system!  
"EXAMPLE_PlaylistsSpecs.txt" works like so:  
  
[something]       # A comment on what something does/ what to look out for  
                  # If the comment is too long, i will continue on the next line like so  
[someting else]     # A comment on something else...  
  
All the available metrics and options are showed off in the last example of "EXAMPLE_PlaylistsSpecs.txt".  
  
Proper formed JSONS look like what is found in "PlaylistsSpecs.json" when first downloaded.
I recommend you copy it in case something goes wrong and you need a fresh but not quite blank slate.
Don't put comments in your real JSONS, or the program will fail.

Note that "PlaylistsSpecs.json" comes with example playlists built-in, you can try running the examples first to check if everything is OK.  
  
Put your custom covers in ‘/Images/’ as PNGs or JPGs.  
  
Once you feel ready, you can edit PlaylistsSpecs.json and modify and add as many playlists as you wish!  
  
If the stock examples don't crash but your custom playlists crash; take a deep breath; checks those pesky commas, quote marks and bracket thingis,
They're most likely the culprits; They're very easy to mess up! Don't forget that everything is case-sensitive at the moment, so keeping one of
the examples close-by while making your playlists is heavily recommended.  
  
## Running

Once everything's good, lauch PoupettePlaylistPacker.exe, and it will automatically put together all the playlists described in "PlaylistsSpecs.json"
grab your playlists in Results/Playlists/[whatever the latest folder is]   
  

## Random stuff and Poupette ASCII art

Pretty messy code, it's my first actual piece of software and first executable  
Very much inspired by Hatopopvr's MyBSList (even more now than before, with the spec system)  
This project was originally only aimed at generating country rank playlists, but it grew to something very similar to MyBSList;  
And I hope I can make grow further for it to become the most extensive ranked playlist generator around!  
I already have Beatleader support in mind and have modified a good chunk of the code accordingly, but I wanted to get this version out first.

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
                             