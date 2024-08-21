from etl import get_files

filepath = "./data/song_data"
test_data = get_files(filepath, pattern= '*.json')
print(test_data)
