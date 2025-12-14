from .projectile import Projectile
from .projectile_constants import *

class ProjectileController:
    def __init__(self):
        self.projectiles = []
        self.cooldown = 0
    
    def spawn_projectile(self, x_pos, y_pos, heading):
        if self.cooldown <= 0:
            print("spawning new projectile at ", x_pos, ", ", y_pos)
            new_projectile = Projectile(x_pos, y_pos, heading)
            self.projectiles.append(new_projectile)
            self.cooldown = COOLDOWN_SECONDS

    
    def update_projectiles(self, time_elapsed):
        self.cooldown -= time_elapsed / 1000

        for projectile in self.projectiles:
            update = projectile.update()
            if not update:
               self.projectiles.remove(projectile)



