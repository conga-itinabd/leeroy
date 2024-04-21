# leeroy 0.0.1
Jenkins Pipeline Manager

With Leeroy, you can run jobs from the terminal and store their parameters for execution.

### General benefits of Leeroy:
 - Fast build launches from the command line.
 - Storage of regular job parameters in one place.

### Who Leeroy is suitable for:
 - For DevOps engineers:  
speeds up the process of creating and debugging pipelines.
 - For users:  
eliminates the need to save tabs in the browser and remember/write down personal parameters.

### Current capabilities of Leeroy:
 - Job execution.
 - Running a sequential chain of jobs.
 - Iterative job execution.
 - Fetching logs based on a template from "/console".
 - Counting specific logs from "/console".
 - Passing caught logs as parameters for the next job execution.

### What Leeroy cannot do yet but will soon be able to:
 - Running jobs with active choice parameters.
 - Fetching logs from pre-built builds.
 - Performing a classic rebuild.

### Possible future additions:
 - Secret management.
 - Folder management.
 - Quick templates for pipeline creation.

# Quick Start:

##### Important to note:
 - Leeroy does not support jobs with active choice parameters  
it may break job's HTML.
 - Leeroy has been tested on Python 3.11.*  
 there is no certainty about other versions, but you can try.
### Downloading and Setup:
```
git clone https://github.com/conga-itinabd/leeroy.git
```
```
cd leeroy; chmod +x setup.sh; ./setup.sh
```
### Usage:
##### Configure your stepsbook and values.
Initialization has two options:  

1)
Generates templates for stepsbook and values with all possible current instructions:
```
leeroy init-doc 
```
2)
Generates empty templates for stepsbook and values:
```
leeroy init
```
 - Now modify the templates according to your needs by filling in values and stepsbook
##### Execution:
```
leeroy stepsbook.yaml -v values.yaml
```
# Uninstall:
```
sudo rm -rf /usr/local/lib/leeroy /usr/local/bin/leeroy
```
# Entities:

### Values:
Contains configuration data for the stepsbook.
##### cfg:
 - required params:  
user - the user which you login to Jenkins  
token - API token that can be generated in your user settings
 - optional params:
skiptls - (yes) if you do not add this field, leeroy wiil use tls  
output - (text/json) if you do not add this field, there will be text output  
debug - (yes) debug mode  
##### keys for stepsbook:
Usage is similar to Jinja2.
keys specified here can be used in the stepsbook
```
url: https://example.com -->> {{ url }} in stepsbook
foo:
  bar: foos_and_bars -->> {{ foo.bar }} in stepsbook
```
### stepsbook:

```
steps:
  build:  # <-- you can use any key here, it converts for step name
    - action: build  # The action of the step. Currently, only "build" is available, but future releases will include "build_ac," "get_data," and "rebuild."
      url: {{ url }}  # <-- here you should put your job url
      parameters: # here add your job parameters:
        example_param: {{ foo.bar }}  # This value will be passed to the "example_param" parameter of your pipeline.
      log:  # getting log by pattern from 'console' of build
        nexus_url: https://nexus.server/build/*****.tar  # <-- find a substring based on the pattern, which can be used further in Stepsbook as 'log.nexus_url'
        image: https://registry.server/#****:latest # sign '#' will cut left part of pattern. here is also availble '****#' and '#***#'
      catch:  # catching number of logs by substrings from 'console' of the build
        - Error  # finding number of 'Error' substings in console of the build
        - Warning  # finding number of 'Warning' substings in console of the build
  report:  # <-- you can use any key here, it converts for step name
    - action: build  # The action of the step. Currently, only "build" is available, but future releases will include "build_ac," "get_data," and "rebuild."
      url: {{ url }}_smth
      parameters:
        logs_from_build_nexus: (( log.build.nexus_url ))  # <-- usage of 'log' from step 'build'
        logs_from_build_image: (( log.build.image ))  # <-- usage of 'log' from step 'build'
        cath_form_tests_Errors: 'Errors: (( catch.tests.Error ))'  # <-- usage of 'catch' from step 'build'
        cath_form_tests_Warnings: (( catch.tests.Warning ))  # <-- usage of 'catch' from step 'build'
      iterations: 4  # <-- number of iterations
```
----
# More about the Project:
This is the first version of the program with plans for significant development. 
 - Send feedback in any convenient way; 
 - make PRs;  
let's make using Jenkins more enjoyable and faster together!


##### Acknowledgments:
 - [Konstantin Zagorulko][Kgithub]  

You could be mentioned here if you contribute to the project!  

----  
**Creator: Egor Lobanov**  
LinkedIn: https://www.linkedin.com/in/egor-lobanov-872788252/

[Kgithub]: <https://github.com/kzagorulko>