from flask import request, flash, redirect, url_for, render_template
from .forms import LoginForm, SignupForm, PokemaneForm
from .models import User, Pokemon, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
import requests
from .battle_logic import Pokemon_battle, execute_battle_step, calculate_damage
import random


def init_routes(app):
    # auth routes
    @app.route("/signup", methods=['GET', 'POST'])
    def signup():
        form = SignupForm()
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data.lower()
            password = form.password.data
            new_user = User(first_name, last_name, email, password)
            db.session.add(new_user)
            db.session.commit()

            flash(f'Thank you for signing up {new_user.first_name}! :)', 'success')
            return redirect(url_for('login'))
        return render_template('signup.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data.lower()
            password = form.password.data
            queried_user = User.query.filter(User.email == email).first()
            if queried_user and check_password_hash(queried_user.password, password):
                login_user(queried_user)
                flash(f'Hello {queried_user.first_name}, thanks for coming back! :)', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password, try again playa', 'danger')
                return redirect(url_for('login'))
        return render_template('login.html', form=form)

    @app.route("/logout")
    def logout():
        user_first_name = current_user.first_name if current_user.is_authenticated else "User"
        logout_user()
        flash(f"Thanks for coming, {user_first_name}! See ya next time!.", "primary")
        return redirect(url_for('home'))

    # main routes
    @app.route("/")
    @app.route("/home")
    def home():
        return render_template('home.html')

    @app.route("/pokemon", methods=['GET', 'POST'])
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

    @app.route("/catch_pokemon/<pokemon_name>", methods=['GET', 'POST'])
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
            return redirect(url_for('get_pokemanes'))
        return redirect(url_for('get_pokemanes'))

    @app.route("/team")
    @login_required
    def team():
        return render_template("team.html", user=current_user)

    @app.route("/enemy_teams")
    def enemy_teams():
        other_users = User.query.filter(User.id != current_user.id).all()
        return render_template("enemy_teams.html", other_users=other_users)

    @app.route("/release_pokemon/<int:pokemon_id>")
    @login_required
    def release_pokemon(pokemon_id):
        pokemon = Pokemon.query.get(pokemon_id)
        if pokemon and pokemon in current_user.team_pokemons:
            current_user.team_pokemons.remove(pokemon)
            db.session.commit()
            flash(f"You released {pokemon.name} from your team.", "success")
        else:
            flash("Unable to release Pokémon.", "danger")

        return redirect(url_for('team'))

    @app.route('/battle', methods=['GET', 'POST'])
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
