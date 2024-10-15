import re
from collections.abc import Collection, Sequence
from copy import deepcopy
from functools import reduce
from itertools import chain
from operator import iconcat
from typing import Union

try:  # pragma: no cover
    from renardo_lib.Patterns import Pattern
    from renardo_lib.TimeVar import TimeVar
except ModuleNotFoundError:  # pragma: no cover
    try:
        from FoxDot.lib.Patterns import Pattern
        from FoxDot.lib.TimeVar import TimeVar
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            '\n\tThe FoxDotChord package requires the renardo or FoxDot '
            'package to be installed.\n\tYou can install this with:\n'
            '\t$ pip install renardo  # https://renardo.org\n'
            '\tOR\n'
            '\t$ pip install FoxDot   # https://foxdot.org\n'
        ) from exc

from ._chord import Chord


class __chords__:  # noqa: N801
    """
    Creates a harmonic progression based on a list of chords.

    Parameters
    ----------
    chords : str
        Many chords

    Examples
    --------

    ## Pattern chords

    You can create a chord pattern in a few ways.

    One of them is using `[]` or `()` with a list of strings:

    >>> PChord['Am7', 'C(7/9)', 'F7Maj', 'G(4/9/13)']
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]
    >>> PChord('Am7', 'C(7/9)', 'F7Maj', 'G(4/9/13)')
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

    Or use `[]` or `()` passing a string of chords separated by `,`:

    >>> PChord['Am7, C(7/9), F7Maj, G(4/9/13)']
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]
    >>> PChord('Am7,C(7/9),F7Maj,G(4/9/13)')
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

    ## Arpeggios

    You can create arpeggios with all chords.

    >>> PChord['C, G'].arp()
    P[0, 2, 4, 4, 6, 8]

    Or create  a new Pattern with each item repeated len(arp_pattern) times
    and incremented by arp_pattern.

    >>> PChord['C, G'].arp([0, 3])
    P[0, 3, 2, 5, 4, 7, 4, 7, 6, 9, 8, 11]

    You can also create the arpeggio of a single chord when defining it.

    >>> PChord['C@, G']
    P[0, 2, 4, Chord('G')]

    ## Repetition

    You can also set how many times the chord will be repeated

    >>> PChord['C!4, Dm!2'].json_value()
    ['TimeVar', [Chord('C'), Chord('Dm')], [4, 2]]

    Or repeat the number of times the arpeggio will be made

    >>> PChord['C!4, Dm!2, G7!2@'].json_value()
    ['TimeVar', [Chord('C'), Chord('Dm'), 4, 6, 8, 10], [4, 2, 2, 2, 2, 2]]

    ## Degrees

    If you want, you can also get the degrees of the chords, to use on the
    bass, for example.

    Picking up the tonic:

    >>> PChord['C, G'].i
    P[0, 4]
    >>> PChord['C, G'].tonic
    P[0, 4]

    Picking up the supertonic:

    >>> PChord['C2, G2'].ii
    P[1, 5]
    >>> PChord['C2, G2'].supertonic
    P[1, 5]

    Picking up the supertonic:

    >>> PChord['C, G'].iii
    P[2, 6]
    >>> PChord['C, G'].third
    P[2, 6]

    Picking up the subdominant:

    >>> PChord['C4, G4'].iv
    P[3, 7]
    >>> PChord['C4, G4'].subdominant
    P[3, 7]

    Picking up the dominant:

    >>> PChord['C5b, G5#'].v
    P[3.5, 8.5]
    >>> PChord['C5+, G5-'].dominant
    P[4.5, 7.5]

    Picking up the submediant:

    >>> PChord['C6, G6'].vi
    P[5, 9]
    >>> PChord['C6, G6'].submediant
    P[5, 9]

    Picking up the maj:

    >>> PChord['C7Maj, G7'].vii
    P[6, 10]
    >>> PChord['C7, G7M'].seven
    P[5.5, 10.5]

    Picking up the ninth:

    >>> PChord['C9b, G9#'].ix
    P[7.5, 12.5]
    >>> PChord['C9+, G9-'].ninth
    P[8.5, 11.5]

    Picking up the eleventh:

    >>> PChord['C11b, G11#'].xi
    P[9, 14.5]
    >>> PChord['C11+, G11-'].eleventh
    P[10.5, 13]

    Picking up the thirteenth:

    >>> PChord['C13b, G13#'].xiii
    P[11.5, 17]
    >>> PChord['C13+, G13-'].thirteenth
    P[12.5, 15.5]

    Taking more than one degree of the chords:

    >>> PChord['C, G'].deg('i, iii')
    P[0, 2, 4, 6]
    >>> PChord['C, G'].degrees('i, v')
    P[0, 4, 4, 8]

    ## Mixing inputs

    >>> PChord['C, D', [1, 4], 'Dm, E#', (2, 3), 1]
    P[Chord('C'), Chord('D'), P[1, 4], Chord('Dm'), Chord('E#'), P(2, 3), 1]

    >>> PChord[1, 'C, D', [1, 4], 'Dm, E#@', (2, 3)]
    P[1, Chord('C'), Chord('D'), P[1, 4], Chord('Dm'), 3, 5, 7, P(2, 3)]

    >>> PChord[(2, 3), 'C!4, D', [1, 4], 'Dm!3@', 1].json_value()
    ['TimeVar', [P(2, 3), Chord('C'), Chord('D'), 1, 1, 3, 5, 1, P(2, 3), Chord('C'), Chord('D'), 4, 1, 3, 5, 1], [1, 4, 1, 1, 3, 3, 3, 1]]

    >>> PChord[1, PChord['C, D'].arp(), [1, 4], PChord['Dm, E#@'], (2, 3)]
    P[1, P[0, 2, 4, 1, 3.5, 5], P[1, 4], P[Chord('Dm'), 3, 5, 7], P(2, 3)]

    Returns
    -------
    ChordPattern
        Chord/note pattern.
    """  # noqa: E501

    @staticmethod
    def __get(chords, args):
        if isinstance(chords, str):
            chords = chords.split(',')
        elif not isinstance(chords, Sequence):
            chords = [chords]

        for arg in chain(chords, args):
            if isinstance(arg, str):
                yield from map(str.strip, arg.split(','))
            else:
                yield arg

    def __new(
        self, chords: Union[str, list], *args: str
    ) -> Union[Pattern, TimeVar]:

        harmony = []
        repets = []
        for chord in self.__get(chords, args):
            repet = 1
            if not isinstance(chord, str):
                harmony.append(chord)
                repets.append(repet)
                continue

            if matcher := re.search(r'[A-Z].*!(?P<repet>\d{1,})', chord):
                chord = re.sub(r'!(?P<repet>\d{1,})', '', chord)
                repet = int(matcher.group('repet'))
            repets.append(repet)

            if chord.endswith('@'):
                harmony.extend(notes := Chord(chord.removesuffix('@')).notes)
                for _ in range(len(notes) - 1):
                    repets.append(repet)
            else:
                harmony.append(Chord(chord))

        pattern = ChordPattern(harmony)
        if any(filter(lambda r: r > 1, repets)):
            return TimeVar(pattern, repets)
        return pattern

    __getitem__ = __call__ = __new


PChord = __chords__()


class ChordPattern(Pattern):
    """
    Class used by `PChord` to manipulate chords/notes/Patterns.

    You probably shouldn't invoke this class manually, when calling
    PChord[...] this class will be returned, so it may be worth knowing
    its methods.
    """

    _degrees = {
        'I': 'tonic',
        'II': 'supertonic',
        'III': 'third',
        'IV': 'subdominant',
        'V': 'dominant',
        'VI': 'submediant',
        'VII': 'maj',
        'IX': 'ninth',
        'XI': 'eleventh',
        'XIII': 'thirteenth',
    }

    def degrees(self, grades: Union[str, list[str]], *args: str) -> Pattern:
        """
        Take certain degrees from all chords in the pattern.

        Parameters
        ----------
        grades : str | list[str]
            Degrees to be selected.
        *args : str
            Degrees to be selected.

        Examples
        --------

        ## Chord degrees

        Use the function to pick certain chord degrees:

        >>> PChord['F, Am, G, C'].degrees('i')
        P[3, 5, 4, 0]

        Or use your shorthand function:

        >>> PChord['F, Am, G, C'].deg('i')
        P[3, 5, 4, 0]

        An interesting example is taking the bass of the chords:

        >>> PChord['F, Am, G, C'].deg('i')
        P[3, 5, 4, 0]

        It is also possible to take more than one degree of the chords:

        >>> PChord['F, Am, G, C'].deg('i', 'iii')
        P[3, 5, 5, 7, 4, 6, 0, 2]
        >>> PChord['F, Am, G, C'].deg(['i', 'iii'])
        P[3, 5, 5, 7, 4, 6, 0, 2]

        Only the degrees that are present in the chord will be returned.

        >>> PChord['C, Dm7'].deg('i', 'vii')
        P[0, 1, 7]
        >>> PChord['C'].deg('vi')
        P[]

        Anything that is not a chord will be disregarded.

        >>> PChord['C', 2, (2, 2), [2, 2]].deg('i')
        P[0]

        Returns
        -------
        Pattern
            Note pattern.
        """
        if isinstance(grades, str):
            grades = grades.split(',')

        notes = (
            getattr(c, self._degrees.get(a.strip(), '_'), None)
            for c in self.data
            for a in map(str.upper, chain(grades, args))
        )

        return Pattern(list(filter(lambda n: n is not None, notes)))

    deg = degrees

    @property
    def i(self) -> Pattern:
        """
        Get the degree `I` (tonic) of the chords.

        Examples
        --------
        >>> PChord['C, G'].i
        P[0, 4]

        >>> PChord['C, G'].tonic
        P[0, 4]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('I')

    @property
    def ii(self) -> Pattern:
        """
        Get the degree `II` (supertonic) of the chords.

        Examples
        --------
        >>> PChord['C2, G2'].ii
        P[1, 5]

        >>> PChord['C2, G2'].supertonic
        P[1, 5]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('II')

    @property
    def iii(self) -> Pattern:
        """
        Get the degree `III` (third) of the chords.

        Examples
        --------
        >>> PChord['C, G'].iii
        P[2, 6]

        >>> PChord['C, G'].third
        P[2, 6]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('III')

    @property
    def iv(self) -> Pattern:
        """
        Get the degree `IV` (subdominant) of the chords.

        Examples
        --------
        >>> PChord['C4, G4'].iv
        P[3, 7]

        >>> PChord['C4, G4'].subdominant
        P[3, 7]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('IV')

    @property
    def v(self) -> Pattern:
        """
        Get the degree `V` (dominant) of the chords.

        Examples
        --------
        >>> PChord['C, G'].v
        P[4, 8]

        >>> PChord['C, G'].dominant
        P[4, 8]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('V')

    @property
    def vi(self) -> Pattern:
        """
        Get the degree `VI` (submediant) of the chords.

        Examples
        --------
        >>> PChord['C6, G6'].vi
        P[5, 9]

        >>> PChord['C6, G6'].submediant
        P[5, 9]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('VI')

    @property
    def vii(self) -> Pattern:
        """
        Get the degree `VII` (seven) of the chords.

        Examples
        --------
        >>> PChord['C7, G7M'].vii
        P[5.5, 10.5]

        >>> PChord['C7, G7M'].seven
        P[5.5, 10.5]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('VII')

    @property
    def ix(self) -> Pattern:
        """
        Get the degree `IX` (ninth) of the chords.

        Examples
        --------
        >>> PChord['C9, G9'].ix
        P[8, 12]

        >>> PChord['C9, G9'].ninth
        P[8, 12]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('IX')

    @property
    def xi(self) -> Pattern:
        """
        Get the degree `XI` (eleventh) of the chords.

        Examples
        --------
        >>> PChord['C11, G11'].xi
        P[10, 14]

        >>> PChord['C11, G11'].eleventh
        P[10, 14]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('XI')

    @property
    def xiii(self) -> Pattern:
        """
        Get the degree `XIII` (thirteenth) of the chords.

        Examples
        --------
        >>> PChord['C13, G13'].xiii
        P[12, 16]

        >>> PChord['C13, G13'].thirteenth
        P[12, 16]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('XIII')

    tonic = i
    supertonic = ii
    third = iii
    subdominant = iv
    dominant = v
    submediant = vi
    seven = vii
    ninth = ix
    eleventh = xi
    thirteenth = xiii

    def arp(self, arp_pattern: Union[Collection, None] = None):
        """
        Create a arpeggio pattern.

        Parameters
        ----------
        arp_pattern : Collection, optional
            Arpeggio pattern.

        Examples
        --------

        ## Creating arpeggios

        You can create arpeggios with all chords.

        >>> PChord['C, G'].arp()
        P[0, 2, 4, 4, 6, 8]

        Or create  a new Pattern with each item repeated len(arp_pattern) times
        and incremented by arp_pattern.

        >>> PChord['C, G'].arp([0, 3])
        P[0, 3, 2, 5, 4, 7, 4, 7, 6, 9, 8, 11]

        Returns
        -------
        Pattern[int]
            Arpeggio pattern.
        """
        notes = [a.notes if hasattr(a, 'notes') else [a] for a in self]
        pattern = Pattern(reduce(iconcat, notes))

        if arp_pattern:
            return pattern.stutter(len(arp_pattern)) + arp_pattern
        return pattern

    def __mul__(self, other):
        """
        Multiple pattern.

        Parameters
        ----------
        other : int
            Times the pattern should be repeated.

        Examples
        --------

        ## Multiplying the pattern

        Multiplying the chord sequence

        >>> PChord['C, G'] * 3
        P[Chord('C'), Chord('G'), Chord('C'), Chord('G'), Chord('C'), Chord('G')]

        Multiplying the chord sequence with notes

        >>> PChord['C, G', 1] * 3
        P[Chord('C'), Chord('G'), 1, Chord('C'), Chord('G'), 1, Chord('C'), Chord('G'), 1]

        Multiplying the chord sequence with notes and microtonal notes

        >>> PChord['C, G', 1, 1.5] * 3
        P[Chord('C'), Chord('G'), 1, 1.5, Chord('C'), Chord('G'), 1, 1.5, Chord('C'), Chord('G'), 1, 1.5]

        Multiplying the chord sequence with notes, microtonal notes and note sequence

        >>> PChord['C, G', 1, 1.5, [1, 2]] * 3
        P[Chord('C'), Chord('G'), 1, 1.5, P[1, 2], Chord('C'), Chord('G'), 1, 1.5, P[1, 2], Chord('C'), Chord('G'), 1, 1.5, P[1, 2]]

        Multiplying the sequence of chords with notes, microtonal notes and sequence of notes playing separately and together

        >>> PChord['C, G', 1, 1.5, [1, 2], (2, 1)] * 3
        P[Chord('C'), Chord('G'), 1, 1.5, P[1, 2], P(2, 1), Chord('C'), Chord('G'), 1, 1.5, P[1, 2], P(2, 1), Chord('C'), Chord('G'), 1, 1.5, P[1, 2], P(2, 1)]

        ## Invalid types

        Apenas interios podem ser usados, caso outro tipo seja passado sera levantado um erro

        >>> PChord['C'] * True
        Traceback (most recent call last):
          ...
        NotImplementedError: Cannot multiplate 'True' -> <class 'bool'>

        >>> PChord['C'] * False
        Traceback (most recent call last):
          ...
        NotImplementedError: Cannot multiplate 'False' -> <class 'bool'>

        >>> PChord['C'] * 'string'
        Traceback (most recent call last):
          ...
        NotImplementedError: Cannot multiplate 'string' -> <class 'str'>

        >>> PChord['C'] * 1.0
        Traceback (most recent call last):
          ...
        NotImplementedError: Cannot multiplate '1.0' -> <class 'float'>

        """  # noqa: E501
        if not isinstance(other, int) or isinstance(other, bool):
            raise NotImplementedError(
                f"Cannot multiplate '{other}' -> {type(other)}"
            )

        copy = self.true_copy()
        copy.data.extend(
            [
                deepcopy(data)
                for _ in range(other - 1)
                for data in self.true_copy().data
            ]
        )
        return copy

    def __add__(self, other):
        """
        Added in pattern.

        Parameters
        ----------
        other : Any
            Element to be added.

        Examples
        --------

        ## Adding elements

        You can use `+` to add an element or another sequence to the chord/note pattern.

        >>> PChord['C'] + Chord('D')
        P[Chord('C'), Chord('D')]

        >>> PChord['C'] + 'D'
        P[Chord('C'), Chord('D')]

        >>> PChord['C'] + ['D']
        P[Chord('C'), Chord('D')]

        >>> PChord['C'] + Pattern('D')
        P[Chord('C'), Chord('D')]

        >>> PChord['C'] + 1
        P[Chord('C'), 1]

        >>> PChord['C'] + 2.0
        P[Chord('C'), 2.0]

        >>> PChord['C'] + PChord['D']
        P[Chord('C'), Chord('D')]
        """  # noqa: E501
        copy = self.true_copy()
        if isinstance(other, Chord):
            copy.data.append(other)
        elif isinstance(other, str):
            copy.data.append(Chord(other))
        elif isinstance(other, (list, Pattern)):
            copy.data.extend(
                [
                    Chord(data) if isinstance(data, str) else deepcopy(data)
                    for data in list(other)
                ]
            )
        else:
            copy.data.append(other)

        return copy
