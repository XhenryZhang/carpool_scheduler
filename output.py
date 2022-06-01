import os, sys, datetime
import input

SOLUTION_FOLDER = "solutions"

def write_file(path: str, seat_info: dict) -> None:
    '''
    Outputs to the specified path the answer to the scheduling.
    path: path to write the new file
    seat_info: contains scheduling answers
    rtype: None
    '''
    with open(path, "w") as out_file:
        if len(seat_info) > 0:
            for key, value in sorted(seat_info.items()):
                # seat_type : list of the names of each rider in that seat
                rider_positions = {
                    input.SEAT_TYPES[input.WINDOW]: [],
                    input.SEAT_TYPES[input.SHOTGUN]: [],
                    input.SEAT_TYPES[input.MIDDLE]: []
                }
                car_type = input.CAR_TYPES[input.config_info[input.CAR_DELIM][key]]
                out_file.write(f'==== Car #{key + 1}: {car_type} ====\n')
                for riders in value:
                    rider_positions[input.SEAT_TYPES[int(riders[1])]].append(riders[0])

                # output to file
                for key, value in rider_positions.items():
                    out_file.write(f'{key}: ')
                    for name in value:
                        out_file.write(f'{name} ')

                    # sports cars don't have window or middle seat type
                    if car_type == input.CAR_TYPES[input.SPORTS] and (key == input.SEAT_TYPES[input.WINDOW] or key == input.SEAT_TYPES[input.MIDDLE]):
                        out_file.write('N / A')

                    out_file.write('\n')
        else:
            out_file.write('The provided constraints are unsatisfiable.\n')

def generate_output(seat_info: dict) -> None:
    print('Generating output...')

    # generate path to new file to create
    output_file_name = os.path.join(SOLUTION_FOLDER, input.target_file)
    date_time = datetime.datetime.now()
    output_file_name = '{}_{}'.format(output_file_name, date_time.strftime("%m%d%Y%H%M%S%f"))
    path = os.path.join(sys.path[0], output_file_name)

    write_file(path, seat_info)
    print(f'Output written to file: {path}')