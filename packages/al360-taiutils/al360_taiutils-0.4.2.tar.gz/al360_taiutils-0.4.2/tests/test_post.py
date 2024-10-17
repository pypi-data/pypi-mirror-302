# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import pytest

from al360_taiutils.webservice import post_with_retries


class TestPost(object):

    def test_post_bad_uri(self):
        uri = 'https://bad_uri'
        input_data = {}
        with pytest.raises(RuntimeError):
            post_with_retries(uri, input_data, max_retries=2, retry_delay=1)
