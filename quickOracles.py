import sc2
from sc2.position import Point2
from sc2.constants import *
import random


class quickOracles(sc2.BotAI):
    def __init__(self):
        self.TECH_TREE = [PYLON, GATEWAY, CYBERNETICSCORE, GATEWAY]
        #self.PROD = []
        WORKERCAP = 50
        
    @staticmethod 
    def distance(posX, posY):
        return ((posX.X()-posY.X())**2)+ ((posX.Y()-posY.Y())**2)

    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.expand()
        await self.techTree()
        await self.production()
        await self.selfDefense()


    async def build_workers(self):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))

    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near=Point2((50,50)))

    async def build_assimilators(self):
        for nexus in self.units(NEXUS).ready:
            vaspenes = self.state.vespene_geyser.closer_than(15.0, nexus)
            for vaspene in vaspenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vaspene.position)
                if worker is None:
                    break
                if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                    await self.do(worker.build(ASSIMILATOR, vaspene))

    async def expand(self):
        if self.units(NEXUS).amount < 2 and self.can_afford(NEXUS):
            await self.expand_now()

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]

    async def techTree(self):
        if(self.units(PYLON).ready.exists):
            pylon = self.units(PYLON).ready.random
            counterDict = {}
            for tech in self.TECH_TREE:
                if not tech in counterDict.keys():
                    counterDict[tech] = 1
                else:
                    counterDict[tech] += 1
                
                if self.can_afford(tech) and not self.already_pending(tech) and len(self.units(tech)) < counterDict[tech]:
                    await self.build(tech, near=pylon)
    
    async def multiBuild(self, unit, count, nearCamp):
        for ii in range(0,count):
            await self.build(unit, near=nearCamp)

                            
    async def production(self):
        if(self.units(CYBERNETICSCORE).ready.exists):
            cyberCore = self.units(CYBERNETICSCORE).ready.random
            for gw in self.units(GATEWAY).ready.noqueue:
                if self.can_afford(STALKER) and self.supply_left > 0:
                    await self.do(gw.train(STALKER))
            if len(self.units(GATEWAY).ready.noqueue) == 0 and self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                await self.build(GATEWAY, near=cyberCore)

    async def selfDefense(self):
        for enemy in self.known_enemy_units:
            for unit in self.units:
                if(unit != PROBE and self.distance(unit.position, enemy.position)< 69):
                    unit.attack(enemy)
    
                    





