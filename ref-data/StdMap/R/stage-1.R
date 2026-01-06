source("setup.R")

"https://api.production.standardsmap.sustainable-trade.org/api/standards?client=NO%20AFFILIATION" |>
  GET() |>
  stop_for_status() |>
  content(as = "parsed", simplifyVector = TRUE) |>
  write_json(path = "../data/stdmap-uncorrected.JSON", pretty = TRUE, auto_unbox = TRUE)

# Perhaps?
# (require '[clj-http.client :as client]
#          '[cheshire.core :as json])
# 
# (let [url "https://api.production.standardsmap.sustainable-trade.org/api/standards?client=NO%20AFFILIATION"]
#   (-> (client/get url {:as :string})      ; GET request, return body as string
#     :body                               ; Extract the body from the response map
#     (json/parse-string true)            ; Parse JSON (true = keywords as keys)
#     (json/generate-string {:pretty true}) ; Convert back to pretty-printed JSON string
#     (->> (spit "../stdmap-uncorrected.JSON")))) ; Write to file