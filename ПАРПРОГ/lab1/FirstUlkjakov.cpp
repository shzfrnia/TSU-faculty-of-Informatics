#include <iostream>
#include <mpi.h>
#include <cmath>


using namespace std;

const int TAG = 8;

void handle(int, int, double);


int main(int argc, char **argv) {
        int rank, size;
        MPI_Init(&argc, &argv);
        MPI_Comm_size(MPI_COMM_WORLD, &size);
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        const double ttime =  MPI_Wtime();
        handle(rank, size, ttime);
        MPI_Finalize();
        return 0;
}


void handle(int rank, int total, double ttime)
{
        MPI_Status status;

        int sum = rank;
        int recv;

        const int groups = (int)(total / log2(total));
        int step = (int)(total/groups);
        int dest, sender;
        cout << "groups is:" << groups << endl;
        cout << "step is:" << step << endl;
        // Первый этап алгоритма -> считается последовательная сумма в маленьких группах

        for(int i=1; i<step;i++) {
          dest = rank + 1;
          sender = rank - 1;

          if(rank%step == i-1) {
            // cout << "i " << i << " rank: " << rank << " " << sum << " rank+1:" << rank+1 << endl;
            MPI_Send(&sum, 1, MPI_INT, rank + 1, TAG, MPI_COMM_WORLD);
          } 

          if(rank%step == i){
             MPI_Recv(&recv, 1, MPI_INT, rank - 1, TAG, MPI_COMM_WORLD, &status);
            // cout << "i " << i << " rank: " << rank << " " << recv << " rank-1:" << rank-1 << endl;
             sum += recv;
          }
        }
        
        // cout << "i " << rank << " Sum is: "  <<sum << endl;
        // Второй этап -> каскадная схема суммирования для оставшихся элементов

        int j = step;


        while (j < total)
         {
                if ((rank + 1) % j != 0) break;

                dest = rank + j;
                sender = rank - j;



                if (dest <= total - 1)
                {
                        MPI_Send(&sum, 1, MPI_INT, dest, TAG, MPI_COMM_WORLD);
                        printf("I %d send %d to %d \n", rank, sum, dest);
                }

                if (sender >= 0)
                {
                        MPI_Recv(&recv, 1, MPI_INT, sender, TAG, MPI_COMM_WORLD, &status);
                        printf("I %d recv %d from %d \n", rank, recv, sender);
                        sum += recv;
                }

                j *= 2;
        }

                const double resultTime = MPI_Wtime() - ttime;
                printf("Процесс %d завершился %f: с значением %d \n", rank, resultTime,sum);
}