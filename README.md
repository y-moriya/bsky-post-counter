# bsky-post-counter
Count bsky posts and record with pixela

{"feed": [
    {"post": {
      "author": {
        "handle" or "did": # 異なればrepost
      }

      "record": {
        "$type": "app.bsky.feed.post" # <- post
        "reply": {}  # <- あればreply
        "embed": {
          "$type": "app.bsky.embed.record" # <- であればquote
        }
      }
    }}
]}  