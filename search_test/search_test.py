from mini_search import MiniSearch

mini_search = MiniSearch()
data = mini_search.index("test").search("背影", sort_by="timestamp")
print(data)

