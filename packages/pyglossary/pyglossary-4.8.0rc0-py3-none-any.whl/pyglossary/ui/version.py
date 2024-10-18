import sys
from os.path import isdir, join

from pyglossary import core


def getGitVersion(gitDir: str) -> str:
	import subprocess

	try:
		outputB, _err = subprocess.Popen(
			[
				"git",
				"--git-dir",
				gitDir,
				"describe",
				"--always",
			],
			stdout=subprocess.PIPE,
		).communicate()
	except Exception as e:
		sys.stderr.write(str(e) + "\n")
		return ""
	# if _err is None:
	return outputB.decode("utf-8").strip()


def getVersion() -> str:
	from pyglossary.core import rootDir

	gitDir = join(rootDir, ".git")
	if isdir(gitDir):
		version = getGitVersion(gitDir)
		if version:
			return version
	return core.VERSION
