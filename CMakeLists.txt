cmake_minimum_required(VERSION 3.18)
project(SobelComparison LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# gasire openmp
find_package(OpenMP REQUIRED)

# gasire tbb
find_package(TBB REQUIRED)

# fetch stb_image pt image reading/writing
include(FetchContent)
FetchContent_Declare(
    stb
    GIT_REPOSITORY https://github.com/nothings/stb.git
    GIT_TAG master
)
FetchContent_MakeAvailable(stb)

# definire executabil
add_executable(sobel_project
    src/main.cpp
    src/sobel_cpu.cpp
    src/sobel_omp.cpp
    src/sobel_tbb.cpp
)

# includere directoare
target_include_directories(sobel_project PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_include_directories(sobel_project PRIVATE ${stb_SOURCE_DIR})

# librarii link
target_link_libraries(sobel_project PRIVATE OpenMP::OpenMP_CXX TBB::tbb)
