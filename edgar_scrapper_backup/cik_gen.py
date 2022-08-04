import pandas

for i in range(0, 8):
    if i < 7:
        ciks = pandas.read_excel('seccik.xlsx', nrows=100000, skiprows=(100000*i), engine='openpyxl', usecols=[2], names=['CIK'], squeeze=True, dtype=object)
        ciks = ciks[ciks.str.match(r'^\d+$')==True]
        for j in range (0, 10):
            cik = ciks[10000*j:10000*(j+1)]
            cik.to_csv(f"cik/cik_{i}{j}.txt", header=False, index=False) 
    else:
        ciks = pandas.read_excel('seccik.xlsx', nrows=20000, skiprows=(100000*i), engine='openpyxl', usecols=[2], names=['CIK'], squeeze=True, dtype=object)
        ciks = ciks[ciks.str.match(r'^\d+$')==True]
        for j in range (0, 2):
            cik = ciks[10000*j:10000*(j+1)]
            cik.to_csv(f"cik/cik_{i}{j}.txt", header=False, index=False) 