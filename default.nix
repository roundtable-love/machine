{ pythonInterpreters, pyproject-nix }:
let
  project = pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
  python = builtins.head (
    pyproject-nix.lib.util.filterPythonInterpreters {
      inherit (project) requires-python;
      inherit pythonInterpreters;
    }
  );
in
(python.pkgs.buildPythonPackage (
  project.renderers.buildPythonPackage {
    inherit python;
    extrasAttrMappings = {
      test = "checkInputs";
    };
  }
)).overrideAttrs
  (prev: {
    nativeBuildInputs = prev.nativeBuildInputs ++ [
      # python.pkgs.pytestCheckHook
    ];
  })
