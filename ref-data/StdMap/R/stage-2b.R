#' NOTE(vsenderov, 2025-11-19):
#' https://graphwise.atlassian.net/jira/software/c/projects/GS1/boards/3477?selectedIssue=GS1-3
#' https://docs.google.com/spreadsheets/d/1kC1DnHEIsKaX39I31gkQyCJ4FqHbn9lDuZC3NEIP0mE/edit?gid=0#gid=0

source("setup.R")

response = read_json("../data/stdmap.json", simplifyVector = TRUE)

# to process sectors and value chain
simple_process = function (prefix = "thesauri/Value_Chain/", path = "valueChain", pos = 3, src = "data/thesauri/StdMap", urlfy = TRUE) {
  aurl = paste0(prefix, local({
    things = unlist(response[[path]])
    things = things[!is.na(things) & things != ""]
    if (urlfy) unique(urlfy(things)) else unique(things)
  }))
  
  data.frame(
    thes_url = aurl,
    name = sapply(strsplit(aurl, "/"), function (x) {
      str_replace_all(x[pos], "_", " ")
    }),
    parent = str_remove(prefix, "/$"),
    src = src
  )
}

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
    data.frame( thes_url = "thesauri/Sustainability", name = "Sustainability theme or pillar", parent ="", src = "data/thesauri/StdMap"),
    data.frame( thes_url = thes_url, name = thes_name, parent = parent, src = our_src)
  )
})

# TODO(vsenderov, 26-01-08): needs refactoring, since I added the simple scheme
concepts_Sustainability = local({
  concept_url = sort(unique(c(
    paste0('thesauri/Sustainability/', unlist(lapply(response$themes, function(x) {
      paste(urlfy(x$parent), urlfy(x$name), sep = "/")}))),
    paste0('thesauri/Sustainability/', unlist(lapply(response$pillars, function(x) {
      paste(urlfy(x$parent), urlfy(x$name), sep = "/")}))))))
  
  concept_name = sapply(str_split(concept_url, "/"), function (x) {
    x[4] %>% str_replace_all("_", " ")   })
  
  # we go back and forth here, not good, but works
  # concept_url_simple = paste0('thesauri/Sustainability/', urlfy(concept_name))
  
  parent = str_remove(concept_url, "/[^/]*$")
  our_src = rep("data/concepts/StdMap", length(concept_name))
  rbind(
    #data.frame( url = concept_url_simple, name = concept_name, parent = parent, src = our_src)
    data.frame( thes_url = concept_url, name = concept_name, parent = parent, src = our_src)
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
concepts_Sector = simple_process(prefix = "thesauri/Sector/", path = "sectors", src = "data/thesauri/StdMap")
  
# Value chain
thes_Value_Chain = data.frame(thes_url = "thesauri/Value_Chain", name = "Value Chain", parent = "", src = "data/thesauri/StdMap")
concepts_Value_Chain = simple_process(prefix = "thesauri/Value_Chain/", path = "valueChain", src = "data/thesauri/StdMap")

# Supply chain
thes_Supply_Chain = data.frame(thes_url = "thesauri/Supply_Chain", name = "Supply Chain", parent = "", src = "data/thesauri/StdMap")
concepts_Supply_Chain = simple_process(prefix = "thesauri/Supply_Chain/", path = "supplyChain", src = "data/thesauri/StdMap")

# Certs
thes_Certs = data.frame(thes_url = "thesauri/Recognition_and_Certificates", name = "Recognition and Certificates", parent = "", src = "data/thesauri/StdMap")
concepts_Certs = simple_process(prefix = "thesauri/Recognition_and_Certificates/", path = "recogAndCerts", src = "data/thesauri/StdMap")#, urlfy = FALSE)

# Non-conversion requirements
thes_nonConversion = data.frame(thes_url = "thesauri/Non_Conversion_Requirements", name = "Non Conversion Requirements", parent = "", src = "data/thesauri/StdMap")
concepts_nonConversion = simple_process(prefix = "thesauri/Non_Conversion_Requirements/", path = "nonConversion", src = "data/thesauri/StdMap")

# Products
concepts_products = rbind(simple_process(prefix = "thesauri/product/products/", path = "products", pos = 4, src = "data/thesauri/StdMap"),
                          simple_process(prefix = "thesauri/product/products/", path = "det_products", pos = 4, src = "data/thesauri/StdMap"))

# Output  
write.csv(rbind(
            thes_Sector,
            concepts_Sector,
            thes_Value_Chain,
            concepts_Value_Chain,
            thes_Supply_Chain,
            concepts_Supply_Chain,
            thes_Sustainability,
            concepts_Sustainability,
            thes_Certs,
            concepts_Certs,
            thes_nonConversion,
            concepts_nonConversion,
            concepts_products), 
          file = "../data/thesauri.csv",
          row.names = FALSE,
          na = "")
