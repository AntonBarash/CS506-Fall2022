import csv
def read_csv(csv_file_path):
    """
        Given a path to a csv file, return a matrix (list of lists)
        in row major.
    """
    f = open(csv_file_path, 'r')
    data = csv.reader(f)
    res = []
    for row in data:
        res.append(row)
    return res

#print(read_csv('dataset_1.csv'))
    
