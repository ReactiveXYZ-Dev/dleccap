from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import input
from builtins import object
import os
import sys
import wget
import json
import time
import threading
from queue import Queue
from .utils import *
from .constants import *

"""
Lecture download procedures

@Version 2.0.0
"""
class Downloader(object):
    
    class ProgressReporter(threading.Thread):
        """
        Report progress for multiple download threading
        
        Arguments:
            threading {Thread}
        """
        def __init__(self, num_workers, msg_queue):
            threading.Thread.__init__(self)
            self._num_workers = num_workers
            self._msg_queue = msg_queue
        
        def run(self):
            """
            Check and report progress
            """
            status = {}
            while self._num_workers > 0:
                msg = self._msg_queue.get()
                # check status
                if msg['type'] == "update":
                    status[msg['title']] = {
                        'current': msg['current'],
                        'total': msg['total']
                    }
                    self._show_progress(status)
                elif msg['type'] == "done":
                    self._num_workers -= 1
        
        def _show_progress(self, status):
            """
            Print the progress in console
            """
            current = 0
            total = 0
            for title, data in list(status.items()):
                current += data['current']
                total += data['total']
            line = "%s / %s bytes (%s recording(s)) in progress" % (current, total, len(status))
            self._print_message(print_info(line, True))
        
        def _print_message(self, msg):
            """
            Print message using stdout
            
            Arguments:
                msg {str}
            """
            sys.stdout.write("\r" + msg)
            sys.stdout.flush()
    
    class Task(threading.Thread):
        """
        Download Thread
        
        Arguments:
            threading {Thread}
        """
        def __init__(self, url, dest_path, filename, msg_queue):
            threading.Thread.__init__(self)
            self._url = url
            self._dest_path = dest_path
            self._filename = filename
            self._msg_queue = msg_queue

        def run(self):
            """
            Run the download task
            """
            filepath = os.path.join(self._dest_path, self._filename)
            # custom progress message
            custom_bar = self._send_updates()
            wget.download(self._url, out=filepath, bar=custom_bar)
            # completion message
            self._send_completion()

        def _send_updates(self):
            def custom_bar(current, total, width=None):
                self._msg_queue.put({
                    'type': 'update',
                    'title': self._filename,
                    'current': current,
                    'total': total
                })
                return None
            return custom_bar
        
        def _send_completion(self):
            self._msg_queue.put({
                'type': 'done',
                'title': self._filename,
                'current': 'Completed',
                'total': 'Completed'
            })

    def __init__(self, url, dest_path):
        """
        Initialize with download configuration
        
        Arguments:
            url {str} -- Target url, either a site or actual video
            concurrency {int} -- Number of download process to run
        """
        self._url = url
        self._dest_path = dest_path
        self._authenticator = None
    
    def set_concurrency(self, conc):
        """
        Inject concurrency
        
        Arguments:
            conc {int} -- Number of threads to run at same time
        """
        self._concurrency = conc

    def set_auth(self, auth):
        """
        Inject authenticator
        
        Arguments:
            auth {Authenticator}
        """
        self._authenticator = auth

    def get_auth(self):
        """
        Retrieve the authenticator
        
        Returns:
            Authenticator
        """
        return self._authenticator

    def requires_auth(self):
        """
        Whether this downloader requires authentication
        
        Returns:
            bool
        """
        return True

    def start(self):
        """
        Check argument and start downloading
        """
        # start downloading
        try:
            if self._is_recording_url(self._url):
                self._download_video()
            elif self._is_site_url(self._url):
                self._download_site()
            else:
                print_error("The URL you entered it not valid!")
        except Exception as e:
           print_error(e.message)
           print_warning("This is probably because of wrong credentials.")

    """
    Helpers
    """
    def _download_video(self):
        # extract video id
        video_id = self._url.split('/')[-1]
        # fetch data from api
        res = self._authenticator.session().get("%s?rk=%s" % (API_BASE_URL, video_id))
        recordings = json.loads(res.text)
        # find the specific recording
        for recording in recordings:
            if recording['recordingkey'] == video_id:
                self._download_with_thread([recording])
                break

    def _download_site(self):
        # extract site id
        site_id = self._url.split('/')[-1]
        # fetch data from api
        res = self._authenticator.session().get("%s?sk=%s" % (API_BASE_URL, site_id))
        recordings = json.loads(res.text)
        # show list of downloadable recordings
        print_info("%i recording%s available:" % (
            len(recordings), ("s" if (len(recordings) != 1) else "")))
        # print lecture info
        for idx, recording in enumerate(recordings):
            print("%i\t(%s)\t%s" % (
                idx + 1, recording["date"], recording["title"]))
        # prompt user to select
        prompt = print_info("Please select one or more comma separated, e.g 1,3,5. Or simply enter to download all of them: ", True)
        ans = input(prompt)
        if ans == '':
            to_dl = recordings
        else:
            to_dl = [ recordings[int(i)-1] for i in ans.split(',') ]
        # download the recordings
        self._download_with_thread(to_dl)
        
    def _download_with_thread(self, recordings):       
        # split recordings into batch of concurrencies
        batches = list(chunks(recordings, int(self._concurrency)))
        for batch_idx, batch in enumerate(batches):
            print_info("Start downloading batch %s ... " % (batch_idx + 1))
            # load a batch
            tasks = []
            msg_queue = Queue()
            for rec_idx, recording in enumerate(batch):
                # add task
                dl_url = self._construct_recording_file_url(recording)
                title = self._construct_recording_title(rec_idx, recording)
                dest_path = os.path.join(self._dest_path, recording['sitename'])
                # check directory
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                task = self.Task(dl_url, dest_path, title, msg_queue)
                tasks.append(task)
            # add the progress reporter
            reporter = self.ProgressReporter(len(tasks), msg_queue)
            tasks.append(reporter)
            # download with threads
            for t in tasks:
                t.start()
            # wait for all of them to finish
            for t in tasks:
                t.join()
            print('') # for new line
        print_success("All done! Enjoy!")

    def _is_recording_url(self, url):
        return "https://leccap.engin.umich.edu/leccap/viewer" in url

    def _is_site_url(self, url):
        return "https://leccap.engin.umich.edu/leccap/site" in url

    def _construct_recording_file_url(self, recording):
        return "https:%s%s/%s.%s" % (recording["mediaPrefix"],
                                     recording["sitekey"],
                                     recording["info"]["movie_exported_name"],
                                     recording["info"]["movie_type"])
    
    def _construct_recording_title(self, idx, recording):
        title = recording['title'].replace('[',"").replace(']',"").replace('/', "-")
        ext = recording['info']['movie_type']
        return "%s-%s.%s" % (idx, title, ext)
