stages:
  - publish
  - sync

variables:
  GIT_STRATEGY: clone

# Repo -> Wiki: publish reviewed docs on every merge to main
publish-to-wiki:
  stage: publish
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
  script:
    - git config --global user.email "ci@example.com"
    - git config --global user.name "Docs CI"
    - git clone "https://oauth2:${WIKI_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.wiki.git" wiki
    - rsync -a --delete --exclude='.git' docs/ wiki/
    - cd wiki
    - git add -A
    - 'git commit -m "Publish docs from ${CI_COMMIT_SHORT_SHA}" || echo "No changes"'
    - git push origin HEAD:master

# Wiki -> Repo: pull UI edits back as an MR (scheduled)
sync-wiki-back:
  stage: sync
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule"'
  script:
    - git config --global user.email "ci@example.com"
    - git config --global user.name "Docs CI"
    - git clone "https://oauth2:${WIKI_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.wiki.git" wiki
    - rsync -a --delete --exclude='.git' wiki/ docs/
    - git checkout -B wiki-sync
    - git add docs/
    - |
      if git diff --cached --quiet; then
        echo "No wiki UI edits to sync"; exit 0
      fi
    - git commit -m "Sync wiki UI edits back to repo"
    - git push -f "https://oauth2:${WIKI_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git" wiki-sync -o merge_request.create -o merge_request.target=main
