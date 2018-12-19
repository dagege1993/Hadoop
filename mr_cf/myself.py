with open('new_ui.data', 'r') as f:
    data_set = f.read()
for data in data_set:
    data = data.strip().split(',')
    if len(data) != 3:
        continue
    print(data)
