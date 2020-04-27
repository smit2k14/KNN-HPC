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

double* split(char* line, char value, int n_features) 
{
    char *temp_string;
    temp_string = (char *)malloc(sizeof(char)*50);
    double *feature_array = (double *) malloc(sizeof(double)*n_features);
    int cnt = 0;
    int cnt2=0;
    for(int i = 0; i<strlen(line);i++)
    {
        if(line[i] == value)
        {
            char *temp_blah;
            feature_array[cnt++] = strtod(temp_string, &temp_blah);
            temp_string = (char *)malloc(sizeof(char)*50);
        }
        else
        {
            temp_string[cnt2++] = line[i];
        }   
    }
    return feature_array;
}

double** read_file(char* fname, int n_lines, int n_features)
{
    FILE* reader;
    reader = fopen(fname, "r");
    double **csv_values = (double**)malloc(sizeof(double *)*n_lines);

    for(int l = 0; l<n_lines; l++)
    {
        csv_values[l] = malloc(sizeof(double)*n_features);
    }
    int cnt = 0;
    
    char* temp_string;
    temp_string = (char *) malloc(sizeof(char)*500);
    while(fgets(temp_string, 500, reader)) 
        fflush(stdout);
        csv_values[cnt++] = split(temp_string, ',', n_features);
    
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
    if(argc < 4){
        printf( "Usage: %s filename n_lines n_features\n", argv[0] );
        return -1;
    }

    char *fname = argv[1]; /* the input filename for points */
    int n_lines = atoi(argv[2]);
    int n_features = atoi(argv[3]);
    FILE* outputFile;
    
    //**********************
    int num_step=atof(argv[1]);
	
    double** points = (double**)malloc(sizeof(double *)*n_lines);

    for(int l = 0; l<n_lines; l++)
    {
        points[l] = malloc(sizeof(double)*n_features);
    }
    
    points = read_file(fname, n_lines, n_features);
	double dis_array[n_lines][2];
    int point = (rand() % n_lines); /* this is the point we'll calculate the nearest neighbors from */
	
    // #omp_set_num_threads(p);
    clock_gettime(CLK, &start_alg);    /* Start the algo timer */

    /*----------------------Core algorithm starts here----------------------------------------------*/

    for(int i=0; i<n_lines; i++) {
        double dist = 0;
        for(int j=0; j<n_features; j++) {
            dist += (points[i][j] - points[point][j]) * (points[i][j] - points[point][j]);
        }
        dis_array[i][0] = i;
        dis_array[i][1] = dist;
    }

    qsort(dis_array, n_lines, sizeof(double *), comparison);

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
    fprintf(outputFile, "%d,%ld,%d,%ld\n", e2e.tv_sec, e2e.tv_nsec, alg.tv_sec, alg.tv_nsec);

    return 0;

}
