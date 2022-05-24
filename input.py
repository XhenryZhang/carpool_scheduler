import os, sys

SEDAN = 0
SPORTS = 1
VAN = 2
CAR_DELIM = "CARS"
SEAT_DELIM = "SEATS"
SEAT_END_DELIM = "END_SEAT"

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
    with open(path, "r") as in_file:
        cur_str = in_file.readline()
        while cur_str and cur_str != f"{SEAT_DELIM}\n":
            cur_str = in_file.readline()
        
        if not cur_str:
            raise IOError(f"No delimeter for {SEAT_DELIM} in input file.")
        
        seat_config = in_file.readline()
        while seat_config and (seat_config != f"{SEAT_END_DELIM}\n" and seat_config != SEAT_END_DELIM):
            seat_config = seat_config.strip()
            seat_config_arr = seat_config.split(" ")

            name = seat_config_arr[0]
            seat_config_arr = seat_config_arr[1:]
            
            # convert to integers and save into configuration dictonary
            seat_config_arr = [int(elem) for elem in seat_config_arr]
            config_info[name] = seat_config_arr
            seat_config = in_file.readline()

def main() -> dict[str, list[int]]:
    f_name = input("Enter the name of the desired configuration file from the config folder: ")
    input_file_name = os.path.join("configs", f_name)
    path = os.path.join(sys.path[0], input_file_name)
    get_car_types(path)
    get_seat_requirements(path)
    
    return config_info
    
# add more methods for stretch goals to parse seating requeusts with specific individuals
if __name__ == '__main__':
    main()