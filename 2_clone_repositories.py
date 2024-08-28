import os
from git import Repo
import traceback

for lang in ('Java', 'Python', 'C++'):
	os.makedirs(f'repos/{lang}', exist_ok=True)
	with open(f'repo_urls/{lang}.txt', 'r') as f:
		for i, url in enumerate(f.readlines()):
			url = url.strip()
			name = '_'.join(url.split('/')[-2:]).replace('.git', '') # convert url to folder name
			folder = f'repos/{lang}/{name}'
			if not os.path.exists(folder):
				try:
					Repo.clone_from(url, folder, depth=1)
				except:
					print(traceback.format_exc())

			if i % 20 == 0:
				print(f'{lang} repo #{i+1}: {url}')
