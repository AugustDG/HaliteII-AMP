using Halite2.hlt;
using System.Collections.Generic;

namespace Halite2
{
  public class MyBot
  {

    public static void Main(string[] args)
    {
      string name = args.Length > 0 ? args[0] : "Sharpie";

      Networking networking = new Networking();
      GameMap gameMap = networking.Initialize(name);
      Planet largestPlanet;

      List<Planet> selectedPlanets = new List<Planet>();

      List<Move> moveList = new List<Move>();
      for (; ; )
      {
        moveList.Clear();
        gameMap.UpdateMap(Networking.ReadLineIntoMetadata());

        foreach (Ship ship in gameMap.GetMyPlayer().GetShips().Values)
        {

          if (ship.GetDockingStatus() != Ship.DockingStatus.Undocked)
          {
            continue;
          }

          foreach (Planet planet in gameMap.GetAllPlanets().Values)
          {
            if (planet.IsOwned())
              break;

            largestPlanet = gameMap.GetPlanet(4);

            if (planet.GetRadius() > largestPlanet.GetRadius())
            {
              largestPlanet = planet;
              break;
            }

            foreach (Planet sPlanet in selectedPlanets)
            {
              if (sPlanet == largestPlanet)
                break;
            }
         
            if (ship.CanDock(largestPlanet))
            {
              moveList.Add(new DockMove(ship, largestPlanet));
              selectedPlanets.Add(largestPlanet);
              break;
            }
            else
            {
              ThrustMove newLThrustMove = Navigation.NavigateShipToDock(gameMap, ship, largestPlanet, Constants.MAX_SPEED);
              if (newLThrustMove != null)
              {
                moveList.Add(newLThrustMove);
                selectedPlanets.Add(largestPlanet);
                break;
              }
            }

            foreach (Planet sPlanet in selectedPlanets)
            {
              if (sPlanet == planet)              
                break;
            }

            if (ship.CanDock(planet))
            {                        
              moveList.Add(new DockMove(ship, planet));
              selectedPlanets.Add(planet);
              break;
            }
            else
            {

              ThrustMove newThrustMove = Navigation.NavigateShipToDock(gameMap, ship, planet, Constants.MAX_SPEED);
              if (newThrustMove != null)
              {
                moveList.Add(newThrustMove);
                selectedPlanets.Add(largestPlanet);
              }

              break;
            }
          }
        }
        Networking.SendMoves(moveList);
      }
    }
  }
}

