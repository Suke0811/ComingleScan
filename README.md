# ComingleScan
 scan comingle rooms and collect jitsi speaker stats

Requirements: 
Libraries:
- panda
- selenium

Software:
- chromedriver.exe for the version of your chrome. 
Check your current chrome version, then download the corresponding chromedriver.


How to use: 
put room names to scan in 'other' string array.
This code will scan the rooms containing those strings. 
i.e. other = ['w1']. This will scan all rooms containing w1 in the room names.

Everytime it jumps into a room, it will ask you which iframe to scan. 
if you see two tabs in comingle screen (i.e. left: cocreate, right: jitsi), then enter 1.
If you only see jitsi, then enter 0.



Known issues:
- iframe search: 
	There was an issue searching list of iframes we have. It could be because I was searching at wrong or at a lower level than I should have searched. Currently, the code ask a user to specify which iframe we should scan. (left is index 0, right is index 1.)
- slow connection: 
	if connections or chrome is slow, this code may attempt to scan a page before loading. You can increase the sleep time. 
- Jitsi speaker stats reset: 
	Jitsi speaker stats get reset if a room becomes empty
- chromedriver.exe failed to launch chrome: 
	This is usually because your chrome browser get updated automatically, but your chromedriver.exe needs to be downloaded manually.