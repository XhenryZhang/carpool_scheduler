from solver import *

def main() -> None:
    # gather user input
    input.main()
    # sanity checks
    sanity_check(input.config_info)
    
    # initialize solver and generate SMT formulas based on configuration files
    carpool_solver = Solver()
    configure_solver(input.config_info, carpool_solver)

    # run solver and extract answers
    ans, benchmarks = extract_seat_info(carpool_solver, True)

    # generate output
    output.generate_output(ans)

# add more methods for stretch goals to parse seating requeusts with specific individuals
if __name__ == '__main__':
    main()