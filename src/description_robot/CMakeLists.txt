cmake_minimum_required(VERSION 3.8)
project(description_robot)

if(NOT CMAKE_COMPILER_IS_GNUCXX)
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# Install launch and urdf directories to share/
install(DIRECTORY launch urdf config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()