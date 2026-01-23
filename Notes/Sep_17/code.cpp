#include <iostream>
using namespace std;

template <typename T>
T add(T a, T b) {
    return a + b;
}


int main() {
    cout << add(3, 4) << endl;        // Works with integers
    cout << add(3.5, 4.5) << endl;    // Works with doubles
    cout << add(string("Hello, "), string("World!")) << endl; // Works with strings
}