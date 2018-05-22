import sys, json, math


commands = []
teller = 0

def move(command):
    commands.append(command);

def executeMoves():
    record = {'moves': commands}
    print(json.dumps(record))
    sys.stdout.flush()


for line in sys.stdin:
    commands = []
    state = json.loads(line)
    # find planet with most ships
    my_planets = [p for p in state['planets']   if p['owner'] == 1]
    other_planets = [p for p in state['planets'] if p['owner'] != 1]
    my_expeditions = [p for p in state['expeditions'] if p['owner'] == 1]
    incoming_expeditions = [p for p in state['expeditions'] if p['owner'] != 1]

    #attackedPlanets = []
    for expedition in my_expeditions:
        # attackedPlanets.append(expedition['destination'])
        for planet in other_planets:
            if (expedition['destination'] == planet['name']):
                other_planets.remove(planet)

    # endangeredPlanets = []
    for expedition in incoming_expeditions:
        for planet in my_planets:
            if (expedition['destination'] == planet['name']):
                shipsToKeep = expedition['ship_count'] - expedition['turns_remaining']
                if(shipsToKeep > 0):
                    planet['ship_count'] = planet['ship_count'] - shipsToKeep

    if not my_planets or not other_planets:
        move(None)
    else:
        for originPlanet in my_planets:
            currentTarget = None
            currentFleetsNeeded = originPlanet['ship_count']
            for victimPlanet in other_planets:
                fleetsNeeded = victimPlanet['ship_count']
                if victimPlanet['owner']:
                    fleetsNeeded += math.sqrt(math.pow(originPlanet['x'] - victimPlanet['x'], 2) + math.pow(originPlanet['y'] - victimPlanet['y'], 2))
                fleetsNeeded = math.ceil(fleetsNeeded)
                if fleetsNeeded < currentFleetsNeeded:
                    currentFleetsNeeded = fleetsNeeded
                    currentTarget = victimPlanet
            if (currentTarget != None) and ((currentFleetsNeeded + 1) < originPlanet['ship_count']):
                #if (currentTarget['name'] not in attackedPlanets):
                if(True):
                    newMove = {
                        'origin': originPlanet['name'],
                        'destination': currentTarget['name'],
                        'ship_count': currentFleetsNeeded + 1
                    }
                    move(newMove)
                    other_planets.remove(currentTarget)
    executeMoves()
