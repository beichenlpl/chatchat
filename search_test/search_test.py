from mini_search import MiniSearch

mini_search = MiniSearch()
data = mini_search.index("test").search("的", sort_by="timestamp")
print(data)

