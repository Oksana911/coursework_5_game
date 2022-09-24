from flask import Flask, render_template, request, redirect, url_for

from classes import WarriorClass, ThiefClass, unit_classes
from equipment import Equipment
from unit import PlayerUnit, EnemyUnit
from base import Arena

app = Flask(__name__)

heroes = {
    "player": PlayerUnit(name="Игрок", unit_class=WarriorClass),
    "enemy": EnemyUnit(name="Враг", unit_class=ThiefClass)
}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template('fight.html', heroes=heroes, result="Начало битвы")


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    arena._end_game()
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    if request.method == 'GET':
        header = "Выбор героя"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        return render_template("hero_choosing.html",
                               result={"header": header, "weapons": weapons, "armors": armors, "classes": classes})

    if request.method == 'POST':
        name = request.form['name']
        unit_class = request.form['unit_class']
        weapon = request.form['weapon']
        armor = request.form['armor']
        new_player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        new_player.equip_weapon(Equipment().get_weapon(weapon))
        new_player.equip_armor(Equipment().get_armor(armor))
        heroes['player'] = new_player
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    if request.method == 'GET':
        header = "Выбор врага"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        return render_template("hero_choosing.html",
                               result={"header": header, "weapons": weapons, "armors": armors, "classes": classes})

    if request.method == 'POST':
        name = request.form['name']
        unit_class = request.form['unit_class']
        weapon = request.form['weapon']
        armor = request.form['armor']
        new_enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        new_enemy.equip_weapon(Equipment().get_weapon(weapon))
        new_enemy.equip_armor(Equipment().get_armor(armor))
        heroes['enemy'] = new_enemy
        return redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run(debug=True)
