#' NOTE(vsenderov, 2025-11-19):
#' https://graphwise.atlassian.net/jira/software/c/projects/GS1/boards/3477?selectedIssue=GS1-3
#' https://docs.google.com/spreadsheets/d/1kC1DnHEIsKaX39I31gkQyCJ4FqHbn9lDuZC3NEIP0mE/edit?gid=0#gid=0

response = read_json("../data/stdmap.json", simplifyVector = TRUE)

# to process sectors and value chain
simple_process = function (prefix = "thesauri/Value_Chain/", path = "valueChain", pos = 3, src = "data/thesauri/StdMap") {
  aurl = paste0(prefix, local({
    things = unlist(response[[path]])
    things = things[!is.na(things) & things != ""]
    unique(urlfy(things))
  }))
  
  data.frame(
    url = aurl,
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
  our_src = rep("data/concepts/StdMap", length(concept_name))
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
concepts_Sector = simple_process(prefix = "thesesauri/Sector/", path = "sectors", src = "data/concepts/StdMap")
  
# Value chain
thes_Value_Chain = data.frame(thes_url = "thesauri/Value_Chain", name = "Value Chain", parent = "", src = "data/thesauri/StdMap")
concepts_Value_Chain = simple_process(prefix = "thesauri/Value_Chain/", path = "valueChain", src = "data/concepts/StdMap")

# Products
concepts_products = rbind(simple_process(prefix = "thesauri/product/products/", path = "products", pos = 4, src = "data/concepts/StdMap"),
                          simple_process(prefix = "thesauri/product/products/", path = "det_products", pos = 4, src = "data/concepts/StdMap"))

# Output  
write.csv(rbind(
            thes_Sector,
            thes_Value_Chain,
            thes_Sustainability), 
          file = "../data/thesauri.csv",
          row.names = FALSE,
          na = "")


write.csv(rbind(
  concepts_Sector,
  concepts_Value_Chain,
  concepts_Sustainability,
  concepts_products), 
  file = "../data/concepts.csv",
  row.names = FALSE,
  na = "")
