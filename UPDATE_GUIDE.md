# Guide de Mise à Jour - Manus CLI v5.5.0

## 🎯 Pourquoi mettre à jour ?

La version **5.5.0** apporte des améliorations majeures :

### ✨ Nouvelles Fonctionnalités

1. **Commande `manus start`** - Splash screen interactif avec "AND AFTER YOU"
2. **Mode interactif corrigé** - `manus chat -i` fonctionne maintenant sans erreur
3. **Meilleure expérience utilisateur** - Vous savez immédiatement que vous pouvez interagir

### 🐛 Corrections de Bugs

- ✅ Correction de l'erreur "Missing argument 'MESSAGE'" avec `manus chat -i`
- ✅ Correction du warning urllib3 (si vous suivez les instructions complètes)

---

## 📦 Instructions de Mise à Jour

### Option 1 : Mise à jour automatique (Recommandée)

Si vous avez déjà la v5.4.0 ou supérieure :

```bash
manus update
```

### Option 2 : Mise à jour manuelle

Si vous avez une version plus ancienne ou si `manus update` ne fonctionne pas :

```bash
# Désinstaller l'ancienne version
pip3 uninstall manus-cli -y

# Installer la nouvelle version depuis GitHub
pip3 install --user git+https://github.com/ehadsagency-ai/manus-cli.git
```

### Option 3 : Mise à jour forcée

Si vous rencontrez des problèmes :

```bash
pip3 install --user --upgrade --force-reinstall git+https://github.com/ehadsagency-ai/manus-cli.git
```

---

## ✅ Vérification de l'Installation

Après la mise à jour, vérifiez que tout fonctionne :

```bash
# Vérifier la version
manus --version
# Devrait afficher : Manus CLI v5.5.0

# Tester le nouveau splash screen
manus start
# Devrait afficher le splash screen avec "AND AFTER YOU"

# Tester le mode interactif
manus chat -i
# Devrait fonctionner sans erreur "Missing argument"
```

---

## 🔧 Résolution des Problèmes

### Problème 1 : `manus: command not found`

**Cause :** Le PATH n'est pas configuré correctement.

**Solution (macOS) :**

```bash
# Ajouter au PATH dans ~/.zshrc ou ~/.bash_profile
echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc

# Recharger le shell
source ~/.zshrc

# Ou redémarrer le terminal
```

**Vérifier le PATH :**

```bash
echo $PATH | grep Python
# Devrait afficher : .../Library/Python/3.9/bin
```

### Problème 2 : Warning urllib3

**Message d'erreur :**
```
urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'
```

**Solution :**

```bash
# Désinstaller urllib3 v2
pip3 uninstall urllib3 -y

# Installer urllib3 v1.26.20 (compatible avec LibreSSL)
pip3 install --user 'urllib3<2.0'

# Réinstaller Manus CLI
pip3 install --user --upgrade --force-reinstall git+https://github.com/ehadsagency-ai/manus-cli.git
```

### Problème 3 : `No such command 'update'`

**Cause :** Vous avez encore l'ancienne version installée.

**Solution :** Utilisez l'Option 2 ou 3 ci-dessus pour mettre à jour manuellement.

### Problème 4 : `No such command 'start'`

**Cause :** La mise à jour n'a pas été effectuée correctement.

**Solution :**

```bash
# Vérifier la version installée
pip3 show manus-cli

# Si la version n'est pas 5.5.0, réinstaller
pip3 install --user --upgrade --force-reinstall git+https://github.com/ehadsagency-ai/manus-cli.git
```

---

## 🎨 Tester les Nouvelles Fonctionnalités

### 1. Tester le Splash Screen

```bash
manus start
```

**Résultat attendu :**
```
╭──────────────────────────────────────────────────────────────────────────────╮
│                                                                              │
│                ███╗   ███╗ █████╗ ███╗   ██╗██╗   ██╗███████╗                │
│                ████╗ ████║██╔══██╗████╗  ██║██║   ██║██╔════╝                │
│                ██╔████╔██║███████║██╔██╗ ██║██║   ██║███████╗                │
│                ██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║╚════██║                │
│                ██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝███████║                │
│                ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝                │
│                                                                              │
│                AI-POWERED COMMAND LINE INTERFACE                             │
│                Professional • Intelligent • Spec-Driven                      │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯

                              ✨ AND AFTER YOU ✨
```

### 2. Tester le Mode Interactif

```bash
manus chat -i
```

**Résultat attendu :**
- Pas d'erreur "Missing argument 'MESSAGE'"
- Affichage du splash screen
- Prompt "You:" pour saisir votre message
- Possibilité de taper "exit" pour quitter

### 3. Tester avec un Rôle Spécifique

```bash
manus start --role developer
```

**Résultat attendu :**
- Splash screen affiché
- Mode interactif avec le rôle "developer"

---

## 📚 Nouvelles Commandes Disponibles

### `manus start`

Démarre Manus CLI avec le splash screen interactif.

```bash
# Démarrage basique
manus start

# Avec un rôle spécifique
manus start --role developer

# Avec un mode spécifique
manus start --mode quality
```

### `manus chat -i` (Corrigé)

Mode interactif via la commande chat (équivalent à `manus start`).

```bash
# Mode interactif basique
manus chat -i

# Avec un rôle
manus chat -i --role developer
```

### `manus update` (Depuis v5.4.0)

Met à jour Manus CLI vers la dernière version.

```bash
manus update
```

---

## 🎓 Commandes Interactives

Une fois en mode interactif, vous pouvez :

- **Taper votre message** et appuyer sur Entrée
- **Taper `exit`, `quit`, `q`, ou `bye`** pour quitter
- **Appuyer sur `Ctrl+C`** pour quitter immédiatement

---

## 📞 Support

Si vous rencontrez des problèmes :

1. **Vérifiez la version** : `manus --version`
2. **Consultez le README** : https://github.com/ehadsagency-ai/manus-cli/blob/main/README.md
3. **Consultez le CHANGELOG** : https://github.com/ehadsagency-ai/manus-cli/blob/main/CHANGELOG.md
4. **Ouvrez une issue** : https://github.com/ehadsagency-ai/manus-cli/issues

---

## 🚀 Prochaines Étapes

Après la mise à jour, essayez :

```bash
# 1. Démarrer en mode interactif
manus start

# 2. Poser une question
You: Bonjour, comment ça va ?

# 3. Créer un projet (active le mode spec-driven)
You: Créer une application web de gestion de tâches

# 4. Quitter
You: exit
```

---

**Bonne utilisation de Manus CLI v5.5.0 ! 🎉**
