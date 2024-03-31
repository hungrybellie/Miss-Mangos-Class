import pygame
import sys
from flashcards import flashcards_by_topic

# Initialize pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flashcard Study Session")
clock = pygame.time.Clock()

# Define the list of topics
topics = list(flashcards_by_topic.keys())

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (241, 140, 117)
YELLOW = (232, 188, 107)

# Define the font
font = pygame.font.Font(None, 36)

# Define the title screen background image
title_image = pygame.image.load("Images\MissMangoCB.png")

# Main game loop
running = True
while running:
    topic_chosen = None
    while topic_chosen is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                topic_chosen = ""  # Exit loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a topic was clicked
                for i, topic in enumerate(topics):
                    text_rect = font.render(topic, True, WHITE).get_rect(topleft=(70, 200 + i * 50))
                    if text_rect.collidepoint(event.pos):
                        topic_chosen = topic

        # Clear the screen
        screen.blit(title_image, (0, 0))

        # Display question prompt
        question_prompt = "Welcome to Flashcards! Choose a topic to study:"
        question_surface = font.render(question_prompt, True, WHITE)
        screen.blit(question_surface, (70, 70))

        # Display the list of topics
        for i, topic in enumerate(topics):
            text_surface = font.render(topic, True, WHITE)
            screen.blit(text_surface, (70, 200 + i * 50))

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(30)

    # Study flashcards for the chosen topic
    if topic_chosen:
        # Get the flashcards for the chosen topic
        flashcards = flashcards_by_topic[topic_chosen]

        # Display and study the flashcards
        card_index = 0
        flipped = False
        study = True
        while study:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    study = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        flipped = not flipped  # Flip the card
                    elif event.key == pygame.K_RIGHT:
                        card_index = (card_index + 1) % len(flashcards)  # Move to the next card
                        flipped = False
                    elif event.key == pygame.K_LEFT:
                        card_index = (card_index - 1) % len(flashcards)  # Move to the previous card
                        flipped = False

            # Clear the screen
            screen.blit(title_image, (0, 0))

            # Draw the flashcard (front or back)
            flashcard_rect = pygame.Rect(200, 200, 400, 200)
            if not flipped:
                pygame.draw.rect(screen, ORANGE, flashcard_rect)
                front_text = font.render(flashcards[card_index]["front"], True, WHITE)
                screen.blit(front_text, (flashcard_rect.centerx - front_text.get_width() // 2, flashcard_rect.centery - front_text.get_height() // 2))
            else:
                pygame.draw.rect(screen, YELLOW, flashcard_rect)
                back_text = font.render(flashcards[card_index]["back"], True, BLACK)
                screen.blit(back_text, (flashcard_rect.centerx - back_text.get_width() // 2, flashcard_rect.centery - back_text.get_height() // 2))

            # Update the display
            pygame.display.flip()

            # Limit the frame rate
            clock.tick(30)

# Clean up
pygame.quit()
sys.exit()