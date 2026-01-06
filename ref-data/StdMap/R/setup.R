# To run:
# Rscript setup.R

if (!require("pacman")) install.packages("pacman")

pacman::p_load(
  httr, 
  jsonlite, 
  dplyr, 
  purrr, 
  stringr, 
  stringdist
)

# str_to_title does Ada Case but we can use str_to_sentence For sentence case
# we also 
#   - fix case
#   - replace & with a space
urlfy = function(x) {
  x %>% str_to_sentence() %>% str_replace_all("&", " and ") %>% str_replace_all("[^[:alnum:]]+", "_") %>% str_replace_all("^_|_$", "")}
