import os
import re
import json
import subprocess
import argparse
from github import Github, InputGitAuthor
from .publishers import GitIssuePublisher, WebPublisher

def extract_message(text):
    pattern = r'\[C:START\](.*?)\[C:END\]'
    matcher = re.search(pattern, text, re.DOTALL)
    if matcher:
        raw_message = matcher.group(1).strip()
        # Remove any extraneous text around the JSON content
        cleaned_message = re.sub(r'^[^{]*|[^}]*$', '', raw_message)
        return cleaned_message
    return None

def get_diff(gh_before, sha):
    return subprocess.check_output(['git', 'diff', gh_before, sha, "--word-diff"]).decode('utf-8')

def review(openai_key, assistant_id, token, repo, branch, message, gh_before, sha, webhook, websecret):
    git_publisher = GitIssuePublisher(token, repo, branch, sha)
    web_publisher = WebPublisher(webhook, websecret)

    try:
        diff = get_diff(gh_before, sha)
    except subprocess.CalledProcessError as e:
        print(f"Error generating git diff: {e}")
        return

    item = f'User-Suggested Message: {message}\n\nCommit Diff: {diff}'

    try:
        note = subprocess.check_output([
            'cururo', 
            '--item', item, 
            '--openai-key', openai_key, 
            '--assistant-id', assistant_id,
            # '--mode', 'testing',
        ]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error running cururo: {e}")
        return
    
    response = extract_message(note)
    if not response:
        print("No response extracted from the note.")
        return

    try:
        response = json.loads(response)
    except json.JSONDecodeError:
        print(f"Error decoding JSON response: {response}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    try:
        issue_number, comment_id = git_publisher.publish(response)
        author = git_publisher.user
    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
      web_publisher.publish(web_publisher.sort_data({
          'message': response['message'].get('provided', ''),
          'suggested': response['message'].get('generated', ''),
          'adherence': int(response['message']['adherence'].get('score', 0)),
          'adherence_comment': response['message']['adherence'].get('comment', ''),  # New field
          'complexity_comment': response['codeComplexity'].get('comment', ''),       # New field
          'vulnerability': int(response['codeVulnerability'].get('score', 0)),
          'vulnerability_comment': response['codeVulnerability'].get('comment', ''), # New field
          'singleResponsibility': int(response['codeSOLID']['singleResponsibility'].get('score', 0)),
          'singleResponsibility_comment': response['codeSOLID']['singleResponsibility'].get('comment', ''),  # New field
          'openClosed': int(response['codeSOLID']['openClosed'].get('score', 0)),
          'openClosed_comment': response['codeSOLID']['openClosed'].get('comment', ''),  # New field
          'liskovSubstitution': int(response['codeSOLID']['liskovSubstitution'].get('score', 0)),
          'liskovSubstitution_comment': response['codeSOLID']['liskovSubstitution'].get('comment', ''),  # New field
          'interfaceSegregation': int(response['codeSOLID']['interfaceSegregation'].get('score', 0)),
          'interfaceSegregation_comment': response['codeSOLID']['interfaceSegregation'].get('comment', ''),  # New field
          'dependencyInversion': int(response['codeSOLID']['dependencyInversion'].get('score', 0)),
          'dependencyInversion_comment': response['codeSOLID']['dependencyInversion'].get('comment', ''),  # New field
      }, {"user": author, "sha": sha, "repo": repo, "branch": branch, "issue": str(issue_number), "comment": str(comment_id)}))
    except Exception as e:
        print(f"Unexpected error: {e}")


        
def main():
    parser = argparse.ArgumentParser(description="Commit message and diff handler with OpenAI assistance.")

    #### Need tokens
    parser.add_argument('--openai-key', default=os.getenv('OPENAI_API_KEY'), help='OpenAI API key')
    parser.add_argument('--assistant-id', default=os.getenv('OPENAI_ASSISTANT_ID'), help='OpenAI assistant ID')
    parser.add_argument('--token', default=os.getenv('GH_TOKEN'), help='GitHub token')

    #### Data of commit
    parser.add_argument('--repo', default=os.getenv('REPO'), help='Repository name')
    parser.add_argument('--branch', default=os.getenv('BRANCH'), help='Branch of work')
    parser.add_argument('--gh-before', default=os.getenv('GH_BEFORE'), help='GitHub before SHA')
    parser.add_argument('--sha', default=os.getenv('SHA'), help='Commit SHA')
    parser.add_argument('--message', default=os.getenv('MESSAGE'), help='Commit message')

    #### External Api to post
    parser.add_argument('--webhook', default=os.getenv('WEBHOOK'), help='Webhook URL')
    parser.add_argument('--websecret', default=os.getenv('WEBSECRET'), help='Webhook secret')

    args = parser.parse_args()

    review(args.openai_key, args.assistant_id, args.token, args.repo, args.branch, args.message, args.gh_before, args.sha, args.webhook, args.websecret)

if __name__ == "__main__":
    main()
    # print(extract_message("This is a test [C:START] ```json{\"message\": \"This is a test ```json {}```\"}``` [C:END] This is a test"))
    # print(extract_message("This is a test [C:START] {\"message\": \"This is a test ```json {}```\"} [C:END] This is a test"))