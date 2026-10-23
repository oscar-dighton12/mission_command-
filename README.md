# Mission command- an interactive dashboard application 
# What is Mission command 
Mission command is a full stack, interactive and dynamic dashbaord application to analyze and display sales data from a csv file.
The program uses containization with Docker to ensure it is portable and can be used on other machines 
# Key features 
-data validation 
-interactive UI with dark mode 
-containerization
# Getting Started 
install python latest version
install and set up docker
# starting the program (option 1 )
1- cd into directory of the dashboard folder after downloading 
    cd dashboard 
2- set up docker with comamand 
    docker build -t mission-command .
3- once set up run command to start the docker application
    docker run -p 8050:8050 mission-command
4- click + Ctrl on the link for 
    http://127.0.0.1:8050
5- to end program, go into command line and press Ctrl + C 
6- if you want to terminate the docker container, terminate in the docker application or command

# tech stack 
-python(pandas)
-markdown languages
-javascript 
-ploty 
-docker 

# future expansions 
-incorporate machine learning to predict trends
-enable database integration to use dynamic data from server rather than static csv file. 
-automated unit testing 

# Author 
-Oscar Dighton 
-3rd year UCC student 

