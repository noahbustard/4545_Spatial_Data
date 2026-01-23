#include <iostream>
#include <nlohmann/json.hpp>
using namespace std;
using json = nlohmann::json;

int main() {
    // Given JSON structure
    json data = {
        {"name", "Artemis"},
        {"age", 23},
        {"is_student", true},
        {"skills", {"C++", "Python", "IoT"}},
        {"address", {{"city", "Wichita Falls"}, {"state", "TX"}}},
        {"projects", {
            {{"title", "Smart Sensor"}, {"completed", false}},
            {{"title", "3D Printer Monitor"}, {"completed", true}}
        }}
    };

    // 1. Traverse and print everything
    cout << "Full JSON structure:\n";
    for (auto& [key, value] : data.items()) {
        cout << key << ": " << value << endl;
    }

    // 2. Print the address
    cout << "\nAddress:\n" << data["address"] << endl;

    // 3. Print the value "IoT" by accessing the proper index
    cout << "\nThird skill (IoT): " << data["skills"][2] << endl;

    // 4. Change the age from 23 to 32
    data["age"] = 32;
    cout << "\nUpdated age: " << data["age"] << endl;

    // 5. Add a value to the skills list (array)
    data["skills"].push_back("JavaScript");
    cout << "\nUpdated skills list: " << data["skills"] << endl;

    // Optional: pretty print the final JSON
    cout << "\nFinal JSON (pretty printed):\n" << data.dump(4) << endl;

    return 0;
}
