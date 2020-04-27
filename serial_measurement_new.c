#include<stdio.h>
#include<math.h>
#include<omp.h>
#include<time.h>
#include<string.h>
#include<stdlib.h>

#define min(x, y) (((x) < (y)) ? (x) : (y))
//  Using the MONOTONIC clock 
#define CLK CLOCK_MONOTONIC

/* Function to compute the difference between two points in time */
struct timespec diff(struct timespec start, struct timespec end);

/* 
    Function to computes the difference between two time instances
    Taken from - http://www.guyrutenberg.com/2007/09/22/profiling-code-using-clock_gettime/ 
    Further reading:
    http://stackoverflow.com/questions/6749621/how-to-create-a-high-resolution-timer-in-linux-to-measure-program-performance
    http://stackoverflow.com/questions/3523442/difference-between-clock-realtime-and-clock-monotonic
*/

void printArray(int **a, int n, int m)
{
    int i, j;
    for(i = 0; i<n; i++)
    {
        for(j = 0; j<m; j++)
        {
            printf("%d ",a[i][j]);
        }
        printf("\n");
    }
}

struct timespec diff(struct timespec start, struct timespec end){
    struct timespec temp;
    if((end.tv_nsec-start.tv_nsec)<0)
	{
        temp.tv_sec = end.tv_sec-start.tv_sec-1;
        temp.tv_nsec = 1000000000+end.tv_nsec-start.tv_nsec;
    }
    else
	{
        temp.tv_sec = end.tv_sec-start.tv_sec;
        temp.tv_nsec = end.tv_nsec-start.tv_nsec;
    }
    return temp;
}

int** generate_numbers(int n_lines, int n_features)
{
    int **csv_values = (int**)malloc(sizeof(int *)*n_lines);
    int l, ll;
    for(l = 0; l<n_lines; l++)
    {
        csv_values[l] = malloc(sizeof(int)*n_features);
    }
    int cnt = 0;
    
    char* temp_string;
    temp_string = (char *) malloc(sizeof(char)*500);
    for(l = 0; l<n_lines; l++)
    {
        for(ll = 0; ll<n_features; ll++)
        {
            csv_values[l][ll] = rand();
        }
    }
    return csv_values;
}



int comparison (const void * a, const void * b) {
    int *aa = a, *bb = b;
    if (aa[1] < bb[1]) return 1;
    return 0;
}

int main(int argc, char* argv[]) {

    struct timespec start_e2e, end_e2e, start_alg, end_alg, e2e, alg;
    /* Should start before anything else */
    clock_gettime(CLK, &start_e2e);
    /* Check if enough command-line arguments are taken in. */
    if(argc < 3){
        printf( "Usage: %s n_lines n_features\n", argv[0] );
        return -1;
    }
 /* the input filename for points */
    int n_lines = atoi(argv[1]);
    int n_features = atoi(argv[2]);
    FILE* outputFile;
    int l,ll;
    int n_steps = 10000;
    //**********************
    int** points = (int**)malloc(sizeof(int *)*n_lines);

    for(l = 0; l<n_lines; l++)
    {
        points[l] = (int *)malloc(sizeof(int)*n_features);
    }
    
    points = generate_numbers(n_lines, n_features);
	
    int **dis_array = (int **)malloc(sizeof(int *)*n_lines);
    for(l = 0;l<n_lines; l++)
    {
        dis_array[l] = (int *)malloc(sizeof(int)*2);
    }
    int point = (rand() % n_lines); /* this is the point we'll calculate the nearest neighbors from */
	
    int i, j;
    int dist;
    
    clock_gettime(CLK, &start_alg);    /* Start the algo timer */
    /*----------------------Core algorithm starts here----------------------------------------------*/
    for(l=0; l<n_steps; l++){
        for(i=0; i<n_lines; i++)
        {
            dist = 0;
            for(j=0; j<n_features; j++)
            {
                //printf("5 %d\n", j);
                dist += (points[i][j] - points[point][j]) * (points[i][j] - points[point][j]);
            }
            dis_array[i][0] = i;
            dis_array[i][1] = dist;
        }
    }
    qsort(dis_array, n_lines, sizeof(int *), comparison);

    // return the first k but i dont think thats needed for now.

    /*----------------------Core algorithm finished--------------------------------------------------*/
    clock_gettime(CLK, &end_alg);    /* End the algo timer */
    /* Ensure that only the algorithm is present between these two
       timers. Further, the whole algorithm should be present. 
    */


    /* Should end before anything else (printing comes later) */
    clock_gettime(CLK, &end_e2e);
    e2e = diff(start_e2e, end_e2e);
    alg = diff(start_alg, end_alg);


    /* problem_name,approach_name,n,p,e2e_sec,e2e_nsec,alg_sec,alg_nsec
        Change problem_name to whatever problem you've been assigned
        Change approach_name to whatever approach has been assigned
        p should be 0 for serial codes!! 
    */

    outputFile = fopen("output_file_serial.txt", "a");    
    fprintf(outputFile, "%lf,%lf,%lf,%lf\n", e2e.tv_sec/n_steps, e2e.tv_nsec/n_steps, alg.tv_sec/n_steps, alg.tv_nsec/n_steps);

    return 0;

}
