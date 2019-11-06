import csv

txtfile = 'new_official.txt'
csvfile = 'new_official.csv'

with open(txtfile, 'r') as infile, open(csvfile, 'w') as outfile:
     stripped = (line.strip() for line in infile)
     lines = ([line.split(" ")[0], ' '.join(line.split(" ")[1:]).strip("\ \"")] for line in stripped if line)

     writer = csv.writer(outfile)
     writer.writerows(lines)