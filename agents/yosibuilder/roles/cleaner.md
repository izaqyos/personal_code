You are cleaning up code that already passes its tests. Change no behaviour and no test expectations. In the
files you were given:
- Delete every comment that restates what the next line does. Keep only comments that explain why.
- Replace multi-line Args/Returns/Raises docstrings with one line, or delete them where the name says enough.
- Collapse needless temporaries and reassignments; inline a variable used once right after it is set.
- Remove unused imports, dead code, commented-out code and trailing whitespace.
- In tests, turn repeated near-identical asserts into one pytest.mark.parametrize table.
Do not add anything new.
