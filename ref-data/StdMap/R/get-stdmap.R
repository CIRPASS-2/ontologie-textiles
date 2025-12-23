library(httr)
library(jsonlite)
library(dplyr)
library(purrr)
library(stringr)
library(stringdist)

response = fromJSON(content(GET("https://api.production.standardsmap.sustainable-trade.org/api/standards?client=NO%20AFFILIATION"), "text", encoding = "UTF-8"))
#write_json(response, path = "stdmap.JSON", pretty = TRUE, auto_unbox = TRUE)

country_code = function(x) { 
  country_codes = read.csv("../manual/flat-ui__data-Mon Dec 15 2025.csv")
  cc = map_chr(x, function(y) {
    if (is.na(y) || y == "") {
      return(NA_character_)
    }
    approx_match = stringdist::amatch(y, country_codes$CountryName, maxDist=Inf, method = "jw")
    country_codes$CountryCode[approx_match]  
  })
  return (cc)
}

country_code_is_exact_match = function(x) {
  country_codes = read.csv("../manual/flat-ui__data-Mon Dec 15 2025.csv")
  ccm = map_lgl(x, function(y) y %in% country_codes$CountryName)
  return (ccm)
}

urlfy = function(x) {
  x %>% str_to_sentence() %>% str_replace_all("&", " and ") %>% str_replace_all("[^[:alnum:]]+", "_") %>% str_replace_all("^_|_$", "")}

# TEST - country mapping

test_countries = unique(c(unlist(response$origin), unlist(response$destination)))
country_codes = read.csv("../manual/flat-ui__data-Mon Dec 15 2025.csv")
tf = data.frame(test_country = test_countries[!country_code_is_exact_match(test_countries)], cc = country_code(test_countries[!country_code_is_exact_match(test_countries)]))
write.csv(tf, file = "../manual/countries-test.csv", row.names = FALSE,  na = "")

typed_response = response %>% mutate(
  id = as.character(id),
  url = paste0("https://www.standardsmap.org/en/factsheet/", as.character(id)),
  lastUpdated = as.Date(lastUpdated),
  description = str_replace_all(description, "[\r\n]", " "),
  weblink = str_extract(description, "https?://\\S+"),
  client = map_chr(client, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),

  origin_country_code = map_chr(origin, ~ paste(na.omit(country_code(.x)), collapse = ";")),
  origin_country_code_exactmatch = map_chr(origin, ~ paste(na.omit(country_code_is_exact_match(.x)), collapse = ";")),
  origin = map_chr(origin, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  
  destination_country_code = map_chr(destination, ~ paste(na.omit(country_code(.x)), collapse = ";" )),
  destination_country_code_exactmatch = map_chr(destination, ~ paste(na.omit(country_code_is_exact_match(.x)), collapse = ";")),
  destination = map_chr(destination, ~ paste(na.omit(.x), collapse= ";")),
  
  yearOfEstablishment = as.integer(str_extract(yearOfEstablishment, "(19|20)\\d{2}")),
  det_products_urlfied =  map_chr(det_products, ~ paste(urlfy(na.omit(.x)), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  det_products = map_chr(det_products, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  
  products_urlfied = map_chr(products, ~ paste(urlfy(na.omit(.x)), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  products = map_chr(products, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  
  sectors = map_chr(sectors, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  isInternational = map_lgl(isInternational, ~ na.omit(.x) == "Yes"),
  mandate = map_chr(mandate, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  valueChain = map_chr(valueChain, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  nonConversion = map_chr(nonConversion, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  supplyChain = map_chr(supplyChain, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  recogAndCerts = map_chr(recogAndCerts, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  sdgs = map_chr(sdgs, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  pillars = map_chr(pillars, ~ {
    if (is.null(.x) || nrow(.x) == 0) {
      return("") 
    }
    parent_child_pairs <- paste(.x$parent, .x$name, sep = "/")%>% str_remove("^NA/") %>% str_remove("/NA$")
    paste(parent_child_pairs[nzchar(parent_child_pairs)], collapse = ";")
  }),
  themes = map_chr(themes, ~ {
    if (is.null(.x) || nrow(.x) == 0) {
      return("") 
    }
    parent_child_pairs <- paste(.x$parent, .x$name, sep = "/")  %>% str_remove("^NA/") %>% str_remove("/NA$")
    paste(parent_child_pairs[nzchar(parent_child_pairs)], collapse = ";")
  }),
  BenchmarkedFEFAC = map_chr(BenchmarkedFEFAC, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  docs_exists = map_lgl(docs$exists, ~ tolower(na.omit(.x)) == "yes"),
  docs_items = map_chr(docs$items, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  docs_links = map_chr(docs$links, ~ {
    regex_pattern <- "https?://\\S+"
    matches <- str_extract_all(.x, regex_pattern)
    url_vector <- matches[[1]]
    if (length(url_vector) == 0) {
      NA_character_
    } else {
      paste(url_vector, collapse = "; ")
    }
  }),
  createdDate = as.POSIXct(createdDate),
  pillarScores_env = pillarScores$Environoment,
  pillarScores_soc = pillarScores$Social,
  pillarScores_ethics = pillarScores[["Management and Ethics"]],
  pillarScores_qual = pillarScores$Quality
) %>% select(
  -docs,
  -pillarScores,
  -themeScores
) %>% rename(
  standard = name,
  weblinkExtra = docs_links,
  descr = description
)

small_response <- typed_response %>%
  select(url, standard, sectors, products, weblink, weblinkExtra, descr)



# write.csv(small_response, file = "StdMap-Standard.csv", row.names = FALSE, na = "") # why go small if we can go full
write.csv(typed_response, file = "../stdmap.csv", row.names = FALSE,  na = "")
