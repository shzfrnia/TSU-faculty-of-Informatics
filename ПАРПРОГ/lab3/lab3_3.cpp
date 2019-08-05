#include <stdio.h>
#include <math.h>
#include <mpi.h>
#include <iostream>

double X1 = -1;
double X2 = 1;
double Y1 = 1;
double Y2 = 2;
double N = 10000;

double function(double x, double y)
{
    return (pow(x, 2) * pow((sin(x + y) + 1.5), 2));
}

double simpson(double a, double b, double y)
{
    double n = N;
    double h = (b - a) / (2 * n);

    double sum1 = 0, sum2 = 0, sum3 = 0;
    for (int i = 1; i <= 2 * n - 1; i += 1)
    {
        double r = function(a + i * h, y);
        if (i % 2 == 0)
        {
            sum1 = sum1 + r;
        }
        else
        {
            sum2 = sum2 + r;
        }
    }

    sum3 = h * (function(b, y) + 4 * sum2 + 2 * sum1 + function(a, y)) / 3;

    return sum3;
}
double solve(int rank, int size)
{
    double sum = 0;
    double sumr = 0;

    double t = 100000;

    double h = (Y2 - Y1) / size;

    double k = Y1 + rank * h;
    double li = Y1 + (rank + 1) * h;

    double h1 = (li - k) / (2 * t);

    double sum1 = 0, sum2 = 0, sum3 = 0;

    for (int i = 1; i < 2 * t - 1; i++)
    {
        double y = k + i * h1;
        double r = simpson(X1, X2, k + i * h1);
        if (i % 2 == 0)
        {
            sum1 = sum1 + r;
        }
        else
        {
            sum2 = sum2 + r;
        }
    }

    sum3 = h1 * (simpson(X1, X2, k) + 4 * sum2 + 2 * sum1 + simpson(X1, X2, li)) / 3;

    return sum3;
}

int main(int argc, char **argv)
{
    int rank, size;
    double time, localResult = 0, result;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    time = MPI_Wtime();

    localResult = solve(rank, size);

    MPI_Reduce(&localResult, &result, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    time = MPI_Wtime() - time;

    printf("%lf sec at rank %d\n", time, rank);

    if (rank == 0)
    {
        printf("result = %.10f\n", result);
    }

    MPI_Finalize();
    return 0;
}