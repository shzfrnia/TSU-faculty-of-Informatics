#include <iostream>
#include <cmath>
#include <utility>

using namespace std;

double func1(double x1, double x2) {
	return x1 + 3*log10(x1) - x2*x2;
}
double func2(double x1, double x2) {
	return 2.0*x1*x1 - x1*x2 - 5.0*x1 + 1.0;
}

double func11(double x1, double x2) {
	return 3 / (x1*log(10)) + 1;
}
double func12(double x1, double x2) {
	return -2.0*x2;
}

double func21(double x1, double x2) {
	return 4.0*x1 - x2 - 5.0;
}
double func22(double x1, double x2) {
	return -x1;
}

double jacobian_det(double x1, double x2) {
	return func11(x1, x2)*func22(x1, x2) - func12(x1, x2)*func21(x1, x2);
}

double** jacobian_reversed(double x1, double x2) {
	double det = jacobian_det(x1, x2);
	if (abs(det) < 1e-6) throw new logic_error("Det is zero"); // Особенная матрица

	double** matrix = new double*[2];
	matrix[0] = new double[2];
	matrix[1] = new double[2];

	matrix[0][0] = func22(x1, x2) / det;
	matrix[0][1] = -func12(x1, x2) / det;
	matrix[1][0] = -func21(x1, x2) / det;
	matrix[1][1] = func11(x1, x2) / det;

	return matrix;
}

pair<double, double> next(double x1, double x2) {
	double** j_rev = jacobian_reversed(x1, x2);

	double next_x1 = x1 - j_rev[0][0] * func1(x1, x2) - j_rev[0][1] * func2(x1, x2);
	double next_x2 = x2 - j_rev[1][0] * func1(x1, x2) - j_rev[1][1] * func2(x1, x2);

	return make_pair(next_x1, next_x2);
}

int main() {
	double x1 = 5, x2 = 5;
	cout << "x + 3*log10(x) - y*y" << endl;
	cout << "2.0*x*x - x*y - 5.0*x + 1.0" << endl;
	cout << "Начальные приближения (точки пересечения): " << x1 << " | " << x2 << endl;
	while (max(abs(func1(x1, x2)), abs(func2(x1, x2))) >= 1e-12) {
		cout  << x1 << '\t' << x2 << endl;
		pair<double, double> nx = next(x1, x2);
		x1 = nx.first;
		x2 = nx.second;
	}

	cout << "x1["<< x1 << "]\tx2[" << x2<< ']';

	return 0;
}