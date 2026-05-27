cmake_minimum_required(VERSION 3.18)
project(OtsuThresholding LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CUDA_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find OpenMP
find_package(OpenMP REQUIRED)

# Fetch stb_image for image reading/writing
include(FetchContent)
FetchContent_Declare(
    stb
    GIT_REPOSITORY https://github.com/nothings/stb.git
    GIT_TAG master
)
FetchContent_MakeAvailable(stb)

# Define the executable
add_executable(otsu_project
    src/main.cpp
    src/otsu_cpu.cpp
    src/otsu_omp.cpp
    src/otsu_cuda.cu
        src/main.cpp
        src/main.cpp
)

# Include directories
target_include_directories(otsu_project PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_include_directories(otsu_project PRIVATE ${stb_SOURCE_DIR})

# Link OpenMP
target_link_libraries(otsu_project PRIVATE OpenMP::OpenMP_CXX)

# Set CUDA architectures
# You can change "native" to a specific compute capability like "75" if native fails
set_target_properties(otsu_project PROPERTIES CUDA_ARCHITECTURES "native")
