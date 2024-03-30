define e = Character("Mango")

# define the song titles and their files
init python:
    # must be persistent to be able to record the scores
    # after adding new songs, please remember to delete the persistent data

    rhythm_game_songs = [
    Song('Rocks', 'audio/rocks.mp3', 'audio/rocks.beatmap.txt'),
    Song('Solar System', 'audio/solar_system.mp3', 'audio/solar_system.beatmap.txt'),
    Song('Addition', 'audio/addition.mp3', 'audio/addition.beatmap.txt')
    ]


    for song in rhythm_game_songs:
            if song.name not in persistent.rhythm_game_high_scores:
                persistent.rhythm_game_high_scores[song.name] = (0, 0)

# map song name to high scores
default persistent.rhythm_game_high_scores = {
    song.name: (0, 0) for song in rhythm_game_songs
}

# the song that the player chooses to play, set in `choose_song_screen` below
default selected_song = None

label start:
    scene bg room

    e "Welcome to Mango Beat! Please press enter to select the lesson you want to do today."

    window hide
    call rhythm_game_entry_label

    e "Nice work hitting those notes! Hope you enjoyed learning this awesome new material!"

    return

# a simpler way to launch the minigame 
label test:
    e "Welcome to Mango Beat! Ready for a challenge?"
    window hide
    $ quick_menu = False

    # avoid rolling back and losing chess game state
    $ renpy.block_rollback()

    $ song = Song('Isolation', 'audio/Isolation.mp3', 'audio/Isolation.beatmap.txt', beatmap_stride=2)
    $ rhythm_game_displayable = RhythmGameDisplayable(song)
    call screen rhythm_game(rhythm_game_displayable)

    # avoid rolling back and entering the chess game again
    $ renpy.block_rollback()

    # restore rollback from this point on
    $ renpy.checkpoint()

    $ quick_menu = True
    window show

    return