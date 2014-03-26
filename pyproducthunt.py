"""Parsing library for reading Product Hunt listings using python.

@author: Sam Pottinger (samnsparky)
@license: GNU GPL v3
"""

import bs4

import persistance


# Based on 20 days of posts, the URL-escaping rules that product hunt seems to
# follow
PRODUCT_HUNT_CHARACTER_MAPPINGS = {
    ' ': '-',
    '.': '-',
    '#': '',
    '(': '',
    ')': '',
    ';': '-',
    '+': '-'
}


def generate_index_url(page=0):
    """Find the URL where information about the posts index can be found.

    @keyword page: The page number of the posts index to find the URL for.
        Defaults to 0 (first page).
    @type page: int
    @return: The URL where the posts index can be found.
    @rtype: str
    """
    return 'http://www.producthunt.co/?page=%d' % page


def parse_index(page=0, content=None):
    """Find information from a posts index page, requesting content if needed.

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
    """
    # Read the page content if not provided
    if not content:
        url = generate_index_url(page)
        response = urllib2.urlopen()
        if (response.code < 200) or (response.code >= 300):
            raise ValueError('Failed to parse %s (%d).' % (url, response.code))
        content = repsonse.read()

    # Create soup
    soup = bs4.BeautifulSoup(content)

    # Parse out
    posts = soup.find_all(class_='post')
    posts_serialized = map(serialize_index, posts)

    return posts_serialized


def serialize_index(post_soup):
    """Parse information from a single post as read from a post index page soup.

    Parse a beautiful soup instance for a single post listed on the post index
    page, returning a dict (serialized) information record for that listing.

    Dictionary returned have the following keys:
     - vote_count: The number of upvotes for the post.
     - data_id: The internal ID for the post.
     - post_target_url: The external URL the post points to.
     - post_title: The title of the post.
     - post_tagline: The tagline of the post.
     - post_comments_url: The URL where comments on the post can be found.
     - post_comments_count: The number of comments on the post.

    Coming soon:
     - post_username: The username of the poster.
     - post_user_headline: The headline of the poster (user headline).
     - datetime: The date and time the post was posted.

    @param post_soup: The page number of the index to parse. Defaults to 0 (first
        index page).
    @type: bs4.BeautifulSoup or content tag
    @return: Single parsed post information.
    @rtype: dict
    """
    # Parse vote information
    upvote_info = post_soup.find(class_='vote-count')
    vote_count = int(upvote_info.getText().replace(',', ''))
    vote_data_id = int(upvote_info['data-id'])

    # Parse information from posting links
    post_target_url_info = post_soup.find(class_='url')
    post_main_link = post_target_url_info.find(class_='post-url')
    post_target_url = post_main_link['href']
    post_title = post_main_link.getText()
    
    post_tagline = post_soup.find(class_='post-tagline').getText()
    
    discussion_link = post_target_url_info.find(class_='view-discussion')
    post_comments_url = discussion_link['data-url']
    
    comments_count_str = discussion_link.getText()
    comments_count_str = comments_count_str.replace(' comments', '')
    comments_count_str = comments_count_str.replace(' comment', '')
    comments_count_str = comments_count_str.replace(',', '')
    comments_count_str = comments_count_str.strip()
    if comments_count_str == 'View details':
        post_comments_count = 0
    else:
        post_comments_count = int(comments_count_str)

    # TODO
    #  - post_username
    #  - post_user_headline
    #    this should be indexed seperately but thats for issue #1

    # TODO: Get the datetime of the post if possible. See issue #2.

    return {
        'vote_count': vote_count,
        'data_id': vote_data_id,
        'post_target_url': post_target_url,
        'post_title': post_title,
        'post_tagline': post_tagline,
        'post_comments_url': post_comments_url,
        'post_comments_count': post_comments_count
    }


def save_index(page=0, content=None):
    """Save information from a posts index page, requesting content if needed.

    Stroe information about the posts listed on product hunt's hompage. The
    posts are shown gradually on a endless scrolling page which actually calls
    on multiple pages. This will save information about the posts on the given
    index page to a mongodb instance.
    """
    raise NotImplementedError()


def escape_url_name(name):
    """Find the likely URL-safe name for a post's human name.

    Product Hunt has rules for how post names become slugs (urls). This will
    take a human name for a post and return a URL for that post.

    Note that some posts have the same names and have an ID for differentiation.
    This funciton does not provide that ID.

    @param name: The human name for a post's title.
    @type name: str
    @return: The machine/URL-safe name for the given post title. Note that some
        posts have the same names and have an ID for differentiation. This
        funciton does not provide that ID.
    @rtype: str
    """
    for (orig, new) in PRODUCT_HUNT_CHARACTER_MAPPINGS.items():
        name = name.replace(orig, new)
    return name


def generate_post_url(post_name, escape_name=True):
    """Generate the URL where information about a post can be found.

    @param post_name: The name of the post to generate a URL for.
    @type post_name: str
    @keyword escape_name: Flag indicating if the provided post_name is a human
        friendly name that needs to be escaped / URL-ified. See escape_url_name.
        Defaults to True.
    @type escape_name: bool
    @return: URL for the post with the given name / title. Note that some
        posts have the same names and have an ID for differentiation. This
        funciton does not provide that ID.
    @rytpe: str
    """
    if escape_name: post_name = escape_url_name(post_name)
    return 'http://www.producthunt.co/posts/%s?modal=true' % post_name


def parse_post(post_name, content=None):
    """Find information from a post, requesting content if needed.

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
    """
    # Read the page content if not provided
    if not content:
        url = generate_post_url(post_name)
        response = urllib2.urlopen()
        if (response.code < 200) or (response.code >= 300):
            raise ValueError('Failed to parse %s (%d).' % (url, response.code))
        content = repsonse.read()

    # Create soup
    soup = bs4.BeautifulSoup(content)
    return serialize_post(soup)


def serialize_post(post_soup):
    """Parse soup with information about a single Product Hunt post.

    Parses a soup created from HTML page for a single Product Hunt post,
    returning a dict (serialized) information record with information for the
    requested post.

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

    @param post_soup: Soup with information about a single post.
    @type: bs4.BeautifulSoup or equivalent
    @return: Dictionary with information about the parsed post.
    @rtype: dict
    """
    # Parse metadata level information
    post_overview = post_soup.find(class_='post-show')
    data_id = int(post_overview['data-id'])
    vote_count_str = post_overview.find(class_='vote-count').getText()
    vote_count_str = vote_count_str.replace(',', '')
    vote_count = int(vote_count_str)

    user_info = post_overview.find(class_='user-name')
    dirty_username = user_info.contents[0]
    username = dirty_username.replace('\n', '').strip()
    dirty_handle = user_info.contents[1]
    twitter_handle = dirty_handle.getText()
    twitter_handle = twitter_handle.replace(')', '')
    twitter_handle = twitter_handle.replace('(', '')

    user_headline = post_overview.find(class_='user-headline').getText()

    overall_url_info = post_overview.find(class_='post-url')
    post_target_url = overall_url_info['href']
    post_title = overall_url_info.getText()
    
    post_tagline = post_overview.find(class_='post-tagline').getText()

    # TODO: Parse related posts

    # TODO: Parse voter information
    # votes_info = post_soup.find(class_='post-votes')

    # Parse comments information
    comments = post_soup.find_all(class_='comment')
    serialized_comments = map(serialize_comment, comments)

    # Parse datetime
    post_datetime = post_soup.find('time')['datetime']

    return {
        'data_id': data_id,
        'vote_count': vote_count,
        'username': username,
        'twitter_handle': twitter_handle,
        'post_target_url': post_target_url,
        'post_title': post_title,
        'post_tagline': post_tagline,
        'comments': serialized_comments,
        'post_datetime': post_datetime
    }


def serialize_comment(comment_soup):
    """Parse soup with information about a single comment on a post.

    Parses a soup with information about a single comment on a single Product
    Hunt post, returning a dict (serialized) with the parsed information.

    Dictionaries returned have the following keys:
     - username: The username of the poster.
     - twitter_handle: The twitter handle of the poster.
     - user_headline: The headline the poster chose for themselves.
     - timestamp: Time / date when the post was added.
     - body: Raw content of the post.

    @param comment_soup: Soup with information about the comment to parse.
    @type comment_soup: bs4.BeautifulSoup or equivalent
    @return: Parsed comment information.
    @rtype: dict
    """
    user_info = comment_soup.find(class_='user-name')
    dirty_username = user_info.contents[0]
    username = dirty_username.replace('\n', '').strip()
    dirty_handle = user_info.contents[1]
    twitter_handle = dirty_handle.getText()
    twitter_handle = twitter_handle.replace(')', '').replace('(', '')

    user_headline = comment_soup.find(class_='user-headline').getText()

    timestamp = comment_soup.find(class_='comment-timestamp').getText()

    body_info = comment_soup.find(class_='comment-body')
    body = body_info.contents[-1]

    return {
        'username': username,
        'twitter_handle': twitter_handle,
        'user_headline': user_headline,
        'timestamp': timestamp,
        'body': body
    }


def save_post(post_name, content=None):
    """Save information from a posts details page, requesting content if needed.

    This will save information about a given post to a specified mongodb
    database instance.
    """
    raise NotImplementedError()
