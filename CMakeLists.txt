cmake_minimum_required(VERSION 3.16)
project(SomeProject LANGUAGES CXX)

add_executable(my_program program.cpp)
target_include_directories(my_program
 PRIVATE
  first_dir/
  second_dir/)
