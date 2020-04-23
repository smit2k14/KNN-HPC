#include<omp.h>
#include<stdio.h>
#include<bits/stdc++.h>

using namespace std;


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
	if((end.tv_nsec-start.tv_nsec)<0){
		temp.tv_sec = end.tv_sec-start.tv_sec-1;
		temp.tv_nsec = 1000000000+end.tv_nsec-start.tv_nsec;
	}
	else{
		temp.tv_sec = end.tv_sec-start.tv_sec;
		temp.tv_nsec = end.tv_nsec-start.tv_nsec;
	}
	return temp;
}

// class KNN {
//     public:

// 		KNN() {}
// 		~KNN() {}

// 		vector< double > split(string line, char value) {
// 			vector< double > v;
// 			string temp_string = "";
// 			for(int i = 0; i<line.length();i++) {
// 				if(line[i] == value) \
// 					v.push_back(stod(temp_string));
// 				else 
// 					temp_string+=line[i];
// 			}
// 			return v;
// 		}

// 		vector< pair< vector< double >, double> > read_file(string fname) {
// 			ifstream reader;
// 			reader.open(fname);
// 			vector< pair< vector< double >, double> > csv_values;
			
// 			if (reader.is_open()) {
// 				string inp_line;
// 				while(getline(reader, inp_line)) 
// 					csv_values.push_back(make_pair(split(inp_line, ','), 0));
// 			}

// 			return csv_values;
// 		}
// };

vector< double > split(string line, char value) {
	vector< double > v;
	string temp_string = "";
	for(int i = 0; i<line.length();i++) {
		if(line[i] == value) \
			v.push_back(stod(temp_string));
		else 
			temp_string+=line[i];
	}
	return v;
}

vector< pair< vector< double >, double> > read_file(string fname) {
	ifstream reader;
	reader.open(fname);
	vector< pair< vector< double >, double> > csv_values;

	if (reader.is_open()) {
		string inp_line;
		while(getline(reader, inp_line)) 
			csv_values.push_back(make_pair(split(inp_line, ','), INT64_MAX));
	}

	return csv_values;
}

bool comparison (pair< vector< double >, double> a, pair< vector< double >, double> b) {
	if (a.second < b.second) return true;
	
	return false;
}

int main(int argc, char* argv[]) {

	struct timespec start_e2e, end_e2e, start_alg, end_alg, e2e, alg;
	/* Should start before anything else */
	clock_gettime(CLK, &start_e2e);

	/* Check if enough command-line arguments are taken in. */
	if(argc < 5){
		printf( "Usage: %s sizeOfInputArray processors inputFile k \n", argv[0] );
		return -1;
	}

	int n=atoi(argv[1]);    /* size of input array */
	int p=atoi(argv[2]);    /* number of processors*/
	string fname = argv[3]; /* the input filename for points */
	int k = atoi(argv[4]);	/* k in knn :) */

	string problem_name = "matrix_multiplication";
	string approach_name = "block";
	//    char buffer[10];
	//    FILE* inputFile;
	FILE* outputFile;
	//    inputFile = fopen(argv[3],"r");

	char outputFileName[50];        
	sprintf(outputFileName,"output/%s_%s_%s_%s_output.txt",problem_name,approach_name,argv[1],argv[2]); 

	//**********************
	int num_step=atof(argv[1]);

	vector< pair< vector< double >, double> > points = read_file(fname);

	int point = (rand() % points.size()); /* this is the point we'll calculate the nearest neighbors from */

	// #omp_set_num_threads(p);
	clock_gettime(CLK, &start_alg);    /* Start the algo timer */

	/*----------------------Core algorithm starts here----------------------------------------------*/

	for(auto i=0; i< points.size(); i++) {
		double dist = 0;
		for(auto j=0; j<points[i].first.size(); j++) {
			dist += (points[i].first[j] - points[point].first[j]) * (points[i].first[j] - points[point].first[j]);
		}
		points[i].second = dist;
	}

	sort(begin(points), end(points), comparison);

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
	//printf("%s,%s,%d,%d,%d,%ld,%d,%ld\n", problem_name, approach_name, n, p, e2e.tv_sec, e2e.tv_nsec, alg.tv_sec, alg.tv_nsec);

	return 0;

}
