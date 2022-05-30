import os, sys

SEDAN = 0 # corresponds to index in SEAT_COUNT and NUM_CAR_TYPE array for this variable's car type
SPORTS = 1
VAN = 2
WINDOW = 0
SHOTGUN = 1
MIDDLE = 2

CAR_DELIM = "CARS"
SEAT_DELIM = "SEATS"
SEAT_END_DELIM = "END_SEAT"
AVOID_DELIM = "AVOID"
AVOID_END_DELIM = "END_AVOID"
NUM_PEOPLE = "NUM_PEOPLE"
PEOPLE_LIST = "NAMES"
SEAT_COUNT = [4, 1, 6]
NUM_CAR_TYPE = [0, 0, 0]

CONFIG_FOLDER = "configs"
SOLUTION_FOLDER = "solutions"

config_info = {}

def get_car_types(path: str) -> None:
    """
    Parses configuration file and extracts car types
    path: path to input configuration file
    rtype: None 
    """
    with open(path, "r") as in_file:
        cur_str = in_file.readline()
        while cur_str and cur_str != f"{CAR_DELIM}\n":
            cur_str = in_file.readline()
        
        car_config = in_file.readline()
        if not car_config:
            raise IOError(f"No delimiter for {CAR_DELIM} in input file or missing car information.")
        
        car_config = car_config.strip()
        car_config_arr = car_config.split(" ")
        
        # convert to integers and save into configuration dictonary
        car_config_arr = [int(elem) for elem in car_config_arr]
        config_info[CAR_DELIM] = car_config_arr
        
def get_seat_requirements(path: str) -> None:
    """
    Parses configuration file and extracts seat types per user
    path: path to input configuration file
    rtype: None
    """
    elems_added = 0
    with open(path, "r") as in_file:
        cur_str = in_file.readline()
        while cur_str and cur_str != f"{SEAT_DELIM}\n":
            cur_str = in_file.readline()
        
        if not cur_str:
            raise IOError(f"No delimeter for {SEAT_DELIM} in input file.")
        
        seat_config = in_file.readline()
        config_info[PEOPLE_LIST] = [] # create array to store names of people

        while seat_config and (seat_config != f"{SEAT_END_DELIM}\n" and seat_config != SEAT_END_DELIM):
            seat_config = seat_config.strip()
            
            # prevent empty string from being counted as a constraint
            if len(seat_config) != 0:
                seat_config_arr = seat_config.split(" ")

                name = seat_config_arr[0].lower()
                config_info[PEOPLE_LIST].append(name)
                seat_config_arr = seat_config_arr[1:]
                
                # convert to integers and save into configuration dictonary
                seat_config_arr = [int(elem) for elem in seat_config_arr]

                if name in config_info:
                    raise ValueError("Repeated name in input file.")

                config_info[name] = seat_config_arr
                elems_added += 1

            seat_config = in_file.readline()
            

    config_info[NUM_PEOPLE] = elems_added
    if elems_added == 0:
        raise IOError(f"No seat data found.")

def main() -> None:
    f_name = input("Enter the name of the desired configuration file from the config folder: ")
    input_file_name = os.path.join(CONFIG_FOLDER, f_name)
    path = os.path.join(sys.path[0], input_file_name)
    get_car_types(path)
    get_seat_requirements(path)
    
    # print(config_info)
    
# add more methods for stretch goals to parse seating requeusts with specific individuals
if __name__ == '__main__':
    main()