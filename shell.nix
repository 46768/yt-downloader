let
pkgs = import <nixpkgs> {};
in pkgs.mkShell {
	packages = [
		pkgs.python313
		(pkgs.python313.withPackages (p: [
			p.python-ffmpeg
			p.yt-dlp
			p.adb-shell
		] ++ p.adb-shell.optional-dependencies.usb))
	];
}
