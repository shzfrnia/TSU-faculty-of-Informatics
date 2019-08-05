#include <iostream>
#include <cmath>
#include <utility>
#include <math.h>
//#inclide <iomanip>

using namespace std;

double func1(double x1, double x2) {
	return x2 - 2*x1 - log10(x1) - 0.5;
}
double func2(double x1, double x2) {
	return x2 - (2 - x1) + exp(x1);
}

double func11(double x1, double x2) {
	return -2 - (1 / x1);
}
double func12(double x1, double x2) {
	return 1;
}

double func21(double x1, double x2) {
	return 1 + exp(x1);
}
double func22(double x1, double x2) {
	return 1;
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
	double x1 = 3.4, x2 = 2.2;
	cout << "y - 2*x - log10(x) - 0.5" << endl;
	cout << "y - (2 - x) + exp(x)" << endl;
	cout << "Начальные приближения (точки пересечения): " << x1 << " | " << x2 << endl;
	while (max(abs(func1(x1, x2)), abs(func2(x1, x2))) >= 1e-6) {
		cout  << x1 << ' ' << x2 << endl;
		pair<double, double> nx = next(x1, x2);
		x1 = nx.first;
		x2 = nx.second;
	}

	cout << endl << "Result:\n " << "x1["<< x1 << "]\tx2[" << x2<< ']';

	return 0;
}