import pickle

with open('description_distances_database.pickle', 'rb') as file:
    distances = pickle.load(file)

for i in range(len(distances)):
    print('\r', i, end='')
    filename = f'description_distances_database/{i}.pickle'
    data = distances[i]
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
