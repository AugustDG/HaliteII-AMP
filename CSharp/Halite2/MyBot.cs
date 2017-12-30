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

      List<Planet> currentPlanets = new List<Planet>();
      List<Ship> currentShips = new List<Ship>();

      List<Move> moveList = new List<Move>();

      for (; ; )
      {
        moveList.Clear();
        gameMap.UpdateMap(Networking.ReadLineIntoMetadata());

        currentShips.AddRange(gameMap.GetMyPlayer().GetShips().Values);
        currentPlanets.AddRange(gameMap.GetAllPlanets().Values);

        foreach (Ship ship in gameMap.GetMyPlayer().GetShips().Values)
        {

          if (ship.GetDockingStatus() != Ship.DockingStatus.Undocked)
          {
            continue;
          }

          foreach (Planet planet in gameMap.GetAllPlanets().Values)
          {
            if (planet.IsOwned())
            {
              continue;
            }

            largestPlanet = planet;

            if (planet.GetRadius() > largestPlanet.GetRadius())
            {
              largestPlanet = planet;
              if (planet.GetDistanceTo(ship) < largestPlanet.GetDistanceTo(ship))
              {
                largestPlanet = planet;
              }
            }       

            if (ship.CanDock(largestPlanet))
            {
              moveList.Add(new DockMove(ship, largestPlanet));
              break;
            }
            else
            {
              ThrustMove newLThrustMove = Navigation.NavigateShipToDock(gameMap, ship, largestPlanet, Constants.MAX_SPEED);
              if (newLThrustMove != null)
              {
                moveList.Add(newLThrustMove);
                break;
              }
            }
          }
        }
        Networking.SendMoves(moveList);
      }
    }
  }
}
