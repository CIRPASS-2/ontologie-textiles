#' NOTE(vsenderov, 2025-11-19):
#' https://graphwise.atlassian.net/jira/software/c/projects/GS1/boards/3477?selectedIssue=GS1-3
#' https://docs.google.com/spreadsheets/d/1kC1DnHEIsKaX39I31gkQyCJ4FqHbn9lDuZC3NEIP0mE/edit?gid=0#gid=0

library(httr)
library(jsonlite)
library(dplyr)
library(purrr)
library(stringr)

# str_to_title does Ada Case but we can use str_to_sentence For sentence case
# we also 
#   - fix case
#   - replace & with a space
urlfy = function(x) {
  x %>% str_to_sentence() %>% str_replace_all("&", " and ") %>% str_replace_all("[^[:alnum:]]+", "_") %>% str_replace_all("^_|_$", "")}

# to process sectors and value chain
simple_process = function (prefix = "thes/Value_Chain/", path = "valueChain") {
  aurl = paste0(prefix, local({
    things = unlist(response[[path]])
    things = things[!is.na(things) & things != ""]
    unique(urlfy(things))
  }))
  
  data.frame(
    url = aurl,
    name = sapply(strsplit(aurl, "/"), function (x) {
      str_replace_all(x[3], "_", " ")
    }),
    parent = str_remove(prefix, "/$"),
    src = "data/thesauri/StdMap"
  )
}

raw_response <- GET("https://api.production.standardsmap.sustainable-trade.org/api/standards?client=NO%20AFFILIATION")
stop_for_status(raw_response) # Stops the script if error occurs (e.g. 404 or 500)

response = fromJSON(content(raw_response, "text", encoding = "UTF-8"))

# Sustainability theme or pillar
thes_Sustainability = local({
  thes_url = sort(unique(c(
    paste0('thesauri/Sustainability/', unlist(lapply(response$themes, function(x) {
      urlfy(x$parent)}))),
    paste0('thesauri/Sustainability/', unlist(lapply(response$pillars, function(x) {
      urlfy(x$parent)}))))))
  thes_name = sapply(str_split(thes_url, "/"), function (x) {
    x[3] %>% str_replace_all("_", " ")   })
  parent = str_remove(thes_url, "/[^/]*$")
  our_src = rep("data/thesauri/StdMap", length(thes_name))
  
  rbind(
    data.frame( thes_url = "thesauri/Sustainability", name = "Sustanability theme or pillar", parent ="", src = "data/thesauri/StdMap"),
    data.frame( thes_url = thes_url, name = thes_name, parent = parent, src = our_src)
  )
})

concepts_Sustainability = local({
  concept_url = sort(unique(c(
    paste0('thes/Sustainability/', unlist(lapply(response$themes, function(x) {
      paste(urlfy(x$parent), urlfy(x$name), sep = "/")}))),
    paste0('thes/Sustainability/', unlist(lapply(response$pillars, function(x) {
      paste(urlfy(x$parent), urlfy(x$name), sep = "/")}))))))
  concept_name = sapply(str_split(concept_url, "/"), function (x) {
    x[4] %>% str_replace_all("_", " ")   })
  parent = str_remove(concept_url, "/[^/]*$")
  our_src = rep("data/thesauri/StdMap", length(concept_name))
  rbind(
    data.frame( url = concept_url, name = concept_name, parent = parent, src = our_src)
  )
})

# Sustainability Standard
# note the data source is still the same data/thes/StdMap, not data/thes/StdMap/Standard
# thes_Standard = data.frame(
#   thes_url = paste0("thes/Sustainability/Standard/", urlfy(response$name)),
#   name = response$name,
#   parent = "thes/Sustainability/Standard",
#   src = "data/thes/StdMap/Standard"
# )

# Sector
thes_Sector = data.frame(thes_url = "thesauri/Sector", name = "Sector", parent = "", src = "data/thesauri/StdMap")
concepts_Sector = simple_process(prefix = "thesesauri/Sector/", path = "sectors")
  
# Value chain
thes_Value_Chain = data.frame(thes_url = "thesauri/Value_Chain", name = "Value Chain", parent = "", src = "data/thesauri/StdMap")
concepts_Value_Chain = simple_process(prefix = "thes/Value_Chain/", path = "valueChain")

# Output  
write.csv(rbind(
            thes_Sector,
            thes_Value_Chain,
            thes_Sustainability), 
          file = "StdMap-Thesauri.csv",
          row.names = FALSE,
          na = "")


write.csv(rbind(
  concepts_Sector,
  concepts_Value_Chain,
  concepts_Sustainability), 
  file = "StdMap-Concepts.csv",
  row.names = FALSE,
  na = "")
