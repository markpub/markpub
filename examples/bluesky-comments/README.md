# Bluesky Comments

Embed Bluesky comments on a MarkPub generated website.

MarkPub supports Bluesky comments on MarkPub pages referenced in
Bluesky posts.

The code is derived from
https://www.coryzue.com/writing/bluesky-comments/  

Current code: https://unpkg.com/browse/bluesky-comments@0.9.0/  

The code is included in
`.markpub/this-website-themes/dolce/_header.html` and
`.markpub/this-website-themes/dolce/page.html`.  

## Embedding Bluesky comments - manual procedure  

Embedding Bluesky comments on a specific MarkPub webpage is a manual
procedure with the following steps:  

- Create a Bluesky post that references a specific webpage.  

- Capture the URL of that particular Bluesky post.  
   it will look similar to this:
```
    https://bsky.app/profile/anderbill.bsky.social/post/3lipv4nlp2s2c
 ```  

- Add the following YAML to the top of the MarkPub Markdown file:
```
---
bluesky_comments_post: https://bsky.app/profile/anderbill.bsky.social/post/3lipv4nlp2s2c
---
```  

- Commit and push the updated Markdown page to the Git repository. The website is rebuilt and Bluesky comments to that post are displayed on that webpage.  


**Note**: This capability may be automated in the future.

