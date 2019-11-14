This is an asyncio bot for monitoring repos. Right now, the bot is setup as me. In the future the bot should be the ascbot.

## Environment Variables
The following environment variables need to be set in order for this bot to operate:

- GH_AUTH: This is the authentication token for the user/bot that is going to be interacting with the GitHub API.
- GH_SECRET: This is the secret for the repo that is generated when the webhook is created.

## Deploying

1. Make changes to this repo, PR in the changes, get a review, and get merged.
2. This will automatically fire a hub.docker.com build under the USGS-Astrogeology organization
3. Navigate to the `asc-gitbot` repo on the internal gitlab instance, select `CI / CD -> Pipelines` from the left hand menus, and click the big green `Run Pipelines` button. I have been having to run this twice recently as the first attempt seems to fail.

## Debugging
The bot is running inside a docker container in a docker swarm, so you can use standard docker debugging techniques to get into the container and see what is going on. A nice enhancement might be a persistent, external to the container log file to avoid having to ever access the container.