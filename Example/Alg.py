
from collections import Counter

def algorithm(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines() #read lines file
            line_counts = Counter (lines) #count occurences
            most_search, count = line_counts.most_common(1)[0] #find common line
            return most_search.strip()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
        

file_path = 'web.hist.txt'#replace with actual file path
feed = algorithm(file_path)

if feed:
    print(f"{feed}") #f-string includes value of `feed`