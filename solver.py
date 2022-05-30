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
            input.NUM_CAR_TYPE[car_type] += 1
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
    name_list = config_info[input.PEOPLE_LIST]
    car_type_list = config_info[input.CAR_DELIM]
    name_index = {name: index for index, name in enumerate(name_list)}
    # generate position variables: X_p_c_s (person p in car number c in seat type s)
    X_p_c_s = [[[Int('X_%s_%s_%s' % (name, car_num, seat_type)) for seat_type in range(3)] for car_num in range(len(car_type_list))] for name in name_list]
    # X_p_c_s[config_info[input.PEOPLE_LIST][0]][0][0] = X_mike_0_0
    
    # encode constraint: X_p_c_s == 1 or X_p_c_s == 0
    # encode constraint: each person is seated in exactly one car
    for name in name_list:
        oc = IntVal(0)
        for car_num in range(len(car_type_list)):
            for seat_type in range(3):
                oc = oc + X_p_c_s[name_index[name]][car_num][seat_type]
                cp_solver.add(Or(X_p_c_s[name_index[name]][car_num][seat_type] == 0, X_p_c_s[name_index[name]][car_num][seat_type] == 1))
        
        cp_solver.add(oc == 1)
    
    # encode constraint: each car has a set number of free seats based on their type
    for car_num in range(len(car_type_list)):
        oc = IntVal(0)
        for name in name_list:
            for seat_type in range(3):
                oc = oc + X_p_c_s[name_index[name]][car_num][seat_type]
        
        cp_solver.add(oc <= input.SEAT_COUNT[car_type_list[car_num]])

    # encode constraint: quantity of each seat type is set based on the car types in configuration
    for seat_type in range(3):
        oc = IntVal(0)
        for name in name_list:
            for car_num in range(len(car_type_list)):
                oc = oc + X_p_c_s[name_index[name]][car_num][seat_type]

        # window
        if seat_type == input.WINDOW:
            cp_solver.add(oc <= 2 * input.NUM_CAR_TYPE[input.SEDAN] + 4 * input.NUM_CAR_TYPE[input.VAN])
        # shotgun
        elif seat_type == input.SHOTGUN:
            total = input.NUM_CAR_TYPE[input.SEDAN] + input.NUM_CAR_TYPE[input.VAN] + input.NUM_CAR_TYPE[input.SPORTS]
            assert(len(config_info[input.CAR_DELIM]) == total)
            cp_solver.add(oc <= total)
        # middle
        elif seat_type == input.MIDDLE:
            cp_solver.add(oc <= input.NUM_CAR_TYPE[input.SEDAN] + input.NUM_CAR_TYPE[input.VAN])

    # encode constraint: seat type restrictions
    for name in name_list:
        oc = IntVal(0)
        for car_num in range(len(car_type_list)):
            for seat_restriction_type in config_info[name]:
                oc = oc + X_p_c_s[name_index[name]][car_num][seat_restriction_type]
        
        cp_solver.add(oc == 0)

        # create a backtracking point, in case peer constraints don't work out
    cp_solver.push()

def generate_output(config_info: dict, cp_solver: Solver) -> None:
    # run the solver <<modify for both test cases>>.,
    print(cp_solver.check())
    m = cp_solver.model()

def main() -> None:
    # gather user input
    input.main()
    # sanity checks
    sanity_check(input.config_info)
    
    # convert specifications to a series of z3 constraints
    # z3.set_param('parallel.enable', True)
    # z3.set_param('parallel.threads.max', 32)
    carpool_solver = Solver()
    configure_solver(input.config_info, carpool_solver)

    # run solver and generate
    generate_output(input.config_info, carpool_solver)

# add more methods for stretch goals to parse seating requeusts with specific individuals
if __name__ == '__main__':
    main()