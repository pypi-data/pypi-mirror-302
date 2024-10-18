Checklist to update version on PyPi and Gitlab:
 1) edit code
 2) edit setup.py (increase version number)
 3) cd to same level as setup.py
# pypi
 4) python -m build
 5) twine upload dist/* --skip-existing
# gitlab
 6) git push