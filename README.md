# WK-5-Pokemon-Site
# Day 2- Poke Forms and Models 
Build a Flask Application that has a home page that just greets the user, and then a second route that will have a form to enter a pokemon name that will on submit update the page with some properties listed about the pokemon(properties listed below).  Use your homework from last Thursday when we did this during python to help you with your API call. 

NOTE YOU WILL BE BUILDING ON THIS APPLICATION FOR THE NEXT TWO WEEKS!
Eventually you will have your user type in a name of a pokemon then check to see if that pokemon is saved in your database, if it is not you will reach out to https://pokeapi.co/ to get the pokemon's information and then save it to your database.  You will allow every user to have up to 5 pokemon (with the ability to remove pokemon too)


There will then be a page where the user can browse other users and then have a choice to attack other users.  You will then compare the pokemon in the user's collection with the pokemon in the other users collection and determine a winner (this determination method can be as simple or as complicated as you like, but you will have to use the information from the pokeapi to decide your winners.)


pokemon properties to include:
                pokemon name
       from the stats section:
                 base stat for hp
                 base stat for defense
                 base stat for attack
       from the sprites section:
                 front_shiny (URL to the image) or any other image you like more 
       from the abilities section:
                 At Least One Ability
and any other properties you might find that interest you.


Upload to github and submit the link to classroom

# Day 3- Add User Login to your Pokemon App
In continuation with this week's homework, your task tonight is to build a form for a user to input data and persist that data into your Pokemon App.

You will need to create the following:
Inside of the blueprint folder for "authentication" (assuming the name is "authentication"):
     - 2 routes: One for "signup" and one for "login"
- 2 User Model with the basic infomation listed:
- ID
- First_name
- Last_name
- email
- password
- date_created
- 2 Form with the following information:
- email
- password
- submit_button
- 1 .env file: to add your DATABASE_URL

Note: You may add more to your Form/Model if you would like, but the min is listed above.

HINT: You will need to add the following dependencies to your virtual environment
- pip install Flask-Login
- pip install Flask-WTF
- pip install Flask-Migrate
- pip install psycopg2
- pip install psycopg2-binary -- For those on mac machines
- pip install email-validator -- Verification of emails inside of forms
- pip install python-dotenv

  # Day 5- Add User Login to your Pokemon App
For homework tonight:
Your pokemon form will now catch any searched pokemon
You will need to:
        make a table to link the Pokemon to the User they belong too
        update your db with flask db migrate flask db upgrade

when they catch a pokemon
        check to see if the user already collected that pokemon
        If it hasn't been collected yet by ANY USER then add that pokemon to the data base
     
        Allow the user to add the pokemon to their collection; if they have less than 5 total pokemon


EACH USER SHOULD HAVE THEIR OWN COLLECTION OF UP TO 5 POKEMON


Note: Creating an ERD my be a good place to start if you are confused on your database design.

 # Day 6- Battle Pokemon
 Last night's home work had your users collect up to 5 pokemon.
Now create some of the CRUD capabilities for your users pokemon collection.


The user should be able to:
Remove a Pokemon (until there are no pokemon left)
Add a Pokemon (up to 5 total pokemon)


Now create a Page where a user can find other users and then attack that user.
When you press a button like Attack next to the users name it should bring you to a page that shows your pokemon and their stats and the front_shiny image  and the user you are attacking stats and front_shiny image (as an image)
Determine a method of determining a winner, note you have stats like Hit Points (hp) Base Defense points and base attack points.  You can also grab any other information you like from the pokemon.  You could even build out different rules for different abilities.  The options here are endless, have some fun with this.


The App should also track the wins and losses by each user.  This will likely be a new column in your User table.
Be sure to display the user's win/loss record on the attack page or the user profile page (if you create one)
