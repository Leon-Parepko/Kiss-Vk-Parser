'''
User config class is used
for login() function, also
it saves your verification code
in ver_code variable.
'''
class User:
    login = 'YOUR_LOGIN'
    password = 'YOUR_PASS'
    ver_code = 0


'''
This class store all the
google drive authorisation
parameters. 
* NOTE: your token file should be 
    in project root directory
    and named "client_secret.json". 
'''
class Drive:
    secret = 'client_secret.json'
    name = 'drive'
    version = 'v3'
    scopes = ['https://www.googleapis.com/auth/drive']


'''
This class contains all
the project settings.
** OS=<str> - depending on machine OS type
    ("unix" or "win"), this application
    might be open in virtual screen 
    mode (on unix typed).
    
** V_SCREEN_RES=[<int>, <int>] - change 
    resolution of virtual 
    screen (only on UNIX!).
    
** ITER_DELAY=<int> - regulates delay between
  every iteration (in minutes, default = 0). 
  It did not affect on overall code performance.
  
** OVERALL_DELAY=<int> - regulates inner code
  delay (works as multiplier, default = 1). 
  IT AFFECTS ON OVERALL CODE PERFORMANCE!
  increase it in case you have slow 
  internet connection or low performance PC.  

** UPLOAD_TIME=<str> - regulates the time
  of archive upload on google drive.
  SYNC BY OS TIME!
  String format is: "H:M - H:M"  
'''
class Settings:
    os = 'Unix'
    v_screen_res = [1920, 1080]
    iter_delay = 60
    overall_delay = 2
    upload_time = '05:00 - 07:00'
