import os, sys

# ---- ADD YOUR OWN CAR BUILDS ----
CAR_TYPES = ['Sedan', 'Sports Car', 'Van']
SEDAN = 0 
SPORTS = 1
VAN = 2

# ---- ADD YOUR OWN SEAT TYPES ----
SEAT_TYPES = ['Window', 'Shotgun', 'Middle']
WINDOW = 0
SHOTGUN = 1
MIDDLE = 2

# ---- CHANGE BASED ON YOUR CAR BUILDS and SEAT TYPES ----
# SEAT_COUNTS[car_build][seat_type] = total number of seats of seat_type on car_build
SEAT_COUNTS = [[2, 1, 1], [0, 1, 0], [4, 1, 1]]

# ---- DETERMINES INPUT DIRECTORY FOR CONFIGURATION FILES ----
CONFIG_FOLDER = "configs"

# ==== CONSTANTS USED TO PARSE CONFIGURATION FILES ====
CAR_DELIM = "CARS"
SEAT_DELIM = "SEATS"
SEAT_END_DELIM = "END_SEAT"
AVOID_DELIM = "AVOID"
AVOID_END_DELIM = "END_AVOID"
NUM_PEOPLE = "NUM_PEOPLE"
PEOPLE_LIST = "NAMES"

target_file = ""
num_car_type = [0, 0, 0]
config_info = {}

def get_car_types(path: str) -> None:
    """
    Parses configuration file and extracts car build types
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
    global target_file
    assert len(SEAT_COUNTS) > 0
    assert len(SEAT_COUNTS[0]) == len(SEAT_TYPES)
    assert len(SEAT_COUNTS) == len(CAR_TYPES)

    f_name = input(f"Enter the name of the desired configuration file from the {CONFIG_FOLDER} folder: ")
    input_file_name = os.path.join(CONFIG_FOLDER, f_name)
    path = os.path.join(sys.path[0], input_file_name)
    target_file = f_name
    get_car_types(path)
    get_seat_requirements(path)

    # print(config_info)
    
# add more methods for stretch goals to parse seating requeusts with specific individuals
if __name__ == '__main__':
    main()