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
