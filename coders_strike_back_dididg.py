import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

checkpoints = {}
pos = {}
# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    
    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"

    # in case of a collision if the opponent is in front of me, colliding is an advantage to me
    # but in case of a collision if the opponent is behind me, colliding is an advantage to them
    


    # creating the dictionary of checkpoints
    # i want each next checkpoint to be the key to the next next checkpoint
    next_cp = (next_checkpoint_x, next_checkpoint_y)
    if next_cp in checkpoints:
        # get the next next checkpoint
        next_next_x, next_next_y = checkpoints[next_cp]
        if 0 in checkpoints:
        # if dict is complete, remove the 0
            checkpoints.pop(0)
    else: 
        next_next_x, next_next_y = 8000, 4500
        # if dict is not complete, keep adding keys:values
        if 0 in checkpoints:
            previous = checkpoints[0]
            if previous != next_cp:
                checkpoints[previous]=next_cp
                checkpoints[0]=next_cp
        else:
            checkpoints[0]=next_cp


    
    # get the previous position and current position
    # to infer if I am reaching the next checkpoint
    if 0 in pos:
        prev_x,prev_y = pos[0]

        speed_x, speed_y = x-prev_x, y-prev_y
    
        # determining if we want to turn to the next next cp before reaching the next one
        nx, ny = x, y
        sx, sy = speed_x, speed_y
        for i in range(3):
            sx, sy = 0.85*sx, 0.85*sy
            nx, ny = nx + sx, ny + sy
        # if in the next 3 turns we are able to slide to the next checkpoint
        # then we should begin turning towards the next next cp
        if (next_checkpoint_x-nx)**2+(next_checkpoint_y-ny)**2<600**2:
            thrust = 0
            print(str(next_next_x) + " " + str(next_next_y) + " SHIELD")
            continue

    # in any case, we store the new position to compute the speed next turn
    pos[0]=(x,y)

    # if opponent is close, speed is not too slow and we want to keep the current direction
    # use the shield
    if (x-opponent_x)**2+(y-opponent_y)**2 < 450**2:
        if next_checkpoint_angle < 20 and next_checkpoint_angle > -20:
            print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " SHIELD")
            continue





    # Thrust value depending on angle and checkpoint distance
    if next_checkpoint_angle > 90 or next_checkpoint_angle < -90:
        thrust = 0
    elif next_checkpoint_angle > 45 or next_checkpoint_angle < -45:
        thrust = 50
    else:
        thrust = 100

    # slow down a bit when approaching a checkpoint
    #if next_checkpoint_dist < 1000: thrust = max(0,thrust - 20 + next_checkpoint_dist//100)
    #if next_checkpoint_dist < 800: thrust = 10





    # print output
    # Boost or no boost
    if next_checkpoint_dist > 3000 and next_checkpoint_angle == 0:
        print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " BOOST")
        
    else:
        print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + str(thrust))
