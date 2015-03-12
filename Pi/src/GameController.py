def select_character(player_id):
    return True

def show_game():
    return


#turn actions



#turn control checking
def is_turn_done(player_id):
    for i in range(0, CHARS_PER_PLAYER):
        #if Players[player_id].characters[i].move != DONE && Players[player_id].characters[i].hp > 0:
            return False
    return True

def reset_turn(player_id):
    #for i in range(0, CHARS_PER_PLAYER):
        #Players[player_id].characters[i].move = MOVE;
    return

def is_game_over(player_id):
    #return Players[main_player_id].characters_remaining == 0
    return False

#main game playing function
def play_game():
    main_player_id = 0
    #show_game()
    #draw_map()
    #load_turn(main_player_id)
   
    while True:
        while not is_turn_done(main_player_id):
            if is_game_over(main_player_id):
                print "Game over. Player", main_player_id, "lost!"
                return
            if not select_character(main_player_id):
                print "Game over. Player", main_player_id, "lost!"
                return
        reset_turn(main_player_id)
        main_player_id = (main_player_id + 1) % 2
        #load_turn(main_player_id)
    return
