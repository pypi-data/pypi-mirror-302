import pandas as pd
import astreintes.calculs


def test_un_seul_site():
    df_sites = pd.DataFrame(
        {
            'nom': ['Clermont'],
            'aga': [6],
            'respi': [4],
            'rotations': [2],
        }
    )
    astreintes.calculs.genere_planning(df_sites)


def test_deux_sites():
    df_sites = pd.DataFrame(
        {
            'nom': ['Caen', 'Rouen'],
            'aga': [6, 3],
            'respi': [2, 3],
            'rotations': [1, 1],
        }
    )
    astreintes.calculs.genere_planning(df_sites)


def test_deux_sites_un_seul_respi():
    df_sites = pd.DataFrame(
        {
            'nom': ['Caen', 'Rouen'],
            'aga': [6, 6],
            'respi': [1, 8],
            'rotations': [1, 1],
        }
    )
    astreintes.calculs.genere_planning(df_sites)


def test_trois_sites():
    df_sites = pd.DataFrame(
        {
            'nom': ['Marseille', 'Toulon', 'Nice'],
            'aga': [8, 3, 4],
            'respi': [4, 3, 3],
            'rotations': [1, 1, 1],
        }
    )
    astreintes.calculs.genere_planning(df_sites)
