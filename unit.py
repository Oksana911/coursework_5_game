from __future__ import annotations
from abc import ABC
from equipment import Weapon, Armor
from classes import UnitClass
from random import uniform
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        """ Присваиваем нашему герою новое оружие """
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        """ Одеваем новую броню """
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        """ логика расчета урона игрока, логика расчета брони цели """

        self.stamina -= self.weapon.stamina_per_hit

        damage = self.weapon.damage * self.unit_class.attack

        if target.stamina > target.armor.stamina_per_turn:
            target_armor = target.armor.defence * target.unit_class.armor
            target.stamina -= target.armor.stamina_per_turn
        else:
            target_armor = 0

        target.get_damage(damage - target_armor)
        return round(damage - target_armor)

    def get_damage(self, damage: int) -> Optional[int]:
        """ Получение урона целью """
        if damage:
            self.hp -= damage
            return round(damage, 1)
        return 0

    def hit(self, target: BaseUnit) -> str:
        """ Удар """
        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            if damage > 0:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
            else:
                return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

    def use_skill(self, target: BaseUnit) -> str:
        """ Метод использования умения """
        if self._is_skill_used:
            return "Навык использован"
        else:
            if self.unit_class.skill._is_stamina_enough:
                self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)

    def add_stamina(self, stamina_points):
        """ Добавление стамины, используется при регенерации """
        if self.stamina + stamina_points * self.unit_class.stamina > self.unit_class.max_stamina:
            self.stamina = self.unit_class.max_stamina
        else:
            self.stamina += stamina_points * self.unit_class.stamina


class PlayerUnit(BaseUnit):
    pass


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """ Метод удар соперника """
        if uniform(1, 100) in range(1, 10):
            if self.stamina > self.unit_class.skill.stamina and not self._is_skill_used:
                return self.use_skill(target)
        return super().hit(target)
