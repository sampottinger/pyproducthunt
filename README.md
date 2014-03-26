pyproducthunt
=============
Research-oriented Python library for reading [Product Hunt](http://www.producthunt.co/) posts as structured data.

<br>
Installation
------------
It's just Python. Use [pip and maybe consider a virutal environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/). Either way, after cloning this repository...

```pip install -r requirements.txt```

<br>
Usage
-----
Product Hunt has index pages and posting pages. 

<br>
**pyproducthunt.parse_index(page=0, content=None)**  

Find information from a posts index page, requesting content if needed.

Find information about the posts listed on product hunt's hompage. The posts
are shown gradually on a endless scrolling page which actually calls on
multiple pages. This will return information about the posts on the given
index page.

Dictionaries returned have the following keys:

 - vote_count: The number of upvotes for the post.
 - data_id: The internal ID for the post.
 - post_target_url: The URL of the post.
 - post_title: The title of the post.
 - post_tagline: The tagline of the post.
 - post_comments_url: The URL where comments on the post can be found.
 - post_comments_count: The number of comments on the post.

Coming soon:

 - post_username: The username of the poster.
 - post_user_headline: The headline of the poster (user headline).
 - datetime: The date and time the post was posted.

@keyword page: The page number of the index to parse. Defaults to 0 (first
    index page).
@type: int
@keyword content: The content of the index page to parse. Will request the
    index page from the internet if None. Defaults to None.
@type content: str
@return: List of parsed post information.
@rtype: list of dict

<br>
**pyproducthunt.parse_post(post_name, content=None)**  

Find information from a post, requesting content if needed.

Find information about a single posts given that post's name. Will request
the HTML content for that post's page if not provided.

Dictionaries returned have the following keys:

 - data_id: The internal Product Hunt ID for the given post.
 - vote_count: The number of upvotes this post has recieved.
 - username: The username of the poster.
 - twitter_handle: The twitter handle of the poster.
 - post_target_url: The external URL that the post points to.
 - post_title: The title of the post.
 - post_tagline: The tagline of the post.
 - comments: List of dictionaries with information about post comments.
 - post_datetime: The date / time when the post was added to Product Hunt.

Coming soon:

 - votes_info
 - related_posts

@param post_name: The name of the post to get information about.
@type: str
@keyword content: The content of the post page to parse. Will request the
    post's page from the internet if None. Defaults to None.
@type content: str
@return: Dictionary with information about the parsed post.
@rtype: dict

<br>
Contributing
------------
Pyproducthunt is released under the [GNU GPL v3 license](https://www.gnu.org/copyleft/gpl.html). Automated tests are a little lacking but, for sanity, we do offer...

```python pyproducthunt_test.py```

In addition to adding to automated tests when appropriate, all contributions should follow the [epydoc](http://epydoc.sourceforge.net/) styling convention. There are lots of TODOs including a save to mongodb feature.

<br>
Authors
-------
- [Sam Pottinger](http://gleap.org)
