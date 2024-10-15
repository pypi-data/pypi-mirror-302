from dataclasses import dataclass, field
from threading import Event, Thread
from time import sleep
from queue import PriorityQueue

from .api import SubredditSort, SubredditT, UserWhere, UserSort, UserT, CommentsSort, RedditAPI


@dataclass
class RedditAPITask:
    priority: int
    method: str = field(compare=False)
    args: tuple = field(compare=False)


class RedditAPIDispatcher(Thread):
    IDLE_SLEEP: float = 1 / 60

    def __init__(self) -> None:
        super().__init__()
        self.running: Event = Event()
        self.task_queue: PriorityQueue[RedditAPITask] = PriorityQueue()
        self.api: RedditAPI = RedditAPI()

    def run(self) -> None:
        self.running.set()

        while self.running.is_set():
            if not self.task_queue.empty():
                task = self.task_queue.get()
                getattr(self.api, task.method)(*task.args)
                self.task_queue.task_done()
            else:
                sleep(self.IDLE_SLEEP)

    def r_about(self, priority: int, subreddit: str) -> None:
        self.task_queue.put(RedditAPITask(priority, "r_about", (subreddit,)))

    def r(
        self,
        priority: int,
        subreddit: str,
        sort: SubredditSort = SubredditSort.HOT,
        t: SubredditT = SubredditT.DAY,
        before: str | None = None,
        after: str | None = None
    ) -> None:
        self.task_queue.put(RedditAPITask(priority, "r", (subreddit, sort, t, before, after)))

    def user_about(self, priority: int, username: str) -> None:
        self.task_queue.put(RedditAPITask(priority, "user_about", (username,)))

    def user(
        self,
        priority: int,
        username: str,
        where: UserWhere = UserWhere.OVERVIEW,
        sort: UserSort = UserSort.NEW,
        t: UserT = UserT.ALL,
        before: str | None = None,
        after: str | None = None
    ) -> None:
        self.task_queue.put(RedditAPITask(priority, "user", (username, where, sort, t, before, after)))

    def comments(self, priority: int, article: str, sort: CommentsSort = CommentsSort.CONFIDENCE, comment: str | None = None) -> None:
        self.task_queue.put(RedditAPITask(priority, "comments", (article, sort, comment)))

    def api_morechildren(self, priority: int, link_id: str, children: list[str], sort: CommentsSort = CommentsSort.CONFIDENCE) -> None:
        self.task_queue.put(RedditAPITask(priority, "api_morechildren", (link_id, children, sort)))
