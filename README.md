Pull-request analysis tool

1. `conda create -n pull-requests python=3.10`
2. `conda install pip`
3. `pip install -r requirements.txt`
4. `pip install -e .`

Data format saved as `pull-requests.txt` locally. Obtained through the github api with the command
`gh api -H "Accept: application/vnd.github+json" repos/{user}/repo/pulls > pull-requests.txt`

Run `python -m source.get_data` to run the script 

Trying pagination with response headers
`curl -I {repo_url} > headers.txt`
