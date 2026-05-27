#ifndef COMMON_H
#define COMMON_H

#include <vector>
#include <string>

// struct cu rezultatele executiei
struct SobelResult {
    double time_total_ms;
    int threads_used;
};

// functii
SobelResult run_sobel_cpu(const unsigned char* image_in, unsigned char* image_out, int width, int height);
SobelResult run_sobel_omp(const unsigned char* image_in, unsigned char* image_out, int width, int height);
SobelResult run_sobel_tbb(const unsigned char* image_in, unsigned char* image_out, int width, int height);

#endif 
