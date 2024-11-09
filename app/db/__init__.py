from ..services.storage import JsonArrayFileStorage, FilesStorage, CacheStorage

products_db = JsonArrayFileStorage("/data/products.json")
files_db = FilesStorage("data/images")
cache_db = CacheStorage()
