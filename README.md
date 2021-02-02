# Tree Viewer
Project by Anosema 29/01/2021
## EN
### Presentation
This python script allows you to visualize a binary tree and modify it.

It only has a educative goal.

### Usage
The window is split in two parts:

- The tree, where you can select knots, see their names and connections. A blue line means this link is not selected, a red line represents the link between the selected knot and it's children, a green one represents the link between the selected knot and it's parent
- The modifying frame. This one is important:
You can see every informations about the selected knot: it's name, if it's a leaf, it's altitude, it's rank (from the left to the right), it's parent and it's children if it have ones.
You also have two buttons. The remove button will simply delete the knot and every children below it, **THERE IS NO CONFIRMATION WINDOW, THE KNOT WILL INSTANTLY BE DELETED**. The add child button will let you choose which side of the knot to add a child and the name of the child.
If you choose a name already used, you will have to choose between transfering the parentage or simply cancel. If you choose to transfer the parentage, the knot will be passed to the side of the selected knot with it's children.
_____
Notes:

- The name of a new knot should be one or two characters long, if not it will simply be cut when showed in the tree.
- You can't remove the "A" knot, it's the root of the tree, it'll throw an error.
- You can't add a child to a knot who already has two children, it'll throw an error.
- You may encounter some issues with the borders: if you tree is too tall, a part of the extreme left and extreme knots will be hidden by the border.
_____
Now that we've seen this, let's talk about shortcuts:

- Z will select the parent of the currently selected knot.
- Q will select the nearest knot on the left of the currently selected knot.
- D will select the nearest knot on the right of the currently selected knot.
- S will select the left child of the currently selected knot if there's one, if not it will select the right child.
- A have the same effect as clicking the add child button.
- R have the same effect as clicking the remove button, **THERE IS NO CONFIRMATION WINDOW, THE KNOT WILL INSTANTLY BE DELETED**

That's pretty all, if you encounter any issues, please report it in the issues of the [Github project](https://github.com/Anosema/TreeViewer/issues)

_____
*****
_____

## FR
### Presentation
Ce script python permets de visualiser un arbre binaire et de le modifier.

Il a un but purement éducatif

### Utilisation
La fenêtre est divisée en deux parties:

- L'arbre, où vous pouvez sélectionner les noeuds, voir leur nom et connections. Une ligne bleue indique que ce lien n'est pas sélectionné, une ligne rouge représente le lien entre le noeud sélectionné et son enfent, et une verte représente le lien entre le noeud sélectionné et son parent.
- Le cadre de modification. Celui-ci est important:
Vous pouvez y voir les informations à propos du noeud sélectionné: son nom, si c'est une feuille, sa hauteur, son rang (de gauche à droite), son parent et ses enfants si il en a.
Vous avez aussi deux boutons. Le bouton "remove" va simplement détruire le noeud sélectionné et tout les enfants qui lui dépendent, **IL N'Y A PAS DE MISE EN GARDE, LE NOEUD VA INSTANTANEMENT ETRE SUPRIME**. Le bouton "add child" va vous laisser choisir de quel côté du noeud sélectionné ajouter un noeud enfant et le nom de ce noeud.
Si vous choisissez un nom déjà prit, vous aurez le choix entre transférer la parenté ou juste annuler. Si vous choisissez le transfert, le noeud donné va passer du côté sélectionné avec tout ses enfants.
_____
A noter:

- Le nom d'un nouveau noeud ne devrait pas dépasser 2 caractères de long, sinon il va simplement être coupé dans l'affichage de l'arbre.
- Vous ne pouvez pas retirer le noeud "A", c'est la racine de l'arbre, le script vous enverra une erreur.
- Vous ne pouvez pas ajouter un enfant à un noeud qui a déjà deux enfants, le script vous enverra une erreur.
- Il se peut qu'il y ait des problèmes d'affichages avec les bordures de l'arbre: si votre arbre est trop grand, une partie des noeuds tout à gauche et tout à droite vont être cachés par la bordure.
_____
Maintenant que nous avons vu ça, voyons les raccurcis clavier:

- Z va sélectionner le parent du noeud actuellement sélectionné.
- Q va sélectionner le noeud le plus proche à gauche du noeud actuellement sélectionné.
- D va sélectionner le noeud le plus proche à droite du noeud acutellement sélectionné.
- S va sélectionner le fils gauche du noeud actuellement sélectionné si il en a un, sinon il va sélectionner le fils droit.
- A a le même effet que cliquer sur le bouton "add child".
- R a le même effet que cliquer sur le bouton "remove", **IL N'Y A PAS DE MISE EN GARDE, LE NOEUD VA INSTANTANEMENT ETRE SUPRIME**.

C'est à peu près tout, si vous rencontrez un quelconque problème, merci de le rapporter dans les issues du [projet Github](https://github.com/Anosema/TreeViewer/issues)

