#include <iostream>
#include <string>
using namespace std;

class Book {
private:
    string title;
    string author;
    string isbn;
    int year;
    int pages;
    float price;
public:
    Book();
    Book(string,string,int,int);
    Book(string,string,int);

    int getYear();
    int getPages();
    float getPrice();
    string getAuthor();
    string getTitle();
    string getIsbn();

    void setPrice(float);
    void setPages(int);
    void setYear(int);
    void setAuthor(string);
    void setTitle(string);
    void setIsbn(string);
};


class Point3D {
private:
    double x;
    double y;
    double z;
    string color;
public:
    Point3D();
    Point3D(double, double, double, string);
    Point3D(double, double, double);

    double getX();
    double getY();
    double getZ();
    string getColor();

    void setX(double);
    void setY(double);
    void setZ(double);
    void setColor(string);

    void move2D(double, double);
    void moveUp(double);

    friend Point3D operator +(const Point3D &lhs, const Point3D &rhs);


    friend ostream &operator<<(ostream &os, const Point3D &p) {
        return os << "[ x: " << p.x << ", y: " << p.y << ", z: " << p.z << ", color: " << p.color << " ]";
    }
};


    Point3D operator +(const Point3D &lhs, const Point3D &rhs) {
        return Point3D(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z);
    }



class Movie {
private:
    string title;
    string director;
    int duration;
    int year;
    int budget;
    bool Trilogy;
    bool Franchise;
public:
    Movie();
    Movie(string, string, int, int);
    Movie(string, string);

    string getTitle();
    string getDirector();
    int getDuration();
    int getYear();
    int getBudget();
    bool isTrilogy();
    bool isFranchise();


};


class Point{
private:
  int x;
  int y;
public:
  Point();
  Point(int,int);
  void Move(int,int);
  void Jump(int,int);
};

void Point::Move(int _x, int _y){
    this->x += _x;
    this->y += _y;
}

void Point::Jump(int _x, int _y) {
    this->x = _x;
    this->y = _y;
}


// linked list class
class Node{
    int data;
    Node *next;
public:
    Node(int);
    int getData();
    Node* getNext();
    void setNext(Node*);
};

class LL{
    Node *start;
public:
    LL();
    void push(int);
    int pop();
    void print();

    LL(const LL &other) {
        this->start = nullptr;
        Node *current = other.start;
        while (current != nullptr) {
            this->push(current->getData());
            current = current->getNext();
        }
    }

    LL &operator=(const LL &other) {
        if (this != &other) {
            // Clear existing list
            while (this->start != nullptr) {
                this->pop();
            }
            // Copy from other
            this->start = nullptr;
            Node *current = other.start;
            while (current != nullptr) {
                this->push(current->getData());
                current = current->getNext();
            }
        }
        return *this;
    }
};

void LL::push(int value) {
    Node *newNode = new Node(value);
    this->start = newNode;
}


class Book {
private:
    string title;
    string author;
    string isbn;
    int pages;
    int year;
    float price;
public:
    Book();
    Book(string, string, int, int);
    Book(string, string, int);

    int getPages();
    int getYear();

    void setPages(int);
    void setYear(int);
};


class Point3D {
private:
    double x;
    double y;
    double z;
    string color;
public:
    Point3D();
    Point3D(double, double, double, string);
    Point3D(double, double, double);

    void move2D(double, double);
    void moveUp(double);


    //Copy Constructor
    Point3D(const Point3D &other) : x(other.x), y(other.y), z(other.z), color(other.color) {}


    Point3D &operator=(const Point3D &other) {
        if (this != &other) { //Check for self-assignment
            this->x = other.x;
            this->y = other.y;
            this->z = other.z;
            this->color = other.color;
        }
        return *this; // Pointer to this
    }

    bool operator==(const Point3D &other) {
        return (this->x == other.x) && (this->y == other.y) && (this->z == other.z) && (this->color == other.color);
    }
    friend Point3D operator+(const Point3D &lhs, const Point3D &rhs) {
        return Point3D(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z);
    };
    friend ostream &operator<<(ostream &os, const Point3D &p) {
        return os << "print";
    };
};

