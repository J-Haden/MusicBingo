import random


def create_bingo_card(song_list):
    """
    Creates a single 5x5 bingo card.

    Parameters:
        song_list (list): List of available songs

    Returns:
        list: 5x5 bingo card grid
    """

    # Select 24 unique songs
    selected_songs = random.sample(song_list, 24)

    # Insert free space
    selected_songs.insert(12, "FREE")

    # Convert list into 5x5 grid
    card = []

    for row in range(5):
        start = row * 5
        end = start + 5
        card.append(selected_songs[start:end])

    return card