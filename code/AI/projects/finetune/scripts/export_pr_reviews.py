#!/usr/bin/env python3
"""
PR Review Export Script

Exports pull request reviews from GitHub repositories to create
training data for fine-tuning. Captures review comments with
associated code context.

Usage:
    python export_pr_reviews.py --repo owner/repo --output ../data/pr_reviews/
    python export_pr_reviews.py --repos repos.txt --output ../data/pr_reviews/ --token $GITHUB_TOKEN
"""

import argparse
import json
import os
import re
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class ReviewComment:
    """A single review comment with context."""
    pr_number: int
    pr_title: str
    repo: str
    comment_id: int
    path: str
    line: Optional[int]
    side: str  # LEFT or RIGHT
    diff_hunk: str
    body: str
    author: str
    created_at: str
    in_reply_to: Optional[int]


@dataclass
class PRReview:
    """A complete PR review."""
    pr_number: int
    pr_title: str
    pr_body: str
    repo: str
    state: str  # APPROVED, CHANGES_REQUESTED, COMMENTED
    author: str
    created_at: str
    body: str
    comments: list[ReviewComment]


class GitHubPRExporter:
    """Export PR reviews using GitHub CLI (gh)."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self._check_gh_cli()

    def _check_gh_cli(self):
        """Verify gh CLI is installed and authenticated."""
        try:
            result = subprocess.run(
                ['gh', 'auth', 'status'],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print("Warning: gh CLI not authenticated. Run 'gh auth login' first.")
        except FileNotFoundError:
            raise RuntimeError(
                "GitHub CLI (gh) not found. Install with: brew install gh"
            )

    def _run_gh(self, args: list[str]) -> dict:
        """Run a gh CLI command and return JSON result."""
        cmd = ['gh'] + args
        if self.token:
            env = os.environ.copy()
            env['GH_TOKEN'] = self.token
        else:
            env = None

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env
        )

        if result.returncode != 0:
            raise RuntimeError(f"gh command failed: {result.stderr}")

        return json.loads(result.stdout) if result.stdout.strip() else {}

    def list_prs(self, repo: str, state: str = 'all', limit: int = 100) -> list[dict]:
        """List pull requests for a repository."""
        prs = self._run_gh([
            'pr', 'list',
            '--repo', repo,
            '--state', state,
            '--limit', str(limit),
            '--json', 'number,title,body,state,author,createdAt,mergedAt,closedAt'
        ])
        return prs

    def get_pr_reviews(self, repo: str, pr_number: int) -> list[dict]:
        """Get reviews for a specific PR."""
        reviews = self._run_gh([
            'api',
            f'repos/{repo}/pulls/{pr_number}/reviews',
            '--paginate'
        ])
        return reviews if isinstance(reviews, list) else []

    def get_review_comments(self, repo: str, pr_number: int) -> list[dict]:
        """Get review comments (inline comments) for a PR."""
        comments = self._run_gh([
            'api',
            f'repos/{repo}/pulls/{pr_number}/comments',
            '--paginate'
        ])
        return comments if isinstance(comments, list) else []

    def export_pr(self, repo: str, pr_number: int, pr_info: dict) -> Optional[PRReview]:
        """Export a single PR with its reviews and comments."""
        reviews = self.get_pr_reviews(repo, pr_number)
        comments = self.get_review_comments(repo, pr_number)

        if not reviews and not comments:
            return None

        # Convert comments to our format
        review_comments = []
        for comment in comments:
            review_comments.append(ReviewComment(
                pr_number=pr_number,
                pr_title=pr_info.get('title', ''),
                repo=repo,
                comment_id=comment.get('id', 0),
                path=comment.get('path', ''),
                line=comment.get('line'),
                side=comment.get('side', 'RIGHT'),
                diff_hunk=comment.get('diff_hunk', ''),
                body=comment.get('body', ''),
                author=comment.get('user', {}).get('login', 'unknown'),
                created_at=comment.get('created_at', ''),
                in_reply_to=comment.get('in_reply_to_id')
            ))

        # Get the main review (if any)
        main_review = None
        for review in reviews:
            if review.get('body') or review.get('state') != 'COMMENTED':
                main_review = review
                break

        if not main_review:
            main_review = {'state': 'COMMENTED', 'body': '', 'user': {'login': 'unknown'}, 'submitted_at': ''}

        return PRReview(
            pr_number=pr_number,
            pr_title=pr_info.get('title', ''),
            pr_body=pr_info.get('body', '') or '',
            repo=repo,
            state=main_review.get('state', 'COMMENTED'),
            author=main_review.get('user', {}).get('login', 'unknown'),
            created_at=main_review.get('submitted_at', ''),
            body=main_review.get('body', '') or '',
            comments=review_comments
        )

    def export_repo(self, repo: str, limit: int = 100) -> list[PRReview]:
        """Export all PR reviews from a repository."""
        print(f"Fetching PRs from {repo}...")
        prs = self.list_prs(repo, state='all', limit=limit)

        print(f"Found {len(prs)} PRs, fetching reviews...")
        reviews = []

        for i, pr in enumerate(prs):
            pr_number = pr['number']
            print(f"  [{i+1}/{len(prs)}] PR #{pr_number}: {pr['title'][:50]}...")

            try:
                review = self.export_pr(repo, pr_number, pr)
                if review and (review.body or review.comments):
                    reviews.append(review)
            except Exception as e:
                print(f"    Error: {e}")
                continue

        print(f"Exported {len(reviews)} PRs with reviews/comments")
        return reviews


def convert_to_training_format(reviews: list[PRReview]) -> list[dict]:
    """Convert PR reviews to training data format."""
    training_data = []

    for review in reviews:
        # Convert inline comments to Q&A format
        for comment in review.comments:
            if not comment.body or not comment.diff_hunk:
                continue

            # Skip very short comments (likely just acknowledgments)
            if len(comment.body) < 20:
                continue

            # Create instruction from the context
            instruction = f"Review this code change in {comment.path}:"

            # The diff hunk is the input (code context)
            code_context = comment.diff_hunk

            # The review comment is the expected output
            output = comment.body

            training_data.append({
                'id': f"pr_{review.pr_number}_comment_{comment.comment_id}",
                'instruction': instruction,
                'input': code_context,
                'output': output,
                'category': 'code_review',
                'language': _detect_language(comment.path),
                'source': 'pr_review',
                'quality': 'high',  # Real human feedback
                'metadata': {
                    'pr_number': review.pr_number,
                    'pr_title': review.pr_title,
                    'file_path': comment.path,
                    'repo': review.repo,
                    'author': comment.author,
                    'created_at': comment.created_at
                }
            })

    return training_data


def _detect_language(filepath: str) -> str:
    """Detect programming language from file path."""
    ext_map = {
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.py': 'python',
        '.go': 'go',
        '.rs': 'rust',
        '.java': 'java',
        '.rb': 'ruby',
        '.php': 'php',
        '.cs': 'csharp',
        '.cpp': 'cpp',
        '.c': 'c',
    }

    ext = Path(filepath).suffix.lower()
    return ext_map.get(ext, 'unknown')


def main():
    parser = argparse.ArgumentParser(
        description='Export PR reviews from GitHub for fine-tuning'
    )
    parser.add_argument(
        '--repo',
        help='Single repository to export (format: owner/repo)'
    )
    parser.add_argument(
        '--repos',
        help='File containing list of repositories (one per line)'
    )
    parser.add_argument(
        '--output',
        default='../data/pr_reviews/',
        help='Output directory'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Maximum PRs to fetch per repo (default: 100)'
    )
    parser.add_argument(
        '--token',
        help='GitHub token (or set GITHUB_TOKEN env var)'
    )
    parser.add_argument(
        '--training-format',
        action='store_true',
        help='Also output in training data format'
    )

    args = parser.parse_args()

    if not args.repo and not args.repos:
        print("Error: Specify --repo or --repos")
        print("\nExample:")
        print("  python export_pr_reviews.py --repo myorg/myrepo --output ../data/pr_reviews/")
        return 1

    # Get list of repos
    repos = []
    if args.repo:
        repos.append(args.repo)
    if args.repos:
        with open(args.repos) as f:
            repos.extend(line.strip() for line in f if line.strip())

    # Export reviews
    exporter = GitHubPRExporter(token=args.token)
    all_reviews = []

    for repo in repos:
        reviews = exporter.export_repo(repo, limit=args.limit)
        all_reviews.extend(reviews)

    # Save results
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    # Save raw export
    raw_output = output_path / 'pr_reviews_raw.json'
    with open(raw_output, 'w') as f:
        json.dump(
            {
                'exported_at': datetime.now().isoformat(),
                'total_reviews': len(all_reviews),
                'reviews': [asdict(r) for r in all_reviews]
            },
            f,
            indent=2,
            default=str
        )
    print(f"\nSaved raw export to {raw_output}")

    # Convert to training format if requested
    if args.training_format:
        training_data = convert_to_training_format(all_reviews)
        training_output = output_path / 'pr_reviews_training.json'

        with open(training_output, 'w') as f:
            json.dump({
                'version': '1.0.0',
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'source': 'pr_reviews',
                    'total_examples': len(training_data)
                },
                'data': training_data
            }, f, indent=2)

        print(f"Saved training format to {training_output}")
        print(f"Total training examples: {len(training_data)}")

    return 0


if __name__ == '__main__':
    exit(main())
