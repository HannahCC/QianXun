__author__ = 'Hannah'
from utils.TimeLocalize import convert_to_localtime, datetime_format


class NoticeBean:
    def __init__(self, notice_model):
        self.id = notice_model.id
        self.title = notice_model.title
        self.updateTime = notice_model.update_time
        if self.updateTime:
            self.updateTime = datetime_format(convert_to_localtime(self.updateTime))


class CanteenNoticeDetailBean(NoticeBean):
    def __init__(self, canteen_notice_model):
        NoticeBean.__init__(self, canteen_notice_model)
        self.manager = canteen_notice_model.manager.name
        self.title = canteen_notice_model.title
        self.canteen = canteen_notice_model.canteen.canteen_name
        self.content = canteen_notice_model.content
        self.readTimes = canteen_notice_model.read_times


class SchoolNoticeDetailBean(NoticeBean):
    def __init__(self, school_notice_model):
        self.title = school_notice_model.title
        self.manager = school_notice_model.manager.name
        self.school = school_notice_model.school.school_name
        self.content = school_notice_model.content
        self.readTimes = school_notice_model.read_times


