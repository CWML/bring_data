####################################################
# Step 1: Install packages with install.packages() #
####################################################

install.packages("tidyverse")
install.packages("here")
install.packages("janitor")
install.packages("openxlsx")
install.packages("rio")
install.packages("skimr")

######################################
# Step 2: Load packages using library()
######################################

library(tidyverse)
library(here)
library(janitor)
library(openxlsx)
library(rio)
library(skimr)


##################################################################################
# Step 3: Import the your data file from the folder where you keep your raw data #
##################################################################################

#excel file
my_data <- import(here("FOLDER NAME", "DATA_FILE.xlsx"))

#csv file
my_data <- import(here("FOLDER NAME", "DATA_FILE.csv"))

#####################################
# Step 4: Inspect the raw data file #
#####################################

# Run each function one at time 

view(DATA_FRAME_NAME)

head(DATA_FRAME_NAME)

glimse(DATA_FRAME_NAME)

skim(DATA_FRAME_NAME)

# It may be a good idea to inspect variables with charter stings as values for misspellings or other possible errors
## Which character values should we check?

linelist_raw %>% count(VARIABLE_NAME)
linelist_raw %>% count(VARIABLE_NAME)
linelist_raw %>% count(VARIABLE_NAME)

## After inspecting, what issues did you find?