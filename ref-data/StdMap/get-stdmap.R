library(httr)
library(jsonlite)
library(dplyr)
library(purrr)
library(stringr)

response = fromJSON(content(GET("https://api.production.standardsmap.sustainable-trade.org/api/standards?client=NO%20AFFILIATION"), "text", encoding = "UTF-8"))
write_json(response, path = "StdMap-Extraction.JSON", pretty = TRUE, auto_unbox = TRUE)
typed_response = response %>% mutate(
  id = as.character(id),
  url = paste0("https://www.standardsmap.org/en/factsheet/", as.character(id)),
  lastUpdated = as.Date(lastUpdated),
  description = str_replace_all(description, "[\r\n]", " "),
  weblink = str_extract(description, "https?://\\S+"),
  client = map_chr(client, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  origin = map_chr(origin, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  destination = map_chr(destination, ~ paste(na.omit(.x), collapse= ";")),
  yearOfEstablishment = as.integer(str_extract(yearOfEstablishment, "(19|20)\\d{2}")),
  det_products = map_chr(det_products, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
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



write.csv(small_response, file = "StdMap-Standard.csv", row.names = FALSE, na = "")
write.csv(typed_response, file = "StdMap-Standard-Extended.csv", row.names = FALSE,  na = "")