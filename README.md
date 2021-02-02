# Tree Viewer
Project by Anosema 29/01/2021
## EN
### Presentation
This python script allows you to visualize a binary tree and modify it.
It only has a educative goal.
### Usage
The window is split in two parts:
	- The tree, where you can select knots, see their names and connections. A blue line means this link is not selected, a red line represents the link between the selected knot and it's children, a green one represents the link between the selected knot and it's parent
	- The modifying frame. This one is important :
	You can see every informations about the selected knot : it's name, if it's a leaf, it's altitude, it's rank (from the left to the right), it's parent and it's children if it have ones.
	You also have two buttons. The remove button will simply delete the knot and every children below it, **THERE IS NO CONFIRMATION WINDOW, THE KNOT WILL INSTANTLY BE DELETED**. The add child button will let you choose which side of the knot to add a child and the name of the child.
	If you choose a name already used, you will have to choose between transfering the parentage or simply cancel. If you choose to transferthe parentage, the knot will be passed to the side of the selected knot with it's children.
	Notes:
		- The name of a new knot should be one or two characters long, if not it will simply be cut when showed in the tree.
		- You can't remove the "A" knot, it's the root of the tree, it'll throw an error.
		- You can't add a child to a knot who already has two children, it'll throw an error.
		- You may encounter some issues with the borders : if you tree is too tall, a part of the extreme left and extreme knots will be hidden by the border.

Now that we've seen this, let's talk about shortcuts.
	- Z will select the parent of the currently selected knot.
	- Q will select the nearest knot on the left of the currently selected knot.
	- D will select the nearest knot on the right of the currently selected knot.
	- S will select the left child of the currently selected knot if there's one, if not it will select the right child.
	- A have the same effect as clicking the add child button.
	- R have the same effect as clicking the remove button, **THERE IS NO CONFIRMATION WINDOW, THE KNOT WILL INSTANTLY BE DELETED**

That's pretty all, if you encounter any issues please report it in the issues of the [Github project](https://github.com/Anosema/TreeViewer)


