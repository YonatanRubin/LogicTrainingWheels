# LibreOffice Proof Sheet 
This sheet is designed to allow for quick trial and error of proofs, helping students to learn the ropes while keeping a neat and tidy workflow. 
Unfortunately, since it was written for the personal usage of the (lazy) writer so most of the magic here is automatically filling the assumptions and the following required showlines. 
Of course this might be less then ideal for students wanting to use it to learn them for the first time, so maybe consider not using it until you've got a better practice with those rules.

## Installation
To install you first need to install libreoffice of course.  
There are two ways, in any case after installing it is recommended to follow "Optimize workflow"

### The lazy way
**WARNING: THIS IS NOT RECOMMENDED AND MIGHT BE A SECURITY RISK**
download the `logic.ods` file and open it. You will get some errors and warnings about using macros. To silence them:  
1. Open `Tools->Options->LibreOffice->Security->Macro Security`
2. Change security level to `Low`
3. Save and restart
### The better way
download the `logic.ods` file and open it. We will install the macros globally. 
1. Open `Tools->Macros->Organize Macros->Basic`
2. in the opened window click again on `Organizer` (for unknown reason there is an organizer inside the organizer)
3. You should see a section called `My Macros` with a folder named `Standard` underneath. There should also be the `logic.ods` file and a folder `Standard` underneath, with two files underneath.
4. Drag and drop each file (separately) from `logic.ods/Standard` to `My Macros/Standard`
5. close and restart 

### Optimize workflow
To optimize the workflow you should probably save the `logic.ods` file as a template. 
1. Select `File->Templates->Save as Template`
2. Choose a name and save it 

If you use caps lock (or the keyboard provided by this library) then you would probably want a quick way to change the casing on the code. 
#### To add as menu item
1. Select `Tools->Customize`
2. In the `Target` select which menu you want the action to appear (I recommend `Format | Text`)
3. In `Category` select `Macros`. Search the command `CustomCase`, right click and press `Add`
4. Move to the position you would like it 
5. Optional: change the name to a more intuitive name such as `Logic Case`
#### To add as a keyboard shortcut
1. Select `Tools->Customize` 
2. Select `Keyboard`
3. In the `Shortcut Keys` section select the desired shortcut.
4. In the `Category` section scroll down and open `Application Macros`, Find the location where you installed the macros and select `Casing`
5. Select `CustomCase` and press `Modify` 

## How to use this spreadsheet 
First copy the exercises from the book to the `H` column. The `F` column removes the exercise number and the spaces between letters (since they are not part of the language). It can support up to 20 exercises, if you need more simply extend the formula from `F20` downwards.  
Now in the `A` column select your exercise using by calling the cell in F referencing the exercise (for example `=F1`).  

From here it is mostly your own job - solve the exercise. 
**TBD**: integrate the verification script as a macro to integrate the verification in the proof workflow 
