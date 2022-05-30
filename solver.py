from z3 import *
import input

def cal_num_seats(config_info: dict) -> int:
    """
    Calculates the number of car seats available to assign
    config_info: configuration information
    rtype: integer representing the number of car seats available
    """
    ans = 0
    for car_type in config_info[input.CAR_DELIM]:
        if car_type >= 0 and car_type <= 2:
            ans += input.SEAT_COUNT[car_type]
        else:
            raise IOError(f"Invalid car type specified in configuration file: {car_type}. Car type must be specified as 0, 1, or 2.")

    return ans

def sanity_check(config_info: dict) -> None:
    """
    Checks for invalid configurations before generation formal constraints for the solver
    config_info: configuration information
    rtype: None
    """
    # check if number of people > number of seats
    num_seats = cal_num_seats(config_info)
    num_people = config_info[input.NUM_PEOPLE]

    if num_people > num_seats:
        raise ValueError(f"Invalid assignment: Number of people to assign, {num_people}, is more than the number of seats available, {num_seats}.")

    # check for illogical or invalid constraints (ex: doesn't want to sit in any of the seat types)
    for name in config_info[input.PEOPLE_LIST]:
        if len(config_info[name]) > 2:
            raise IOError(f"Too many constraints specified for {name}. The maximum is 2.")

        for seat_constraint in config_info[name]:
            if seat_constraint > 2 or seat_constraint < 0:
                raise IOError(f"{seat_constraint} isn't a valid seat constraint for {name}. Constraint must be specified as 0, 1, or 2.")

def configure_solver(config_info: dict, cp_solver: Solver) -> None:
    """
    Encodes the constraints from input file as an SMT formula
    config_info: configuration information
    cp_solver: z3 Solver object to construct with SMT formula
    rtype: None
    """
    # generate position variables: X_p_c_s (person p in car number c in seat type s)
    X = [[[]]]
    # encode constraint: one person in one type of seat on one car
    cp_solver.add(x + 1 == 4)

def main() -> None:
    # gather user input
    input.main()
    # sanity checks
    sanity_check(input.config_info)
    # convert specifications to a series of z3 constraints
    carpool_solver = Solver()
    configure_solver(input.config_info, carpool_solver)
    # run the solver
    print(carpool_solver.check())
    print(carpool_solver.model())

    # display solver output


# add more methods for stretch goals to parse seating requeusts with specific individuals
if __name__ == '__main__':
    main()