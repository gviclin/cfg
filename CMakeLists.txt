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
