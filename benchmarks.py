import matplotlib.pyplot as plt

from solver import *

FILES_TO_CHECK = ["sat_1", "sat_2", "sat_3", "sat_3_2xCARS", "sat_3_3xCARS", "sat_3_4xCARS", "sat_4", "sat_5", "sat_6", "sat_7", "sat_8"]
CARS = [12, 24, 46, 48]
CONSTRAINTS = [10, 19, 29, 39, 49, 66]
START = 2
CAR_END = 5
ITERATIONS = 10
times = {}
constraint_time_array = []
car_time_array = []
def main() -> None:
    iteration = 0
    # gather user input
    for file_name in FILES_TO_CHECK:
        times[file_name] = 0
    while iteration < ITERATIONS:
        for file_name in FILES_TO_CHECK:
            input.extract_config(file_name)
            # sanity checks
            sanity_check(input.config_info)
            
            # initialize solver and generate SMT formulas based on configuration files
            carpool_solver = Solver()
            configure_solver(input.config_info, carpool_solver)

            # run solver and extract answers
            ans, benchmarks = extract_seat_info(carpool_solver, True)
            times[file_name] += benchmarks.time

            # generate output
            output.generate_output(ans)
        iteration += 1
    count = 0
    for name in times:
        times[name] = times[name]/ITERATIONS
        print(times[name])
        if count >= START and count <= CAR_END:
            car_time_array.append(times[name])
        if count == START or count > CAR_END:
            constraint_time_array.append(times[name])
        count += 1
    plt.scatter(CARS, car_time_array)
    plt.plot(CARS, car_time_array)
    plt.title("Solving Time With Increasing Cars")
    plt.xlabel("Number of Cars")
    plt.ylabel("Time (seconds)")
    plt.show()
    constraint_time_array.sort()
    plt.scatter(CONSTRAINTS, constraint_time_array)
    plt.plot(CONSTRAINTS, constraint_time_array)
    plt.title("Solving Time With Increasing Constraints")
    plt.xlabel("Number of Constraints")
    plt.ylabel("Time (seconds)")
    plt.show()
# add more methods for stretch goals to parse seating requeusts with specific individuals
if __name__ == '__main__':
    main()