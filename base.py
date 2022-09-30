from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = 'Бой не закончен'

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> str:
        """ Проверка здоровья игрока и врага """
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья"
            return self._end_game()
        elif self.enemy.hp <= 0:
            self.battle_result = f"Игрок {self.player.name} выиграл битву"
            return self._end_game()
        elif self.player.hp <= 0:
            self.battle_result = f"Игрок {self.player.name} проиграл битву"
            return self._end_game()
        # return self.battle_result

    def _stamina_regeneration(self):
        """ Регенерация стамины для игрока и врага за ход """
        self.player.add_stamina(self.STAMINA_PER_ROUND)
        self.enemy.add_stamina(self.STAMINA_PER_ROUND)

    def next_turn(self):
        """ КНОПКА СЛЕДУЮЩИЙ ХОД """
        result = self._check_players_hp()
        if result:
            return result
        self._stamina_regeneration()
        return self.enemy.hit(self.player)

    def _end_game(self) -> str:
        """ КНОПКА ЗАВЕРШЕНИЕ ИГРЫ """
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self) -> str:
        """ КНОПКА УДАР ИГРОКА """
        self.player.hit(self.enemy)
        self.next_turn()
        return self.player.hit(self.enemy)

    def player_use_skill(self):
        """ КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ """
        self.player.use_skill(self.enemy)
        self.next_turn()
        return self.player.use_skill(self.enemy)
