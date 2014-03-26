import os
import unittest

import pyproducthunt


class TestPyProductHunt(unittest.TestCase):

    def test_parse_index(self):
        with open(os.path.join('test_content', 'index.html')) as f:
            results = pyproducthunt.parse_index(content=f.read())

        self.assertEqual(len(results), 20)

        sample = results[0]
        self.assertEqual(sample['vote_count'], 92)
        self.assertEqual(sample['data_id'], 2181)
        self.assertEqual(sample['post_target_url'], 'http://goodui.org/')
        self.assertEqual(sample['post_title'], 'GoodUI')
        self.assertEqual(
            sample['post_tagline'],
            'Collection of clever UX patterns & ideas'
        )
        self.assertEqual(sample['post_comments_url'], '/posts/goodui')
        self.assertEqual(sample['post_comments_count'], 9)

    def test_parse_post(self):
        with open(os.path.join('test_content', 'product.html')) as f:
            results = pyproducthunt.parse_post('', content=f.read())

        self.assertEqual(results['data_id'], 2255)
        self.assertEqual(results['vote_count'], 75)
        self.assertEqual(results['username'], 'PETIT Edouard')
        self.assertEqual(results['twitter_handle'], '@EdouardPetit')
        self.assertEqual(
            results['post_target_url'],
            'https://www.woovent.com/en'
        )
        self.assertEqual(results['post_title'], 'Woovent')
        self.assertEqual(
            results['post_tagline'],
            'Finally an app to put your Facebook events on steroids'
        )
        self.assertEqual(len(results['comments']), 3)
        self.assertEqual(results['post_datetime'], '2014-03-26')

        sample_comment = results['comments'][0]
        self.assertEqual(sample_comment['username'], 'Adrien Dulong')
        self.assertEqual(sample_comment['twitter_handle'], '@adulong')
        self.assertEqual(sample_comment['user_headline'], 'CEO')
        self.assertEqual(sample_comment['timestamp'], '2h ago')


if __name__ == '__main__':
    unittest.main()