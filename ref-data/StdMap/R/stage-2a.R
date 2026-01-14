source("setup.R")

response = read_json("../data/stdmap.json", simplifyVector = TRUE)

# Helper to process and urlfy hierarchical structures
# TODO(vsenderov, 2026-01-08): this is a vibe-coded function and it works,
#.  however the linter complains about it and it is weird
process_hierarchy <- function(as_urlfied = FALSE) {
  function(.x) {
    if (is.null(.x) || (is.data.frame(.x) && nrow(.x) == 0)) {
      return("") 
    }
    
    parents <- .x$parent
    names <- .x$name
    
    if (as_urlfied) {
      # Apply urlfy to each element. 
      # We wrap it in a safe check to handle NAs gracefully.
       parents <- map_chr(parents, ~ if(is.na(.x) || .x == "") NA_character_ else urlfy(.x))
       names <- map_chr(names, ~ if(is.na(.x) || .x == "") NA_character_ else urlfy(.x))
    }
    
    # Combine parent and name with a slash
    #pairs = names
    pairs <- paste(parents, names, sep = "/") %>% 
       str_remove("^NA/") %>% 
       str_remove("/NA$")
    
    # Filter out empty pairs and collapse into a single string
    result <- paste(pairs[nzchar(pairs)], collapse = ";")
    
    # Clean up any newlines
    return(str_replace_all(result, "[\r\n]", " "))
  }
}

country_code = function(x) { 
  country_codes = read.csv("../data/cc-cname-mapping-2025-12-15.csv")
  cc = map_chr(x, function(y) {
    if (is.na(y) || y == "") {
      return(NA_character_)
    }
    approx_match = stringdist::amatch(y, country_codes$CountryName, maxDist=Inf, method = "jw")
    country_codes$CountryCode[approx_match]  
  })
  return (cc)
}

# (require '[clojure.data.csv :as csv]
#          '[clojure.java.io :as io]
#   '[clj-fuzzy.metrics :as metrics]) ; Jaro-Winkler implementation
# 
# (defn country-code [x]
#   (let [path "../manual/flat-ui__data-Mon Dec 15 2025.csv"
#         ;; Load CSV and transform into a map of {:name "CountryName", :code "CountryCode"}
#         country-codes (with-open [reader (io/reader path)]
#                         (doall
#                          (map (fn [[name code]] {:name name :code code})
#                               (rest (csv/read-csv reader)))))]
#     
#     ;; Map over the input sequence 'x'
#     (map (fn [y]
#            (if (or (nil? y) (= y ""))
#              nil ; Equivalent to NA_character_
#              (let [;; Find the best match based on Jaro-Winkler distance
#                    best-match (apply max-key 
#                                      #(metrics/jaro-winkler (:name %) y) 
#                                      country-codes)]
#                (:code best-match))))
#          x)))

country_code_is_exact_match = function(x) {
  country_codes = read.csv("../data/cc-cname-mapping-2025-12-15.csv")
  ccm = map_lgl(x, function(y) y %in% country_codes$CountryName)
  return (ccm)
}


# TEST - country mapping
test_countries = unique(c(unlist(response$origin), unlist(response$destination)))
# country_code(test_countries[1]) => ES
# country_code(test_countries[189]) => MK
# country_code(test_countries[251]) => CI
# data.frame(test_country = test_countries[!country_code_is_exact_match(test_countries)], cc = country_code(test_countries[!country_code_is_exact_match(test_countries)]))

# Helper to process and urlfy hierarchical structures

# Helper to process and urlfy hierarchical structures



# DONE(vsenderov, 2025-01-06): na.omit here is potentially problematic
# better to rewrite stuff as isInternational = map_lgl(isInternational, ~ .x %in% "Yes")
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
  
  sectors_urlfied = map_chr(sectors, ~ paste(urlfy(na.omit(.x)), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  sectors = map_chr(sectors, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  
  isInternational = map_lgl(isInternational, ~ .x %in% "Yes"),
  isInternationalStandard = map_lgl(typology, ~ .x %in% "isInternationalStandard"),
  isInternational = as.integer(isInternational | isInternationalStandard),
  isPrivate = as.integer(map_lgl(typology, ~ .x %in% "isPrivateStandard")),
  isPublic = as.integer(map_lgl(typology, ~ .x %in% "isPublicStandard")),
  
  hasThirdPartyVerification = as.integer(hasThirdPartyVerification),
  isConsumableLabel = as.integer(isConsumableLabel) ,
  
  mandata_urlfied = map_chr(mandate, ~ paste(urlfy(na.omit(.x)), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  mandate = map_chr(mandate, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  
  valueChain_urlfied = map_chr(valueChain, ~ paste(urlfy(na.omit(.x)), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  valueChain = map_chr(valueChain, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  
  nonConversion_urlfied = map_chr(nonConversion, ~ paste(urlfy(na.omit(.x)), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  nonConversion = map_chr(nonConversion, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  
  supplyChain_urlfied = map_chr(supplyChain, ~ paste(urlfy(na.omit(.x)), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  supplyChain = map_chr(supplyChain, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  
  recogAndCerts_urlfied = map_chr(recogAndCerts, ~ paste(urlfy(na.omit(.x)), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  recogAndCerts = map_chr(recogAndCerts, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  
  sdgs = map_chr(sdgs, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  # pillars = map_chr(pillars, ~ {
  #   if (is.null(.x) || nrow(.x) == 0) {
  #     return("") 
  #   }
  #   parent_child_pairs <- paste(.x$parent, .x$name, sep = "/")%>% str_remove("^NA/") %>% str_remove("/NA$")
  #   paste(parent_child_pairs[nzchar(parent_child_pairs)], collapse = ";")
  # }),
  
  pillars_urlfied = map_chr(pillars, process_hierarchy(as_urlfied = TRUE)),
  pillars         = map_chr(pillars, process_hierarchy(as_urlfied = FALSE)),
  
  # themes = map_chr(themes, ~ {
  #   if (is.null(.x) || nrow(.x) == 0) {
  #     return("") 
  #   }
  #   parent_child_pairs <- paste(.x$parent, .x$name, sep = "/")  %>% str_remove("^NA/") %>% str_remove("/NA$")
  #   paste(parent_child_pairs[nzchar(parent_child_pairs)], collapse = ";")
  # }),
  
  themes_urlfied = map_chr(themes, process_hierarchy(as_urlfied = TRUE)),
  themes         = map_chr(themes, process_hierarchy(as_urlfied = FALSE)),
  
 #BenchmarkedFEFAC = map_chr(BenchmarkedFEFAC, ~ paste(na.omit(.x), collapse = ";") %>% str_replace_all("[\r\n]", " ")),
  
  benchmarkedBefore2022 = as.integer(map_lgl(BenchmarkedFEFAC, ~ "before2022" %in% .x)),
  benchmarkedAfter2022  = as.integer(map_lgl(BenchmarkedFEFAC, ~ "after2022" %in% .x)),
  
  docs_exists = as.integer(map_lgl(docs$exists, ~ tolower(na.omit(.x)) == "yes")),
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
  -themeScores,
  -BenchmarkedFEFAC
) %>% rename(
  standard = name,
  weblinkExtra = docs_links,
  descr = description
)

#small_response <- typed_response %>%
#  select(url, standard, sectors, products, weblink, weblinkExtra, descr)
# write.csv(small_response, file = "StdMap-Standard.csv", row.names = FALSE, na = "") # why go small if we can go full

write.csv(typed_response, file = "../data/stdmap.csv", row.names = FALSE,  na = "")
