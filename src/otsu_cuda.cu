#include "common.h"
#include "cuda_utils.h"
#include <vector>
#include <chrono>

// CUDA Kernel to calculate the histogram
// We use shared memory to compute local histograms per block efficiently
__global__ void histogram_kernel(const unsigned char* d_image, int* d_histogram, int total_pixels) {
    // Shared memory for local block histogram
    __shared__ int shared_hist[256];

    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    int local_tid = threadIdx.x;

    // Initialize shared memory
    if (local_tid < 256) {
        shared_hist[local_tid] = 0;
    }
    __syncthreads(); // Ensure all threads have initialized shared memory

    // Compute local histogram
    if (tid < total_pixels) {
        atomicAdd(&shared_hist[d_image[tid]], 1);
    }
    __syncthreads(); // Wait for all threads to finish computing local histogram

    // Add local histogram to global histogram
    if (local_tid < 256) {
        atomicAdd(&d_histogram[local_tid], shared_hist[local_tid]);
    }
}

// CUDA Kernel to apply the threshold
__global__ void apply_threshold_kernel(const unsigned char* d_image_in, unsigned char* d_image_out, int threshold, int total_pixels) {
    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    if (tid < total_pixels) {
        d_image_out[tid] = (d_image_in[tid] >= threshold) ? 255 : 0;
    }
}

OtsuResult run_otsu_cuda(const unsigned char* image_in, unsigned char* image_out, int width, int height) {
    OtsuResult result;
    int total_pixels = width * height;

    auto t_start = std::chrono::high_resolution_clock::now();

    // CUDA events for precise GPU timing
    cudaEvent_t start_event, stop_event;
    CUDA_CHECK(cudaEventCreate(&start_event));
    CUDA_CHECK(cudaEventCreate(&stop_event));

    // 0. Allocate Device Memory and Copy Data
    unsigned char *d_image_in = nullptr;
    unsigned char *d_image_out = nullptr;
    int *d_histogram = nullptr;

    CUDA_CHECK(cudaMalloc((void**)&d_image_in, total_pixels * sizeof(unsigned char)));
    CUDA_CHECK(cudaMalloc((void**)&d_image_out, total_pixels * sizeof(unsigned char)));
    CUDA_CHECK(cudaMalloc((void**)&d_histogram, 256 * sizeof(int)));

    CUDA_CHECK(cudaMemcpy(d_image_in, image_in, total_pixels * sizeof(unsigned char), cudaMemcpyHostToDevice));

    // Configure grid and block dimensions
    int blockSize = 256;
    int gridSize = (total_pixels + blockSize - 1) / blockSize;

    // 1. Calculate Histogram (GPU)
    CUDA_CHECK(cudaMemset(d_histogram, 0, 256 * sizeof(int))); // Reset histogram

    CUDA_CHECK(cudaEventRecord(start_event));
    histogram_kernel<<<gridSize, blockSize>>>(d_image_in, d_histogram, total_pixels);
    CUDA_CHECK(cudaEventRecord(stop_event));
    CUDA_CHECK(cudaEventSynchronize(stop_event));

    float time_histogram_ms;
    CUDA_CHECK(cudaEventElapsedTime(&time_histogram_ms, start_event, stop_event));
    result.time_histogram_ms = time_histogram_ms;

    // 2. Calculate Otsu Threshold (CPU)
    // First, copy histogram back to host
    std::vector<int> h_histogram(256);
    CUDA_CHECK(cudaMemcpy(h_histogram.data(), d_histogram, 256 * sizeof(int), cudaMemcpyDeviceToHost));

    auto t0_thresh = std::chrono::high_resolution_clock::now();
    float sum = 0;
    for (int i = 0; i < 256; ++i) sum += i * h_histogram[i];

    float sumB = 0;
    int wB = 0;
    int wF = 0;
    float varMax = 0;
    int threshold = 0;

    for (int i = 0; i < 256; ++i) {
        wB += h_histogram[i];
        if (wB == 0) continue;
        wF = total_pixels - wB;
        if (wF == 0) break;
        sumB += (float)(i * h_histogram[i]);
        float mB = sumB / wB;
        float mF = (sum - sumB) / wF;
        float varBetween = (float)wB * (float)wF * (mB - mF) * (mB - mF);
        if (varBetween > varMax) {
            varMax = varBetween;
            threshold = i;
        }
    }
    auto t1_thresh = std::chrono::high_resolution_clock::now();
    result.threshold = threshold;
    result.time_threshold_ms = std::chrono::duration<double, std::milli>(t1_thresh - t0_thresh).count();

    // 3. Apply Threshold (GPU)
    CUDA_CHECK(cudaEventRecord(start_event));
    apply_threshold_kernel<<<gridSize, blockSize>>>(d_image_in, d_image_out, threshold, total_pixels);
    CUDA_CHECK(cudaEventRecord(stop_event));
    CUDA_CHECK(cudaEventSynchronize(stop_event));

    float time_apply_ms;
    CUDA_CHECK(cudaEventElapsedTime(&time_apply_ms, start_event, stop_event));
    result.time_apply_ms = time_apply_ms;

    // 4. Copy Result Back and Cleanup
    CUDA_CHECK(cudaMemcpy(image_out, d_image_out, total_pixels * sizeof(unsigned char), cudaMemcpyDeviceToHost));

    CUDA_CHECK(cudaFree(d_image_in));
    CUDA_CHECK(cudaFree(d_image_out));
    CUDA_CHECK(cudaFree(d_histogram));
    CUDA_CHECK(cudaEventDestroy(start_event));
    CUDA_CHECK(cudaEventDestroy(stop_event));

    auto t_end = std::chrono::high_resolution_clock::now();
    result.time_total_ms = std::chrono::duration<double, std::milli>(t_end - t_start).count();

    return result;
}
