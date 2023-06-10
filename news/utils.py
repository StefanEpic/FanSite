from django.contrib.auth.mixins import UserPassesTestMixin


class TestIsModerator(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.groups.filter(name='Moderators').exists()
