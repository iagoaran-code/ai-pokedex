from pokedex import Pokedex

def test_api_returns_correct_id():
    bot = Pokedex()
    data = bot.get_pokemon_data("pikachu")
    
    # This checks if the ID for Pikachu is actually 25
    assert data["id"] == 25

def test_invalid_pokemon_returns_none():
    bot = Pokedex()
    data = bot.get_pokemon_data("not_a_real_pokemon")
    
    assert data is None
