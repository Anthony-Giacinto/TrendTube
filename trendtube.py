import os
import string
import matplotlib.pyplot as plt
import datetime
from selenium import webdriver
from googleapiclient.discovery import build
from nltk.corpus import stopwords


_api_key = os.environ.get('YT_API_KEY')
_web_browser = 'chrome'
_web_driver = r'C:\Program Files (x86)\chromedriver.exe'


class Video:
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

    def __init__(self, id, title='', tags=None, duration='', view_count=0, likes=0, dislikes=0, comment_count=0,
                 made_for_kids=None):
        """
        :param id: (str) The ID of the YouTube video.
        :param title: (str/list(str)) The video title; Can be converted into a list of the words in the title (default is '').
        :param tags: (list(str)) The video tags (default is None).
        :param duration: (str) The duration of the video (default is '').
        :param view_count: (int) Amount of views on the video (default is 0).
        :param likes: (int) Amount of likes on the video (default is 0).
        :param dislikes: (int) Amount of dislikes on the video (default is 0).
        :param comment_count: (int) Amount of comments on the video (default is 0).
        :param made_for_kids: (bool) If the video is designated as child-directed (default is None).
        """

        self._id = id
        self._title = title
        self._tags = tags
        self._duration = duration
        self._view_count = view_count
        self._likes = likes
        self._dislikes = dislikes
        self._comment_count = comment_count
        self._made_for_kids = made_for_kids

    def __repr__(self):
        return f'Video(id={self._id}, title={self._title}, tags={self._tags}, duration={self._duration}, ' \
               f'view_count={self._view_count}, likes={self._likes}, dislikes={self._dislikes}, ' \
               f'like_ratio={self.like_ratio}, comment_count={self._comment_count}, ' \
               f'made_for_kids={self._made_for_kids})'

    def __str__(self):
        return self.title

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def tags(self):
        return self._tags

    @property
    def duration(self):
        return self._duration

    @property
    def view_count(self):
        return int(self._view_count)

    @property
    def likes(self):
        return int(self._likes)

    @property
    def dislikes(self):
        return int(self._dislikes)

    @property
    def like_ratio(self):
        return round(self.likes/self.dislikes, 2)

    @property
    def comment_count(self):
        return int(self._comment_count)

    @property
    def made_for_kids(self):
        return self._made_for_kids

    def find_attributes(self):
        """ Uses the Youtube video ID to find the other video attributes. """

        part = ['snippet', 'contentDetails', 'statistics', 'status']
        fields = 'items(snippet(title, tags), ' \
                 'contentDetails(duration), ' \
                 'statistics(viewCount, likeCount, dislikeCount, commentCount), ' \
                 'status(madeForKids))'

        youtube = build('youtube', 'v3', developerKey=_api_key).videos()
        items = youtube.list(part=part, fields=fields, id=id).execute()['items'][0]
        snippet = items['snippet']
        statistics = items['statistics']
        self._title = snippet['title']
        if 'tags' in snippet:
            self._tags = list(set(tag.lower() for tag in snippet['tags']))
        self._duration = items['contentDetails']['duration']
        self._view_count = statistics['viewCount']
        self._likes = statistics['likeCount']
        self._dislikes = statistics['dislikeCount']
        if 'commentCount' in statistics:
            self._comment_count = statistics['commentCount']
        self._made_for_kids = items['status']['madeForKids']

    def split_title(self, combine=False):
        """ Converts self.title into a list containing the unique individual words within the title.

        :param combine: (bool) Includes the original title string within the self.title list (default is False).
        """

        t = []
        for title in self._title.split():
            if (title[0] in string.punctuation) and (title[-1] in string.punctuation):
                title = title[1:-1]
            elif (title[0] in string.punctuation) and not (title[-1] in string.punctuation):
                title = title[1:]
            elif not (title[0] in string.punctuation) and (title[-1] in string.punctuation):
                title = title[:-1]
            if title != '':
                t.append(title)
        t = list(set(t))

        if combine:
            self._title = [self._title]
            self._title.extend(t)
        else:
            self._title = t

    def split_tags(self, combine=False):
        """ Splits up each individual tag by a separator and only keeps the unique tags. Will either replace self.tags
        with the separated tags of extend self.tags with these splits tags.

        :param combine: (bool) If True, extends self.tags with separated tags to combine individual words with phrases
        (default is False).
        """

        if self._tags:
            t = list(set([t for tag in self._tags for t in tag.split()]))
            if combine:
                self._tags.extend(t)
            else:
                self._tags = t
        else:
            raise TypeError("self.tags is None; There are no tags associated with this video.")

    @staticmethod
    def __remove_stopwords(words, custom=True):
        """ Removes some commonly used, unimportant words (stop words) from the desired list of words.

        :param words: (list(str)) The list of words to be updated.
        :param custom: (bool) Some custom strings that will be removed if True (default is True).
        :return: (list(str)) Returns the updated list of words.
        """

        ignore = list(set(stopwords.words('english')))
        if custom:
            ignore.extend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
            ignore.extend(string.punctuation)
            ignore.extend(['-', '+', '*', '/', '.', '(', ')', '&', '|'])
            ignore.extend(['video', 'youtube', 'new', 'get', 'ft'])
        return [w for w in words if w.lower() not in ignore]

    def stop_title(self):
        """ Removes some commonly used / unimportant words from the title. Best used after splitting self.title. """

        self._title = self.__remove_stopwords(self._title)

    def stop_tags(self):
        """ Removes some commonly used / unimportant words from the tags. Best used after splitting self.tags. """

        self._tags = self.__remove_stopwords(self._tags)


class Trending:
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

    def __init__(self):
        self._videos = []
        self._titles = []
        self._tags = []
        self._title_frequencies = dict()
        self._tag_frequencies = dict()
        self._date = None

    def __repr__(self):
        return f'Trending(videos={self._videos}, titles={self._titles}, tags={self._tags}, ' \
               f'title_frequencies={self._title_frequencies}, tag_frequencies={self._tag_frequencies}, ' \
               f'date={self._date})'

    def __len__(self):
        return len(self._videos)

    @property
    def videos(self):
        return self._videos

    @property
    def titles(self):
        return self._titles

    @property
    def tags(self):
        return self._tags

    @property
    def title_frequencies(self):
        return self._title_frequencies

    @property
    def tag_frequencies(self):
        return self._tag_frequencies

    @property
    def date(self):
        return self._date

    def get_videos(self, web_browser=_web_browser, web_driver=_web_driver):
        """ Finds all the YouTube video within the trending page.

        :param web_browser: (str) The desired web browser to use (default is global variable: _web_browser).
        :param web_driver: (str) The path to your web driver (default is global variable: _web_driver).
        """

        browser_dict = {'chrome': (webdriver.Chrome, webdriver.ChromeOptions),
                        'firefox': (webdriver.Firefox, webdriver.FirefoxOptions)}

        # Open the browser in headless mode
        options = browser_dict[web_browser][1]()
        options.headless = True
        with browser_dict[web_browser.lower()][0](executable_path=web_driver, options=options) as driver:
            # Go to the YouTube Trending page
            driver.get('https://www.youtube.com/feed/trending')

            # Find the video IDs
            self._date = datetime.datetime.utcnow()
            ids = []
            for i in driver.find_elements_by_id('thumbnail'):
                url = i.get_attribute('href')
                if url:
                    ids.append(url[url.index('=') + 1:])

        # Requests the videos from the Trending page using the least amount of requests
        _part = ['snippet', 'contentDetails', 'statistics', 'status', 'id']
        _fields = 'items(snippet(title, tags), ' \
                  'contentDetails(duration), ' \
                  'statistics(viewCount, likeCount, dislikeCount, commentCount), ' \
                  'status(madeForKids), ' \
                  'id)'
        youtube = build('youtube', 'v3', developerKey=_api_key).videos()
        count, num, amount = 0, 50, len(ids)
        finished = False
        while not finished:
            x = count + num
            if x < amount:
                id_list = ids[count: x]
                count += num
            else:
                id_list = ids[count:]
                finished = True

            for video in youtube.list(part=_part, fields=_fields, id=id_list).execute()['items']:
                kwargs = {'id': video['id'], 'title': video['snippet']['title'],
                          'duration': video['contentDetails']['duration'],
                          'made_for_kids': video['status']['madeForKids'],
                          'view_count': video['statistics']['viewCount'],
                          'likes': video['statistics']['likeCount'],
                          'dislikes': video['statistics']['dislikeCount']}

                if 'tags' in video['snippet']:
                    kwargs['tags'] = list(set(tag.lower() for tag in video['snippet']['tags']))
                else:
                    kwargs['tags'] = []
                if 'commentCount' in video['statistics']:
                    kwargs['comment_count'] = video['statistics']['commentCount']
                else:
                    kwargs['comment_count'] = 0

                self._videos.append(Video(**kwargs))

    def combine_titles(self, split=False, combine=False, stop_words=False):
        """ Combines the titles from multiple YouTube videos.

        :param split: (bool) It True, splits up each title into individual words and only keeps the unique words
        (default is False).
        :param combine: (bool) If split and combine is True, combines the unique words with the original title
        (default is False).
        :param stop_words: (bool) If True, will remove some commonly used, unimportant words (stop words) from
        the titles (default is False).
        """

        for vid in self._videos:
            if split:
                vid.split_title(combine=combine)
            if stop_words:
                vid.stop_title()
            self._titles.extend(vid.title)

    def combine_tags(self, split=False, combine=False, stop_words=False):
        """ Combines the tags from multiple YouTube videos.

        :param split: (bool) It True, splits up each individual tag into individual words and only keeps the unique tags
        (default is False).
        :param combine: (bool) If split and combine is True, combines the unique split tags with the original tags
        (default is False).
        :param stop_words: (bool) If True, will remove some commonly used, unimportant words (stop words) from the tags
        (default is False).
        """

        for vid in [vid for vid in self._videos if vid.tags]:
            if split:
                vid.split_tags(combine=combine)
            if stop_words:
                vid.stop_tags()
            self._tags.extend(vid.tags)

    def combine(self, split=False, combine=False, stop_words=False):
        """ Combines the titles together and the tags together from multiple YouTube videos.

        :param split: (bool) It True, splits up each title into individual words and only keeps the unique words;
        splits up each individual tag into individual words and only keeps the unique tags  (default is False).
        :param combine: (bool) If split and combine is True, combines the unique words with the original title;
        combines the unique split tags with the original tags (default is False).
        :param stop_words: (bool) If True, will remove some commonly used, unimportant words (stop words) from the
        titles and the tags (default is False).
        """

        for vid in self._videos:
            if split:
                vid.split_title(combine=combine)
                vid.split_tags(combine=combine)
            if stop_words:
                vid.stop_title()
                vid.stop_tags()
            self._titles.extend(vid.title)
            self._tags.extend(vid.tags)

    def count(self, title=False, tag=False, name=None, index=None):
        """ Finds the number of times that a word from the title or a tag appears in self.titles or self.tags.

        :param title: (bool) For counting words contained within the title (default is False).
        :param tag: (bool) For counting words contained within the tags (default is False).
        :param name: (str) The name of the desired title/tag to check (default is None).
        :param index: (int) The desired index of the title/tag to check (default is None).
        :return: (int) The number of times that tag element appears in self.tags.
        """

        if title:
            if name:
                return self._titles.count(name)
            elif index:
                return self._titles.count(self._titles[index])
        elif tag:
            if name:
                return self._tags.count(name)
            elif index:
                return self._tags.count(self._tags[index])
        else:
            return None

    def find_title_frequencies(self, threshold=1):
        """ Finds the number of times that each tag element appears in self.tags if that value is above
        some desired threshold. Only useful if self.tags is a combination of tags from multiple videos.

        :param threshold: (int) The frequency threshold value (default is 1).
        :return: (dict) A dictionary of tags and frequencies {tag: frequency}.
        """

        title_frequencies = {title: self._titles.count(title) for title in self._titles
                             if self._titles.count(title) >= threshold}
        self._title_frequencies = dict(sorted(title_frequencies.items(), key=lambda kv: kv[1]))

    def find_tag_frequencies(self, threshold=1):
        """ Finds the number of times that each tag element appears in self.tags if that value is above
        some desired threshold. Only useful if self.tags is a combination of tags from multiple videos.

        :param threshold: (int) The frequency threshold value (default is 1).
        :return: (dict) A dictionary of tags and frequencies {tag: frequency}.
        """

        tag_frequencies = {tag: self._tags.count(tag) for tag in self._tags if self._tags.count(tag) >= threshold}
        self._tag_frequencies = dict(sorted(tag_frequencies.items(), key=lambda kv: kv[1]))

    def bar_plot(self, title=False, tag=False, threshold=1):
        """ A bar plot for the tag/title frequencies within the YouTube trending page.

        :param title: (bool) For plotting title data (default is False).
        :param tag: (bool) For plotting tag data (default is False).
        :param threshold: (int) The frequency threshold value; only used if self.frequencies has not
        been found yet (default is 1).
        """

        if title:
            if len(self._title_frequencies) == 0:
                self.find_title_frequencies(threshold=threshold)
            keys = self._title_frequencies.keys()
            vals = self._title_frequencies.values()
            plot_title = 'Frequency of Words from YouTube Video Titles on the Trending Page'
        elif tag:
            if len(self._tag_frequencies) == 0:
                self.find_tag_frequencies(threshold=threshold)
            keys = self._tag_frequencies.keys()
            vals = self._tag_frequencies.values()
            plot_title = 'Frequency of a Given Tag on the YouTube Trending Page'
        else:
            return None

        fig = plt.figure()
        ax = fig.add_subplot()
        rects = ax.barh(range(len(vals)), vals, color='darkorange')
        for rect, key in zip(rects, keys):
            ax.annotate('{}'.format(key), xy=(0.1, rect.get_y() + rect.get_height()/2 - 0.02), xytext=(0, 0),
                        textcoords='offset points')

        date = self._date.strftime("%Y-%m-%d %H:%M:%S")
        ax.set_title(plot_title + f'\n{date}', fontweight='bold')
        ax.xaxis.grid()
        ax.set_axisbelow(True)
        plt.xticks(range(max(vals) + 2))
        ax.yaxis.set_visible(False)
        plt.show()


if __name__ == '__main__':
    trend = Trending()
    trend.get_videos()
    trend.combine_tags(split=True, combine=True, stop_words=True)
    trend.bar_plot(tag=True, threshold=5)
