from unittest import TestCase


class TestDifficultyMap(TestCase):

    def setUp(self):

        import arithmetics

        self.Term = arithmetics.Terms
        self.difficulty_dct = arithmetics.DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP
        self.terms_counts_found = {v['terms_count'] for v in self.difficulty_dct.values()}
        self.terms_types_found = {v['terms_type'] for v in self.difficulty_dct.values()}

    def test_min_terms_count_DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP(self):

        min_terms_count_allowed = self.Term.MIN_TERMS_COUNT
        min_terms_count_found = min(self.terms_counts_found)

        self.assertGreaterEqual(
            min_terms_count_found, min_terms_count_allowed
        )

    def test_max_terms_count_DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP(self):

        max_terms_count_allowed = self.Term.MAX_TERMS_COUNT
        max_terms_count_found = max(self.terms_counts_found)

        self.assertGreaterEqual(
            max_terms_count_found, max_terms_count_allowed
        )

    def test_terms_types_DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP(self):

        self.assertEquals(
            self.terms_types_found, self.Term.TERMS_TYPES
        )


class TestIntAndFloatTerm(TestCase):

    def setUp(self):

        import arithmetics
        self.Term = arithmetics.Terms

    # _int_term
    def test__int_term(self):
        self.assertEqual(
            self.Term._int_term(max_val=0), 0
        )

    def test_is_int__int_term(self):
        self.assertIsInstance(
            self.Term._int_term(max_val=1), int
        )

    # _float_term
    def test__float_term(self):
        max_val = 15
        term_val = self.Term._float_term(max_val=max_val)
        self.assertTrue(0 <= term_val <= max_val)

    def test_is_float__float_term(self):
        self.assertIsInstance(
            self.Term._float_term(max_val=1), float
        )


class TestAllTermsMethod(TestCase):

    def setUp(self):

        import arithmetics
        self.Term = arithmetics.Terms
        self.difficulties_available = arithmetics.DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP.keys()

    def test_len_above_min_all_terms(self):
        inst = self.Term(difficulty_lvl='1')

        min_terms_count_allowed = self.Term.MIN_TERMS_COUNT
        terms_lst = inst.all_terms()

        self.assertGreaterEqual(len(terms_lst), min_terms_count_allowed)

    def _contains_x_type_all_terms(self, x_type):
        found_type = False

        for lvl in self.difficulties_available:
            inst = self.Term(difficulty_lvl=lvl)

            terms = inst.all_terms()

            for t in terms:
                if type(t) is x_type:
                    found_type = True

        self.assertTrue(found_type, msg='Did not find {}.'.format(x_type))

    def test_contains_float_all_terms(self):
        self._contains_x_type_all_terms(x_type=float)

    def test_contains_int_all_terms(self):
        self._contains_x_type_all_terms(x_type=int)


