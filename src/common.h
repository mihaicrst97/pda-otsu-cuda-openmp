#ifndef COMMON_H
#define COMMON_H

#include <vector>
#include <string>

// Structure to hold the execution results
struct SobelResult {
    double time_total_ms;
};

// Function declarations
SobelResult run_sobel_cpu(const unsigned char* image_in, unsigned char* image_out, int width, int height);
SobelResult run_sobel_omp(const unsigned char* image_in, unsigned char* image_out, int width, int height);
SobelResult run_sobel_tbb(const unsigned char* image_in, unsigned char* image_out, int width, int height);

#endif // COMMON_H
