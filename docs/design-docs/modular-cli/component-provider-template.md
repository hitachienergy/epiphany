# Context

This design document presents findings on what are important pieces of modules communication it Dockerized Custom Modules approach described [here](./modularization-approaches.md). 

# Plan 

Idea is to have something running and working mimicking real world modules. I used GNU make to perform this. With GNU make I was able to easily implement “run” logic. I also wanted to package everything into docker images to experience real world containers limitations of communication, work directory sharing and other stuff. 

 
