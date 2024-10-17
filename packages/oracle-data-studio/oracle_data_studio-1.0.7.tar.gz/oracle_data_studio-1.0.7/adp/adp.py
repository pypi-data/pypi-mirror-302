'''
Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/.

Copyright (c) 2023-2024, Oracle and/or its affiliates.

'''

from .adp_misc import AdpMisc
from .adp_analytics import AdpAnalytics
from .adp_ingest import AdpIngest
from .adp_insight import AdpInsight
from .rest import Rest

class Adp:
    '''
    A class used to represent ORDS API
    '''
    def __init__(self, rest : Rest) -> None:
        self.set_rest(rest)
        # pylint: disable-msg=C0103
        self.Analytics = self.InAnalytics(rest)
        self.Ingest = self.InIngest(rest)
        self.Insight = self.InInsight(rest)
        self.Misc = self.InMisc(rest)


    class InAnalytics(AdpAnalytics):
        '''
            Class for analytic view
        '''
        def __init__(self, rest : Rest) -> None:
            super().__init__()
            super().set_rest(rest)

    class InIngest(AdpIngest):
        '''
            Class for copy tables from db link or cloud storage
        '''
        def __init__(self, rest : Rest) -> None:
            super().__init__()
            super().set_rest(rest)

    class InInsight(AdpInsight):
        '''
            Class for insights
        '''
        def __init__(self, rest : Rest) -> None:
            super().__init__()
            super().set_rest(rest)

    class InMisc(AdpMisc):
        '''
            Class for additional functions
        '''
        def __init__(self, rest : Rest) -> None:
            super().__init__()
            super().set_rest(rest)


    def set_rest(self, rest : Rest) -> None:
        '''
            Set REST class
        '''

        self.rest = rest

    def get_rest(self) -> Rest:
        '''
            Access to Rest class
        '''
        return self.rest
