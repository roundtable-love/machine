{

  description = "Machine: Exit Babylon, speak Machine.";

  inputs = {

    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    flake-parts.url = "github:hercules-ci/flake-parts";

    pyproject-nix = {
      url = "github:kingarrrt/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    systems.url = "github:nix-systems/default";

  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {

      systems = import inputs.systems;

      flake = { };

      perSystem =
        { lib, pkgs, ... }:
        let
          default = pkgs.callPackage ./. { inherit (inputs) pyproject-nix; };
          transpile = {
            type = "app";
            program = lib.getExe' default "transpile";
            meta.description = "Transpiler: ";
          };
        in
        {

          apps = {
            default = transpile;
            inherit transpile;
            compile = {
              type = "app";
              program = lib.getExe' default "compile";
              meta.description = "Compiler: compile human expression to standard.";
            };
          };

          packages = { inherit default; };

          devShells.default = pkgs.mkShellNoCC {
            inputsFrom = [ default ];
            packages = with default.optional-dependencies; dev ++ test;
          };

        };

    };

}
