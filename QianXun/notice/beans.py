__author__ = 'Hannah'
from utils.TimeLocalize import convert_to_localtime, datetime_format


class NoticeBean:
    def __init__(self, notice_model):
        self.id = notice_model.id
        self.title = notice_model.title
        self.update_time = notice_model.update_time
        if self.update_time:
            self.update_time = datetime_format(convert_to_localtime(self.update_time))


class CanteenNoticeDetailBean(NoticeBean):
    def __init__(self, canteen_notice_model):
        NoticeBean.__init__(self, canteen_notice_model)
        self.manager = canteen_notice_model.manager.name
        self.canteen = canteen_notice_model.canteen.canteen_name
        self.content = canteen_notice_model.content
        self.read_times = canteen_notice_model.read_times


class SchoolNoticeDetailBean(NoticeBean):
    def __init__(self, school_notice_model):
        self.manager = school_notice_model.manager.name
        self.school = school_notice_model.school.school_name
        self.content = school_notice_model.content
        self.read_times = school_notice_model.read_times


