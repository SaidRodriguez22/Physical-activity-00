# Etape1: Chargement du fichier
## Choix de la méthode de chargement (suggestions de Copilot)

Le fichier `0_z.csv` commence par une ligne de commentaire (`# accelerometer data in g`), suivie de l'en-tête `t,x,y,z`. Pandas doit donc ignorer cette première ligne, sinon il prendrait le commentaire pour l'en-tête. Copilot a proposé trois options.

**Option 1 : `pd.read_csv('0_z.csv', skiprows=1)`**
- `skiprows=1` saute la première ligne du fichier, quel que soit son contenu.
- Avantage : simple et explicite.
- Limite : elle suppose qu'il y a exactement une ligne à ignorer. Si un fichier avait deux lignes de commentaire, ou aucune, le chargement serait faux (perte de l'en-tête, ou commentaire lu comme données).

**Option 2 : `pd.read_csv('0_z.csv', comment='#')`**
- `comment='#'` ignore tout ce qui suit le caractère `#` sur une ligne. Une ligne qui commence par `#` est donc complètement ignorée.
- Avantage : ne dépend pas du nombre de lignes de commentaire, donc plus robuste si les fichiers varient.
- Limite : si un `#` apparaissait au milieu d'une ligne de données, la fin de la ligne serait ignorée (ce n'est pas le cas ici).

**Option 3 : `pd.read_csv('0_z.csv', skiprows=1, comment='#')`**
- Combine les deux : saute la première ligne, puis ignore d'éventuelles autres lignes de commentaire.
- Limite : redondante ici, car la première ligne est déjà un commentaire que `comment='#'` suffirait à ignorer. Elle cumule aussi les limites de l'option 1.

**Remarque sur le code proposé** : les trois lignes sont exécutées à la suite et réaffectent chacune la variable `df`. Seule la dernière compte, il faut donc n'en garder qu'une.

**Choix retenu : option 2.** Elle exprime directement l'intention (« ignorer les lignes de commentaire ») et reste valable si le nombre de lignes de commentaire change.

import pandas as pd

# choix de l'Option 2 :
df = pd.read_csv('0_z.csv', comment='#')

## Calcul de l'ENMO (suggestions de Copilot et choix retenu)

L'ENMO (*Euclidean Norm Minus One*) se calcule pour chaque échantillon : `sqrt(x² + y² + z²) − 1`, en g. On prend la norme des trois axes, ce qui rend la mesure indépendante de l'orientation du capteur, puis on retire 1 g, la gravité mesurée au repos.

Copilot a proposé trois façons de l'appliquer.

**Option 1 : `calculate_enmo(x, y, z)` appelée sur les colonnes**
- La fonction prend `x`, `y`, `z` et renvoie l'ENMO. Appelée avec `df['x'], df['y'], df['z']`, elle calcule toutes les lignes d'un coup, grâce à la vectorisation de numpy.
- Avantage : rapide, lisible, et réutilisable sur un simple nombre ou sur un tableau.

**Option 2 : `df.apply(lambda row: ..., axis=1)`**
- Appelle la fonction ligne par ligne.
- Inconvénient : beaucoup plus lente (ici 21 000 lignes) pour un résultat identique, car l'option 1 fait déjà le calcul sur toute la colonne.

**Option 3 : `calculate_enmo_vectorized(df)`**
- Même calcul vectorisé, mais la fonction prend directement le DataFrame et dépend donc des noms de colonnes `x`, `y`, `z`.
- Avantage : appel court. Inconvénient : moins générale que l'option 1, qui fonctionne avec n'importe quelles données.

**Corrections apportées au code de Copilot**
- **Suppression de `np.abs`** : Copilot renvoyait la valeur absolue « pour éviter les valeurs négatives ». Or les valeurs négatives ont un sens : au repos, la norme est parfois légèrement inférieure à 1 g (bruit, calibration). Les rendre positives, ou les tronquer à 0, biaiserait l'intégration par époque. On les conserve.
- **Chargement** : `skiprows=1` remplacé par `comment='#'` (voir le choix précédent).
- **Doublons** : les fonctions et l'application de l'ENMO étaient écrites plusieurs fois. Une seule version est conservée.

**Choix retenu : option 1**, avec un appel vectorisé sur les colonnes. Elle est rapide, réutilisable, et ne dépend pas de la structure du DataFrame.

def calculate_enmo(x, y, z):
    """ENMO = norme euclidienne (x, y, z) - 1, en g. Valeurs négatives conservées."""
    return np.sqrt(x**2 + y**2 + z**2) - 1

df['enmo'] = calculate_enmo(df['x'], df['y'], df['z'])