using namespace std;

#include <vector>

class Point {
public:
    Point() : x(0), y(0) { }
    Point(double x, double y) : x(x), y(y) { }
    double x, y;
};

class Quad {
public:
    Quad() : p() { }
    Quad(Point p0, Point p1, Point p2) : p() {
        p[0] = p0;
        p[1] = p1;
        p[2] = p2;
    }
    Point p[3];
    double arclen() const;
    Point eval(double t) const;
    bool isLine() const;
    void print(std::ostream& o) const;
};

class Thetas {
public:
    void init(const vector<Quad>& qs);
    Point xy(double s) const;
    Point dir(double s) const;
    double arclen;
private:
    vector<Point> xys;
    vector<Point> dirs;
};

vector<Quad> optimize(const Thetas& curve);
