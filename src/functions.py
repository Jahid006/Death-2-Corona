import pygame
import sys, json
from objects.bullet import Bullet
from objects.corona import Corona
from time import sleep
from objects.background import Background


def check_keydown_events(event, vaccine, game_settings, screen, bullets):
    if event.key == pygame.K_RIGHT:
        vaccine.moving_right = True

    elif event.key == pygame.K_LEFT:
        vaccine.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullets(game_settings, screen, bullets,  vaccine)

    elif event.key == pygame.K_ESCAPE:  # Exit if player pushes escape button.
        sys.exit()


def check_keyup_events(vaccine):

    if vaccine.moving_right:
        vaccine.moving_right = False

    if vaccine.moving_left:
        vaccine.moving_left = False


def check_events(vaccine, game_settings, screen, bullets, play_button, stats, coronas, sb):
    """Respond to key presses and mouse clicks."""

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        # When right or left key is pressed below conditions will be executed.
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, vaccine, game_settings, screen, bullets)  # Call the function for key pressed.

        elif event.type == pygame.KEYUP:
            check_keyup_events(vaccine)  # Call the function for key released.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, bullets, game_settings, screen, vaccine, coronas, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, bullets, game_settings, screen, vaccine, coronas, sb):
    """Start a new game when the player clicks Play."""

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        game_settings.dynamic_settings()  # Reset the game settings.
        pygame.mouse.set_visible(False)  # Hide the mouse cursor.

        stats.reset_stats()
        stats.game_active = True

    # Reset the scoreboard  images .
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_vaccines()

    # Empty the list of coronas and bullets.
    coronas.empty()
    bullets.empty()

    # Create a new fleet and center the vaccine.
    create_fleet(game_settings, screen, coronas, vaccine)
    vaccine.center_vaccine()


def update_screen(game_settings, screen, vaccine, bullets, coronas,play_button, stats, sb):
    """Update images on the screen and flip to the new screen."""

    #BackGround = Background('images/covid.jpg', [0,0])
    #screen.fill([255, 255, 255])
    #screen.blit(BackGround.image, BackGround.rect)

    screen.fill(game_settings.bg_color)  # Redraw the screen during each pass through the loop.

    for bullet in bullets.sprites():  # Redraw all bullets behind vaccine and coronas.
        bullet.draw_bullet()

    vaccine.blitme()

    coronas.draw(screen)
    # Draw the score information.
    sb.show_score()
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()  # Make the most recently drawn screen visible.


def update_bullets(bullets, coronas, game_settings, screen, vaccine, stats, sb):
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_collisions(bullets, coronas, game_settings, screen, vaccine, stats, sb)


def check_bullet_collisions(bullets, coronas, game_settings, screen, vaccine, stats, sb):
    # Check for any bullets that have hit coronas.
    # If so, get rid of the bullet and the corona.
    collisions = pygame.sprite.groupcollide(bullets, coronas, True, True)

    if collisions:
        for coronas in collisions.values():
            stats.score += game_settings.corona_points * len(coronas)
            sb.prep_score()
        check_high_score(stats, sb)

    # If all coronas in screen have been shoot down.

    if len(coronas) == 0:
        bullets.empty()  # Destroy existing bullets
        game_settings.increase_speed()  # Speed up the game.
        create_fleet(game_settings, screen, coronas, vaccine)  # Create new fleet.
        # Increase level.
        stats.level += 1
        sb.prep_level()


def fire_bullets(game_settings, screen, bullets, vaccine):
    # Create a new bullet and add it to the bullets group.
    if len(bullets) <= game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen,  vaccine)
        bullets.add(new_bullet)


def get_number_of_coronas_x(game_settings, corona_width):
    available_space_x = game_settings.screen_width - 2 * corona_width
    number_of_coronas_x = int(available_space_x / (2 * corona_width))
    return number_of_coronas_x


def create_fleet(game_settings, screen, coronas, vaccine):
    """Create a full fleet of coronas."""
    # Create an corona and find the number of coronas in a row.
    # Spacing between each corona is equal to one corona width.
    corona = Corona(game_settings, screen)

    number_coronas_x = get_number_of_coronas_x(game_settings, corona.rect.width)
    number_rows = get_number_rows(game_settings, vaccine.rect.height, corona.rect.height)

    # Create the rows of coronas.
    for row_number in range(number_rows):
        for corona_number in range(number_coronas_x):
            create_corona(game_settings, screen, coronas, corona_number, row_number)


def create_corona(game_settings, screen, coronas, corona_number, row_number):

    corona = Corona(game_settings, screen)
    corona_width = corona.rect.width
    corona.x = corona_width + 2 * corona_width * corona_number
    corona.rect.x = corona.x
    corona.rect.y = corona.rect.height + 2 * corona.rect.height * row_number
    coronas.add(corona)


def update_coronas(game_settings, coronas, vaccine, stats, screen, bullets, sb):
    """
    Check if the fleet is at an edge, and then update the postions of all coronas in the fleet.
    """
    check_fleet_edges(game_settings, coronas)
    coronas.update()
    # Look for corona-vaccine collisions.

    if pygame.sprite.spritecollideany(vaccine, coronas):
        vaccine_hit(game_settings, stats, screen, vaccine, coronas, bullets, sb)
        # print("Vaccine hit!!!")

    # Look for coronas hitting the bottom of the screen.
    check_coronas_bottom(game_settings, stats, screen, vaccine, coronas, bullets, sb)


def change_fleet_direction(game_settings, coronas):
    """Drop the entire fleet and change the fleet's direction."""
    for corona in coronas.sprites():
        corona.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def check_fleet_edges(game_settings, coronas):
    """Respond appropriately if any coronas have reached an edge."""
    for corona in coronas.sprites():
        if corona.check_edges():
            change_fleet_direction(game_settings, coronas)
            break


def vaccine_hit(game_settings, stats, screen, vaccine, coronas, bullets, sb):
    """Respond to vaccine being hit by corona."""
    # Decrement vaccines_left.
    stats.vaccines_left -= 1
    print(stats.vaccines_left)
    if stats.vaccines_left > 0:

        # Update score board.
        sb.prep_vaccines()
        # Empty the list of coronas and bullets.
        coronas.empty()
        bullets.empty()
        # Create a new fleet and center the vaccine.
        create_fleet(game_settings, screen, coronas, vaccine)
        vaccine.center_vaccine()
        # Pause.

        sleep(0.5)
    else:
        stats.game_active = False
        # Show the mouse cursor.
        pygame.mouse.set_visible(True)


def check_coronas_bottom(game_settings, stats, screen, vaccine, coronas, bullets, sb):
    """Check if any coronas have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for corona in coronas.sprites():
        if corona.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the vaccine got hit.
            vaccine_hit(game_settings, stats, screen, vaccine, coronas, bullets, sb)
            break


def get_number_rows(game_settings, vaccine_height, corona_height):
    """Determine the number of rows of coronas that fit on the screen."""
    available_space_y = (game_settings.screen_height -
                         (3 * corona_height) - vaccine_height)
    number_rows = int(available_space_y / (2 * corona_height))
    return number_rows


def check_high_score(stats, sb):
    if stats.score >= stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

        with open("resource/data.json", "w") as outfile:
            json.dump({"high": stats.high_score}, outfile)



if __name__ == '__main__':
    print("Go to main file and run from there.")
