from . import main
from flask import render_template, request, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
import requests 
from ..auth.forms import PokemaneForm
from app.models import Pokemon, teams, db, User
from .battle_logic import Pokemon_battle, execute_battle_step, calculate_damage  
import random


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/pokemon", methods=['GET', 'POST'])
@login_required
def get_pokemanes():
    form = PokemaneForm()
    pokemon_names = []
    
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_names = form.pokemane.data.lower()
        print(pokemon_names)
        pokemon = Pokemon.query.filter_by(name=pokemon_names).first()

        if pokemon:
      
            pokemanes_dict = {
                "name": pokemon.name,
                "ability_name": pokemon.ability_name,
                "base_experience": pokemon.base_experience,
                "sprite_url": pokemon.sprite_url,
                "attack_base_stat": pokemon.attack_base_stat,
                "hp_base_stat": pokemon.hp_base_stat,
                "defense_base_stat": pokemon.defense_base_stat
            }
            return render_template("pokemon.html", pokemanes_dict=pokemanes_dict, form=form)
        else:
            url = "https://pokeapi.co/api/v2/pokemon/"
            response = requests.get(url + pokemon_names)
            
            if response.ok:
                data = response.json()
                
                pokemanes_dict = {
                    "name": data["name"],
                    "ability_name": data["abilities"][0]["ability"]["name"],
                    "base_experience": data["base_experience"],
                    "sprite_url": data["sprites"]["front_shiny"],
                    "attack_base_stat": data["stats"][1]["base_stat"],
                    "hp_base_stat": data["stats"][0]["base_stat"],
                    "defense_base_stat": data["stats"][2]["base_stat"]
                }
                
                new_pokemon = Pokemon(
                name=pokemanes_dict['name'],
                sprite_url=pokemanes_dict['sprite_url'],
                attack_base_stat=pokemanes_dict['attack_base_stat'],
                base_experience=pokemanes_dict['base_experience'],
                hp_base_stat=pokemanes_dict['hp_base_stat'],
                defense_base_stat=pokemanes_dict['defense_base_stat'],
                ability_name=pokemanes_dict['ability_name'],
                )

                db.session.add(new_pokemon)
                db.session.commit()

                return render_template("pokemon.html", pokemanes_dict=pokemanes_dict, form=form)
            else:
                return render_template("pokemon.html", form=form)
    
    return render_template("pokemon.html", form=form)


@main.route("/catch_pokemon/<pokemon_name>", methods=['GET', 'POST'])
@login_required
def catch_pokemon(pokemon_name):
    if request.method == 'POST':
        
        pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
        
        if pokemon in current_user.team_pokemons:
            flash(f"WYD!? You already have {pokemon.name} in your team...", "warning")
        elif current_user.can_add_pokemon_to_team():
            current_user.team_pokemons.append(pokemon)
            db.session.commit()
            flash(f"You caught {pokemon.name}!", "success")
        else:
            flash("WYD?! Your team is full. Release a Pokémon before adding more...", "danger")
        return redirect(url_for('main.get_pokemanes'))
    else:
        return redirect(url_for('main.get_pokemanes'))
      
@main.route("/team")
@login_required
def team():
    return render_template("team.html", user=current_user)

@main.route("/enemy_teams")
def enemy_teams():
    other_users = User.query.filter(User.id != current_user.id).all()
    return render_template("enemy_teams.html", other_users=other_users)

@main.route("/release_pokemon/<int:pokemon_id>")
@login_required
def release_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon and pokemon in current_user.team_pokemons:
        current_user.team_pokemons.remove(pokemon)
        db.session.commit()
        flash(f"You released {pokemon.name} from your team.", "success")
    else:
        flash("Unable to release Pokémon.", "danger")
    
    return redirect(url_for('main.team'))  

@main.route('/battle', methods=['GET', 'POST'])
@login_required
def battle():
    selected_enemy_user_id = request.args.get('enemy_user_id')
    selected_enemy_user = User.query.get(selected_enemy_user_id)

    current_step = int(request.form.get('step', 0)) if request.method == 'POST' else 0

    user_team = [Pokemon_battle(
        pokemon.name,
        pokemon.hp_base_stat,
        pokemon.attack_base_stat,
        pokemon.defense_base_stat,
        sprite_url=pokemon.sprite_url
    ) for pokemon in current_user.team_pokemons]

    enemy_team = [Pokemon_battle(
        pokemon.name,
        pokemon.hp_base_stat,
        pokemon.attack_base_stat,
        pokemon.defense_base_stat,
        sprite_url=pokemon.sprite_url
    ) for pokemon in selected_enemy_user.team_pokemons]

    battle_state = None
    messages = []
    messages2 = []
    if request.method == 'POST':
        battle_state, messages, messages2 = execute_battle_step(user_team, enemy_team, current_step)
    
    if battle_state == "You Have Defeated The Ops":
        flash("Noiceee! Your team won the battle! Great Success!", "success")
    elif battle_state == "The Enemy Has Defeated You":
        flash("Oh no! Your team lost the battle! Edit your team and come back again playa", "danger")

    return render_template('battle.html', battle_state=battle_state, selected_enemy_user=selected_enemy_user, current_step=current_step, user_team=user_team, enemy_team=enemy_team, messages=messages, messages2=messages2)