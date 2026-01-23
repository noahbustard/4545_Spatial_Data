#include <iostream>
#include <string>


using namespace std;

struct Node{
    int id;
    string name;
    Node* next;
    Node(){
        id = 0;
        name = " ";
        next = nullptr;
    }
    Node(int id, string name): id(id),name(name),next(nullptr){}
    void print(){
        cout<<"["<<id<<","<<name<<"]";
    }
};

class AnimalList{
    Node* front;
    void _add(Node* a ){
        Node* t = new Node(a->id, a->name);
        if(!front){
            front = a;
        } else {
            a->next = front;
            front = a;
        }

    }
public:
    AnimalList(): front(nullptr) {}
    void add(Node* a) {
        _add(a);
    }
    void add(int id, string name) {
        _add(new Node(id, name));
    }
    void print() {
        Node* travel = front;
        while(travel){
            travel->print();
            travel = travel->next;
        }
    }
};

int main(){

    int i;
    string name;
    AnimalList list;

    while(cin >> i >> name){
        list.add(i, name);
    }
    list.print();
    return 0;
}