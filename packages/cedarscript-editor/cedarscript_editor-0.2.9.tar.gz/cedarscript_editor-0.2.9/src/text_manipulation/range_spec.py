import re
from collections.abc import Sequence
from typing import NamedTuple

from cedarscript_ast_parser import Marker, RelativeMarker, RelativePositionType, MarkerType, BodyOrWhole
from .indentation_kit import get_line_indent_count

MATCH_TYPES = ('exact', 'stripped', 'normalized', 'partial')


class RangeSpec(NamedTuple):
    start: int
    end: int
    indent: int = 0

    def __str__(self):
        return (f'{self.start}:{self.end}' if self.as_index is None else f'%{self.as_index}') + f'@{self.indent}'

    def __len__(self):
        return self.end - self.start

    @property
    def as_index(self) -> int | None:
        return None if len(self) else self.start

    @property
    def collapsed(self):
        return self.set_length(0)

    def set_length(self, range_len: int):
        return self._replace(end=self.start + range_len)

    def inc(self, count: int = 1):
        return self._replace(start=self.start + count, end=self.end + count)

    def dec(self, count: int = 1):
        return self._replace(start=self.start - count, end=self.end - count)

    def read(self, src: Sequence[str]) -> Sequence[str]:
        return src[self.start:self.end]

    def write(self, src: Sequence[str], target: Sequence[str]):
        target[self.start:self.end] = src

    def delete(self, src: Sequence[str]) -> Sequence[str]:
        result = self.read(src)
        del src[self.start:self.end]
        return result

    @staticmethod
    def normalize_line(line: str):
        return re.sub(r'[^\w]', '.', line.strip(), flags=re.UNICODE)

    @classmethod
    def from_line_marker(
            cls,
            lines: Sequence[str],
            search_term: Marker,
            search_range: 'RangeSpec' = None
    ):
        """
        Find the index of a specified line within a list of strings, considering different match types and an offset.

        This function searches for a given line within a list, considering 4 types of matches in order of priority:
        1. Exact match
        2. Stripped match (ignoring leading and trailing whitespace)
        3. Normalized match (ignoring non-alphanumeric characters)
        4. Partial (Searching for a substring, using `casefold` to ignore upper- and lower-case differences).

        The function applies the offset across all match types while maintaining the priority order.

        :Args:
            :param lines: The list of strings to search through.
            :param search_term:
                search_marker.value: The line to search for.
                search_marker.offset: The number of matches to skip before returning a result.
                          0 skips no match and returns the first match, 1 returns the second match, and so on.
            :param search_range: The index to start the search from. Defaults to 0. The index to end the search at (exclusive).
                                  Defaults to (0, -1), which means search to the end of the list.

        :returns:
            RangeSpec: The index for the desired line in the 'lines' list.
                 Returns None if no match is found or if the offset exceeds the number of matches within each category.

        :Example:
            >> lines = ["Hello, world!", "  Hello, world!  ", "Héllo, wörld?", "Another line", "Hello, world!"]
            >> _find_line_index(lines, "Hello, world!", 1)
            4  # Returns the index of the second exact match

        Note:
            - The function prioritizes match types in the order: exact, stripped, normalized, partial.
            - The offset is considered separately for each type.
        """
        search_start_index, search_end_index, _ = search_range if search_range is not None else (0, -1, 0)
        search_line = search_term.value
        assert search_line, "Empty marker"
        assert search_term.type == MarkerType.LINE, f"Invalid marker type: {search_term.type}"

        matches = {t: [] for t in MATCH_TYPES}

        stripped_search = search_line.strip()
        normalized_search_line = cls.normalize_line(stripped_search)

        if search_start_index < 0:
            search_start_index = 0
        if search_end_index < 0:
            search_end_index = len(lines)

        assert search_start_index < len(lines), (
            f"search start index ({search_start_index}) "
            f"must be less than line count ({len(lines)})"
        )
        assert search_end_index <= len(lines), (
            f"search end index ({search_end_index}) "
            f"must be less than or equal to line count ({len(lines)})"
        )

        for i in range(search_start_index, search_end_index):
            line = lines[i]
            reference_indent = get_line_indent_count(line)

            # Check for exact match
            if search_line == line:
                matches['exact'].append((i, reference_indent))

            # Check for stripped match
            elif stripped_search == line.strip():
                matches['stripped'].append((i, reference_indent))

            # Check for normalized match
            elif normalized_search_line == cls.normalize_line(line):
                matches['normalized'].append((i, reference_indent))

            # Last resort!
            elif normalized_search_line.casefold() in cls.normalize_line(line).casefold():
                matches['partial'].append((i, reference_indent))

        offset = search_term.offset or 0
        for match_type in MATCH_TYPES:
            if offset < len(matches[match_type]):
                index, reference_indent = matches[match_type][offset]
                match match_type:
                    case 'normalized':
                        print(f'Note: using {match_type} match for {search_term}')
                    case 'partial':
                        print(f"Note: Won't accept {match_type} match at index {index} for {search_term}")
                        continue
                if isinstance(search_term, RelativeMarker):
                    match search_term.qualifier:
                        case RelativePositionType.BEFORE:
                            index += -1
                        case RelativePositionType.AFTER:
                            index += 1
                        case RelativePositionType.AT:
                            pass
                        case _ as invalid:
                            raise ValueError(f"Not implemented: {invalid}")
                return cls(index, index, reference_indent)

        return None


RangeSpec.EMPTY = RangeSpec(0, -1, 0)


class IdentifierBoundaries(NamedTuple):
    whole: RangeSpec
    body: RangeSpec

    def __str__(self):
        return f'IdentifierBoundaries({self.whole} (BODY: {self.body}) )'

    @property
    def start_line(self) -> int:
        return self.whole.start + 1

    @property
    def body_start_line(self) -> int:
        return self.body.start + 1

    @property
    def end_line(self) -> int:
        return self.whole.end

    # See the other bow_to_search_range
    def location_to_search_range(self, location: BodyOrWhole | RelativePositionType) -> RangeSpec:
        match location:
            case BodyOrWhole.BODY:
                return self.body
            case BodyOrWhole.WHOLE | RelativePositionType.AT:
                return self.whole
            case RelativePositionType.BEFORE:
                return RangeSpec(self.whole.start, self.whole.start, self.whole.indent)
            case RelativePositionType.AFTER:
                return RangeSpec(self.whole.end, self.whole.end, self.whole.indent)
            case RelativePositionType.INSIDE_TOP:
                return RangeSpec(self.body.start, self.body.start, self.body.indent)
            case RelativePositionType.INSIDE_BOTTOM:
                return RangeSpec(self.body.end, self.body.end, self.body.indent)
            case _ as invalid:
                raise ValueError(f"Invalid: {invalid}")
