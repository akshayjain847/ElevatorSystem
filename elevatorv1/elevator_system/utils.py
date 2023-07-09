class ElevatorUtility:
    def update_list_of_request_in_elevator(self, optimal_elevator, floor_requested, floor_list):
        optimal_current_floor = optimal_elevator.current_floor
        optimal_direction = optimal_elevator.direction
        if optimal_current_floor not in floor_list:
            floor_list.insert(0, optimal_current_floor)

        if floor_requested in floor_list:
            return floor_list

        if len(floor_list) == 0:
                floor_list.append(floor_requested)
        elif floor_requested >= floor_list[0]:
            index = 0
            while index < len(floor_list) and floor_requested >= floor_list[index]:
                index += 1
            floor_list.insert(index, floor_requested)
        else:
            index = 0
            while index < len(floor_list) and floor_requested <= floor_list[index]:
                index += 1
            floor_list.insert(index, floor_requested)

        return floor_list
    
    def calculate_time_to_reach_floor(self, elevator, floor):
        if elevator.direction == 'up':
            if floor >= elevator.current_floor:
                return abs(floor - elevator.current_floor)
            else:
                return 2 * (elevator.current_floor - floor)  # Time to reach the top floor and then come back down
        elif elevator.direction == 'down':
            if floor <= elevator.current_floor:
                return abs(floor - elevator.current_floor)
            else:
                return 2 * (elevator.current_floor - floor)  # Time to reach the bottom floor and then come back up
        else:
            return abs(floor - elevator.current_floor)