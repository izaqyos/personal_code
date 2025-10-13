#include <iostream>
#include <vector>

// Function that takes a vector by value using move semantics
void process_vector(std::vector<int> && vec) {
    // Do some processing on the vector
    for (int i = 0; i < vec.size(); ++i) {
        vec[i] = vec[i] * 2;
    }

    // Print the processed vector
    std::cout << "Processed vector: ";
    for (int i = 0; i < vec.size(); ++i) {
        std::cout << vec[i] << " ";
    }
    std::cout << std::endl;
}

int main() {
    // Create a vector of integers
    std::vector<int> my_vector = {1, 2, 3, 4, 5};

    // Pass the vector to the function using move semantics
    process_vector(std::move(my_vector));

    // Attempt to access the vector after it has been moved
    std::cout << "Attempt to access moved vector: ";
    for (int i = 0; i < my_vector.size(); ++i) {
        std::cout << my_vector[i] << " ";
    }
    std::cout << std::endl;

    return 0;
}

