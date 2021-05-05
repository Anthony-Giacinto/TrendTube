# TrendTube
Grabs data from the YouTube videos on the trending page in your local area. Can plot the frequency of the words within the video titles or the video tags that appear on the trending page. Uses Selenium to find the video IDs on the trending page and uses the YouTube API to access data on those videos.

## Table of Contents
* [General info](#general-info)
* [Screenshot](#screenshot)
* [How to Use](#how-to-use)
* [Classes](#classes)

## General Info
* This project was created with Python 3.7 .
* This project requires the use of a web driver compatible with either Chrome or Firefox.

## Screenshot
![tag_chart](/image/tag_chart.png)

## How to Use
---------------------------------------------------------------------------------------------------------------------------------
*On First use*  

Update your global variables to your values:
* Change "api_key" to your YouTube API key
* Change "web_browser" to either "chrome" or "firefox". This depends on your desired web driver.
* Change "web_driver" to the path of your web driver.
---------------------------------------------------------------------------------------------------------------------------------
*How To Use*

* Create a Trending object
* Get the trending video data
* Combine the desired data
* Plot

---------------------------------------------------------------------------------------------------------------------------------
*Example Code*

    trend = Trending()
    trend.get_videos()
    trend.combine_tags(split=True, combine=True, stop_words=True)
    trend.bar_plot(tag=True, threshold=5)

---------------------------------------------------------------------------------------------------------------------------------

## Classes
---------------------------------------------------------------------------------------------------------------------------------
*Trending*

    """ The videos contained within the YouTube Trending page.

    Instance Attributes:
        videos: (list(Video Objects)) The videos on the trending page.
        titles: (list(str)) The titles of all the videos.
        tags: (list(str)) The tags of all the videos.
        title_frequencies: (dict) A dictionary of titles (or words within the title) and the amount of times
        they appear with the titles.
        tag_frequencies: (dict) A dictionary of tags and the amount of times they appear with the tags.
        date: (datetime object) The date and time that the video IDs were scraped from YouTube in UTC.

    Methods:
        get_videos: Finds all the YouTube video within the trending page.
        combine_titles: Combines the titles from multiple YouTube videos.
        combines_tags: Combines the tags from multiple YouTube videos.
        combine: Combines the tags from multiple YouTube videos.
        count: Finds the number of times that a word from the title or a tag appears in self.titles or self.tags.
        find_title_frequencies: Finds the number of times that each tag element appears in self.tags if that value
        is above some desired threshold. Only useful if self.tags is a combination of tags from multiple videos.
        find_tag_frequencies: Finds the number of times that each tag element appears in self.tags if that value
        is above some desired threshold. Only useful if self.tags is a combination of tags from multiple videos.
        bar_plot: A bar plot for the tag/title frequencies within the YouTube trending page.
    """
    
---------------------------------------------------------------------------------------------------------------------------------
*Video*

    """ A YouTube video object.
    
    Instance Attributes:
        id: (str) The ID of the YouTube video.
        title: (str/list(str)) The video title; Can be converted into a list of the words in the title (default is '').
        tags: (list(str)) The video tags (default is None).
        duration: (str) The duration of the video (default is '').
        view_count: (int) Amount of views on the video (default is 0).
        likes: (int) Amount of likes on the video (default is 0).
        dislikes: (int) Amount of dislikes on the video (default is 0).
        like_ratio: (float) The like to dislike ratio (likes/dislikes).
        comment_count: (int) Amount of comments on the video (default is 0).
        made_for_kids: (bool) If the video is designated as child-directed (default is None).

    Methods:
        split_title: Converts self.title into a list containing the unique individual words within the title.
        split_tags: Splits up each individual tag by a separator and only keeps the unique tags. Will either
        replace self.tags with the separated tags of extend self.tags with these splits tags.
        stop_title: Removes some commonly used / unimportant words from the title. Best used after splitting self.title.
        stop_tags: Removes some commonly used / unimportant words from the tags. Best used after splitting self.tags.
    """

---------------------------------------------------------------------------------------------------------------------------------
