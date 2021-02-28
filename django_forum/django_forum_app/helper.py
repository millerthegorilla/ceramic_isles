
class PostsCommentsIterator:
    def __init__(self, posts, comments):
        breakpoint()
        self._posts = posts
        self._posts_count = posts.count()
        self._comments = comments
        self._comments_count = comments.count()
        self._index = 0

    def __next__(self):
        try:
            if self._index < self._posts_count:
                result = self._posts[self._index]
            else:
                result = self._comments[self._index - self._posts_count]
        except IndexError:
            raise StopIteration
        self._index +=1;
        return result


class PostsComments:
    def __init__(self, posts, comments):
        self._posts = list(posts)
        self._posts_count = posts.count()
        self._comments = list(comments)
        self._comments_count = comments.count()

    def count(self):
        return self._posts_count + self._comments_count

    def __len__(self):
        return self.count()

    def __iter__(self):
        return PostsCommentsIterator(self._posts, self._comments)

    def __repr__(self):
            return '<posts - ' + str(self._posts) + '><comments - ' + str(self._comments) + '>'

    def __getitem__(self, index):
        breakpoint()
        if isinstance(index, int): 
            if self._posts_count:
                if index < self._posts_count:
                    return self._posts[index]
                else:
                    return self._comments[index - self._posts_count]
            return self._comments[index]
        else:
            result = []
            if index.start < self._posts_count:
                if index.stop < self._posts_count:
                    return self._posts[self.index.start:self.index.stop]
                else:
                    result = self.posts[self.index.start:]
                    if index.stop < self._comments_count - self._posts_count:
                        return result + self._comments[index.stop - self._posts_count]
                    else:
                        return result + self._comments[0:]