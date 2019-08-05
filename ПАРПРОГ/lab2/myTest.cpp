#include <stdio.h>
#include <math.h>
#include <mpi.h>
#include <iostream>

#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))

double f(double x)
{
    return (log(1 + x) / x);
}

void handle(int, int, double);

int main(int argc, char **argv)
{
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    const double ttime = MPI_Wtime();
    handle(rank, size, ttime);
    MPI_Finalize();
    return 0;
}

void handle(int rank, int total, double ttime)
{
    double sum, tsum;
    const int n = 20; // Кол-во отрезков интегрирования
    const double a = 0.5, b = 4;
    const double h = (b - a) / total;
    const double k = a + rank * h;
    const double li = a + (rank + 1) * h;

    printf("Процессор: %d границы [%f:%f]\n", rank, k, li);

    const double diff = li - k;
    const double N = 2 * n;
    const double step = diff / N;
    double sum1 = 0, sum2 = 0;
    for (struct { int i; double xi; } s = {1, k + s.i * step}; s.i <= 2 * n - 1; ++s.i, s.xi = k + s.i * step)
    {
        double r = f(s.xi);
        if (s.i % 2 == 0)
        {
            sum1 += r;
        }
        else
        {
            sum2 += r;
        }
    }

    sum = step * (f(k) + 4 * sum2 + 2 * sum1 + f(li)) / 3;

    MPI_Reduce(&sum, &tsum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);

    if (rank == 0)
    {
        const double diffTime = MPI_Wtime() - ttime;
        printf("Закончил %.10f Время %f\n", tsum, diffTime);
    }
}