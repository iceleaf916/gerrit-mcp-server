import unittest
from unittest.mock import patch, MagicMock
import asyncio

from gerrit_mcp_server.main import post_review_comment


class TestPostReviewComment(unittest.TestCase):
    @patch('gerrit_mcp_server.main.run_curl')
    def test_post_review_comment_with_labels(self, mock_run_curl):
        mock_run_curl.return_value = (0, '{"done": true}', '')
        asyncio.run(post_review_comment(
            '123',
            labels={'Verified': 1},
            gerrit_base_url='https://gerrit-review.googlesource.com'
        ))
        expected_payload_str = '{"labels": {"Verified": 1}}'
        mock_run_curl.assert_called_with(
            [
                '-X',
                'POST',
                '-H',
                'Content-Type: application/json',
                '--data',
                expected_payload_str,
                'https://gerrit-review.googlesource.com/changes/123/revisions/current/review'
            ],
            'https://gerrit-review.googlesource.com'
        )

    @patch('gerrit_mcp_server.main.run_curl')
    def test_post_review_comment_with_single_comment(self, mock_run_curl):
        mock_run_curl.return_value = (0, '{"done": true}', '')
        asyncio.run(post_review_comment(
            '123',
            comments=[{"file_path": "test.py", "line_number": 1, "message": "test comment"}],
            gerrit_base_url='https://gerrit-review.googlesource.com'
        ))
        expected_payload_str = '{"comments": {"test.py": [{"line": 1, "message": "test comment"}]}}'
        mock_run_curl.assert_called_with(
            [
                '-X',
                'POST',
                '-H',
                'Content-Type: application/json',
                '--data',
                expected_payload_str,
                'https://gerrit-review.googlesource.com/changes/123/revisions/current/review'
            ],
            'https://gerrit-review.googlesource.com'
        )

    @patch('gerrit_mcp_server.main.run_curl')
    def test_post_review_comment_with_multiple_comments(self, mock_run_curl):
        mock_run_curl.return_value = (0, '{"done": true}', '')
        asyncio.run(post_review_comment(
            '123',
            comments=[
                {"file_path": "test.py", "line_number": 1, "message": "first comment"},
                {"file_path": "test.py", "line_number": 10, "message": "second comment"},
                {"file_path": "other.py", "line_number": 5, "message": "third comment"}
            ],
            gerrit_base_url='https://gerrit-review.googlesource.com'
        ))
        expected_payload_str = '{"comments": {"test.py": [{"line": 1, "message": "first comment"}, {"line": 10, "message": "second comment"}], "other.py": [{"line": 5, "message": "third comment"}]}}'
        mock_run_curl.assert_called_with(
            [
                '-X',
                'POST',
                '-H',
                'Content-Type: application/json',
                '--data',
                expected_payload_str,
                'https://gerrit-review.googlesource.com/changes/123/revisions/current/review'
            ],
            'https://gerrit-review.googlesource.com'
        )

    @patch('gerrit_mcp_server.main.run_curl')
    def test_post_review_comment_with_message(self, mock_run_curl):
        mock_run_curl.return_value = (0, '{"done": true}', '')
        asyncio.run(post_review_comment(
            '123',
            message='LGTM',
            gerrit_base_url='https://gerrit-review.googlesource.com'
        ))
        expected_payload_str = '{"message": "LGTM"}'
        mock_run_curl.assert_called_with(
            [
                '-X',
                'POST',
                '-H',
                'Content-Type: application/json',
                '--data',
                expected_payload_str,
                'https://gerrit-review.googlesource.com/changes/123/revisions/current/review'
            ],
            'https://gerrit-review.googlesource.com'
        )

    @patch('gerrit_mcp_server.main.run_curl')
    def test_post_review_comment_with_comments_and_labels(self, mock_run_curl):
        mock_run_curl.return_value = (0, '{"done": true}', '')
        asyncio.run(post_review_comment(
            '123',
            comments=[{"file_path": "test.py", "line_number": 1, "message": "test comment"}],
            labels={'Verified': 1},
            gerrit_base_url='https://gerrit-review.googlesource.com'
        ))
        expected_payload_str = '{"comments": {"test.py": [{"line": 1, "message": "test comment"}]}, "labels": {"Verified": 1}}'
        mock_run_curl.assert_called_with(
            [
                '-X',
                'POST',
                '-H',
                'Content-Type: application/json',
                '--data',
                expected_payload_str,
                'https://gerrit-review.googlesource.com/changes/123/revisions/current/review'
            ],
            'https://gerrit-review.googlesource.com'
        )

    def test_post_review_comment_empty_params_raises_error(self):
        with self.assertRaises(ValueError) as context:
            asyncio.run(post_review_comment('123'))
        self.assertEqual(str(context.exception), "labels, comments, and message cannot all be empty")


if __name__ == '__main__':
    unittest.main()
