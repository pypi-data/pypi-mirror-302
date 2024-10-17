from random import randrange

import pytest

from tj_text.typograph import en_typus, ru_typus
from tj_text.typograph.chars import (
    HBAR,
    HYPHEN,
    HYPHEN_MINUS,
    MDASH,
    NBHYPHEN,
    NBSP,
    WORD_JOINER,
)
from tj_text.typograph.constants import (
    CURRENCY_SYMBOLS,
    CURRENCY_SYMBOLS_USED_IN_FORMULAS,
    POLISH_ZLOTY,
)
from tj_text.typograph.core import TypusCore
from tj_text.typograph.mixins import RuExpressions
from tj_text.typograph.processors import EscapeHtml, EscapePhrases, Expressions


@pytest.fixture()
def typus_factory():
    def factory(expression_mixin_cls, *, include=None, exclude=None):
        class Typus(expression_mixin_cls, TypusCore):
            processors = (EscapePhrases, EscapeHtml, Expressions)
            expressions = filter(
                lambda expr: (
                    (expr in include if include else True)
                    and (expr not in exclude if exclude else True)
                ),
                expression_mixin_cls.expressions,
            )

        return Typus()

    return factory


class TestEnRuExpressions:
    """Tests for typograph.mixins.EnRuExpressions class."""

    @pytest.mark.parametrize(
        'word_parts',
        [
            ('из', 'под'),
            ('когда', 'либо'),
            ('сим', 'карта'),
            ('QR', 'код'),
            ('где', 'нибудь'),
        ],
    )
    @pytest.mark.parametrize('hyphen', [HYPHEN, HYPHEN_MINUS])
    def test_expr_rep_hyphen_between_short_words(self, word_parts, hyphen):
        word = hyphen.join(word_parts)
        expected_word = NBHYPHEN.join(word_parts)
        text = (
            f'{word} проверим{word}дефис неразрывный {word} подставляется '
            f'корректно{word}между словами {word}.'
        )
        expected_text = (
            f'{expected_word} проверим{word}дефис неразрывный {expected_word} '
            f'подставляется корректно{word}между словами {expected_word}.'
        )

        result = en_typus(text)

        assert result == expected_text

    def test_add_word_joiner_between_digits_and_mdash(self):
        assert en_typus(f'28{MDASH}31') == f'28{WORD_JOINER}{MDASH}{WORD_JOINER}31'

    def test_add_word_joiner_between_digit_and_horizontal_bar(self):
        assert en_typus(f'28{HBAR}31') == f'28{WORD_JOINER}{HBAR}{WORD_JOINER}31'

    def test_nbsp_before_hbar_between_digits(self):
        assert en_typus(f'28 {HBAR} 31') == f'28{NBSP}{HBAR} 31'

    def test_nbsp_before_hbar_between_words(self):
        assert en_typus(f'abc {HBAR} def') == f'abc{NBSP}{HBAR} def'

    def test_nbsp_after_hbar_start_of_line(self):
        assert en_typus(f'{HBAR} 31') == f'{HBAR}{NBSP}31'

    def test_nbsp_before_hbar_end_of_line(self):
        assert en_typus(f'word {HBAR}') == f'word{NBSP}{HBAR}'

    @pytest.mark.parametrize(
        'source,expected',
        [
            ('1 apple', '1_apple'),
            ('12 apples', '12_apples'),
            ('123 apples', '123_apples'),
            ('1234 apples', '1234_apples'),
            ('1200 км', '1200_км'),
            ('400 + 3', '400_+ 3'),
            ('4000 1', '4000_1'),
            ('40 000,00 bucks', '40_000,00_bucks'),
            ('12345 apples', '12345 apples'),
        ],
    )
    def test_whitespace_after_digits(self, source, expected):
        assert en_typus(source, debug=True) == expected

    @pytest.mark.parametrize('source', ['1/2', '1/4', '5/16'])
    def test_preserve_fractions(self, source):
        assert en_typus(source) == source

    @pytest.mark.parametrize(
        'source,expected',
        [
            ('Т-Банк', f'Т{NBHYPHEN}Банк'),
            ('T-Pay', f'T{NBHYPHEN}Pay'),
            ('банк-посредник', f'банк{NBHYPHEN}посредник'),
            ('топ-менеджер', f'топ{NBHYPHEN}менеджер'),
            ('1234-number', f'1234{NBHYPHEN}number'),
            ('123-number', f'123{NBHYPHEN}number'),
            ('a23d-investment', f'a23d{NBHYPHEN}investment'),
        ],
        ids=[
            'russian letters',
            'english letters',
            'four-letter word',
            'three-letter word',
            'four digits',
            'three digits',
            'letters and digits',
        ],
    )
    def test_non_breaking_hyphen_if_word_before_has_4_symbols_or_fewer(
        self, source, expected
    ):
        assert en_typus(source) == expected

    @pytest.mark.parametrize(
        'source,expected',
        [
            ('бизнес-зал', f'бизнес{NBHYPHEN}зал'),
            ('business-trip', f'business{NBHYPHEN}trip'),
            ('киловатт-часа', f'киловатт{NBHYPHEN}часа'),
            ('киловатт-час', f'киловатт{NBHYPHEN}час'),
            ('somelaw-1234', f'somelaw{NBHYPHEN}1234'),
            ('somelaw-123', f'somelaw{NBHYPHEN}123'),
            ('somelaw-a12d', f'somelaw{NBHYPHEN}a12d'),
        ],
        ids=[
            'russian letters',
            'english letters',
            'four-letter word',
            'three-letter word',
            'four digits',
            'three digits',
            'letters and digits',
        ],
    )
    def test_non_breaking_hyphen_if_word_after_has_4_symbols_or_fewer(
        self, source, expected
    ):
        assert en_typus(source) == expected

    @pytest.mark.parametrize(
        'source,expected',
        [
            ('грейс-период', 'грейс-период'),
            ('интернет-эквайринг', 'интернет-эквайринг'),
            ('word1-1word', 'word1-1word'),
            (
                '<a href="/invest/social/profile/T-Investments/">',
                '<a href="/invest/social/profile/T-Investments/">',
            ),
            (
                '<a href="/invest/social/my-pro/t-pay/">',
                '<a href="/invest/social/my-pro/t-pay/">',
            ),
        ],
        ids=[
            'five letters before and after',
            'more than five letters',
            'five letters and digits',
            'html tag attribute mixed case',
            'html tag attribute lower case',
        ],
    )
    def test_non_breaking_hyphen_not_applied(self, source, expected):
        assert en_typus(source) == expected


class TestRuExpressions:
    """Tests for typograph.mixins.RuExpressions class."""

    def test_expressions_from_parent_class_are_in_child(self):
        for expression in ru_typus.expressions:
            assert expression in RuExpressions.expressions

    @pytest.mark.parametrize(
        'word',
        [
            'без',
            'перед',
            'при',
            'через',
            'над',
            'под',
            'про',
            'для',
            'около',
            'среди',
            'из-под',
            'из-за',
            'по-над',
        ],
    )
    def test_expr_rep_positional_spaces_after_long_prepositions(
        self, word, typus_factory
    ):
        typus = typus_factory(RuExpressions, exclude={'rep_hyphen_between_short_words'})
        text = (
            f'{word.capitalize()} проверяем{word} предлог {word} неразрывным '
            f'{word}пробелом {word}. {word.capitalize()} тоже.'
        )
        expected_result = (
            f'{word.capitalize()}{NBSP}проверяем{word} предлог {word}{NBSP}неразрывным '
            f'{word}пробелом {word}. {word.capitalize()}{NBSP}тоже.'
        )

        result = typus(text)

        assert result == expected_result

    @pytest.mark.parametrize('word', ['же', 'ли', 'бы', 'б', 'уж'])
    def test_expr_rep_positional_spaces_before_particles(self, word):
        text = f'Проверяем{word} частицу {word} неразрывным {word}пробелом {word}.'
        expected_result = (
            f'Проверяем{word} частицу{NBSP}{word} '
            f'неразрывным {word}пробелом{NBSP}{word}.'
        )

        result = ru_typus(text)

        assert result == expected_result

    @pytest.mark.parametrize(
        'original,expected',
        [
            ('несмотря на', f'несмотря{NBSP}на'),
            ('в отличие от', f'в{NBSP}отличие{NBSP}от'),
            ('в связи с', f'в{NBSP}связи{NBSP}с'),
        ],
    )
    def test_rep_positional_spaces_for_verbose_prepositions(self, original, expected):
        original_text = (
            f'{original.capitalize()} проверяем {original} неразрывным пробелом. '
            f'{original.capitalize()} даже в начале второго предложения.'
        )
        expected_result = (
            f'{expected.capitalize()}{NBSP}проверяем {expected}{NBSP}неразрывным '
            f'пробелом. '
            f'{expected.capitalize()}{NBSP}даже в{NBSP}начале второго предложения.'
        )

        result = ru_typus(original_text)

        assert result == expected_result

    @pytest.mark.parametrize(
        'original,expected', [('когда-нибудь', f'когда{NBHYPHEN}нибудь')]
    )
    def test_rep_custom_replacements(self, original, expected):
        original_text = (
            f'{original} проверим {original} слово-исключение '
            f'{original} будет сразу{original} заменено{original}.'
        )
        expected_result = (
            f'{expected} проверим {expected} слово-исключение '
            f'{expected} будет сразу{original} заменено{original}.'
        )

        result = ru_typus(original_text)

        assert result == expected_result

    @pytest.mark.parametrize(
        'currency',
        CURRENCY_SYMBOLS + CURRENCY_SYMBOLS_USED_IN_FORMULAS + [POLISH_ZLOTY],
    )
    @pytest.mark.parametrize('spaces_count', [0, 1, 10])
    def test_add_nbsp_between_number_and_currency_symbol_only(
        self, currency, spaces_count
    ):
        target_number = randrange(10000)
        original_text = f'{target_number}{" " * spaces_count}{currency} денег'
        expected_text = f'{target_number}{NBSP}{currency} денег'

        result = ru_typus(original_text)

        assert result == expected_text
