#ifndef CUDA_UTILS_H
#define CUDA_UTILS_H

#include <iostream>
#include <cuda_runtime.h>

// Macro to wrap CUDA calls and check for errors
#define CUDA_CHECK(call)                                                    \
    do {                                                                    \
        cudaError_t err = call;                                             \
        if (err != cudaSuccess) {                                           \
            std::cerr << "CUDA Error in " << __FILE__ << " at line " << __LINE__ \
                      << ": " << cudaGetErrorString(err) << std::endl;      \
            exit(EXIT_FAILURE);                                             \
        }                                                                   \
    } while (0)

#endif // CUDA_UTILS_H
