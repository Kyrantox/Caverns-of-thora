import pygame
from pygame.locals import *
from classes import *
from constantes import *

pygame.init()

# Ouverture de la fenêtre Pygame (carré : largeur = hauteur)
fenetre = pygame.display.set_mode((cote_fenetre, cote_fenetre))

# Icone
icone = pygame.image.load(image_icone)
pygame.display.set_icon(icone)
# Titre
pygame.display.set_caption(titre_fenetre)

# BOUCLE PRINCIPALE
continuer = 1

while continuer:
    # Chargement et affichage de l'écran d'accueil
    accueil = pygame.image.load(image_accueil).convert()
    fenetre.blit(accueil, (0, 0))

    # Rafraichissement
    pygame.display.flip()

    # On remet ces variables à 1 à chaque tour de boucle
    music_intro = 0
    musique_intro = pygame.mixer.Sound(musique_accueil)
    continuer_jeu = 1
    continuer_accueil = 1

    # BOUCLE D'ACCUEIL
    while continuer_accueil:
        if music_intro == 0 :
            musique_intro.play()
            music_intro += 1  # Permet de limiter la vitesse de lancement


        # Limitation de vitesse de la boucle
        pygame.time.Clock().tick(60)

        for event in pygame.event.get():

            # Si l'utilisateur quitte, on met les variables
            # de boucle à 0 pour n'en parcourir aucune et fermer
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                continuer_accueil = 0
                continuer_jeu = 0
                continuer = 0
                # Variable de choix du niveau
                choix = 0

            elif event.type == KEYDOWN:
                # Lancement du niveau 7
                if event.key == K_SPACE:
                    boucle_menu = 1
                    while boucle_menu ==1 :
                        aide= pygame.image.load(image_aide)
                        fenetre.blit(aide, (0,0))
                        pygame.display.flip()

                        for event in pygame.event.get():
                            if event.type == KEYDOWN and event.key == K_SPACE or event.key == K_ESCAPE:
                                accueil = pygame.image.load(image_accueil).convert()
                                fenetre.blit(accueil, (0,0))
                                pygame.display.flip()
                                boucle_menu = 0

                # Lancement du niveau 1
                elif event.key == K_F1:
                    continuer_accueil = 0  # On quitte l'accueil
                    choix = 'n1'  # On définit le niveau à charger
                # Lancement du niveau 2
                elif event.key == K_F2:
                    continuer_accueil = 0
                    choix = 'n2'
                # Lancement du niveau 3
                elif event.key == K_F3:
                    continuer_accueil = 0
                    choix = 'n3'
                # Lancement du niveau 4
                elif event.key == K_F4:
                    continuer_accueil = 0
                    choix = 'n4'
                # Lancement du niveau 5
                elif event.key == K_F5:
                    continuer_accueil = 0
                    choix = 'n5'
                # Lancement du niveau 6
                elif event.key == K_F6:
                    continuer_accueil = 0
                    choix = 'n6'
                # Lancement du niveau 7
                elif event.key == K_F7:
                    continuer_accueil = 0
                    choix = 'n7'

    # on vérifie que le joueur a bien fait un choix de niveau
    # pour ne pas charger s'il quitte
    if choix != 0:
        # Chargement du fond
        fond = pygame.image.load(image_fond).convert()

        # Génération d'un niveau à partir d'un fichier
        niveau = Niveau(choix)
        niveau.generer()
        niveau.afficher(fenetre)

        # Création du joueur
        player = Perso("images/player_droite.png", "images/player_gauche.png",
                   "images/player_haut.png", "images/player_bas.png", niveau)

        #Création monstre
        monster = Mob("images/momie_droite.png", "images/momie_gauche.png", "images/momie_dos.png", "images/momie_face.png", niveau)
        fantom = Fantom("images/chouvette_droite.png", "images/chouvette_gauche.png", "images/chouvette_dos.png", "images/chouvette_face.png", niveau)
        marteau = Arme("images/marteau.png", niveau,3)

    musique_intro.stop()

    # BOUCLE DE JEU
    while continuer_jeu:

        # Limitation de vitesse de la boucle
        pygame.time.Clock().tick(30)
        pygame.mixer.music.load(musique)
        pygame.mixer.music.play()

        for event in pygame.event.get():

            # Si l'utilisateur quitte, on met la variable qui continue le jeu
            # ET la variable générale à 0 pour fermer la fenêtre
            if event.type == QUIT:
                continuer_jeu = 0
                continuer = 0

            elif event.type == KEYDOWN:
                # Si l'utilisateur presse Echap ici, on revient seulement au menu
                if event.key == K_ESCAPE:
                    continuer_jeu = 0
                    pygame.mixer.music.stop()

                # Touches de déplacement du joueur
                elif event.key == K_RIGHT:
                    player.deplacer('droite')
                elif event.key == K_LEFT:
                    player.deplacer('gauche')
                elif event.key == K_UP:
                    player.deplacer('haut')
                elif event.key == K_DOWN:
                    player.deplacer('bas')
                elif event.key == K_SPACE :
                    if marteau.utilisation <= 0:
                        player.casse = False
                    player.casser(player.cote)
                    marteau.utilisation = marteau.utilisation - 1

        # Affichages aux nouvelles positions
        fenetre.blit(fond, (0, 0))
        niveau.afficher(fenetre)
        fenetre.blit(player.direction, (player.x, player.y))  # player.direction = l'image dans la bonne direction
        fenetre.blit(monster.direction, (monster.x, monster.y))  # monster.direction = l'image dans la bonne direction
        fenetre.blit(fantom.direction, (fantom.x, fantom.y))  # monster.direction = l'image dans la bonne direction
        if player.casse==False and marteau.utilisation >= 0:
            fenetre.blit(marteau.image, (marteau.x, marteau.y)) #Affiche le marteau
        pygame.display.flip()
        monster.deplacer()
        fantom.deplaceNoColition()
        if player.case_y == marteau.case_y and player.case_x == marteau.case_x:
            player.casse = True


        # Défaite -> Retour à l'accueil
        if player.case_y == monster.case_y and player.case_x == monster.case_x :
            continuer_jeu = 0
            pygame.mixer.music.stop()
        # Victoire -> Retour à l'accueil
        if niveau.structure[player.case_y][player.case_x] == 'a':
            continuer_jeu = 0
            pygame.mixer.music.stop()