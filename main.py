from upemtk import *
from random import randint


def dessine_plateau(plateau, taille_case):
    lettre = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z"]
    cree_fenetre(((len(plateau[0]) + 1) * taille_case)+taille_case, ((len(plateau)) + 1) * taille_case+taille_case)
    rectangle(0, 0, (len(plateau[0]) + 1) * taille_case+taille_case, (len(plateau) + 1) * taille_case+taille_case, remplissage="blue")

    for largueur_plateau in range(1, len(plateau) + 1):
        texte(25, (largueur_plateau * taille_case) + 25, lettre[largueur_plateau - 1])
        for longueur_plateau in range(1, (len(plateau[largueur_plateau - 1])) + 1):
            rectangle(longueur_plateau * taille_case, (largueur_plateau * taille_case),
                      (longueur_plateau + 1) * taille_case,
                      (largueur_plateau + 1) * taille_case, epaisseur=3, remplissage="blue")

    for collonne in range(1, len(plateau[0]) + 1):
        texte((taille_case * collonne) + 25, 20, collonne)

    mise_a_jour()


def pion(color, joueur, lst_joueur, plateau):
    plateau[(lst_joueur[1]) - 1][(lst_joueur[0]) - 1] = 0
    cercle((lst_joueur[0] * taille_case) + (taille_case / 2), (lst_joueur[1] * taille_case) + (taille_case / 2),
           taille_case / 2, remplissage=color, tag=joueur)
    plateau[(lst_joueur[1]) - 1][(lst_joueur[0]) - 1] = 1


def verfication_pion_joueur(lst_joueur1, lst_joueur2, plateau):
    while lst_joueur1 == lst_joueur2:
        lst_joueur2 = [randint(1, len(plateau[0])), randint(1, len(plateau[0]))]
        efface("joueur2")
        pion("red", "joueur2", lst_joueur2, plateau)
    return lst_joueur1, lst_joueur2


def verification_pion_ia(lst_joueur1, lst_robot, plateau):
    while lst_joueur1 == lst_robot:
        lst_robot = [randint(1, len(plateau[0])), randint(1, len(plateau[0]))]
        efface("ia")
        pion("grey", "ia", lst_robot, plateau)
    return lst_joueur1, lst_robot


def recuper_liste_meilleur_case(case_libre, plateau):
    lst_case = []
    lst_possibiliter=[]
    print(case_libre)
    for case in case_libre:
        lst_prochaine_case_libre=case_alentour(case,plateau)
        nb_possibiliter=len(verification_deplacement_pion(lst_prochaine_case_libre,plateau))
        texte((taille_case-1)*case[0]+(taille_case/2),(taille_case-1)*case[1]+(taille_case/2),(nb_possibiliter,case),tag="nb",taille=8,)
        lst_possibiliter.append(nb_possibiliter)
    max_possibiliter = max(lst_possibiliter)
    lst_possibiliter_max=[i for i, element in enumerate(lst_possibiliter) if element == max_possibiliter]
    for i in lst_possibiliter_max:
        lst_case.append(case_libre[i])
    return lst_case




def deplacement_pion(couleur, joueur_tag, joueur, plateau, ia):
    case_libre_joueur = case_alentour(joueur, plateau)

    case_libre = verification_deplacement_pion(case_libre_joueur, plateau)
    affichage_case_deplacement_possible(case_libre)
    if case_libre == []:
        return False, True
    if ia:
        case_libre_ia=recuper_liste_meilleur_case(case_libre, plateau)
        attend_clic_gauche()
        efface("nb")
        position = randint(0, len(case_libre_ia) - 1)
        nv_x, nv_y = case_libre_ia[position][0], case_libre_ia[position][1]
        nv_deplacement = [[nv_x, nv_y]]

    else:
        x, y = attend_clic_gauche()
        nv_x, nv_y = x // taille_case, y // taille_case
        nv_deplacement = [[nv_x, nv_y]]
    efface("case_libre")

    if nv_deplacement[0] in case_libre:
        plateau[(joueur[1]) - 1][(joueur[0] - 1)] = 0
        joueur[0], joueur[1] = nv_x, nv_y
        efface(joueur_tag)
        pion(couleur, joueur_tag, joueur, plateau)
        plateau[(nv_y) - 1][(nv_x) - 1] = 1
        mise_a_jour()
        return False, False
    return True, False


def verification_deplacement_pion(case_libre_joueur, plateau):
    # probleme de deplacement case, tout les case ne sont pas pleine
    nv_case_libre_joueur = []

    for case in range(len(case_libre_joueur)):
        if plateau[(case_libre_joueur[case][1]) - 1][(case_libre_joueur[case][0]) - 1] == 0:
            nv_case_libre_joueur.append(case_libre_joueur[case])
    return nv_case_libre_joueur


def affichage_case_deplacement_possible(nv_case_libre_joueur):
    for i in nv_case_libre_joueur:
        rectangle(i[0] * taille_case, i[1] * taille_case, (i[0] + 1) * taille_case,
                  (i[1] + 1) * taille_case, remplissage="green", tag="case_libre")
    mise_a_jour()


def case_alentour(joueur, plateau):
    case_libre = []

    if joueur[0] > 1:
        case_libre.append([joueur[0] - 1, joueur[1]])  # case gauche
    if joueur[0] < len(plateau[0]):
        case_libre.append([joueur[0] + 1, joueur[1]])  # case droite
    if joueur[1] > 1:
        case_libre.append([joueur[0], joueur[1] - 1])  # case au dessus du pion
    if joueur[1] < len(plateau):
        case_libre.append([joueur[0], joueur[1] + 1])  # case en dessous du pion
    if joueur[0] > 1 and joueur[1] > 1:
        case_libre.append([joueur[0] - 1, joueur[1] - 1])  # case au coin superieur a gauche du pion
    if joueur[0] < len(plateau[0]) and joueur[1] < len(plateau):
        case_libre.append([joueur[0] + 1, joueur[1] + 1])  # case au coin superieur a droite du pion
    if joueur[0] > 1 and joueur[1] < len(plateau):
        case_libre.append([joueur[0] - 1, joueur[1] + 1])  # case  coin a inferieur gauche du pion
    if joueur[0] < len(plateau[0]) and joueur[1] > 1:
        case_libre.append([joueur[0] + 1, joueur[1] - 1])  # case en coin a inferieur droite du pion
    return case_libre


def verifiacation_deplacement(nv_deplacement, joueur_adverse, plateau, joueur):
    # interdiction deplacement sur un joueur ,sur lui meme ou sur une case noir
    if nv_deplacement == joueur_adverse or plateau[(nv_deplacement[0][1]) - 1][
        nv_deplacement[0][0] - 1] == 2 or nv_deplacement == joueur:
        return False
    return True


def case_noir(plateau, ia, joueur_adverse):
    if ia:
        case_libre_joueur_adverse = case_alentour(joueur_adverse, plateau)
        case_noir_ia = verification_deplacement_pion(case_libre_joueur_adverse, plateau)
        liste_meilleur_case_noir=recuper_liste_meilleur_case(case_noir_ia, plateau)
        if len(case_noir_ia) > 0:
            case_ia = randint(0, len(liste_meilleur_case_noir) - 1)
            case_noir_x, case_noir_y = liste_meilleur_case_noir[case_ia][0], liste_meilleur_case_noir[case_ia][1]


        else:
            return False
    else:
        x, y = attend_clic_gauche()
        case_noir_x, case_noir_y = x // taille_case, y // taille_case

    if plateau[(case_noir_y) - 1][(case_noir_x) - 1] == 0 and case_noir_x > 0 and case_noir_y > 0:
        plateau[(case_noir_y) - 1][(case_noir_x) - 1] = 2
        rectangle(case_noir_x * taille_case, case_noir_y * taille_case, (case_noir_x + 1) * taille_case,
                  (case_noir_y + 1) * taille_case, remplissage="black")
        texte((taille_case - 1) * case_noir_x + (taille_case / 2), (taille_case - 1) * case_noir_y + (taille_case / 2),
              (case_noir_x, case_noir_y), tag="nb", taille=8, couleur="white")
        return False
    return True


def jouer(tour_deplacement, pose_case_noir, tour, couleur, tag, joueur, plateau, ia, joueur_adverse):
    # crre 2 fonction
    while tour_deplacement:
        tour_deplacement, vainqueur = deplacement_pion(couleur, tag, joueur, plateau, ia)
    if vainqueur:
        return not tour_joueur, True
    while pose_case_noir:
        pose_case_noir = case_noir(plateau, ia, joueur_adverse)
    return not tour, False


def dimension_plateau(dimension):
    """
    Créé une liste avec des sous liste dans lequel chaque sous liste equivaut a une ligne d'un tableau
    et chaque element de la sous liste equivaut a une collonne du tableau
    :param hauteur:int
    :param longueur: int
    :return: list plateu
    """
    plateau = []
    for ligne in range(dimension[0]):
        ligne_plateau = []
        for collonne in range(dimension[1]):
            ligne_plateau.append(0)
        plateau.append(ligne_plateau)
    return plateau


def defaite(vainqueur, joueur):
    if vainqueur:
        return False, joueur
    return True, joueur


def button(coordonne_button, x_souris, y_souris):
    if x_souris > coordonne_button[0] and x_souris < coordonne_button[2] and y_souris > coordonne_button[
        1] and y_souris < coordonne_button[3]:
        return True
    return False


def menu_accueil():
    rectangle(0, 0, 600, 450, remplissage="#133337")
    texte(190, 50, "MODES DE JEU", "blue")
    rectangle(200, 120, 400, 170, 'black', 'medium aquamarine')
    texte(220, 130," 2 JOUEUR")
    rectangle(200, 320, 400, 370, 'black', '#E51944')
    texte(280, 330, "IA")
    rectangle(200, 220, 400, 270, 'black', '#E00D0D')
    texte(220, 230, "CAVALIER")
    x_souris, y_souris = attend_clic_gauche()
    ia = button([200, 300, 400, 350], x_souris, y_souris)
    mode_2_joueur = button([200, 100, 400, 150], x_souris, y_souris)
    cavalier = button([200, 200, 400, 250], x_souris, y_souris)
    if ia:
        return 1
    elif mode_2_joueur:
        return 2
    elif cavalier:
        return 3
    else:
        return 0


def menu_rejouer(vainqueur, mode):
    ferme_fenetre()
    cree_fenetre(600, 450)
    rectangle(0, 0, 600, 450, remplissage="#133337")
    texte(200, 100, str(vainqueur) + (" a perdu"), taille=30, couleur="blue")
    rectangle(240, 200, 400, 240, remplissage='red')
    texte(240, 200, " REJOUER")
    rectangle(240, 300, 400, 340, remplissage="red")
    texte(240, 300, "QUITTER")
    x_souris, y_souris = attend_clic_gauche()
    rejouer_menu_de_fin = button((240, 200, 400, 240), x_souris, y_souris)
    quitter_menu_fin = button((240, 300, 400, 340), x_souris, y_souris)
    if rejouer_menu_de_fin:
        return mode
    elif quitter_menu_fin:
        return 0
    ferme_fenetre()


def menu_dimension(hauteur_tableau, longueur_tableau):
    configue_dimension_tableau = True

    cree_fenetre(500, 500)

    while configue_dimension_tableau:
        rectangle(0, 0, 500, 500, remplissage="#133337")
        rectangle(225, 125, 275, 175, remplissage="white")
        # button configuration hauteur
        texte(50, 50, "Nombre de case en collonne")
        texte(235, 135, hauteur_tableau)
        rectangle(100, 125, 150, 175, remplissage="red")
        rectangle(110, 150, 140, 155, remplissage="black")
        rectangle(350, 125, 400, 175, remplissage="green")
        rectangle(360, 150, 390, 155, remplissage="black")
        rectangle(373, 135, 376, 165, remplissage="black")
        texte(50, 260, "Nombre de case en ligne")
        rectangle(225, 325, 275, 375, remplissage="white")
        texte(235, 335, longueur_tableau)
        rectangle(100, 325, 150, 375, remplissage="red")
        rectangle(110, 350, 140, 355, remplissage="black")
        rectangle(350, 325, 400, 375, remplissage="green")
        rectangle(360, 350, 390, 355, remplissage="black")
        rectangle(373, 335, 376, 365, remplissage="black")
        rectangle(180, 425, 300, 465, remplissage="purple")
        texte(190, 425, "JOUER")
        x_souris, y_souris = attend_clic_gauche()
        if button((180, 425, 300, 465), x_souris, y_souris):
            configue_dimension_tableau = False
        elif button((100, 125, 150, 175), x_souris, y_souris):
            hauteur_tableau -= 1
        elif button((350, 125, 400, 175), x_souris, y_souris):
            hauteur_tableau += 1
        elif button((100, 325, 150, 375), x_souris, y_souris):
            longueur_tableau -= 1
        elif button((350, 325, 400, 375), x_souris, y_souris):
            longueur_tableau += 1

    return longueur_tableau, hauteur_tableau


taille_case = 75
main = True
hauteur_tableau = 6
longueur_tableau = 6
while main:
    cree_fenetre(600, 450)
    mode = menu_accueil()
    while mode > 0:
        ferme_fenetre()
        plateau = dimension_plateau(menu_dimension(hauteur_tableau, longueur_tableau))
        ferme_fenetre()
        tour_joueur = True
        tour_deplacement = True
        pose_case_noir = True
        rejouer = True
        vainqueur = False
        # pion
        dessine_plateau(plateau, taille_case)
        joueur1 = [randint(1, len(plateau[0])), randint(1, len(plateau))]
        pion("yellow", "joueur1", joueur1, plateau)
        if mode == 1:
            robot = [randint(1, len(plateau[0])), randint(1, len(plateau))]
            pion("grey", "ia", robot, plateau)
            joueur1, robot = verification_pion_ia(joueur1, robot, plateau)
        elif mode == 3 or mode == 2:
            joueur2 = [randint(1, len(plateau[0])), randint(1, len(plateau))]
            pion("red", "joueur2", joueur2, plateau)
            joueur1, joueur2 = verfication_pion_joueur(joueur1, joueur2, plateau)

        while rejouer:
            # joueur 1
            while tour_joueur:
                tour_joueur, vainqueur = jouer(tour_deplacement, pose_case_noir, tour_joueur, "yellow", "joueur1",
                                               joueur1, plateau, False, None)
            rejouer, vainqueur_manche = defaite(vainqueur, "joueur 1")
            # joueur adverse
            if rejouer:
                if mode == 1:
                    while not tour_joueur:
                        tour_joueur, vainqueur = jouer(tour_deplacement, pose_case_noir, tour_joueur, "grey", "ia",
                                                       robot, plateau, True, joueur1)
                    rejouer, vainqueur_manche = defaite(vainqueur, "ia")
                else:
                    rejouer, vainqueur_manche = defaite(vainqueur, "joueur 1")

                while not tour_joueur:
                    tour_joueur, vainqueur = jouer(tour_deplacement, pose_case_noir, tour_joueur, "red", "joueur2",
                                                   joueur2, plateau, False, None)
                rejouer, vainqueur_manche = defaite(vainqueur, "joueur 2")
        mode = menu_rejouer(vainqueur_manche, mode)
    ferme_fenetre()
