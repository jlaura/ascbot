import os

import aiohttp
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

from .utils import get_secret

routes = web.RouteTableDef()
router = routing.Router()

@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
    """ Whenever an issue is opened, greet the author and say thanks."""
    # get the URL from the event
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]
    repo = event.data["repository"]["name"]

    if repo == 'bottest':
        message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
        await gh.post(url, data={"body": message})

@routes.post("/")
async def main(request):
    # read the GitHub webhook payload
    body = await request.read()

    # our authentication token and secret
    gh_secret = get_secret("GH_SECRET") 
    oauth_token = get_secret("GH_AUTH")
    # a representation of GitHub webhook event
    event = sansio.Event.from_http(request.headers, body, secret=gh_secret)

    # create the client context so we get a release on the session and then 
    # grab then listen on the session for posts from the webhook
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "ascbot",
                                  oauth_token=oauth_token) 

        # call the appropriate callback for the event
        await router.dispatch(event, gh)

    # return a "Success"
    return web.Response(status=200)

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)