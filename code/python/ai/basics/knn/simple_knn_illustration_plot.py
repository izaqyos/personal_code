import math
import matplotlib.pyplot as plt

def plot_knn(train_data, test_point, k, predicted_class):
    """
    Plots the training data, test point, and k-nearest neighbors.

    Args:
        train_data (list): List of tuples containing training points and their labels.
        test_point (tuple): The test point to classify.
        k (int): The number of neighbors to consider.
        predicted_class (str): The predicted class for the test point.
    """

    # Extract training points and labels
    train_points, train_labels = zip(*train_data)

    # Plot training points
    for point, label in train_data:
        plt.scatter(point[0], point[1], marker='o', c='blue' if label == 'A' else 'red', label=label)

    # Plot test point
    plt.scatter(test_point[0], test_point[1], marker='x', c='black', label='Test Point')

    # Get and plot k-nearest neighbors
    neighbors = get_neighbors(train_data, test_point, k)
    for dist, label in neighbors:
        neighbor_point = train_points[train_labels.index(label)]
        plt.plot([test_point[0], neighbor_point[0]], [test_point[1], neighbor_point[1]], 'g--')  # Green dashed line

    # Add labels and legend
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'KNN Classification (k={k}) - Predicted Class: {predicted_class}')
    plt.legend()
    plt.show()

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
plot_knn(train_data, test_point, k, predicted_class)
