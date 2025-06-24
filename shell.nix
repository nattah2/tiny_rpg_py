{ pkgs ? import <nixpkgs> {} }:
let
  pythonPackages = pkgs.python3Packages;
in
pkgs.mkShell {
  name = "rpg-dev-env";
  venvDir = "./venv";

  buildInputs = [
    pythonPackages.python
    pythonPackages.venvShellHook  # This handles the venv creation
    pythonPackages.colorama
    pythonPackages.termcolor
    pythonPackages.flake8
    pkgs.pyright
    pythonPackages.pylint
    pythonPackages.numpy
    pythonPackages.python-lsp-server
    pythonPackages.pip
    pkgs.sqlite
  ];

  postShellHook = ''
    export CURRENT_ENVIRONMENT=GAMEDEV
    export DATABASE_PATH="$PWD/data/database.db"
    export USER_PATH="$PWD/data/user_data"
    unset SOURCE_DATE_EPOCH
    echo "Welcome to the RPG dev environment! Python and dependencies are ready."
  '';
}

  # For some reason if you rename the folder and try and enter it it doesn't work.
