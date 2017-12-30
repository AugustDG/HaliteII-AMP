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

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []

    # For every ship that I control
    for ship in range(0,len(ships)):
        entities_by_distance = game_map.nearby_entities_by_distance(ship)
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
                for current in range(0, len(ships)):
                    ships[current].navigate(ship.closest_point_to(planets[current%len(planets)]), game_map, speed=hlt.constants.MAX_SPEED/2))

                    command_queue.append(Lnavigate_command)
            break
           
    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
