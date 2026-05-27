#ifndef COMMON_H
#define COMMON_H

#include <vector>
#include <string>

// Structure to hold the execution results
struct OtsuResult {
    int threshold;
    double time_histogram_ms;
    double time_threshold_ms;
    double time_apply_ms;
    double time_total_ms;
};

// Function declarations
OtsuResult run_otsu_cpu(const unsigned char* image_in, unsigned char* image_out, int width, int height);
OtsuResult run_otsu_omp(const unsigned char* image_in, unsigned char* image_out, int width, int height);
OtsuResult run_otsu_cuda(const unsigned char* image_in, unsigned char* image_out, int width, int height);

#endif // COMMON_H
