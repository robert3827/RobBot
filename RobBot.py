  
import sc2
import quickOracles
import stalkersBad
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer





def main():
    sc2.run_game(sc2.maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, quickOracles.quickOracles()),
    Computer(Race.Terran, Difficulty.Hard)
], realtime=False)

if __name__ == '__main__':
    main()