cmake_minimum_required(VERSION 3.16)
project(SomeProject LANGUAGES CXX)

add_executable(my_program program.cpp)
target_include_directories(my_program
 PRIVATE
  first_dir/
  second_dir/)


 
add_library(my_lib STATIC my_lib_source.cpp)
target_include_directories(my_lib PUBLIC some_directory)

add_executable(my_program my_program_source.cpp)
target_link_libraries(my_program PRIVATE my_lib)

target_compile_definitions

You can define macros in CMake with add_definitions :
add_definitions(-DCMAKEMACROSAMPLE="Windows PC")


project(CMakeHello)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
add_executable(cmake_hello main.cpp)


cmake -H. -Bbuild
# H indicates source directory
# B indicates build directory
# For CLion, you can navigate to CLion -> Preferences -> Build, Execution and Deployment -> CMake -> Generation Path
