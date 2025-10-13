import math

def euclidean_distance(point1, point2):
    return math.sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(point1, point2)))

def get_neighbors(train_data, test_point, k):
    distances = []
    for train_point, label in train_data:
        dist = euclidean_distance(test_point, train_point)
        distances.append((dist, label))
    distances.sort()
    return distances[:k]

def predict_classification(train_data, test_point, k):
    neighbors = get_neighbors(train_data, test_point, k)
    print(f"get neighbors {neighbors} for k={k} of {test_point}")
    class_counts = {}
    for _, label in neighbors:
        class_counts[label] = class_counts.get(label, 0) + 1
    print(f"simple KNN, use max instead of MSE. count: {class_counts}")
    return max(class_counts, key=class_counts.get)  

train_data = [
    ((1, 2), "A"),
    ((3, 4), "B"),
    ((5, 6), "A"),
    ((7, 8), "B"),
]

test_point = (4, 5)  
k = 3

predicted_class = predict_classification(train_data, test_point, k)
print(f"Predicted class for {test_point}: {predicted_class}")
