{
  description = "Teeny Tiny Compiler - Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        python3
        gcc
      ];

      shellHook = ''
        echo "🐍 Teeny Tiny Compiler development environment"
        echo "Python: $(python3 --version)"
        echo "GCC: $(gcc --version | head -n 1)"
      '';
    };
  };
}
