from github import Github, Auth
from dotenv import load_dotenv
import os

load_dotenv()

auth = Auth.Token(os.getenv('GITHUB_PAT'))
g = Github(auth=auth)

N = 5000

for lang in ('Java', 'Python', 'C++'):
	content = []
	for i, repo in enumerate(g.search_repositories('language:Java', sort='updated')[:N]):
		content += [repo.clone_url]
		if i % 100 == 0:
			print(f'{lang} repo {i+1}/{N}: {repo.clone_url}')

	f = open(f'repo_urls/{lang}.txt', 'w')
	f.write('\n'.join(content))
	f.close()

g.close()
