from collections.abc import Iterator

from pyglossary.entry import Entry
from pyglossary.glossary_types import EntryType
from pyglossary.xdxf.transform import XdxfTransformer

_xdxfTr: XdxfTransformer | None = None


def xdxf_transform(text: str) -> str:
	global _xdxfTr
	if _xdxfTr is None:
		# if self._xsl:
		# 	self._xdxfTr = XslXdxfTransformer(encoding="utf-8")
		# 	return
		_xdxfTr = XdxfTransformer(encoding="utf-8")

	return _xdxfTr.transformByInnerString(text)  # type: ignore


def getHtmlDefi(entry: EntryType):
	if entry.defiFormat == "m":
		return f"<pre>{entry.defi}</pre>"
	if entry.defiFormat == "x":
		return xdxf_transform(entry.defi)
	# now assume it's html
	defi = entry.defi
	if len(entry.l_word) > 1:
		defi = "".join(f"<b>{word}</b><br/>" for word in entry.l_word) + defi
	return defi


def mergeHtmlEntriesWithSameHeadword(
	entryIter: Iterator[EntryType],
) -> Iterator[EntryType]:
	try:
		last: EntryType = next(entryIter)
	except StopIteration:
		return
	last.detectDefiFormat()
	for entry in entryIter:
		if entry.isData():
			if last is not None:
				yield last
				last = None
			continue

		entry.detectDefiFormat()

		if last is None:
			last = entry
			continue
		if entry.l_word[0] != last.l_word[0]:
			yield last
			last = entry
			continue

		defi = getHtmlDefi(last) + "\n<hr>\n" + getHtmlDefi(entry)

		last = Entry(
			entry.l_word[0],
			defi,
			defiFormat="h",
		)

	if last is not None:
		yield last


def mergePlaintextEntriesWithSameHeadword(
	entryIter: Iterator[EntryType],
) -> Iterator[EntryType]:
	try:
		last: EntryType = next(entryIter)
	except StopIteration:
		return
	for entry in entryIter:
		if entry.isData():
			if last is not None:
				yield last
				last = None
			continue

		if last is None:
			last = entry
			continue
		if entry.l_word[0] != last.l_word[0]:
			yield last
			last = entry
			continue

		defi = (
			last.defi
			+ "\n\n"
			+ "-" * 40
			+ "\n"
			+ ", ".join(entry.l_word)
			+ "\n"
			+ entry.defi
		)

		last = Entry(
			entry.l_word[0],
			defi,
			defiFormat="m",
		)

	if last is not None:
		yield last
