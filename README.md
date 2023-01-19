# GIST Identity validation
As part of the cnp team, we manage multiple services for our clients, one of them are the Identity validation tickets.

Everytime a glober tries to login to the work profile on a new mobile device, we need to establish a videoconference with them in order to validate their identity.

If the glober doesn't answer, we must close the tickets in two platforms: Invgate and google admin.

## Motivation
As the work is repetitive, an opportunity to automate it was considered, in order to optimize time management and be able to focus on more important tasks while the script is running.

## What does the script do?
Basically the script closes the tickets in both platforms, helped by selenium, an automated open-source tool which help us interact with the browser(in this case google chrome).

Once logged in, the script saves a list with all of the emails of the Identity validation tickets that the user has assigned.
After that, it executes a series of steps:

### Invgate
-Open the ticket

-Charge the time(5 min)

-Update the ticket status("Glober no respondió")

-Close the ticket

### Google admin
-Open a new tab

-Log into the platform

-look for pending devices

-Based on the file which contains the mails, delete each user from the platform

**It is important to be aware when the script finish closing tickets on invgate as it will ask for MFA in order to log into google admin. If the user doesn't approve the MFA, the script will finish for security reasons, anyway, a backup of the mails will be saved in case the script is executed again.**

## Installation
the first requirement is to have python installed, in case you don't have it, you can download it here:

https://www.python.org/downloads/

-open the CMD, powershell or command line interface.

-with the following command, locate into the project folder:

    cd project_folder_path

-with the following command, install all of the requirements included in the "requirements.txt" file:

    pip install -r requirements.txt

Example: 

![image](https://user-images.githubusercontent.com/118286467/207648865-e4474266-fdc3-4ac6-b3ca-96235cdc4f06.png)
