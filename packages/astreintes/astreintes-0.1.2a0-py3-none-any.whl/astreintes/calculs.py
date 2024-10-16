import numpy as np
import pandas as pd

import astreintes.models as models
from astreintes.models import N_SEMAINES


def _repartition(p, n_semaines=N_SEMAINES, max_astreintes=13):
    """
    Calcule la répartition d'un nombre entier (en général semaines) en len(p) personnes,
    avec un maximum (13 par défaut) et des affinités (vecteur p).
    :param p: préférence pour chaque technicien ou site
    :param n_semaines: nombre de semaines à répartir, 52 semaines par an par default
    :param max_astreintes: 13 semaines maximum par technicien par défault,
    peut-être un scalaire ou un vecteur size(p)
    :return:
    """
    p = p / p.sum()  # on normalise les probabilités à 1
    max_astreintes = np.zeros_like(p) + max_astreintes if np.isscalar(max_astreintes) else max_astreintes
    # pas le droit à plus de n_semaines par an, tout en restant normalisé à un
    i = p > max_astreintes / n_semaines
    if np.sum(i):
        p[i] = max_astreintes[i] / n_semaines
        p[~i] = p[~i] * (1 - p[i]) / np.sum(p[~i])
    # on répartit du mieux possible les arrondis selon les affinités
    f = n_semaines / p.sum()
    n = np.floor(f * p).astype(int)
    decimal = f * p - n
    n_missing = int(n_semaines - n.sum())
    # Indices des plus grandes décimales
    i = np.argsort(-decimal, stable=True)[:n_missing]
    n[i] += 1
    return n


def _assignation(counts, seed=None):
    """
    Assigne les astreintes a partir d'un vecteur ou chaque entrée représente le nombre d'astreintes
    par personne.
    :param counts:
    :param seed:
    :return:
    """
    if seed is not None:
        np.random.seed(seed)
    n, n_semaines = (counts.size, counts.sum())
    assign = np.zeros(n_semaines, dtype=int)
    remaining = counts.copy()
    last = -1
    for i in np.arange(n_semaines):
        j = np.where(remaining == np.max(remaining))[0]
        if len(j) > 1:
            j = np.random.choice(np.setdiff1d(j, last))
        else:
            j = j[0]
        assign[i] = j
        remaining[j] -= 1
        last = j
    return assign


def _sites2effectifs(df_sites: pd.DataFrame) -> pd.DataFrame:
    """
    Crée une dataframe d'effectifs fictive à partir d'une dataframe sites
    Les techs AGA sont nommés A0 - A1 ... , les techs respi R0 - R1 ...
    :param df_sites:
    :return: df_effectifs
    """
    df_effectifs = []
    for j in range(df_sites.shape[0]):
        df_effectifs.append(
            pd.DataFrame(
                {
                    'specialite': ['aga'] * df_sites.loc[j, 'aga'] + ['respi'] * df_sites.loc[j, 'respi'],
                    'nom': [f'A{i}' for i in np.arange(df_sites.loc[j, 'aga'])]
                    + [f'R{i}' for i in np.arange(df_sites.loc[j, 'respi'])],
                    'site': df_sites.loc[j, 'nom'],
                }
            )
        )
    df_effectifs = pd.concat(df_effectifs)
    df_effectifs['preference'] = 1
    df_effectifs['id_tech'] = np.arange(df_effectifs.shape[0])
    df_effectifs.reset_index(inplace=True)
    return df_effectifs


def _planning_sites(counts):
    """
    :param counts: np.array (nrails, nsites)
    :return: np.array( nsemaines, nrails)
    """
    nr, ns = counts.shape
    planning = np.zeros((N_SEMAINES, nr), dtype=int) - 1
    for week in np.arange(N_SEMAINES):
        counts_ = counts.copy()
        sites_ = np.ones(nr, dtype=bool)
        for ir in np.arange(nr):
            # on cherche le site avec le plus d'astreintes a caser,
            # sauf s'il s'agit du précédent
            imaxs = np.argsort(-counts[ir, sites_])
            imax = imaxs[0]
            for im in imaxs:
                if im == planning[week - 1, ir]:
                    continue
                if counts[ir, im] > 0:
                    imax = im
                    break
            isite = np.where(sites_)[0][imax]
            planning[week, ir] = isite
            counts_[ir, :] = 0
            sites_[isite] = False
            counts[ir, isite] += -1
    return planning.T


def _calcul_rotations(df_sites: pd.DataFrame, df_effectifs: pd.DataFrame, params: models.Parametres):
    n_sites = df_sites.shape[0]
    # première étape est de trouver la spécialité ayant le moins d'intervenants
    n_mixed = df_sites.rotations.sum() - params.min_aga - params.min_respi
    rails = params.min_aga * ['aga'] + params.min_respi * ['respi'] + n_mixed * ['mixed']
    df_rail = pd.DataFrame(dict(specialite=rails, **{n: 0 for n in df_sites['nom']}))
    if n_sites == 1:
        df_rail.loc[:, df_sites['nom']] = N_SEMAINES
        sites_per_rail = np.zeros((len(rails), N_SEMAINES), dtype=int)
    else:
        n_mixed = df_sites.rotations.sum() - params.min_aga - params.min_respi
        rails = params.min_aga * ['aga'] + params.min_respi * ['respi'] + n_mixed * ['mixed']
        df_rail = pd.DataFrame(dict(specialite=rails, **{n: 0 for n in df_sites['nom']}))
        # on détermine le nombre d'astreintes par site en fonction de la contrainte: 2 options
        # soit on répartit les astreintes en fonction des effectifs, soit on les répartit uniformément
        if params.repartition == 'site':
            site_preference = np.ones(n_sites)
        else:
            site_preference = (df_sites['aga'] + df_sites['respi']) / df_sites['rotations']
        specialites_ordre = df_sites.loc[:, ['aga', 'respi']].min().sort_values()
        for spec in list(specialites_ordre.index) + ['mixed']:
            ir = df_rail['specialite'] == spec
            if spec == 'mixed':
                if np.sum(ir) == 0:
                    continue
                npax = df_sites.loc[:, ['aga', 'respi']].values.sum(axis=1)
            else:
                npax = df_sites.loc[:, spec].values
            df_rail.loc[ir, df_sites['nom']] = _repartition(site_preference, max_astreintes=npax * params.max_astreintes)
            # on essaie de compenser avec les rails suivants pour balancer entre les sites
            site_preference = 1 / ((p := df_rail[df_sites['nom']].sum(axis=0).values) / sum(p))
        assert np.all(df_rail.loc[:, df_sites['nom']].sum(axis=1) == N_SEMAINES)
        assert np.all(df_rail.loc[:, df_sites['nom']].sum(axis=0) == N_SEMAINES)
        sites_per_rail = _planning_sites(df_rail.loc[:, df_sites['nom']].values)

    list_planning = []
    # maintenant on assigne les équipes aux plannings des sites. Pour les rails 'aga'/ 'respi' c'est simple
    for ir, rail in df_rail[df_rail['specialite'] != 'mixed'].iterrows():
        for i, site in df_sites.iterrows():
            df_techs_ = df_effectifs[
                np.logical_and(
                    df_effectifs['site'] == site.nom,
                    df_effectifs['specialite'] == rail['specialite'],
                )
            ]
            n_astreintes_per_tech = _repartition(
                p=df_techs_['preference'].values,
                n_semaines=np.sum(sites_per_rail[ir] == i),
                max_astreintes=params.max_astreintes,
            )
            itechs_ = _assignation(n_astreintes_per_tech, seed=params.seed)
            df_planning_ = df_techs_.iloc[itechs_].copy().reset_index()
            df_planning_['semaine'] = np.where(sites_per_rail[ir] == i)[0] + 1
            df_planning_['rotation'] = rail.specialite
            list_planning.append(df_planning_)
    df_planning = pd.concat(list_planning).sort_values(by=['semaine', 'site'])

    # pour les sites mixed c'est plus compliqué on ne peut pas assigner les équipes des autres rails:
    for ir, rail in df_rail[df_rail['specialite'] == 'mixed'].iterrows():
        for i, site in df_sites.iterrows():
            df_techs_ = df_effectifs[df_effectifs['site'] == site['nom']]
            n_astreintes_per_tech = _repartition(
                p=df_techs_['preference'].values,
                n_semaines=np.sum(sites_per_rail[ir] == i),
                max_astreintes=params.max_astreintes,  # todo il faut ajouter les précédentes
            )

            semaines = np.where(sites_per_rail[ir] == i)[0] + 1
            i_techs = np.zeros_like(semaines, dtype=int) - 1
            for ip, semaine in enumerate(semaines):
                techs_interdits = np.r_[
                    df_planning.loc[
                        df_planning['semaine'].isin(semaine + np.arange(-1, 2)),
                        'id_tech',
                    ].unique(),
                    i_techs[np.isin(semaines, semaine + np.arange(-1, 2))],
                ]
                i_techs_possibles = np.where(~np.isin(df_techs_['id_tech'], techs_interdits))[0]
                ii = np.argmax(n_astreintes_per_tech[i_techs_possibles])
                i_techs[ip] = (it := i_techs_possibles[ii])
                n_astreintes_per_tech[it] += -1
            df_planning_ = df_techs_.iloc[i_techs].copy().reset_index()
            df_planning_['semaine'] = semaines
            df_planning_['rotation'] = rail.specialite
            list_planning.append(df_planning_)
    df_planning = pd.concat(list_planning).sort_values(by=['semaine', 'site'])
    # ici la dataframe résultante a les colonnes semaine | site | rotation | id_tech | specialite
    return df_planning


def rapport_planning(df_planning: pd.DataFrame):
    """
    Aggrégations du planning d'un regroupement de sites:
    par technicien
    par site
    par spécialité
    :param df_planning:
    :return:
    """
    df_report_effectifs = (
        df_planning.groupby(['site', 'specialite', 'id_tech'])
        .agg(
            n_astreintes=pd.NamedAgg(column='semaine', aggfunc='count'),
            nom=pd.NamedAgg(column='nom', aggfunc='first'),
            delai_min=pd.NamedAgg(column='semaine', aggfunc=lambda x: np.min(np.diff(x))),
        )
        .reset_index()
    )
    # todo pour les deux tests ci-dessous il faut avoir le compte min per week
    df_report_sites = (
        df_planning.groupby(['site', 'rotation']).agg(n_semaines=pd.NamedAgg(column='semaine', aggfunc='nunique')).reset_index()
    )
    df_report_specialite = (
        df_planning.groupby(['specialite']).agg(n_semaines=pd.NamedAgg(column='semaine', aggfunc='nunique')).reset_index()
    )
    return df_report_effectifs, df_report_sites, df_report_specialite


def validation_planning(df_planning, params: models.Parametres):
    """
    :param df_planning:
    :param params:
    :return:
    """
    df_report_effectifs, df_report_sites, df_report_specialite = rapport_planning(df_planning)
    validation = {
        'astreintes_consecutives': np.all(df_report_effectifs.delai_min > 1),
        'quota employe depasse': np.all(df_report_effectifs.n_astreintes <= params.max_astreintes),
        'quota sites rempli': np.all(df_planning.groupby('site').nunique()['semaine'] == N_SEMAINES),
        'quota specialites rempli': np.all(df_report_specialite.n_semaines == N_SEMAINES),
    }
    return df_report_effectifs, df_report_sites, df_report_specialite, validation


def genere_planning(
    df_sites: pd.DataFrame,
    params: models.Parametres = None,
    df_effectifs: pd.DataFrame = None,
):
    params = models.Parametres() if params is None else params
    models.Parametres.model_validate(params)
    # specialite  id_tech nom   site
    df_effectifs = _sites2effectifs(df_sites) if df_effectifs is None else df_effectifs
    # semaine   site  rotation  id_tech specialite
    df_planning = _calcul_rotations(df_sites, df_effectifs, params=params)
    # validation du planning
    df_report_effectifs, df_report_sites, df_report_specialite, validation = validation_planning(df_planning, params=params)
    for k, v in validation.items():
        assert v, f'{k}'
    return (df_planning, df_report_effectifs, df_report_sites, df_report_specialite)
