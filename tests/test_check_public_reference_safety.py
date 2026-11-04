import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "check_public_reference_safety.py"


class PublicReferenceSafetyTests(unittest.TestCase):
    def run_check(self, root: Path):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_allows_documented_placeholders_and_redacted_examples(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "arn:aws:iam::111122223333:role/example\n"
                "arn:aws:iam::123456789012:role/example\n"
                "ghp_<redacted>\n"
                "sk-<redacted>\n",
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("passed", result.stdout)

    def test_rejects_secret_shapes_and_unexpected_account_id_without_echoing_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            aws_key = "AKIA" + "A" * 16
            github_token = "ghp_" + "b" * 36
            openai_key = "sk-" + "c" * 32
            private_key_header = "-----BEGIN " + "PRIVATE KEY-----"
            account_id = "9999" + "8888" + "7777"
            payload = "\n".join(
                [aws_key, github_token, openai_key, private_key_header, account_id]
            )
            (root / "example.txt").write_text(payload, encoding="utf-8")

            result = self.run_check(root)

            self.assertEqual(result.returncode, 1)
            for label in (
                "AWS access key ID",
                "GitHub token",
                "OpenAI API key",
                "private key",
                "unexpected AWS account ID",
            ):
                self.assertIn(label, result.stderr)
            for value in (aws_key, github_token, openai_key, account_id):
                self.assertNotIn(value, result.stderr)


    def test_scans_tfvars_and_auto_tfvars_without_exposing_matched_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            access_key = "AKIA" + "A" * 16
            temporary_key = "ASIA" + "B" * 16
            account_id = "999988887777"
            (root / "terraform.tfvars").write_text(
                f'aws_access_key_id = "{access_key}"\n',
                encoding="utf-8",
            )
            (root / "deployment.auto.tfvars").write_text(
                f'account_id = "{account_id}"\n'
                f'aws_access_key_id = "{temporary_key}"\n',
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("terraform.tfvars:1: AWS access key ID", result.stderr)
            self.assertIn("deployment.auto.tfvars:1: unexpected AWS account ID", result.stderr)
            self.assertIn("deployment.auto.tfvars:2: AWS access key ID", result.stderr)
            for value in (access_key, temporary_key, account_id):
                self.assertNotIn(value, result.stderr)

    def test_redacted_tfvars_and_generated_terraform_files_are_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "safe.auto.tfvars").write_text(
                'account_id = "111122223333"\n'
                'github_token = "ghp_<redacted>"\n'
                'api_key = "sk-<redacted>"\n',
                encoding="utf-8",
            )
            generated = root / ".terraform"
            generated.mkdir()
            (generated / "unsafe.auto.tfvars").write_text(
                'aws_access_key_id = "AKIA' + "Z" * 16 + '"\n',
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
