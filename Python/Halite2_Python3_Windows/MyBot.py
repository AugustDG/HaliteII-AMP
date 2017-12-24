"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging
# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("AMP-Settler")
# Then we print our start message to the logs
logging.info("Starting my Settler bot!")

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()
    planets = game.map.all_planets()
    ships = game_map.get_me().all_ships()
    largest_planet = max(Lplanet.radius for Lplanet in planets)

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    # For every ship that I control
    for ship in range(0,len(ships)):
        # If the ship is docked
        if ships[ship].docking_status != ships[ship].DockingStatus.UNDOCKED:
            # Skip this ship
            continue       

        # For each planet in the game (only non-destroyed planets are included)
        for planet in range(0, len(planets)):
            # If the planet is owned
            if planets[planet].is_owned():
                # Skip this planet               
                continue

            if ships[ship].can_dock(largest_planet):
                command_queue.append(ships[ship].dock(largest_planet))
            else:
                Lnavigate_command = ships[ship].navigate(largest_planet, game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships=False)

                if Lnavigate_command:
                    command_queue.append(Lnavigate_command)
            break
            # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
            if ships[ship].can_dock(planets[planet]):
                # We add the command by appending it to the command_queue
                command_queue.append(ships[ship].dock(planets[planet]))
            else:
                # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
                # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
                # We run this navigate command each turn until we arrive to get the latest move.
                # Here we move at half our maximum speed to better control the ships
                # In order to execute faster we also choose to ignore ship collision calculations during navigation.
                # This will mean that you have a higher probability of crashing into ships, but it also means you will
                # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
                # wish to turn that option off.
                navigate_command = ships[ship].navigate(
                    ships[ship].closest_point_to(planets[ship%len(planets)]),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)
                # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                # or we are trapped (or we reached our destination!), navigate_command will return null;
                # don't fret though, we can run the command again the next turn)
                if navigate_command:
                    command_queue.append(navigate_command)
            break
    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
